"""Behavioral checks for forecast timing, split discipline, and saved artifacts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.regression import (
    FEATURES, TARGET, build_examples, digest, download_bike_data,
    evaluate_study, fit_linear, infer_study, leakage_demo, load_split,
    predict_artifact, prepare_study, read_daily, report_study, run_study,
    train_study, training_cv, validate_study,
)

SMOKE = ROOT / "data/samples/forecast-demand/daily.csv"


class RegressionTests(unittest.TestCase):
    def prepared(self, directory):
        run = Path(directory) / "study"
        manifest = prepare_study(SMOKE, run)
        return run, manifest

    def test_forecast_features_only_use_observed_past(self):
        daily = read_daily(SMOKE)
        examples, future = build_examples(daily)
        self.assertEqual(len(examples), 84)
        self.assertEqual(examples.iloc[0]["prior_day_requests"], daily.iloc[6]["requests"])
        self.assertEqual(examples.iloc[0]["prior_week_requests"], daily.iloc[0]["requests"])
        self.assertEqual(examples.iloc[0][TARGET], daily.iloc[7]["requests"])
        self.assertNotIn(TARGET, future)
        self.assertEqual(future.iloc[0]["prior_week_requests"], daily.iloc[-7]["requests"])
        altered = daily.copy()
        altered.loc[90, "requests"] += 100
        revised, _ = build_examples(altered)
        pd.testing.assert_frame_equal(examples.iloc[:-1], revised.iloc[:-1])
        self.assertEqual(examples.iloc[-1]["prior_day_requests"], revised.iloc[-1]["prior_day_requests"])

    def test_chronological_split_rows_and_raw_bytes(self):
        before = SMOKE.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            run, manifest = self.prepared(directory)
            self.assertEqual([manifest["splits"][name]["rows"] for name in ["train", "validation", "final_test"]], [56, 14, 14])
            train, validation, test = [load_split(run, name) for name in ["train", "validation", "final_test"]]
            self.assertLess(train.target_date.max(), validation.target_date.min())
            self.assertLess(validation.target_date.max(), test.target_date.min())
            self.assertEqual(manifest["source_sha256"], digest(SMOKE))
        self.assertEqual(SMOKE.read_bytes(), before)

    def test_train_and_validate_do_not_open_final_test(self):
        with tempfile.TemporaryDirectory() as directory:
            run, _ = self.prepared(directory)
            test_path = run / "final_test.csv"
            original = test_path.read_bytes()
            test_path.unlink()
            validation_path = run / "validation.csv"
            validation_bytes = validation_path.read_bytes()
            validation_path.unlink()
            trained = train_study(run)
            self.assertEqual(trained["training_rows"], 56)
            validation_path.write_bytes(validation_bytes)
            selected = validate_study(run)
            self.assertIn(selected["selected"], trained["models"])
            self.assertFalse(test_path.exists())
            test_path.write_bytes(original)
            self.assertEqual(evaluate_study(run)["test_rows"], 14)

    def test_imputer_is_fitted_on_training_and_json_matches_pipeline(self):
        training = pd.DataFrame({"prior_day_requests": [1.0, np.nan, 3.0, 5.0], TARGET: [2.0, 4.0, 6.0, 10.0]})
        pipeline, artifact = fit_linear(training, ["prior_day_requests"])
        self.assertEqual(artifact["fill_values"], [3.0])
        query = pd.DataFrame({"prior_day_requests": [np.nan, 1000.0]})
        np.testing.assert_allclose(predict_artifact(artifact, query), pipeline.predict(query[["prior_day_requests"]].to_numpy()), rtol=1e-12)
        self.assertEqual(artifact["fill_values"], [3.0])

    def test_target_feature_and_all_missing_training_feature_are_rejected(self):
        training = pd.DataFrame({"prior_day_requests": [np.nan, np.nan], TARGET: [1, 2]})
        with self.assertRaisesRegex(ValueError, "past-only"):
            fit_linear(training, [TARGET])
        with self.assertRaisesRegex(ValueError, "no observed training"):
            fit_linear(training, ["prior_day_requests"])

    def test_training_cv_uses_earlier_targets_within_training_only(self):
        with tempfile.TemporaryDirectory() as directory:
            run, _ = self.prepared(directory)
            training = load_split(run, "train")
            folds = training_cv(training)
            self.assertEqual(len(folds), 3)
            self.assertTrue((folds.last_fit_target < folds.first_check_target).all())
            self.assertTrue(folds.mae.ge(0).all())
            self.assertEqual(folds.fit_rows.tolist(), [14, 28, 42])

    def test_leakage_demonstration_is_invalid_and_not_a_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            run, _ = self.prepared(directory)
            warning = leakage_demo(load_split(run, "train"), load_split(run, "validation"))
            self.assertLess(warning["invalid_validation_mae"], 1e-8)
            self.assertIn("unavailable", warning["warning"])
            models = train_study(run)["models"]
            self.assertEqual(set(models), {"training_mean", "previous_day", "previous_week", "linear_day", "linear_week"})

    def test_frozen_stages_prevent_accidental_refit_reselection_and_reevaluation(self):
        with tempfile.TemporaryDirectory() as directory:
            run, _ = self.prepared(directory)
            train_study(run); validate_study(run); evaluate_study(run)
            before = (run / "final_evaluation.json").read_bytes()
            for stage in [train_study, validate_study, evaluate_study]:
                with self.subTest(stage=stage.__name__), self.assertRaises(ValueError):
                    stage(run)
            self.assertEqual((run / "final_evaluation.json").read_bytes(), before)
            with self.assertRaisesRegex(ValueError, "new run"):
                prepare_study(SMOKE, run)

    def test_changed_split_and_changed_selected_artifact_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            run, _ = self.prepared(directory)
            path = run / "train.csv"
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            with self.assertRaisesRegex(ValueError, "split changed"):
                train_study(run)
            path.write_bytes(original)
            train_study(run); validate_study(run)
            (run / "candidates.json").write_text((run / "candidates.json").read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "changed after selection"):
                evaluate_study(run)

    def test_inference_uses_frozen_artifact_and_does_not_require_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            run, _ = self.prepared(directory)
            train_study(run); selected = validate_study(run)
            # Inference is separate from final evaluation and can run without it.
            output = infer_study(run)
            self.assertEqual(len(output), 1)
            self.assertEqual(output.iloc[0]["model"], selected["selected"])
            self.assertNotIn(TARGET, output)
            frame = pd.read_csv(run / "future_features.csv")
            frame[TARGET] = 999
            path = Path(directory) / "invalid.csv"; frame.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "features only"):
                infer_study(run, path)

    def test_invalid_dates_gaps_duplicates_and_counts_are_explained(self):
        original = pd.read_csv(SMOKE, dtype=str)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            cases = []
            bad = original.copy(); bad.loc[1, "date"] = bad.loc[0, "date"]; cases.append((bad, "consecutive"))
            bad = original.drop(index=5); cases.append((bad, "consecutive"))
            bad = original.copy(); bad.loc[0, "requests"] = "-1"; cases.append((bad, "whole-number"))
            bad = original.copy(); bad.loc[0, "requests"] = "1.5"; cases.append((bad, "whole-number"))
            bad = original.copy(); bad.loc[0, "requests"] = ""; cases.append((bad, "whole-number"))
            bad = original.copy(); bad.loc[0, "requests"] = "1000000001"; cases.append((bad, "upper bound"))
            for frame, message in cases:
                frame.to_csv(path, index=False)
                with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                    read_daily(path)

    def test_end_to_end_scores_match_exact_prediction_table_and_preserve_source(self):
        before = SMOKE.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "study"
            result = run_study(SMOKE, run, plots=True)
            predictions = pd.read_csv(run / "final_predictions.csv")
            for score in result["scores"]:
                records = predictions.loc[predictions.model == score["model"]]
                np.testing.assert_allclose(records.residual, records.actual_requests - records.predicted_requests)
                self.assertAlmostEqual(score["mae"], records.residual.abs().mean())
            selection = json.loads((run / "selection.json").read_text())
            self.assertEqual(result["selected"], selection["selected"])
            self.assertEqual(set(predictions.model), {result["selected"], "training_mean", "previous_day", "previous_week"})
            html = (run / "index.html").read_text()
            self.assertIn('scope="col"', html)
            self.assertIn('aria-describedby="residuals-description"', html)
            for name in ["forecast.png", "residuals.png"]:
                self.assertEqual((run / name).read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn("positive means underprediction", (run / "summary.txt").read_text())
            print("SMOKE_STUDY", json.dumps(result, sort_keys=True))
        self.assertEqual(SMOKE.read_bytes(), before)

    def test_documented_cli_runs_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "study"
            process = subprocess.run([sys.executable, str(ROOT / "examples/bike-demand/scripts/study.py"), "all", "--input", str(SMOKE), "--run", str(run)], cwd=directory, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertTrue((run / "forecast.csv").exists())
            self.assertIn("Selected final MAE", process.stdout)

    def test_cached_external_data_must_match_its_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "day.csv"; path.write_bytes(b"changed")
            (Path(directory) / "provenance.json").write_text(json.dumps({"day_csv_sha256": "wrong"}))
            with patch("urllib.request.urlopen") as network, self.assertRaisesRegex(ValueError, "checksum changed"):
                download_bike_data(directory)
            network.assert_not_called()

    @unittest.skipUnless(os.environ.get("ML_AI_REAL_DATA") == "1", "Real UCI integration enabled in CI; offline unit tests remain available.")
    def test_real_uci_dataset_download_and_complete_workflow(self):
        path = download_bike_data(ROOT / "runs/datasets/bike-sharing")
        raw = path.read_bytes()
        self.assertEqual(len(read_daily(path)), 731)
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "uci"
            result = run_study(path, run, holdout_days=110, plots=True, dataset_label="UCI Bike Sharing daily counts, CC BY 4.0")
            manifest = json.loads((run / "split_manifest.json").read_text())
            self.assertEqual([manifest["splits"][name]["rows"] for name in ["train", "validation", "final_test"]], [504, 110, 110])
            self.assertEqual(result["test_rows"], 110)
            self.assertTrue(np.isfinite([row["mae"] for row in result["scores"]]).all())
            print("REAL_UCI_STUDY", json.dumps(result, sort_keys=True))
            print("REAL_UCI_PROVENANCE", (path.parent / "provenance.json").read_text())
        self.assertEqual(path.read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
