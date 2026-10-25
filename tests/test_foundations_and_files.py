from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.foundations import run_first_example, storage_rule
from practical_ml_ai.python_workflow import read_events, read_tickets, run_workflow, summarize_tickets


class FoundationTests(unittest.TestCase):
    def test_threshold_boundary(self):
        self.assertFalse(storage_rule(80))
        self.assertTrue(storage_rule(81))
        self.assertFalse(storage_rule(0))
        self.assertTrue(storage_rule(100))

    def test_invalid_measurements_do_not_produce_a_decision(self):
        for value in [True, -1, 101, float("nan"), float("inf"), "85"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                storage_rule(value)

    def test_script_runs_without_site_packages_from_another_folder(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "first.txt"
            result = subprocess.run([sys.executable, "-S", str(ROOT / "examples/first-run/scripts/first_run.py"), "--storage-percent", "80", "--output", str(output)], cwd=temporary, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Within the chosen threshold", output.read_text())
            self.assertIn("no model was trained", result.stdout)


class FileWorkflowTests(unittest.TestCase):
    def test_fixture_summaries_and_raw_bytes_are_preserved(self):
        tickets = ROOT / "data/samples/service-files/tickets.csv"
        events = ROOT / "data/samples/service-files/events.json"
        before = [tickets.read_bytes(), events.read_bytes()]
        with tempfile.TemporaryDirectory() as temporary:
            report = run_workflow(tickets, events, temporary)
            self.assertEqual(report["tickets"]["count"], 4)
            self.assertEqual(report["tickets"]["total_minutes"], 60)
            self.assertEqual(report["tickets"]["average_minutes"], 15)
            self.assertEqual(report["tickets"]["by_category"]["network"], {"ticket_count": 2, "total_minutes": 25})
            self.assertEqual(report["events"]["by_severity"], {"info": 2, "warning": 1, "critical": 0})
            self.assertEqual(json.loads((Path(temporary) / "report.json").read_text()), report)
        self.assertEqual(before, [tickets.read_bytes(), events.read_bytes()])

    def test_empty_tickets_has_no_fabricated_average(self):
        result = summarize_tickets([])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["total_minutes"], 0)
        self.assertIsNone(result["average_minutes"])

    def test_missing_header_and_bad_minutes_have_actionable_errors(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "tickets.csv"
            path.write_text("ticket_id,category\na,network\n")
            with self.assertRaisesRegex(ValueError, "needs.*minutes"):
                read_tickets(path)
            path.write_text("ticket_id,category,minutes\na,network,unknown\n")
            with self.assertRaisesRegex(ValueError, "line 2.*whole number"):
                read_tickets(path)

    def test_duplicate_ids_are_not_silently_counted_twice(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "tickets.csv"
            path.write_text("ticket_id,category,minutes\na,network,5\na,network,5\n")
            with self.assertRaisesRegex(ValueError, "duplicate ticket_id"):
                read_tickets(path)

    def test_json_requires_valid_record_objects_and_labels(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "events.json"
            for value in [{"event_id": "a"}, [{"event_id": "a", "source": "test", "severity": "urgent"}], [None]]:
                path.write_text(json.dumps(value))
                with self.subTest(value=value), self.assertRaises(ValueError):
                    read_events(path)

    def test_file_workflow_script_uses_no_third_party_packages(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run([sys.executable, "-S", str(ROOT / "examples/service-files/scripts/summarize.py"), "--tickets", str(ROOT / "data/samples/service-files/tickets.csv"), "--events", str(ROOT / "data/samples/service-files/events.json"), "--output", temporary], cwd=temporary, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Total handling minutes: 60", result.stdout)

    def test_generated_output_cannot_replace_raw_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "report.json"
            path.write_text("[]")
            with self.assertRaisesRegex(ValueError, "separate"):
                run_workflow(ROOT / "data/samples/service-files/tickets.csv", path, temporary)


if __name__ == "__main__":
    unittest.main()
