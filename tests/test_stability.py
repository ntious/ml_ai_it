"""The core stability exercise separates seed variation from split variation."""
import os
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.stability import FIXED_MODEL_SEED, SPLIT_SEEDS, TRAINING_SEEDS, compare_variation


def synthetic_split(seed=3, rows=600):
    """Authored records with a learnable label; not the wine data."""
    rng = np.random.default_rng(seed)
    frame = pd.DataFrame({"a": rng.normal(size=rows), "b": rng.normal(size=rows)})
    frame["record_id"] = np.arange(rows)
    frame["label"] = (frame.a + rng.normal(scale=.8, size=rows) > .8).astype(int)
    parts = np.split(frame.sample(frac=1, random_state=seed), [420, 510])
    return dict(zip(["train", "validation", "test"], parts)), ["a", "b"]


class StabilityExerciseTests(unittest.TestCase):
    def test_experiments_vary_one_factor_each_and_never_use_the_final_test(self):
        split, features = synthetic_split()
        table, spreads, boundary = compare_variation(split, features)
        seed_runs, split_runs = table[table.experiment.str.startswith("A")], table[table.experiment.str.startswith("B")]
        self.assertEqual(seed_runs.seed.tolist(), list(TRAINING_SEEDS))
        self.assertEqual(split_runs.seed.tolist(), list(SPLIT_SEEDS))
        self.assertEqual(set(seed_runs.training_rows), {420})
        self.assertEqual(set(seed_runs.validation_rows), {90})
        self.assertTrue((split_runs.training_rows + split_runs.validation_rows == 510).all())
        self.assertEqual(boundary, {"final_test_rows_used": 0, "development_rows": 510, "excluded_final_test_rows": 90})
        self.assertEqual(spreads["A: training seed"]["balanced_accuracy"]["runs"], 5)
        self.assertIsInstance(FIXED_MODEL_SEED, int)

    def test_final_test_labels_cannot_change_any_result(self):
        split, features = synthetic_split()
        flipped = {**split, "test": split["test"].assign(label=1 - split["test"].label)}
        pd.testing.assert_frame_equal(compare_variation(split, features)[0], compare_variation(flipped, features)[0])

    @unittest.skipUnless(os.environ.get("ML_AI_REAL_DATA") == "1", "Real-source integration runs in core CI.")
    def test_real_wine_exercise_reports_both_spreads(self):
        table, spreads, boundary = compare_variation()
        self.assertEqual(len(table), 10)
        self.assertEqual(boundary["final_test_rows_used"], 0)
        for name in ["A: training seed", "B: data split"]:
            self.assertGreater(spreads[name]["balanced_accuracy"]["sd"], 0)


if __name__ == "__main__":
    unittest.main()
