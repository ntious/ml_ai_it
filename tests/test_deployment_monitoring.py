"""Batch input-shift monitoring must not report an undefined shift as no change."""
from pathlib import Path
import sys
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.deployment import mean_shift


class MeanShiftTests(unittest.TestCase):
    def test_zero_training_variance_is_unavailable_with_raw_difference(self):
        training = pd.DataFrame({"constant": [5.0, 5.0, 5.0], "varied": [1.0, 2.0, 3.0]})
        current = pd.DataFrame({"constant": [7.5, 7.5], "varied": [2.0, 4.0]})
        shift = mean_shift(training, current)
        self.assertAlmostEqual(shift["largest_standardized"], 1 / training.varied.std(ddof=0))
        self.assertEqual(shift["unavailable"], "constant: zero training variance, raw mean difference 2.5")

    def test_no_defined_scale_gives_no_standardized_shift(self):
        training = pd.DataFrame({"constant": [5.0, 5.0]})
        shift = mean_shift(training, pd.DataFrame({"constant": [5.0]}))
        self.assertIsNone(shift["largest_standardized"])
        self.assertIn("raw mean difference 0", shift["unavailable"])

    def test_defined_scales_match_the_standardized_mean_difference(self):
        training = pd.DataFrame({"a": [0.0, 2.0], "b": [10.0, 30.0]})
        current = pd.DataFrame({"a": [3.0], "b": [20.0]})
        shift = mean_shift(training, current)
        self.assertAlmostEqual(shift["largest_standardized"], 2.0)
        self.assertEqual(shift["unavailable"], "")


if __name__ == "__main__":
    unittest.main()
