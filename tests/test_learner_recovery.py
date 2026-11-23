"""Exercise failure paths without downloading data or installing frameworks."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError
import pandas as pd
from practical_ml_ai.network_help import DownloadError, describe, with_download_help
from practical_ml_ai.report_terms import explain_terms
from practical_ml_ai.continuation_data import fetch_source, publish_report

spec = importlib.util.spec_from_file_location('course_bootstrap', Path(__file__).resolve().parents[1] / 'scripts/bootstrap.py')
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)

class LearnerRecoveryTests(unittest.TestCase):
    def test_framework_version_rejected_before_environment_creation(self):
        with patch.object(sys, 'argv', ['bootstrap', '--profile', 'frameworks']), patch.object(sys, 'version_info', (3,13)), patch.object(bootstrap.platform, 'system', return_value='Linux'), patch.object(bootstrap.venv.EnvBuilder, 'create') as create:
            with self.assertRaisesRegex(SystemExit, 'verified course framework'):
                bootstrap.main()
            create.assert_not_called()

    def test_environment_creation_failure_has_guidance(self):
        for error in (PermissionError('denied'), subprocess.CalledProcessError(1, ['ensurepip'])):
            with self.subTest(error=type(error).__name__), patch.object(sys, 'argv', ['bootstrap']), patch.object(bootstrap.venv.EnvBuilder, 'create', side_effect=error):
                with self.assertRaisesRegex(SystemExit, 'python3.12-venv'):
                    bootstrap.main()

    def test_direct_data_call_used_by_notebooks_explains_download_failure(self):
        original = URLError('offline')
        with tempfile.TemporaryDirectory() as d, patch('practical_ml_ai.continuation_data.RUNS_ROOT', Path(d)), patch('urllib.request.urlopen', side_effect=original):
            from practical_ml_ai.continuation_data import SOURCES
            with self.assertRaises(DownloadError) as caught:
                fetch_source(next(iter(SOURCES)))
            self.assertIs(caught.exception.__cause__, original)
            self.assertIn('worked reports', str(caught.exception))
            self.assertEqual(describe(caught.exception), str(caught.exception))

    def test_local_failure_keeps_original_exception(self):
        original = FileNotFoundError('missing local.csv')
        @with_download_help
        def read():
            raise original
        with self.assertRaises(FileNotFoundError) as caught:
            read()
        self.assertIs(caught.exception, original)

    def test_definitions_reach_saved_reports_without_changing_metrics(self):
        summary = {'split_group_overlap': False}
        tables = {'test_scores': pd.DataFrame([{'precision': .75, 'recall': .5, 'f1': .6}])}
        with tempfile.TemporaryDirectory() as d:
            publish_report(d, 'Example', summary, tables, [])
            html = (Path(d)/'index.html').read_text(encoding='utf-8')
            text = (Path(d)/'summary.txt').read_text(encoding='utf-8')
            self.assertIn('TP / (TP + FP)', html)
            self.assertIn('does not prove all leakage', text)
            self.assertNotIn('<code>specificity</code>', html)
            self.assertEqual(pd.read_csv(Path(d)/'test_scores.csv').precision.iloc[0], .75)
