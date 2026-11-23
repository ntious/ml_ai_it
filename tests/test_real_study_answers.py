"""Numbers quoted in complete-study feedback must match what the studies produce."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
VERIFIED = ROOT / "runs/verified"


def feedback(slug):
    page = (ROOT / "docs/lessons" / slug / "solutions.md").read_text(encoding="utf-8")
    start = page.index("## Complete-study results feedback")
    return page[start:page.index("\n## ", start + 1)]


class FixtureAnswerTests(unittest.TestCase):
    def test_module_2_to_4_answers_match_fresh_fixture_runs(self):
        from practical_ml_ai.python_workflow import run_workflow
        from practical_ml_ai.data.events import prepare_file
        from practical_ml_ai.exploration import run_exploration
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            run_workflow(ROOT / "data/samples/service-files/tickets.csv", ROOT / "data/samples/service-files/events.json", out / "m2")
            category = pd.read_csv(out / "m2/category_summary.csv").set_index("category").loc["network"]
            self.assertEqual((category.ticket_count, category.total_minutes), (2, 25))
            self.assertIn("2 tickets (T001 and T003) and 25 total minutes", feedback("02-python-workflows"))

            prepare_file(ROOT / "data/samples/network-events/events.csv", out / "m3")
            observed = pd.read_csv(out / "m3/cleaned_events.csv").latency_ms.dropna()
            self.assertEqual((len(observed), observed.mean(), observed.median()), (5, 24.0, 20.0))
            self.assertIn("mean of the five observed values is 24 ms and the median is 20 ms", feedback("03-data-processing"))

            run_exploration(ROOT / "data/samples/service-workload/daily.csv", out / "m4")
            p95 = pd.read_csv(out / "m4/request_latency.csv").p95_latency_ms.dropna()
            self.assertEqual((len(p95), p95.median(), round(p95.mean(), 1)), (23, 34.0, 38.7))
            self.assertIn("23 observed values and their median is 34.0 ms", feedback("04-exploration"))


@unittest.skipUnless((VERIFIED / "module14/routing_confusion.csv").is_file(), "Needs verified framework artifacts (site build).")
class VerifiedRunAnswerTests(unittest.TestCase):
    def test_framework_answers_match_verified_artifacts(self):
        comparison = pd.read_csv(VERIFIED / "module09/comparison.csv").set_index("method")
        self.assertEqual(tuple(comparison.loc["neural", ["tp", "fn", "fp"]]), (118, 10, 30))
        generation = pd.read_csv(VERIFIED / "module10/generation_evaluation.csv")
        self.assertEqual((int(generation.schema_valid.sum()), int(generation.correct.sum())), (99, 39))
        self.assertEqual(json.loads((VERIFIED / "module11/summary.json").read_text(encoding="utf-8"))["trainable_parameters"], 460800)
        routing = pd.read_csv(VERIFIED / "module14/routing_confusion.csv").set_index("expected_tool")
        self.assertEqual(sum(routing.loc[name, name] for name in routing.index), 22)


if __name__ == "__main__":
    unittest.main()
