"""Tuning and encoding exercises keep selection on development data only."""
import os
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai import encoding, tuning


def numeric_split(seed=5, rows=480):
    rng = np.random.default_rng(seed)
    frame = pd.DataFrame({"a": rng.normal(size=rows), "b": rng.normal(size=rows), "c": rng.normal(size=rows)})
    frame["label"] = (frame.a - frame.b + rng.normal(scale=.7, size=rows) > .6).astype(int)
    parts = np.split(frame.sample(frac=1, random_state=seed), [320, 400])
    return dict(zip(["train", "validation", "test"], parts)), ["a", "b", "c"]


def coded_frames(seed=9, rows=600):
    """Authored -1/0/1 attributes; 'x' predicts the label only through its categories."""
    rng = np.random.default_rng(seed)
    frame = pd.DataFrame({name: rng.choice([-1, 0, 1], rows) for name in ["x", "y", "z"]})
    frame["label"] = ((frame.x == 0) ^ (rng.random(rows) < .1)).astype(int)
    return frame.iloc[:450].copy(), frame.iloc[450:].copy(), ["x", "y", "z"]


class TuningExerciseTests(unittest.TestCase):
    def test_fixed_budget_includes_boosting_and_reports_one_choice_per_family(self):
        split, features = numeric_split()
        trials, chosen, boundary = tuning.tune(split, features)
        self.assertEqual(boundary, {"cv_fits": 36, "configurations": 12, "final_test_rows_used": 0})
        self.assertEqual(sorted(trials.family.unique()), ["gradient_boosting", "logistic", "tree"])
        self.assertEqual(chosen.family.tolist(), ["logistic", "tree", "gradient_boosting"])
        for row in chosen.itertuples():
            best = trials[trials.family == row.family].cv_mean_balanced_accuracy.max()
            self.assertAlmostEqual(row.cv_mean_balanced_accuracy, best)

    def test_validation_and_test_labels_cannot_change_the_chosen_settings(self):
        split, features = numeric_split()
        flipped = {**split, "validation": split["validation"].assign(label=1 - split["validation"].label),
                   "test": split["test"].assign(label=1 - split["test"].label)}
        original, changed = tuning.tune(split, features)[1], tuning.tune(flipped, features)[1]
        self.assertEqual(original.settings.tolist(), changed.settings.tolist())


class EncodingExerciseTests(unittest.TestCase):
    def test_one_hot_captures_a_category_that_a_numeric_code_cannot(self):
        training, validation, features = coded_frames()
        table, evidence = encoding.compare(training, validation, features)
        scores = table.set_index("representation").balanced_accuracy
        self.assertGreater(scores["one_hot"], scores["codes_as_numbers"] + .2)
        self.assertEqual(table.set_index("representation").model_input_columns.to_dict(),
                         {"codes_as_numbers": 3, "one_hot": 9, "one_hot_plus_count": 10})
        self.assertEqual(evidence["final_test_rows_used"], 0)

    def test_unseen_validation_code_is_reported_and_handled(self):
        training, validation, features = coded_frames()
        training = training[training.y != 1]
        table, evidence = encoding.compare(training, validation, features)
        self.assertEqual(evidence["validation_codes_unseen_in_training"], {"y": [1]})
        self.assertEqual(len(table), 3)

    def test_minus_one_count_counts_codes_per_record(self):
        counts = encoding.minus_one_count(pd.DataFrame({"x": [-1, 1], "y": [-1, 0]}))
        self.assertEqual(counts.minus_one_count.tolist(), [2, 0])

    @unittest.skipUnless(os.environ.get("ML_AI_REAL_DATA") == "1", "Real-source integration runs in core CI.")
    def test_real_phishing_representations(self):
        training, validation, features = encoding.load()
        table, evidence = encoding.compare(training, validation, features)
        self.assertEqual(len(features), 30)
        self.assertEqual(table.representation.tolist(), ["codes_as_numbers", "one_hot", "one_hot_plus_count"])
        self.assertGreater(table.balanced_accuracy.min(), .5)


if __name__ == "__main__":
    unittest.main()
