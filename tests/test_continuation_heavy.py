"""Opt-in actual frameworks/model checks, executed in Linux CPU CI."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@unittest.skipUnless(os.environ.get("ML_AI_HEAVY") == "1", "Executed by the Linux CPU framework job.")
class FrameworkWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from practical_ml_ai.course_runner import run_module
        cls.temporary = tempfile.TemporaryDirectory()
        cls.base = Path(cls.temporary.name)
        cls.results = {number: run_module(number, cls.base / f"m{number}") for number in [8, 9, 10, 11, 12, 14]}

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_actual_tensorflow_training_checkpoint_and_reload(self):
        for number in [8, 9]:
            result = self.results[number]
            self.assertGreater(result["weight_change_norm"], 0)
            self.assertTrue(result["saved_model_replay_verified"])
            self.assertTrue(1 <= result["best_validation_epoch"] <= result["epochs_requested"])
            self.assertTrue((self.base / f"m{number}/model.keras").is_file())
            self.assertTrue(0 <= result["test"]["balanced_accuracy"] <= 1)

    def test_real_training_vocabulary_is_recorded(self):
        vocabulary = json.loads((self.base / "m9/vocabulary.json").read_text())
        self.assertGreater(len(vocabulary), 100)
        self.assertEqual(self.results[9]["vocabulary_fitted_on"], "training only")
        self.assertGreater(self.results[9]["sample_rows"], 5000)
        # Broad collapse guard for this fixed historical teaching benchmark,
        # not a population-performance claim or a test-selected training target.
        self.assertGreater(self.results[9]["test"]["recall"], .5)
        self.assertGreater(self.results[9]["linear_baseline"]["recall"], .5)
        history = __import__("pandas").read_csv(self.base / "m9/learning_history.csv")
        self.assertTrue(np.isfinite(history.validation_loss).all())

    def test_llm_schema_failures_are_not_repaired(self):
        from practical_ml_ai.language import parse_label
        self.assertEqual(self.results[10]["real_examples"], 100)
        self.assertTrue(0 <= self.results[10]["strict_schema_rate"] <= 1)
        for value in ['{"label":"spam","extra":1}', "spam", '{"label":"unknown"}']:
            self.assertIsNone(parse_label(value))
        self.assertEqual(parse_label('{"label":"ham"}'), 0)

    def test_matched_generation_evidence_uses_same_ids(self):
        import pandas as pd
        table=pd.read_csv(self.base/"m10/matched_comparison.csv")
        generation=pd.read_csv(self.base/"m10/generation_evaluation.csv")
        self.assertEqual(table.text_id.tolist(),generation.text_id.tolist())
        self.assertEqual(table.actual.tolist(),generation.actual.tolist())
        self.assertEqual(len(table),100)
        self.assertAlmostEqual(float(table.baseline_correct.mean()),self.results[10]["matched_baseline_accuracy"])
        tuned=pd.read_csv(self.base/"m11/generation_comparison.csv")
        self.assertEqual(len(tuned),100)
        self.assertAlmostEqual(float(tuned.base_correct.mean()),self.results[11]["base_generation_accuracy"])
        self.assertAlmostEqual(float(tuned.adapted_correct.mean()),self.results[11]["adapted_generation_accuracy"])

    def test_actual_adapter_updates_and_replay(self):
        result = self.results[11]
        self.assertGreater(result["adapter_update_norm"], 0)
        self.assertGreater(result["trainable_parameters"], 0)
        self.assertTrue(result["adapter_replay_verified"])
        self.assertTrue(np.isfinite(result["adapted_test_completion_loss"]))
        from safetensors.torch import load_file
        from practical_ml_ai.language import local_model
        state = load_file(self.base / "m11/adapter/adapter_model.safetensors")
        self.assertTrue(any("lora_B" in name and float(value.norm()) > 0 for name, value in state.items()))
        self.assertGreater(result["adapted_schema_rate"], result["base_schema_rate"])
        base, _, _ = local_model()
        self.assertFalse(any("lora" in name for name, _ in base.named_parameters()))
        self.assertTrue(all(not value.requires_grad for value in base.parameters()))
        self.assertLessEqual(result["selected_step"], result["steps"])

    def test_training_and_generation_denominators_and_intervals(self):
        import pandas as pd
        for number in [10, 11]:
            intervals = pd.read_csv(self.base / f"m{number}/rate_intervals.csv")
            self.assertTrue((intervals.observations == 100).all())
            np.testing.assert_allclose(intervals.rate, intervals.successes / intervals.observations)
            self.assertTrue((intervals.ci_low <= intervals.rate).all())
            self.assertTrue((intervals.rate <= intervals.ci_high).all())
        manifest = json.loads((self.base / "m11/split_manifest.json").read_text())
        for a, b in [("training_subset", "validation_subset"), ("training_subset", "final_subset"), ("validation_subset", "final_subset")]:
            self.assertFalse(set(manifest[a]) & set(manifest[b]))
        validation = pd.read_csv(self.base / "m11/validation_generation.csv")
        self.assertEqual(len(validation), 40)

    def test_service_schema_rejects_mutated_real_record(self):
        from practical_ml_ai.classical import classification_bundle
        from practical_ml_ai.deployment import checked_predict
        bundle = classification_bundle()
        record = bundle["split"]["test"].iloc[0][bundle["features"]].to_dict()
        self.assertTrue(0 <= checked_predict(bundle, record)["probability"] <= 1)
        for mutation in ["missing", "target", "nonfinite", "boolean"]:
            changed = dict(record)
            if mutation == "missing": changed.pop(bundle["features"][0])
            if mutation == "target": changed["quality"] = 7
            if mutation == "nonfinite": changed[bundle["features"][0]] = float("inf")
            if mutation == "boolean": changed[bundle["features"][0]] = True
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                checked_predict(bundle, changed)

    def test_bounded_tools_and_invalid_control_plans(self):
        from practical_ml_ai.continuation_data import wine_splits
        from practical_ml_ai.language import bounded_agent, execute_tool
        import pandas as pd
        split, features, _ = wine_splits()
        frame = pd.concat(list(split.values()))
        self.assertEqual(execute_tool({"tool":"summary","arguments":{}}, frame, features)["observations"], 1599)
        for plan in [{"tool":"shell","arguments":{}}, {"tool":"feature","arguments":{"name":"password"}}, {"tool":"summary","arguments":{"write":True}}]:
            with self.assertRaises(ValueError):
                execute_tool(plan, frame, features)
        self.assertLessEqual(bounded_agent("Delete all records")["tool_calls"], 1)
        traces = json.loads((self.base / "m14/tool_trace.json").read_text())
        self.assertTrue(all(row["tool_calls"] <= 1 for row in traces))
        self.assertTrue(all(row["steps_used"] <= 3 for row in traces))
        self.assertGreaterEqual(len(traces), 20)
        self.assertFalse(self.results[14]["destructive_tools_available"])
        correct = sum(row["chosen_tool"] == row["expected_tool"] for row in traces)
        self.assertAlmostEqual(correct / len(traces), self.results[14]["routing_accuracy"])
        unsupported = [row for row in traces if row["expected_tool"] == "refuse"]
        self.assertEqual(sum(row["chosen_tool"] == "refuse" for row in unsupported),
                         self.results[14]["unsupported_correctly_refused"])
        for budget in [1, 2]:
            result = bounded_agent("Count wine rows.", max_steps=budget)
            self.assertEqual(result["result"]["status"], "incomplete")
            self.assertLessEqual(result["steps_used"], budget)
        with self.assertRaises(ValueError):
            bounded_agent("Count wine rows.", max_steps=4)

    def test_every_remaining_public_cli(self):
        paths = {8:"wine-neural-network",9:"sms-neural-nlp",10:"sms-llm",11:"sms-fine-tuning",12:"model-service",14:"bounded-assistant"}
        for number, name in paths.items():
            options = []
            # Full default budgets are exercised above and by fresh notebooks.
            # The second run checks CLI plumbing with an explicitly smaller budget.
            if number in [8, 9]: options = ["--epochs", "3"]
            if number == 10: options = ["--examples", "20"]
            if number == 11: options = ["--steps", "25"]
            process = subprocess.run([sys.executable, str(ROOT / "examples" / name / "scripts/run.py"),
                                      "--output", str(self.base / f"cli{number}"), *options],
                                     cwd=self.base, capture_output=True, text=True, timeout=1200)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertTrue((self.base / f"cli{number}/summary.json").exists())

    def test_streamlit_forms_and_real_inference(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / "apps/wine_quality.py"), default_timeout=180).run()
        self.assertEqual(len(app.exception), 0)
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertGreaterEqual(len(app.metric), 2)
        app.radio[0].set_value("Local LLM triage").run()
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(len(app.success) + len(app.error) >= 1)

    def test_streamlit_server_health(self):
        process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", str(ROOT / "apps/wine_quality.py"),
                                    "--server.headless", "true", "--server.address", "127.0.0.1", "--server.port", "8765"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            ready = False
            for _ in range(40):
                try:
                    with urllib.request.urlopen("http://127.0.0.1:8765/_stcore/health", timeout=1) as response:
                        ready = response.read().decode().strip() == "ok"
                    if ready: break
                except OSError:
                    time.sleep(.25)
            self.assertTrue(ready)
        finally:
            process.terminate()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired: process.kill(); process.wait()


if __name__ == "__main__":
    unittest.main()
