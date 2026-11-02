"""Offline checks for the provider-neutral client and the monitoring decision-record draft."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.llm_client import OutputContractError, check_output, classify

from practical_ml_ai import monitoring_record as decision_record

LABELS = {"spam", "ham"}
GOOD = '{"label": "spam", "reason": "asks for a code"}'


def sequence(*responses):
    calls = []
    items = iter(responses)

    def send(prompt):
        calls.append(prompt)
        item = next(items)
        if isinstance(item, Exception):
            raise item
        return item
    send.calls = calls
    return send


class ClientTests(unittest.TestCase):
    def test_accepts_the_declared_shape(self):
        self.assertEqual(check_output(GOOD, LABELS)["label"], "spam")

    def test_rejects_each_contract_violation(self):
        for bad in ["not json", "[]", '{"label": "spam"}', '{"label": "spam", "reason": "x", "extra": 1}',
                    '{"label": "phish", "reason": "x"}', None, "null", "42", '["label", "reason"]',
                    '{"label": [], "reason": "x"}', '{"label": "spam", "reason": 42}',
                    '{"label": "spam", "reason": " "}']:
            with self.subTest(bad=bad), self.assertRaises(OutputContractError):
                check_output(bad, LABELS)

    def test_retries_transient_failure_then_succeeds(self):
        send = sequence(TimeoutError(), ConnectionError(), GOOD)
        result, calls = classify(send, "p", LABELS)
        self.assertEqual((result["label"], calls, len(send.calls)), ("spam", 3, 3))

    def test_gives_up_after_the_attempt_limit_without_accepting_bad_output(self):
        send = sequence(TimeoutError(), ConnectionError())
        with self.assertRaisesRegex(RuntimeError, "gave up after 2 attempts"):
            classify(send, "p", LABELS, attempts=2)
        self.assertEqual(len(send.calls), 2)

    def test_bad_output_is_not_retried_as_transport_failure(self):
        send = sequence("nope", GOOD)
        with self.assertRaises(OutputContractError):
            classify(send, "p", LABELS)
        self.assertEqual(len(send.calls), 1)

    def test_retry_waits_stop_at_the_last_call(self):
        with patch("practical_ml_ai.llm_client.time.sleep") as sleep:
            with self.assertRaises(RuntimeError):
                classify(sequence(TimeoutError(), TimeoutError(), TimeoutError()), "p", LABELS, wait=0.25)
            self.assertEqual([c.args[0] for c in sleep.call_args_list], [0.25, 0.5])

    def test_invalid_retry_settings_fail_before_a_call(self):
        for kwargs in [{"attempts": True}, {"attempts": 1.5}, {"wait": -1}, {"wait": float("nan")}, {"wait": float("inf")}]:
            send = sequence(GOOD)
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                classify(send, "p", LABELS, **kwargs)
            self.assertEqual(len(send.calls), 0)

    def test_unexpected_exception_is_not_swallowed(self):
        with self.assertRaises(KeyError):
            classify(sequence(KeyError("boom")), "p", LABELS)

    def test_attempts_must_be_positive(self):
        with self.assertRaises(ValueError):
            classify(sequence(GOOD), "p", LABELS, attempts=0)


class DecisionRecordTests(unittest.TestCase):
    HEADER = "batch,rows,mean_prediction_seconds,largest_standardized_mean_shift,fp,fn,recall,precision,selection_rate\n"

    def write(self, body):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "batch_monitoring.csv"
        path.write_text(self.HEADER + body, encoding="utf-8")
        return path

    def test_flags_use_only_declared_thresholds(self):
        rows = decision_record.read_batches(self.write("1,61,0.0005,0.39,6,3,0.4,0.25,0.13\n2,61,0.0006,0.60,6,2,0.67,0.4,0.16\n"))
        none = decision_record.draft_record(rows)
        self.assertEqual(none.count("no threshold declared"), 4)
        flagged = decision_record.draft_record(rows, latency_limit=0.001, shift_limit=0.5)
        self.assertIn("| 0.600 | ABOVE |", flagged)
        self.assertIn("| 0.390 | within |", flagged)

    def test_missing_shift_is_reported_as_unavailable(self):
        rows = decision_record.read_batches(self.write("1,10,0.0005,,1,1,0.5,0.5,0.2\n"))
        self.assertIn("unavailable", decision_record.draft_record(rows, shift_limit=0.5))

    def test_workload_and_partial_shift_gaps_are_retained(self):
        rows = decision_record.read_batches(self.write("1,10,0.0005,0.2,1,1,0.5,0.5,0.8\n"))
        rows[0]["standardized_shift_unavailable"] = "constant_feature: zero training variance"
        report = decision_record.draft_record(rows, shift_limit=0.5)
        self.assertIn("| 0.800 | constant_feature: zero training variance |", report)
        self.assertIn("within", report)

    def test_nonfinite_measurements_are_unavailable_and_invalid_thresholds_rejected(self):
        rows = decision_record.read_batches(self.write("1,10,inf,nan,1,1,0.5,0.5,0.2\n"))
        self.assertIn("unavailable", decision_record.draft_record(rows, latency_limit=0.5))
        for limit in [-1, float("nan"), float("inf")]:
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                decision_record.draft_record(rows, shift_limit=limit)

    def test_rejects_a_file_without_the_expected_columns(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "x.csv"
        path.write_text("a,b\n1,2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            decision_record.read_batches(path)


if __name__ == "__main__":
    unittest.main()
