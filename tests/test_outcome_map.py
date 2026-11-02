"""The generated outcome map stays consistent with its data and the lesson pages."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_outcome_map as outcome_map


class OutcomeMapTests(unittest.TestCase):
    def test_data_is_consistent_with_modules_and_bridges(self):
        data, modules = outcome_map.load()
        self.assertEqual(outcome_map.validate(data, modules), [])

    def test_every_course_outcome_has_direct_evidence(self):
        data, _ = outcome_map.load()
        for outcome in data["outcomes"]:
            with self.subTest(outcome=outcome["id"]):
                self.assertTrue(any(outcome["id"] in item["direct"] for item in data["modules"]))

    def test_generated_pages_are_current(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/build_outcome_map.py"), "--check"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
