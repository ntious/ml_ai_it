"""A public repository must not depend on unpinned sources or describe itself as private or unfinished."""
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

# Maintainer guides describe the publication process itself, so they are not learner pages.
MAINTAINER_PAGES = {"maintainers.md", "release-checklist.md", "publishing.md", "review-guide.md"}
STALE = re.compile(r"(?i)not yet merged|under review|until (?:the )?(?:site is published|publication|first deployment)|"
                   r"return(?:s)? (?:\"?404|404)|repository is (?:also )?(?:private|visible only)|visible only to people|"
                   r"(?:given|have) (?:been given )?access to the repository|enables publication|Development edition|Phase [ABC]\b|"
                   r"needs? (?:learner )?piloting\.|prototype is pending")


class PinnedSourceTests(unittest.TestCase):
    def test_every_dataset_and_the_model_are_pinned(self):
        from practical_ml_ai.continuation_data import SOURCES
        for name, spec in SOURCES.items():
            self.assertRegex(spec.get("sha256", ""), r"^[0-9a-f]{64}$", name)
        from practical_ml_ai.language import MODEL_REVISION
        self.assertRegex(MODEL_REVISION, r"^[0-9a-f]{40}$")

    def test_source_without_a_reviewed_checksum_is_refused_before_download(self):
        from practical_ml_ai import continuation_data
        unreviewed = {"id": 1, "slug": "example", "members": ["x.csv"], "citation": "example", "sha256": ""}
        with patch.dict(continuation_data.SOURCES, {"unreviewed": unreviewed}), \
             patch("urllib.request.urlopen", side_effect=AssertionError("network must not be used")):
            with self.assertRaisesRegex(ValueError, "No reviewed SHA-256"):
                continuation_data.fetch_source("unreviewed")

    def test_model_without_a_pinned_revision_is_refused_before_loading(self):
        from practical_ml_ai import language
        language.local_model.cache_clear()
        with patch.object(language, "MODEL_REVISION", ""):
            with self.assertRaisesRegex(ValueError, "reviewed model revision"):
                language.local_model()


class PublicTextTests(unittest.TestCase):
    def test_learner_pages_do_not_describe_the_repository_as_private_or_unfinished(self):
        pages = [ROOT / "README.md", ROOT / "QUICKSTART.md", *(ROOT / "docs").rglob("*.md"), ROOT / "curriculum/site.json"]
        found = [f"{page.relative_to(ROOT).as_posix()}: {match.group(0)}" for page in pages
                 if "maintenance" not in page.parts for match in STALE.finditer(page.read_text(encoding="utf-8"))
                 if page.name not in MAINTAINER_PAGES]
        self.assertEqual(found, [])

    def test_security_policy_and_single_author_attribution(self):
        from build_downloads import ROOT_FILES
        policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("Report a vulnerability", policy)
        self.assertIn("SECURITY.md", ROOT_FILES)
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn('family-names: "Nti"', citation)
        self.assertNotIn("contributors\"", citation)
        self.assertIn("Copyright (c) 2026 Isaac K. Nti", (ROOT / "LICENSE").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
