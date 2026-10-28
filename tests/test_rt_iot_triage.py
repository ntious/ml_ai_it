"""RT-IoT transfer: validation compares the model with constant review policies.

With most flows labelled as attacks, reviewing everything can cost less than a
model's misses. Selection must show that comparison and use validation only.
"""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rt_iot_run", ROOT / "projects/rt-iot-triage/scripts/run.py")
rt_iot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rt_iot)


def synthetic_flows(seed=7, rows=3000, attack_rate=.9, informative=True):
    """Authored flow-like records; not RT-IoT data."""
    rng = np.random.default_rng(seed)
    attack = rng.random(rows) < attack_rate
    signal = attack if informative else rng.random(rows) < attack_rate
    return pd.DataFrame({"proto": rng.choice(["tcp", "udp"], rows), "service": rng.choice(["-", "http", "mqtt"], rows),
                         "flow_duration": rng.exponential(1, rows) + 2 * signal, "fwd_pkts_tot": rng.integers(1, 50, rows),
                         "bwd_pkts_tot": rng.integers(0, 50, rows),
                         "Attack_type": np.where(attack, "DOS_SYN_Hping", "MQTT_Publish")})


class RtIotSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame = synthetic_flows()
        cls.result = rt_iot.study(cls.frame)

    def test_validation_compares_full_grid_and_both_constant_policies(self):
        validation = self.result["validation"]
        self.assertEqual(validation.loc[validation.policy == "logistic", "threshold"].tolist(), rt_iot.THRESHOLDS)
        self.assertEqual(sorted(validation.policy.unique()), ["always_review", "logistic", "never_review"])
        self.assertTrue((validation.assumed_cost == 5 * validation.fn + validation.fp).all())

    def test_recommended_policy_has_minimum_validation_cost(self):
        validation, summary = self.result["validation"], self.result["summary"]
        selected = self.result["evaluation"].query("validation_selected")
        self.assertEqual(selected.policy.tolist(), [summary["validation_selected_policy"]])
        logistic = validation[validation.policy == "logistic"]
        self.assertEqual(logistic.loc[logistic.threshold == summary["threshold"], "assumed_cost"].min(), logistic.assumed_cost.min())
        chosen = validation[(validation.policy == summary["validation_selected_policy"])
                            & ((validation.threshold == summary["threshold"]) | validation.threshold.isna())]
        self.assertEqual(chosen.assumed_cost.min(), validation.assumed_cost.min())

    def test_final_labels_cannot_change_any_choice(self):
        test_rows = self.result["predictions"].source_row.to_numpy()
        flipped = self.frame.copy()
        attack = ~flipped.Attack_type.isin(rt_iot.NORMAL)
        flipped.loc[flipped.index[test_rows], "Attack_type"] = np.where(attack.iloc[test_rows], "MQTT_Publish", "DOS_SYN_Hping")
        changed = rt_iot.study(flipped)
        pd.testing.assert_frame_equal(changed["validation"], self.result["validation"])
        for key in ["threshold", "validation_selected_policy"]:
            self.assertEqual(changed["summary"][key], self.result["summary"][key])
        self.assertFalse(changed["evaluation"].equals(self.result["evaluation"]))

    def test_cheaper_constant_policy_wins_and_ties_prefer_less_workload(self):
        actual = np.array([1] * 9 + [0])
        model = rt_iot.score(actual, np.array([1] * 6 + [0] * 4, dtype=bool), "logistic", .5)  # 3 misses: cost 15
        review_all = rt_iot.score(actual, rt_iot.constant_decisions("always_review", 10), "always_review")  # cost 1
        self.assertEqual(rt_iot.choose([model, review_all])["policy"], "always_review")
        same_cost = rt_iot.score(actual, np.array([1] * 10, dtype=bool), "logistic", .05)
        fewer_alerts = dict(same_cost, alerts_per_1000=same_cost["alerts_per_1000"] - 1)
        self.assertIs(rt_iot.choose([same_cost, fewer_alerts]), fewer_alerts)

    def test_model_is_still_evaluated_when_inputs_carry_no_signal(self):
        result = rt_iot.study(synthetic_flows(informative=False))
        # The model keeps its own validation threshold, whichever policy validation recommends.
        self.assertEqual(result["evaluation"].policy.tolist(), ["logistic", "always_review", "never_review"])
        self.assertEqual(result["evaluation"].validation_selected.sum(), 1)
        prevalence = result["summary"]["attack_prevalence"]
        self.assertTrue(all(.8 < value < 1 for value in prevalence.values()))


@unittest.skipUnless(os.environ.get("ML_AI_REAL_DATA") == "1", "Real-source integration runs in core CI.")
class RtIotRealSourceTests(unittest.TestCase):
    def test_pinned_archive_study_reports_adverse_comparison_inputs(self):
        cache = Path(os.environ.get("ML_AI_RUNS_DIR", ROOT / "runs")) / "datasets/rt-iot2022/original.zip"
        with tempfile.TemporaryDirectory() as folder:
            rt_iot.run(Path(folder) / "study", cache)
            summary = json.loads((Path(folder) / "study/summary.json").read_text(encoding="utf-8"))
            evaluation = pd.read_csv(Path(folder) / "study/evaluation.csv")
        self.assertEqual((summary["rows"], summary["sha256"]), (123117, rt_iot.DIGEST))
        self.assertEqual(summary["train"] + summary["validation"] + summary["test"], 123117)
        self.assertIn(summary["threshold"], rt_iot.THRESHOLDS)
        self.assertGreater(summary["attack_prevalence"]["test"], .5)
        self.assertEqual(evaluation.validation_selected.sum(), 1)
        self.assertTrue(((evaluation[["tp", "fp", "fn", "tn"]].sum(axis=1)) == summary["test"]).all())
        self.assertEqual(set(summary["test_assumed_cost_per_1000"]), {"logistic", "always_review", "never_review"})


if __name__ == "__main__":
    unittest.main()
