"""Real-data behavior checks. Invalid control inputs are mutations of real rows."""
import json
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
from practical_ml_ai.continuation_data import binary_metrics, fetch_source, sms_splits, wine_splits
from practical_ml_ai.classical import classification_bundle, run_classification, run_clustering, run_fairness


class ContinuationCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.base = Path(cls.temporary.name)
        cls.results = {
            6: run_classification(cls.base / "m6"),
            7: run_clustering(cls.base / "m7"),
            13: run_fairness(cls.base / "m13"),
        }

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_real_sources_and_retained_provenance(self):
        for name in ["wine", "sms", "adult"]:
            folder = fetch_source(name)
            meta = json.loads((folder / "provenance.json").read_text())
            self.assertEqual(meta["license"], "CC-BY-4.0")
            self.assertEqual(len(meta["archive_sha256"]), 64)
            self.assertTrue((folder / "original.zip").is_file())

    def test_wine_chemistry_groups_and_record_ids_do_not_cross_splits(self):
        split, features, manifest = wine_splits()
        self.assertEqual(manifest["raw_rows"], 1599)
        self.assertEqual(len(features), 11)
        for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]:
            self.assertFalse(set(split[a].record_id) & set(split[b].record_id))
            left = set(pd.util.hash_pandas_object(split[a][features], index=False))
            right = set(pd.util.hash_pandas_object(split[b][features], index=False))
            self.assertFalse(left & right)

    def test_test_labels_do_not_select_classifier(self):
        original = wine_splits()
        first = classification_bundle()["selection"]
        split, features, manifest = original
        changed = {key: value.copy() for key, value in split.items()}
        changed["test"]["label"] = 1 - changed["test"]["label"]
        with patch("practical_ml_ai.classical.wine_splits", return_value=(changed, features, manifest)):
            second = classification_bundle()["selection"]
        self.assertEqual((first["model"], first["threshold"]), (second["model"], second["threshold"]))

    def test_classification_confusion_counts_reconcile(self):
        result = self.results[6]["test"]
        self.assertEqual(result["n"], result["tp"] + result["tn"] + result["fp"] + result["fn"])
        self.assertTrue(0 <= result["balanced_accuracy"] <= 1)
        self.assertTrue((self.base / "m6/tree_rules.txt").read_text().strip())
        predictions = pd.read_csv(self.base / "m6/test_predictions.csv")
        self.assertTrue(predictions.probability.between(0, 1).all())

    def test_clustering_does_not_use_quality_and_profiles_are_complete(self):
        result = self.results[7]
        self.assertFalse(result["quality_used_for_fit_or_selection"])
        counts = pd.read_csv(self.base / "m7/cluster_counts.csv")
        self.assertEqual(counts.observations.sum(), result["test_observations"])
        self.assertGreater(len(counts), 1)
        profiles = pd.read_csv(self.base / "m7/cluster_profiles.csv")
        self.assertNotIn("quality", profiles)
        self.assertTrue(np.isfinite(profiles.to_numpy()).all())

    def test_sms_text_deduplication_and_real_subset(self):
        split, manifest = sms_splits()
        self.assertEqual(manifest["sample_rows"], 1200)
        self.assertTrue(all(part.label.nunique() == 2 for part in split.values()))
        for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]:
            self.assertFalse(set(split[a].text_id) & set(split[b].text_id))

    def test_fairness_group_denominators_and_scope(self):
        result = self.results[13]
        self.assertFalse(result["protected_attributes_used_for_fitting"])
        audit = pd.read_csv(self.base / "m13/group_audit.csv")
        for attribute in ["sex", "race"]:
            rows = audit.loc[audit.attribute == attribute]
            self.assertEqual(rows.n.sum(), result["test_rows"])
            self.assertTrue((rows.n == rows.tp + rows.tn + rows.fp + rows.fn).all())
        # Undefined rates are unavailable, never fabricated.
        self.assertIsNone(binary_metrics([], [])["recall"])

    def test_reports_have_named_values_and_scoped_tables(self):
        for number in [6, 7, 13]:
            html = (self.base / f"m{number}/index.html").read_text()
            self.assertIn('scope="col"', html)
            self.assertIn('href="#main"', html)
            self.assertIn('tabindex="0"', html)
            self.assertTrue((self.base / f"m{number}/summary.txt").is_file())

    def test_all_three_documented_classical_scripts(self):
        for number, path in [(6, "wine-classification"), (7, "wine-clustering"), (13, "income-fairness")]:
            output = self.base / f"cli{number}"
            process = subprocess.run([sys.executable, str(ROOT / "examples" / path / "scripts/run.py"), "--output", str(output)], cwd=self.base, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads((output / "summary.json").read_text())["module"], number)


if __name__ == "__main__":
    unittest.main()
