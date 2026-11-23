"""Meaningful checks for data loss, ambiguity, and reproducibility boundaries."""
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.data.events import FIELDS, prepare_events, prepare_file


def row(**changes):
    values = dict(event_id="a", timestamp="2026-01-01T10:00:00+01:00", source="network_monitor", latency_ms="10", bytes_sent="100")
    return dict(values, **changes)


class EventPreparationTests(unittest.TestCase):
    def test_sample_reconciles_and_keeps_missing_latency(self):
        frame = pd.read_csv(ROOT / "data/samples/network-events/events.csv", dtype=str, keep_default_na=False)
        original = frame.copy(deep=True)
        result = prepare_events(frame)
        self.assertEqual((result.report["rows_input"], len(result.cleaned), len(result.rejected)), (12, 6, 6))
        self.assertEqual(result.report["accepted_missing_latency"], 1)
        self.assertAlmostEqual(result.report["latency_summary"]["mean_ms"], 24.0)
        self.assertEqual(result.report["latency_summary"]["median_ms"], 20.0)
        self.assertEqual(result.cleaned.loc[result.cleaned.event_id == "net-003", "timestamp"].item(), "2026-01-01T09:04:00Z")
        pd.testing.assert_frame_equal(frame, original)

    def test_conflicts_quarantine_both_versions(self):
        result = prepare_events(pd.DataFrame([row(), row(latency_ms="99")]))
        self.assertTrue(result.cleaned.empty)
        self.assertEqual(len(result.rejected), 2)
        self.assertTrue(result.rejected.reasons.str.contains("conflicting_event_key").all())

    def test_exact_duplicate_does_not_discard_first_record(self):
        result = prepare_events(pd.DataFrame([row(), row()]))
        self.assertEqual(len(result.cleaned), 1)
        self.assertEqual(result.rejected.reasons.tolist(), ["exact_duplicate"])

    def test_event_ids_can_repeat_across_distinct_sources(self):
        result = prepare_events(pd.DataFrame([row(), row(source="authentication_gateway")]))
        self.assertEqual(len(result.cleaned), 2)

    def test_nonfinite_fractional_and_negative_numeric_data_rejected(self):
        rows = [row(event_id=str(i), **change) for i, change in enumerate([
            {"latency_ms": "inf"}, {"bytes_sent": "NaN"}, {"bytes_sent": "1.5"}, {"bytes_sent": "-1"}
        ])]
        result = prepare_events(pd.DataFrame(rows))
        self.assertEqual(len(result.rejected), 4)
        self.assertTrue(result.cleaned.empty)
        self.assertIsNone(result.report["latency_summary"]["mean_ms"])

    def test_schema_failure_is_explicit(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns.*timestamp"):
            prepare_events(pd.DataFrame({"event_id": ["a"]}))

    def test_byte_integer_boundary_is_exact_and_overflow_is_rejected(self):
        limit = 2**63 - 1
        result = prepare_events(pd.DataFrame([row(event_id="max", bytes_sent=str(limit)), row(event_id="overflow", bytes_sent=str(limit + 1))]))
        self.assertEqual(result.cleaned["bytes_sent"].tolist(), [limit])
        self.assertEqual(result.rejected["reasons"].tolist(), ["invalid_bytes"])

    def test_empty_input_with_headers_has_valid_report(self):
        result = prepare_events(pd.DataFrame(columns=FIELDS))
        self.assertEqual(result.report["rows_input"], 0)
        self.assertEqual(result.report["latency_summary"]["observed_count"], 0)

    def test_file_run_preserves_input_and_repeats_results(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "events.csv"
            pd.DataFrame([row(), row(event_id="b", latency_ms="")]).to_csv(source, index=False)
            before = source.read_bytes()
            prepare_file(source, root / "first")
            prepare_file(source, root / "second")
            self.assertEqual(before, source.read_bytes())
            for name in ["cleaned_events.csv", "rejected_events.csv", "quality_report.json", "summary.txt"]:
                self.assertEqual((root / "first" / name).read_bytes(), (root / "second" / name).read_bytes())

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "cleaned_events.csv"
            pd.DataFrame([row()]).to_csv(source, index=False)
            with self.assertRaisesRegex(ValueError, "input must be separate"):
                prepare_file(source, source.parent)


if __name__ == "__main__":
    unittest.main()
