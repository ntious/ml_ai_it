"""The generated outcome map stays consistent with its data and the lesson pages."""
from pathlib import Path
import copy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_outcome_map as outcome_map


class OutcomeMapTests(unittest.TestCase):
    def test_data_is_consistent_with_modules_and_bridges(self):
        data, modules = outcome_map.load()
        self.assertEqual(outcome_map.validate(data, modules), [])

    def test_coverage_gaps_are_allowed_and_visible(self):
        data, modules = outcome_map.load()
        for module in data["modules"]:
            module["support"] = list(set(module["support"] + module["direct"]))
            module["direct"] = []
        self.assertEqual(outcome_map.validate(data, modules), [])
        self.assertIn("No direct core-module evidence", outcome_map.map_page(data, modules))

    def test_duplicate_identifiers_and_unknown_schema_are_rejected(self):
        for collection in ("outcomes", "extensions", "modules", "additional_activities"):
            data, modules = outcome_map.load()
            data[collection].append(copy.deepcopy(data[collection][0]))
            with self.subTest(collection=collection):
                self.assertIn(f"duplicate IDs in {collection}", outcome_map.validate(data, modules))
        data, modules = outcome_map.load()
        data["schema_version"] = 999
        self.assertIn("unsupported schema_version", outcome_map.validate(data, modules))

    def test_additional_evidence_requires_known_activity(self):
        data, modules = outcome_map.load()
        data["modules"][0]["additional_direct"] = ["MISSING"]
        self.assertIn("module 1: unknown additional activity MISSING", outcome_map.validate(data, modules))

    def test_practice_regeneration_preserves_authored_surroundings(self):
        item = outcome_map.load()[0]["modules"][0]
        text = "## Responsible-AI check\n\nInstructor introduction.\n" + outcome_map.PRACTICE_START + "\nOld generated text\n" + outcome_map.PRACTICE_END + "\nInstructor conclusion.\n"
        revised = outcome_map.with_practice(text, outcome_map.practice_block(item))
        self.assertIn("Instructor introduction.", revised)
        self.assertTrue(revised.endswith("Instructor conclusion.\n"))
        self.assertNotIn("Old generated text", revised)
        self.assertEqual(revised, outcome_map.with_practice(revised, outcome_map.practice_block(item)))
        with self.assertRaises(ValueError):
            outcome_map.with_practice(text.replace(outcome_map.PRACTICE_END, ""), outcome_map.practice_block(item))

    def test_generated_pages_are_current(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/build_outcome_map.py"), "--check"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_windows_checkout_line_endings_do_not_hide_content_changes(self):
        data, modules = outcome_map.load()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            paths = ["docs/outcome-map.md"]
            for module in modules:
                paths.extend([module["lesson"], str(Path(module["lesson"]).with_name("practice.md"))])
            for name in paths:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                source = (ROOT / name).read_text(encoding="utf-8")
                target.write_bytes(source.replace("\n", "\r\n").encode("utf-8"))
            with patch.object(outcome_map, "ROOT", root), patch.object(outcome_map, "load", return_value=(data, modules)), patch.object(outcome_map, "validate", return_value=[]), patch.object(sys, "argv", ["build_outcome_map.py", "--check"]):
                outcome_map.main()
                target = root / "docs/outcome-map.md"
                target.write_bytes(target.read_bytes() + b"Unreviewed content\r\n")
                with self.assertRaisesRegex(SystemExit, "Stale generated outcome text"):
                    outcome_map.main()


if __name__ == "__main__":
    unittest.main()
