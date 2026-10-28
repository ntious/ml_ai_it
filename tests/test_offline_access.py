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
from unittest.mock import patch
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

    @staticmethod
    def course_folder(root, tracked=True):
        """A minimal course tree with an untracked private note; optionally a Git checkout."""
        (root / "docs").mkdir(parents=True)
        for name, text in [("README.md", "course\n"), ("pyproject.toml", "[project]\n"), ("docs/lesson.md", "lesson\n")]:
            (root / name).write_text(text, encoding="utf-8")
        if tracked:
            for arguments in [("init", "-q"), ("add", "README.md", "pyproject.toml", "docs/lesson.md")]:
                subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)
        (root / "docs/private-notes.md").write_text("untracked draft\n", encoding="utf-8")
        return root

    def assert_refused_without_archive(self, root, message):
        from build_downloads import SourceListUnavailable, build_source_archive, source_members
        with self.assertRaisesRegex(SourceListUnavailable, message):
            source_members(root)
        target = Path(tempfile.gettempdir()) / f"refused-{root.name}-{id(self)}.zip"
        with patch("build_downloads.ROOT", root), self.assertRaises(SourceListUnavailable):
            build_source_archive(target)
        self.assertFalse(target.exists())

    def test_untracked_files_in_a_checkout_never_enter_the_archive(self):
        from build_downloads import source_members
        with tempfile.TemporaryDirectory() as folder:
            root = self.course_folder(Path(folder))
            members = {path.relative_to(root.resolve()).as_posix() for path in source_members(root)}
        self.assertEqual(members, {"README.md", "pyproject.toml", "docs/lesson.md"})

    def test_missing_git_metadata_refuses_instead_of_scanning(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assert_refused_without_archive(self.course_folder(Path(folder) / "ml_ai_it", tracked=False), "not a Git checkout")

    def test_git_not_installed_refuses(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self.course_folder(Path(folder))
            with patch("build_downloads.subprocess.run", side_effect=FileNotFoundError("git")):
                self.assert_refused_without_archive(root, "Git could not be run")

    def test_failing_git_command_refuses(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self.course_folder(Path(folder))
            failure = subprocess.CalledProcessError(128, ["git", "ls-files"])
            with patch("build_downloads.subprocess.run", side_effect=failure):
                self.assert_refused_without_archive(root, "not a Git checkout, or Git failed")

    def test_copy_inside_another_repository_refuses(self):
        with tempfile.TemporaryDirectory() as folder:
            outer = Path(folder)
            subprocess.run(["git", "init", "-q"], cwd=outer, check=True, capture_output=True)
            self.assert_refused_without_archive(self.course_folder(outer / "ml_ai_it", tracked=False), "inside another repository")

    def test_checkout_without_the_course_root_files_refuses(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "notes.md").write_text("not the course\n", encoding="utf-8")
            for arguments in [("init", "-q"), ("add", "notes.md")]:
                subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)
            self.assert_refused_without_archive(root, "do not include the course")

    def test_command_line_reports_the_refusal(self):
        with tempfile.TemporaryDirectory() as folder:
            from build_downloads import main
            root = self.course_folder(Path(folder) / "ml_ai_it", tracked=False)
            with patch("build_downloads.ROOT", root), self.assertRaises(SystemExit) as stopped:
                main(["--source-only", str(root / "out.zip")])
            self.assertIn("No archive written", str(stopped.exception.code))
            self.assertFalse((root / "out.zip").exists())

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
