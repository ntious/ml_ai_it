"""Learners can study without the reading site or repository access.

Site downloads return 404 until publication, and the repository may be
private, so an instructor-built source archive and in-source paths must work.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class OfflineAccessTests(unittest.TestCase):
    def test_source_only_archive_is_complete_reproducible_and_excludes_runtime_files(self):
        from build_downloads import build_source_archive
        modules = json.loads((ROOT / "curriculum/modules.json").read_text(encoding="utf-8"))["modules"]
        practice = json.loads((ROOT / "curriculum/practice.json").read_text(encoding="utf-8"))["modules"]
        with tempfile.TemporaryDirectory() as folder:
            first = build_source_archive(Path(folder) / "a/ml_ai_it-source.zip")
            second = build_source_archive(Path(folder) / "b/ml_ai_it-source.zip")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            names = set(zipfile.ZipFile(first).namelist())
        required = ["README.md", "QUICKSTART.md", "pyproject.toml", "docs/setup/student-workspace.md",
                    *[module["notebook"] for module in modules], *[module["script"] for module in modules],
                    *[entry[kind] for entry in practice for kind in ["practice", "solutions"]]]
        self.assertEqual([name for name in required if "ml_ai_it/" + name not in names], [])
        self.assertTrue(all(name.startswith("ml_ai_it/") for name in names))
        top_level = tuple("ml_ai_it/" + folder for folder in ["runs/", "site/", ".venv", "node_modules/", "documentations/", "dist/", "build/"])
        self.assertEqual([name for name in names if name.startswith(top_level) or "__pycache__/" in name], [])

    def test_untracked_files_in_a_checkout_never_enter_the_archive(self):
        from build_downloads import source_members
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "docs").mkdir()
            (root / "README.md").write_text("course\n", encoding="utf-8")
            (root / "docs/lesson.md").write_text("tracked\n", encoding="utf-8")
            run = lambda *arguments: subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)
            run("init", "-q"); run("add", "README.md", "docs/lesson.md")
            (root / "docs/private-notes.md").write_text("untracked draft\n", encoding="utf-8")
            members = {path.relative_to(root).as_posix() for path in source_members(root)}
        self.assertEqual(members, {"README.md", "docs/lesson.md"})

    def test_extracted_archive_without_git_uses_the_allowlist(self):
        from build_downloads import source_members
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "ml_ai_it"
            (root / "docs").mkdir(parents=True)
            (root / "README.md").write_text("course\n", encoding="utf-8")
            (root / "docs/lesson.md").write_text("lesson\n", encoding="utf-8")
            (root / "docs/figure.png").write_bytes(b"not allowlisted")
            members = {path.relative_to(root).as_posix() for path in source_members(root)}
        self.assertEqual(members, {"README.md", "docs/lesson.md"})

    def test_every_page_with_site_downloads_links_the_offline_route(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/check_source_links.py")],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])

    def test_offline_route_maps_each_download_kind_to_source(self):
        page = (ROOT / "docs/setup/student-workspace.md").read_text(encoding="utf-8")
        self.assertIn("## If a download link does not open", page)
        for location in ["notebooks/lessons/", "notebooks/practice/", "data/samples/", "runs/datasets/",
                         "scripts/build_downloads.py --source-only", "projects/phishing-triage/notebooks/complete-study.ipynb"]:
            self.assertIn(location, page)
            if "/" in location and not location.startswith(("runs/", "scripts/")):
                self.assertTrue((ROOT / location.split(" ")[0]).exists(), location)


if __name__ == "__main__":
    unittest.main()
