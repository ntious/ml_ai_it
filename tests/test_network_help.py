"""Download-failure hints and retrying a run after a failed download."""
from pathlib import Path
import tempfile
import unittest
from urllib.error import URLError

from practical_ml_ai.continuation_data import new_run
from practical_ml_ai.network_help import describe, is_network_error


class NetworkHelpTests(unittest.TestCase):
    def test_download_errors_get_a_retry_hint_and_local_errors_do_not(self):
        hint = describe(URLError("Tunnel connection failed: 403 Forbidden"))
        self.assertIn("run the same command again", hint)
        self.assertIn("new folder name", hint)
        self.assertTrue(is_network_error(OSError("Max retries exceeded with url: huggingface.co")))
        missing = FileNotFoundError(2, "No such file or directory", "nope.csv")
        self.assertFalse(is_network_error(missing))
        self.assertEqual(describe(missing), str(missing))

    def test_retry_reuses_an_empty_run_directory_but_never_one_with_results(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "module06"
            self.assertEqual(new_run(run), run)  # first attempt creates the folder
            self.assertEqual(new_run(run), run)  # failed download left it empty: retry works
            (run / "summary.txt").write_text("result", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "fresh output directory"):
                new_run(run)
            file_path = Path(temporary) / "a-file"
            file_path.write_text("x", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "fresh output directory"):
                new_run(file_path)


if __name__ == "__main__":
    unittest.main()
