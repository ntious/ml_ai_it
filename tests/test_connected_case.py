"""Protect the connected reading route and its external-source boundaries.

These checks validate routing and source identity, not reproduction of the
upstream research model or attainment of institutional learning outcomes.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / 'curriculum/connections.json').read_text(encoding='utf-8'))
CASE = ROOT / 'docs/cases/three-tier-lstm'


class ConnectedCaseTests(unittest.TestCase):
    def test_every_module_has_a_reciprocal_connection_route(self):
        entries = REGISTRY['modules']
        self.assertEqual([entry['id'] for entry in entries], list(range(1, 15)))
        overview = (ROOT / 'docs/connections.md').read_text(encoding='utf-8')
        for entry in entries:
            with self.subTest(module=entry['id']):
                lesson = ROOT / entry['lesson']
                self.assertTrue(lesson.is_file())
                self.assertIn('connections.md#module-' + str(entry['id']) + '-', lesson.read_text(encoding='utf-8'))
                self.assertIn('### Module ' + str(entry['id']) + ' ', overview)
                target = ROOT / entry['case_page'] if entry['case_page'] else CASE / 'extensions.md'
                self.assertTrue(target.is_file())
                self.assertIn(target.name, lesson.read_text(encoding='utf-8'))

    def test_optional_and_complementary_encounters_keep_their_scope(self):
        entries = {entry['id']: entry for entry in REGISTRY['modules']}
        for number in [2, 4, 12]:
            self.assertEqual(entries[number]['encounter'], 'optional')
        for number in [9, 10, 11, 14]:
            self.assertEqual(entries[number]['encounter'], 'complement')
            self.assertIsNone(entries[number]['case_page'])
        self.assertEqual(entries[7]['encounter'], 'contrast')
        self.assertEqual(entries[8]['encounter'], 'checkpoint')

    def test_upstream_reading_links_use_the_reviewed_revision(self):
        revision = REGISTRY['external_case']['revision']
        self.assertRegex(revision, r'^[0-9a-f]{40}$')
        self.assertIn('not rerun', REGISTRY['external_case']['execution'])
        count = 0
        for page in CASE.glob('*.md'):
            for found in re.finditer(r'https://github.com/ntious/3-Tier-LSTM/(?:blob|tree)/([^/)]+)', page.read_text(encoding='utf-8')):
                self.assertEqual(found.group(1), revision, page.name)
                count += 1
        self.assertGreater(count, 20)

    def test_passport_and_case_source_notes_are_available_as_source(self):
        self.assertTrue((ROOT / 'templates/pipeline-passport.md').is_file())
        self.assertTrue((CASE / 'source-notes.md').is_file())
        # The published connection route must carry no raw attachment or
        # independent copy of upstream implementation/data.
        self.assertTrue(all(path.suffix == '.md' for path in CASE.iterdir()))


if __name__ == '__main__':
    unittest.main()
