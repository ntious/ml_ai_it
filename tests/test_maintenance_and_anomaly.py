import hashlib
import importlib.util
import io
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from practical_ml_ai.anomaly import study

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("health", ROOT / "scripts/check_external_health.py")
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class MaintenanceTests(unittest.TestCase):
    def test_local_addresses_and_documented_placeholders_are_not_public_checks(self):
        self.assertIsNotNone(health.exclusion("http://localhost:8888/"))
        self.assertIsNotNone(health.exclusion("https://github.com/ntious/ml_ai_it/blob/TESTED_COMMIT/a.md"))
        self.assertIsNone(health.exclusion("https://ntious.github.io/ml_ai_it/"))

    def test_sources_cover_all_six_pinned_archives(self):
        entries = health.sources()
        self.assertEqual({s["name"] for s in entries}, {"bike", "rt-iot", "wine", "sms", "adult", "phishing"})
        self.assertTrue(all(len(s["sha256"]) == 64 for s in entries))

    def test_changed_bytes_fail_without_replacing_pin(self):
        pin = hashlib.sha256(b"approved").hexdigest()
        opener = lambda *a, **k: io.BytesIO(b"changed")
        result = health.probe("https://example.org/archive.zip", pin, opener=opener)
        self.assertFalse(result["ok"])
        self.assertEqual(pin, hashlib.sha256(b"approved").hexdigest())

    def test_transient_failure_is_retried(self):
        calls = []
        def opener(*a, **k):
            calls.append(1)
            if len(calls) < 3:
                raise TimeoutError("temporary")
            return io.BytesIO(b"data")
        result = health.probe("https://example.org/a", hashlib.sha256(b"data").hexdigest(), opener=opener, sleep=lambda _: None)
        self.assertTrue(result["ok"])
        self.assertEqual(len(calls), 3)


class AnomalyTests(unittest.TestCase):
    def fixture(self):
        rng = np.random.default_rng(5)
        dates = pd.date_range("2011-01-01", "2012-12-31")
        return pd.DataFrame({"dteday": dates, "cnt": rng.integers(500, 3000, len(dates)), "temp": rng.random(len(dates))})

    def test_future_values_cannot_change_fit_or_thresholds(self):
        raw = self.fixture()
        a, _, _, protocol = study(raw)
        raw.loc[raw.dteday >= "2012-07-01", "cnt"] *= 10
        b, _, _, changed = study(raw)
        self.assertEqual(protocol, changed)
        pd.testing.assert_frame_equal(a[a.partition != "test"], b[b.partition != "test"])
        self.assertFalse(a[a.partition == "test"].equals(b[b.partition == "test"]))

    def test_workload_reconciles_and_replay_is_deterministic(self):
        a, workload, _, _ = study(self.fixture())
        pd.testing.assert_frame_equal(a, study(self.fixture())[0])
        for row in workload.itertuples():
            selected = a[(a.partition == row.partition) & (a.method == row.method)]
            self.assertEqual(row.flagged_days, int(selected.flagged.sum()))
            self.assertEqual(row.days, len(selected))

    def test_missing_day_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "consecutive"):
            study(self.fixture().drop(index=50))


if __name__ == "__main__":
    unittest.main()
