"""Real-source end-to-end and tamper/selection contracts for the optional project."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai import capstone as c
from practical_ml_ai.capstone_models import candidate, export_model, numeric_predict


class ConfigurationTests(unittest.TestCase):
    def test_bounded_search_and_seed_contracts(self):
        config = c.read_json(ROOT / "projects/phishing-triage/configs/study.json")
        self.assertEqual(c.config_check(config)["cv_folds"], 3)
        for field, value in [("schema_version", True), ("training_seeds", [11, 11]), ("thresholds", [True, .5]),
                             ("false_negative_cost", float("nan")), ("max_cv_fits", 3)]:
            changed = copy.deepcopy(config); changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                c.config_check(changed)


@unittest.skipUnless(os.environ.get("ML_AI_REAL_DATA") == "1", "Capstone real-source acceptance runs in core CI.")
class CapstoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        cls.directory = cls.root / "study"
        config = c.read_json(ROOT / "projects/phishing-triage/configs/study.json")
        config.update(training_seeds=[11, 23], split_seeds=[101, 202], bootstrap_repetitions=50)
        config["search"] = {"logistic": {"C": [1.]}, "tree": {"max_depth": [6]},
                            "forest": {"max_depth": [6], "min_samples_leaf": [5], "n_estimators": [10]}}
        cls.config = cls.root / "config.json"
        c.save(cls.config, config)
        c.prepare(cls.directory, cls.config)
        # Selection stages may hash the final file for integrity but never parse its labels.
        original = c.part
        def development_only(run, name):
            if name == "test":
                raise AssertionError("Final labels accessed before freeze")
            return original(run, name)
        with patch.object(c, "part", side_effect=development_only):
            for stage in [c.tune, c.split_study, c.stability, c.freeze]:
                stage(cls.directory)
        for stage in [c.evaluate, c.deliver, c.report]:
            stage(cls.directory)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_full_orchestration_and_resume(self):
        c.verify(self.directory, "report")
        marker = c.digest(self.directory / "report.done.json")
        process = subprocess.run([sys.executable, str(ROOT / "projects/phishing-triage/scripts/run.py"), "all",
                                  "--run", str(self.directory), "--config", str(self.config), "--advanced", "--resume"],
                                 cwd=self.root, text=True, capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout.count("VERIFIED_SKIP"), 8)
        self.assertEqual(c.digest(self.directory / "report.done.json"), marker)

    def test_outer_and_inner_groups_never_cross(self):
        parts = {name: c.part(self.directory, name) for name in ["train", "validation", "test"]}
        for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]:
            self.assertFalse(set(parts[a].profile_id) & set(parts[b].profile_id))
        train = parts["train"].set_index("record_id")
        for fold in c.read_json(self.directory / "inner_folds.json"):
            self.assertFalse(set(train.loc[fold["fit_record_ids"]].profile_id) & set(train.loc[fold["check_record_ids"]].profile_id))
        self.assertEqual(len(pd.read_csv(self.directory / "search_trials.csv")), 9)

    def test_every_seed_and_stability_summary_are_reported(self):
        rows = pd.read_csv(self.directory / "validation_runs.csv")
        summary = pd.read_csv(self.directory / "validation_stability.csv").set_index("family")
        for family in ["logistic", "tree", "forest"]:
            values = rows.loc[rows.family == family]
            self.assertEqual(set(values.seed), {11, 23})
            self.assertAlmostEqual(float(summary.loc[family, "mean"]), values.cost_per_1000.mean())
            self.assertAlmostEqual(float(summary.loc[family, "std"]), values.cost_per_1000.std(ddof=1))
            self.assertEqual(values.threshold.nunique(), 1)
        choice = c.read_json(self.directory / "selection.json")
        self.assertEqual(choice["seeds"], [11] if choice["family"] == "dummy" else [11, 23])

    def test_numeric_export_matches_actual_fitted_estimators(self):
        info, config = c.protocol(self.directory); train = c.part(self.directory, "train")
        for family in ["dummy", "logistic", "tree", "forest"]:
            parameters = {} if family == "dummy" else c.read_json(self.directory / "tuning.json")["selected"][family]["parameters"]
            model = candidate(family, parameters, 11).fit(train[info["features"]], train.label)
            artifact = export_model(model, family, info["features"], 11)
            # JSON round trip; no object deserialization or pickle is used.
            restored = json.loads(json.dumps(artifact))
            np.testing.assert_allclose(numeric_predict(restored, train.iloc[:128]),
                                       model.predict_proba(train.iloc[:128][info["features"]])[:, 1], atol=1e-10)

    def test_frozen_predictions_costs_and_delivery_reconcile(self):
        rows = pd.read_csv(self.directory / "final_predictions.csv")
        evaluation = c.read_json(self.directory / "evaluation.json")
        config = c.read_json(self.directory / "config.json")
        actual = c.scores(rows.label, rows.probability.to_numpy(), evaluation["threshold"], config)
        self.assertAlmostEqual(actual["cost_per_1000"], evaluation["ensemble"]["cost_per_1000"])
        self.assertEqual(actual["tp"] + actual["fp"] + actual["fn"] + actual["tn"], len(rows))
        bundle = c.read_json(self.directory / "inference_bundle.json")
        request = c.read_json(self.directory / "example_request.json")
        self.assertAlmostEqual(c.predict(bundle, request)["probability"], float(rows.iloc[0].probability))
        for mutated in [{**request, "label": 1}, {**request, next(iter(request)): True}, {**request, next(iter(request)): 2}]:
            with self.assertRaises(ValueError): c.predict(bundle, mutated)
        self.assertTrue(all(row["rejected"] for row in c.read_json(self.directory / "service_checks.json")))
        self.assertFalse(c.read_json(self.directory / "release_decision.json")["live_deployment_approved"])

    def test_split_variation_is_separate_and_training_seed_fixed(self):
        rows = pd.read_csv(self.directory / "split_sensitivity.csv")
        self.assertEqual(set(rows.split_seed), {101, 202})
        self.assertEqual(rows.training_seed.nunique(), 1)
        self.assertEqual(set(rows.training_seed), {17})

    def test_changed_data_models_or_optional_evidence_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "study"; shutil.copytree(self.directory, copied)
            (copied / "split-study.done.json").unlink()
            with self.assertRaises(OSError):
                c.verify(copied, "freeze")
        for filename in ["train.csv", "selection.json", "split_sensitivity.csv"]:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temporary:
                copied = Path(temporary) / "study"; shutil.copytree(self.directory, copied)
                with (copied / filename).open("a", encoding="utf-8") as output: output.write("\n")
                with self.assertRaises(ValueError): c.verify(copied, "report")

    def test_repeated_and_out_of_order_stages_do_not_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "study"; shutil.copytree(self.directory, copied)
            (copied / "split-study.done.json").unlink()
            with self.assertRaisesRegex(ValueError, "before freezing"):
                c.split_study(copied)
        before = c.digest(self.directory / "selection.json")
        with self.assertRaises(ValueError): c.freeze(self.directory)
        self.assertEqual(c.digest(self.directory / "selection.json"), before)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(OSError): c.evaluate(Path(temporary))


if __name__ == "__main__":
    unittest.main()
