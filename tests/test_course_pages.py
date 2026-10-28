"""Lesson pages keep module-specific guidance instead of shared template text."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULES = json.loads((ROOT / "curriculum/modules.json").read_text(encoding="utf-8"))["modules"]
TEMPLATE_PHRASES = ["On authored arguments", "Primary explanation", "Further reading:", "this module’s mechanism",
                    "Having already viewed a public final report", "Visible input arguments"]


class CoursePageTests(unittest.TestCase):
    def test_lessons_and_practice_notebooks_have_no_template_phrases(self):
        pages = [*(ROOT / "docs/lessons").rglob("*.md"), *(ROOT / "notebooks/practice").glob("*.ipynb")]
        found = [f"{page.relative_to(ROOT).as_posix()}: {phrase}" for page in pages
                 for phrase in TEMPLATE_PHRASES if phrase in page.read_text(encoding="utf-8")]
        self.assertEqual(found, [])

    def test_examples_use_call_notation_not_argument_lists(self):
        pattern = re.compile(r"(?:Predict the result on|For) `\[")
        found = [page.relative_to(ROOT).as_posix() for page in (ROOT / "docs/lessons").rglob("*.md")
                 if pattern.search(page.read_text(encoding="utf-8"))]
        self.assertEqual(found, [])

    def test_every_fixture_practice_has_a_reasoning_task_with_feedback(self):
        practice = json.loads((ROOT / "curriculum/practice.json").read_text(encoding="utf-8"))["modules"]
        # Modules 5, 6 and 8 use the fuller prototype structure with real-data sandboxes.
        for entry in [entry for entry in practice if entry["id"] not in (5, 6, 8)]:
            folder = ROOT / "docs/lessons" / entry["slug"]
            with self.subTest(module=entry["id"]):
                self.assertIn("## Reason beyond the visible checks", (folder / "practice.md").read_text(encoding="utf-8"))
                self.assertIn("## Reasoning task feedback", (folder / "solutions.md").read_text(encoding="utf-8"))
                self.assertIn("## Connect this to the full experiment", (folder / "concepts.md").read_text(encoding="utf-8"))
                module = next(m for m in MODULES if m["id"] == entry["id"])
                self.assertIn(module["script"], (folder / "concepts.md").read_text(encoding="utf-8"))

    def test_shared_rubric_lives_in_the_study_workflow_only(self):
        workflow = (ROOT / "docs/study-workflow.md").read_text(encoding="utf-8")
        self.assertIn("## How explanations are judged", workflow)
        copies = [page.relative_to(ROOT).as_posix() for page in (ROOT / "docs/lessons").rglob("*.md")
                  if "A satisfactory response includes" in page.read_text(encoding="utf-8")
                  or "Submit or retain your changed executable code" in page.read_text(encoding="utf-8")]
        self.assertEqual(copies, [])

    def test_research_guide_includes_a_located_worked_comparison(self):
        page = (ROOT / "docs/advanced/research-comparison.md").read_text(encoding="utf-8")
        worked = page[page.index("## Worked example"):page.index("## Practice a methodological comparison")]
        self.assertIn("arXiv:2103.03098", worked)
        for location in ["§2.2", "Figure 1", "§5", "Appendix B"]:
            self.assertIn(location, worked)
        for heading in ["**Evaluation differences.**", "**Limitations of the comparison.**", "**Course decision.**"]:
            self.assertIn(heading, worked)


if __name__ == "__main__":
    unittest.main()
