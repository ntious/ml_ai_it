"""Selection-boundary and statistical contracts that need no heavy model."""
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from practical_ml_ai.agent_study import bounded_agent, requests_frame, router_configuration
from practical_ml_ai.continuation_data import sms_splits
from practical_ml_ai.language_studies import evaluation_subset, rate_record
from practical_ml_ai.neural import select_threshold


class PhaseBContracts(unittest.TestCase):
    def test_full_sms_corpus_keeps_deduplication_boundary(self):
        split, manifest = sms_splits(limit=None)
        self.assertEqual(manifest["sample_rows"], 5159)
        for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]:
            self.assertFalse(set(split[a].text_id) & set(split[b].text_id))
        self.assertEqual(sum(map(len, split.values())), manifest["sample_rows"])
        with self.assertRaises(ValueError):
            sms_splits(limit=True)
        for invalid in [20, 39]:
            with self.assertRaisesRegex(ValueError, "at least 40"):
                sms_splits(limit=invalid)
        smallest, _ = sms_splits(limit=40)
        self.assertTrue(all(part.label.nunique() == 2 for part in smallest.values()))

    def test_subset_does_not_invent_rows_or_change_labels(self):
        split, _ = sms_splits(limit=None)
        chosen = evaluation_subset(split["test"], 100)
        lookup = split["test"].set_index("text_id").label
        self.assertEqual(len(chosen), 100)
        self.assertEqual(chosen.label.tolist(), lookup.loc[chosen.text_id].tolist())
        self.assertEqual(chosen.text_id.tolist(), evaluation_subset(split["test"], 100).text_id.tolist())
        nearly_all = evaluation_subset(split["test"], len(split["test"]) - 1)
        self.assertEqual(len(nearly_all), len(split["test"]) - 1)
        self.assertEqual(nearly_all.label.nunique(), 2)
        for invalid in [True, 0, 8, 100000]:
            with self.assertRaises(ValueError):
                evaluation_subset(split["test"], invalid)

    def test_zero_and_perfect_rates_still_have_uncertainty(self):
        zero = rate_record("base", "schema", 0, 100)
        perfect = rate_record("adapted", "schema", 100, 100)
        self.assertGreater(zero["ci_high"], 0)
        self.assertLess(perfect["ci_low"], 1)
        self.assertEqual(perfect["successes"], perfect["observations"])

    def test_threshold_uses_balanced_accuracy_and_stable_ties(self):
        threshold, table = select_threshold(np.array([0, 0, 1, 1]), np.array([.1, .2, .3, .4]))
        self.assertAlmostEqual(threshold, .25)
        self.assertEqual(table.iloc[0].balanced_accuracy, 1)

    def test_final_request_labels_cannot_select_router_offsets(self):
        frame = requests_frame()
        changed = frame.copy()
        changed.loc[changed.split == "test", "expected_tool"] = "refuse"

        class Tokenizer:
            def apply_chat_template(self, messages, **kwargs):
                return messages[-1]["content"]

        # Fixed validation likelihoods; no real-model behavior is claimed here.
        observed = {row.request: index // 2 for index, row in enumerate(frame.loc[frame.split == "validation"].itertuples())}

        def likelihoods(model, tokenizer, prompt, candidates):
            scores = np.array([-2., -1., -3.])
            if prompt in observed:
                scores[observed[prompt]] += 2
            return scores.tolist()

        with patch("practical_ml_ai.agent_study.local_model", return_value=(None, Tokenizer(), "test-revision")), patch("practical_ml_ai.agent_study.completion_scores", side_effect=likelihoods):
            with patch("practical_ml_ai.agent_study.requests_frame", return_value=frame):
                before = router_configuration.__wrapped__()
            with patch("practical_ml_ai.agent_study.requests_frame", return_value=changed):
                after = router_configuration.__wrapped__()
        np.testing.assert_array_equal(before[4], after[4])
        self.assertEqual(before[5], after[5])

    def test_invalid_budgets_fail_before_model_loading(self):
        with patch("practical_ml_ai.agent_study.router_configuration") as model:
            for kwargs in [{"max_steps": 0}, {"max_steps": 4}, {"max_steps": True}, {"max_calls": 2}, {"max_calls": True}]:
                with self.assertRaises(ValueError):
                    bounded_agent("Count rows.", **kwargs)
            with self.assertRaises(ValueError):
                bounded_agent("")
            model.assert_not_called()

    def test_user_install_data_prefix_is_searched(self):
        import practical_ml_ai.agent_study as agent
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "user/share/ml_ai_it/agent-requests.csv"
            destination.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "data/samples/agent-requests.csv", destination)
            with patch.object(agent, "ROOT", root / "absent"), patch.object(agent.sys, "prefix", str(root / "venv")), patch.object(agent.sysconfig, "get_path", return_value=str(root / "user")):
                self.assertIn(destination, agent.request_paths())
                self.assertEqual(int((agent.requests_frame().split == "test").sum()), 26)

    def test_long_prompt_preserves_assistant_boundary_and_loss_mask(self):
        from practical_ml_ai.language import packed_example
        tokenizer = SimpleNamespace(encode=lambda text, **kwargs: list(range(300)) if text == "complete chat prompt" else [7, 8], eos_token_id=9)
        # Exercise packing without making torch a core-profile dependency.
        tensor_api = SimpleNamespace(tensor=lambda value, **kwargs: value, long="long")
        with patch.dict(sys.modules, {"torch": tensor_api}), patch("practical_ml_ai.language.sms_prompt", return_value="complete chat prompt"):
            inputs, labels = packed_example(tokenizer, SimpleNamespace(text="long SMS", label=1))
        self.assertEqual(inputs[0][:300], list(range(300)))
        self.assertEqual(labels[0][:300], [-100] * 300)
        self.assertEqual(inputs[0][300:], [7, 8, 9])
        self.assertEqual(labels[0][300:], [7, 8, 9])


if __name__ == "__main__":
    unittest.main()
