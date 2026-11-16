"""Static packaging checks, not behavioral tests of an AI model."""
from pathlib import Path
import os
import hashlib
import json
import re
import unittest

ROOT = Path(os.environ.get('RESEARCH_SKILL_ROOT', Path(__file__).resolve().parents[1]))
TOPICS = ('evidence', 'writing', 'paper', 'methods', 'evaluation', 'visuals', 'submission', 'records')

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.core = (ROOT / 'SKILL.md').read_text(encoding='utf-8')

    def test_metadata_and_folder_name(self):
        self.assertTrue(self.core.startswith('---\n'))
        front = self.core.split('---', 2)[1]
        name = re.search(r'^name:\s*(\S+)$', front, re.M)
        self.assertIsNotNone(name)
        self.assertEqual(name.group(1), ROOT.name)
        self.assertRegex(name.group(1), r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        desc = re.search(r'^description:\s*(.+)$', front, re.M)
        self.assertIsNotNone(desc)
        self.assertLessEqual(len(desc.group(1)), 1024)
        self.assertLessEqual(len(name.group(1)), 64)

    def test_main_size_budget(self):
        self.assertLessEqual(len(self.core.splitlines()), 100)
        self.assertLessEqual(len(self.core.split()), 1000)

    def test_no_bulk_guide_requirement(self):
        self.assertNotIn('read the entire selected guide', self.core.casefold())
        self.assertNotIn('read R00 through R09', self.core)
        self.assertIn('Do not load all modules', self.core)

    def test_eight_bilingual_routes(self):
        for topic in TOPICS:
            for language in ('en', 'th'):
                rel = f'references/{topic}.{language}.md'
                with self.subTest(file=rel):
                    self.assertIn(f']({rel})', self.core)
                    self.assertTrue((ROOT / rel).is_file())

    def test_all_local_links_resolve(self):
        for doc in ROOT.rglob('*.md'):
            if 'provenance' in doc.parts:
                continue
            text = doc.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)', text):
                target = target.split('#', 1)[0]
                if not target or '://' in target or target.startswith('mailto:'):
                    continue
                with self.subTest(document=str(doc), target=target):
                    self.assertTrue((doc.parent / target).exists())

    def test_rules_present_once_per_language(self):
        for language in ('en', 'th'):
            ids = []
            for topic in TOPICS:
                path = ROOT / f'references/{topic}.{language}.md'
                if path.exists():
                    ids.extend(re.findall(r'^## (R\d\d)\b', path.read_text(encoding='utf-8'), re.M))
            self.assertCountEqual(ids, [f'R{i:02}' for i in range(31)])

    def test_bilingual_rule_alignment(self):
        for topic in TOPICS:
            paths = [ROOT / f'references/{topic}.{language}.md' for language in ('en', 'th')]
            if not all(p.exists() for p in paths):
                self.fail(f'Missing language module for {topic}')
            ids = [re.findall(r'^## (R\d\d)\b', p.read_text(encoding='utf-8'), re.M) for p in paths]
            self.assertEqual(ids[0], ids[1])

    def test_missing_evidence_gate_in_core(self):
        for fragment in ('first ask the researcher', 'actual environment photographs',
                         'Do not guess', 'search for substitutes', 'generate replacements',
                         '[SOURCE REQUIRED]', 'explicit approval', 'independent supported work'):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.core)

    def test_style_and_integrity_remain_in_core(self):
        for fragment in ('Keywords:', 'contractions', 'Greek', 'Contributions',
                         'raw records', 'Microsoft Word', 'every final page', 'metadata',
                         'Never claim', 'Submission candidate'):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.core)

    def test_no_double_translation_loading(self):
        self.assertIn('one language', self.core)
        self.assertIn('not both translations', self.core)

    def test_existing_tools_and_source_preserved(self):
        for rel in ('scripts/lint_manuscript.py', 'assets/project-brief.yaml',
                    'assets/qa-report.md', 'provenance/humanizer-original.md'):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_current_rule_fingerprints(self):
        manifest = json.loads((ROOT / "provenance/rule-map.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["rules"]), 62)
        for item in manifest["rules"]:
            text = (ROOT / item["file"]).read_text(encoding="utf-8")
            matches = list(re.finditer(r"^## (R\d\d)\b.*$", text, re.M))
            blocks = {m.group(1): text[m.start():matches[i+1].start() if i+1 < len(matches) else len(text)].strip()
                      for i, m in enumerate(matches)}
            actual = hashlib.sha256(blocks[item["rule"]].encode()).hexdigest()
            self.assertEqual(actual, item["sha256"], f"{item['language']} {item['rule']}")

    def test_no_cache_or_secret_files(self):
        forbidden = {'.env', '.DS_Store'}
        for path in ROOT.rglob('*'):
            if path.is_file():
                self.assertNotIn(path.name, forbidden)
                self.assertNotEqual(path.suffix, '.pyc')

if __name__ == '__main__':
    unittest.main()
