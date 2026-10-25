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

    def test_llm_schema_failures_are_not_repaired(self):
        from practical_ml_ai.language import parse_label
        self.assertEqual(self.results[10]["real_examples"], 8)
        self.assertTrue(0 <= self.results[10]["strict_schema_rate"] <= 1)
        for value in ['{"label":"spam","extra":1}', "spam", '{"label":"unknown"}']:
            self.assertIsNone(parse_label(value))
        self.assertEqual(parse_label('{"label":"ham"}'), 0)

    def test_actual_adapter_updates_and_replay(self):
        result = self.results[11]
        self.assertGreater(result["adapter_update_norm"], 0)
        self.assertGreater(result["trainable_parameters"], 0)
        self.assertTrue(result["adapter_replay_verified"])
        self.assertTrue(np.isfinite(result["adapted_test_completion_loss"]))
        state = np.load(self.base / "m11/adapter.npz", allow_pickle=False)
        self.assertGreater(np.linalg.norm(state["b"]), 0)

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
        self.assertEqual(bounded_agent("Delete all records")["tool_calls"], 0)
        traces = json.loads((self.base / "m14/tool_trace.json").read_text())
        self.assertTrue(all(row["tool_calls"] <= 1 for row in traces))

    def test_every_remaining_public_cli(self):
        paths = {8:"wine-neural-network",9:"sms-neural-nlp",10:"sms-llm",11:"sms-fine-tuning",12:"model-service",14:"bounded-assistant"}
        for number, name in paths.items():
            process = subprocess.run([sys.executable, str(ROOT / "examples" / name / "scripts/run.py"),
                                      "--output", str(self.base / f"cli{number}")],
                                     cwd=self.base, capture_output=True, text=True, timeout=600)
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
