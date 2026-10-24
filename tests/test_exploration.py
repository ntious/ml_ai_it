"""Behavioral checks for descriptive exploration and its evidence artifacts."""
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.exploration import CHARTS, describe_charts, read_workload, run_exploration, summarize_workload

SAMPLE = ROOT / "data/samples/service-workload/daily.csv"


class Report(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.ids, self.headers, self.captions = [], set(), 0, 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "img":
            self.images.append(attrs)
        if tag == "th" and attrs.get("scope") == "col":
            self.headers += 1
        if tag == "caption":
            self.captions += 1


class ExplorationTests(unittest.TestCase):
    def fixture(self):
        frame, quality = read_workload(SAMPLE)
        return frame, quality, *summarize_workload(frame, quality)

    def test_sample_reconciles_and_retains_spike(self):
        frame, quality, summary, tables = self.fixture()
        self.assertEqual((quality["input_rows"], quality["observations"], quality["exact_duplicates_removed"], quality["labels_normalized"]), (25, 24, 1, 1))
        self.assertEqual(summary["total_requests"], 4180)
        self.assertEqual(summary["observed_latency"], 23)
        self.assertEqual(summary["missing_latency"], 1)
        self.assertAlmostEqual(summary["mean_daily_service_p95_ms"], 890 / 23)
        self.assertEqual(summary["median_daily_service_p95_ms"], 34)
        self.assertEqual(summary["iqr_upper_fence_ms"], 58)
        self.assertEqual(summary["flagged_observations"], [{"date": "2027-01-07", "service": "network_monitor", "p95_latency_ms": 160.0}])
        manifest = json.loads((ROOT / "data/manifests/service-workload.json").read_text())
        self.assertEqual(hashlib.sha256(SAMPLE.read_bytes()).hexdigest(), manifest["files"][0]["sha256"])
        self.assertEqual(len(frame), 24)
        self.assertEqual(tables["latency_distribution"]["count"].tolist(), [16, 6, 0, 0, 1])
        self.assertEqual(int(tables["daily_requests"]["requests"].max()), 560)
        self.assertEqual(int(tables["service_comparison"]["requests"].sum()), 4180)

    def test_missing_latency_is_not_dropped_from_workload_totals(self):
        frame, quality, summary, tables = self.fixture()
        observed = frame.dropna(subset=["p95_latency_ms"])
        self.assertEqual(int(observed["requests"].sum()), 4050)
        self.assertEqual(len(tables["request_latency"]), 23)
        self.assertEqual(summary["total_requests"] - int(observed["requests"].sum()), 130)
        self.assertEqual(int(tables["latency_distribution"]["count"].sum()), len(observed))

    def test_sensitivity_does_not_change_core_observations(self):
        frame, _, summary, _ = self.fixture()
        sensitivity = frame.loc[frame["p95_latency_ms"] != 160, "p95_latency_ms"].dropna()
        self.assertEqual(len(sensitivity), 22)
        self.assertAlmostEqual(sensitivity.mean(), 730 / 22)
        self.assertEqual(sensitivity.median(), 33)
        self.assertEqual(len(frame), 24)
        self.assertEqual(summary["observed_latency"], 23)

    def write_input(self, directory, rows):
        path = Path(directory) / "daily.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["date", "service", "requests", "p95_latency_ms"])
            writer.writerows(rows)
        return path

    def test_conflicting_keys_are_rejected_instead_of_arbitrarily_selected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_input(directory, [["2027-01-01", "network_monitor", 10, 20], ["2027-01-01", " NETWORK_MONITOR ", 11, 20]])
            with self.assertRaisesRegex(ValueError, "Conflicting"):
                read_workload(path)

    def test_invalid_count_date_service_and_nonfinite_latency_have_errors(self):
        cases = [
            (["2027-01-01", "network_monitor", "1.5", 20], "whole-number"),
            (["2027-01-01", "network_monitor", -1, 20], "whole-number"),
            (["2027-01-01", "network_monitor", 10, "inf"], "finite"),
            (["2027-01-01", "network_monitor", 10, -1], "nonnegative"),
            (["2027-02-30", "network_monitor", 10, 20], "valid"),
            (["2027-01-01", "unknown", 10, 20], "normalize"),
            (["2027-01-01", "network_monitor", str(2**63), 20], "int64"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            for row, expected in cases:
                path = self.write_input(directory, [row])
                with self.subTest(row=row), self.assertRaisesRegex(ValueError, expected):
                    read_workload(path)

    def test_grouped_request_counts_cannot_silently_overflow(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_input(directory, [["2027-01-01", "network_monitor", str(2**63 - 1), 20], ["2027-01-02", "network_monitor", 1, 20]])
            with self.assertRaisesRegex(ValueError, "Combined requests"):
                read_workload(path)

    def test_absent_dates_are_not_created_as_zero_observations(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_input(directory, [["2027-01-01", "network_monitor", 10, 20], ["2027-01-03", "network_monitor", 20, 30]])
            frame, quality = read_workload(path)
            summary, tables = summarize_workload(frame, quality)
            self.assertEqual(summary["dates_observed"], 2)
            self.assertEqual(tables["daily_requests"]["requests"].tolist(), [10, 20])
            self.assertEqual(tables["daily_requests"]["services_observed"].tolist(), [1, 1])
            self.assertIn("fewer than two service observations: 2", describe_charts(summary, tables)["daily_requests"][1])

    def test_empty_input_is_explained(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "at least one"):
                read_workload(self.write_input(directory, []))

    def test_all_missing_latency_has_no_fabricated_distribution_or_average(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_input(directory, [["2027-01-01", "network_monitor", 10, ""]])
            frame, quality = read_workload(path)
            summary, tables = summarize_workload(frame, quality)
            self.assertIsNone(summary["mean_daily_service_p95_ms"])
            self.assertIsNone(summary["median_daily_service_p95_ms"])
            self.assertEqual(summary["total_requests"], 10)
            self.assertEqual(summary["flagged_observations"], [])
            self.assertEqual(int(tables["latency_distribution"]["count"].sum()), 0)
            self.assertIn("No observed latency", describe_charts(summary, tables)["latency_distribution"][1])
            report = run_exploration(path, Path(directory) / "out")
            self.assertIsNone(report["mean_daily_service_p95_ms"])
            self.assertTrue((Path(directory) / "out/request_latency.png").is_file())

    def test_generated_report_pairs_figures_tables_and_descriptions_and_keeps_raw(self):
        before = SAMPLE.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            summary = run_exploration(SAMPLE, output)
            self.assertEqual(json.loads((output / "summary.json").read_text()), summary)
            page = Report(); page.feed((output / "index.html").read_text())
            self.assertEqual(len(page.images), 5)
            self.assertEqual(page.captions, 5)
            self.assertGreater(page.headers, 10)
            for name, image in zip(CHARTS, page.images):
                self.assertEqual(image["src"], name + ".png")
                self.assertTrue(image["alt"])
                self.assertIn(image["aria-describedby"], page.ids)
                self.assertEqual((output / image["src"]).read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                self.assertTrue((output / (name + ".csv")).is_file())
            text = (output / "chart_descriptions.md").read_text()
            self.assertIn("not establish", text)
            self.assertIn("23", text)
        self.assertEqual(SAMPLE.read_bytes(), before)

    def test_output_cannot_replace_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observations.csv"
            path.write_bytes(SAMPLE.read_bytes())
            with self.assertRaisesRegex(ValueError, "separate"):
                run_exploration(path, directory)
            self.assertEqual(path.read_bytes(), SAMPLE.read_bytes())


if __name__ == "__main__":
    unittest.main()
