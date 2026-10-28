"""Behavioral checks for uncertainty, calibration and authentic IT boundaries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from practical_ml_ai.learning import wilson_interval, calibration_table


class StatisticalTeachingTests(unittest.TestCase):
    def test_interval_known_counts_and_sample_size(self):
        low,high=wilson_interval(15,20)
        self.assertAlmostEqual(low,.531299,places=5)
        self.assertAlmostEqual(high,.888138,places=5)
        small=wilson_interval(3,4)
        self.assertGreater(small[1]-small[0],high-low)
        self.assertAlmostEqual(wilson_interval(0,20)[0],0.)
        self.assertAlmostEqual(wilson_interval(20,20)[1],1.)

    def test_invalid_counts_are_not_invented_rates(self):
        for args in [(0,0),(5,4),(-1,4),(True,4),(1.5,4),(1,4,1)]:
            with self.subTest(args=args),self.assertRaises(ValueError):wilson_interval(*args)

    def test_calibration_includes_endpoints_and_preserves_denominators(self):
        table=calibration_table([0,0,1,1],[0.,.1,.9,1.],bins=5)
        self.assertEqual(table.n.sum(),4)
        self.assertEqual(table.bin.tolist(),[0,4])
        self.assertEqual(table.observed_rate.tolist(),[0.,1.])
        self.assertAlmostEqual(float(table.iloc[-1].mean_probability),.95)

    def test_bad_calibration_inputs_fail(self):
        for y,p in [([],[]),([0],[float("nan")]),([2],[.5]),([0,1],[.5]),([0],[1.1])]:
            with self.subTest(y=y,p=p),self.assertRaises(ValueError):calibration_table(y,p)

    def test_content_boundary_matches_masked_truncation(self):
        from practical_ml_ai.language import sms_content
        content=sms_content("Contact test@example.com " + "word "*100)
        self.assertNotIn("test@example.com",content)
        self.assertEqual(len(content),240)
        self.assertIn("[EMAIL]",content)

    def test_core_preflight_runs_outside_project(self):
        with tempfile.TemporaryDirectory() as folder:
            result=subprocess.run([sys.executable,str(ROOT/"scripts/preflight.py"),"--profile","core"],cwd=folder,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(result.stdout)
        self.assertEqual(report["missing"],[])
        self.assertEqual(Path(report["project_root"]),ROOT)


@unittest.skipUnless(os.environ.get("ML_AI_REAL_DATA")=="1","Real-source integration runs in core CI.")
class PhishingBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from practical_ml_ai.phishing import prepare,train
        cls.temporary=tempfile.TemporaryDirectory();cls.directory=Path(cls.temporary.name)/"study"
        prepare(cls.directory);train(cls.directory)

    @classmethod
    def tearDownClass(cls):cls.temporary.cleanup()

    def test_profile_groups_cannot_cross_splits(self):
        parts={name:pd.read_csv(self.directory/(name+".csv"),dtype={"profile_id":str}) for name in ["train","validation","test"]}
        for a,b in [("train","validation"),("train","test"),("validation","test")]:
            self.assertFalse(set(parts[a].profile_id)&set(parts[b].profile_id))
        self.assertEqual(sum(map(len,parts.values())),10698)
        self.assertEqual(set(parts["test"].label),{0,1})

    def test_validation_selection_ignores_test_labels_and_guards_repetition(self):
        from practical_ml_ai.phishing import validate,evaluate,report,train
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/"study";shutil.copytree(self.directory,target)
            validate(target);original=json.loads((target/"selection.json").read_text(encoding="utf-8"))
            (target/"selection.json").unlink()
            test=pd.read_csv(target/"test.csv");test["label"]=1-test.label;test.to_csv(target/"test.csv",index=False)
            validate(target)
            self.assertEqual(json.loads((target/"selection.json").read_text(encoding="utf-8")),original)
            with self.assertRaises(ValueError):validate(target)
            with self.assertRaises(ValueError):train(target)
            evaluate(target);result=report(target)
            self.assertIn(result["chosen"],["dummy","forest","logistic","tree"])
            self.assertEqual(len(result["test_scores"]),len({result["chosen"],"dummy"}))
            self.assertTrue((target/"index.html").is_file())
            with self.assertRaises(ValueError):evaluate(target)

    def test_training_predictions_have_no_target_column(self):
        for name in ["dummy","forest","logistic","tree"]:
            prediction=pd.read_csv(self.directory/("test_"+name+".csv"))
            self.assertEqual(set(prediction),{"record_id","model","probability","predicted"})
            self.assertTrue(prediction.probability.between(0,1).all())
