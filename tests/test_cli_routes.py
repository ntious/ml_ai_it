"""Exercise the two earlier data CLI routes not covered by subprocess tests.

Shared-function tests already establish numerical behavior. These checks add
the user-facing path: a command launched outside the checkout saves its report.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EarlierDataCommandTests(unittest.TestCase):
    def test_module03_script_writes_named_artifacts_from_another_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "preparation"
            command = [sys.executable, str(ROOT / "examples/network-events/scripts/prepare.py"),
                       "--input", str(ROOT / "data/samples/network-events/events.csv"),
                       "--output", str(output)]
            process = subprocess.run(command, cwd=temporary, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((output / "quality_report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["rows_accepted"], 6)
            self.assertTrue((output / "rejected_events.csv").is_file())
            self.assertTrue((output / "summary.txt").is_file())

    def test_module04_script_writes_reading_and_numerical_routes(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "exploration"
            command = [sys.executable, str(ROOT / "examples/service-workload/scripts/explore.py"),
                       "--input", str(ROOT / "data/samples/service-workload/daily.csv"),
                       "--output", str(output)]
            process = subprocess.run(command, cwd=temporary, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((output / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(report["total_requests"], 4180)
            self.assertTrue((output / "index.html").is_file())
            self.assertTrue((output / "chart_descriptions.md").is_file())


if __name__ == "__main__":
    unittest.main()
