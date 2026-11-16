"""Static instruction contracts. These do not test model compliance or Word rendering."""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/research-paper-craft'

class WordLayoutContractTests(unittest.TestCase):
    def test_bilingual_module_is_routed(self):
        core = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        for lang in ('en', 'th'):
            path = f'references/word-layout.{lang}.md'
            self.assertIn(f']({path})', core)
            self.assertTrue((SKILL / path).is_file())

    def test_rule_ids_match_in_both_languages(self):
        for lang in ('en', 'th'):
            path = SKILL / f'references/word-layout.{lang}.md'
            self.assertTrue(path.is_file(), str(path))
            ids = re.findall(r'^## (R\d+)\b', path.read_text(encoding='utf-8'), re.M)
            self.assertEqual(ids, [f'R{i}' for i in range(31, 41)])

    def test_word_first_guards_are_core_not_optional(self):
        core = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        for phrase in ('Word-first', 'Do not rebuild', 'DOCX', 'patch plan', 'word-layout'):
            self.assertIn(phrase, core)

    def test_scope_covers_each_spacing_level(self):
        path = SKILL / 'references/word-layout.en.md'
        self.assertTrue(path.exists())
        text = path.read_text(encoding='utf-8')
        for phrase in ('character spacing', 'word spacing', 'line spacing', 'paragraph spacing',
                       'Thai', 'Shift+Enter', 'nonbreaking', 'kerning', 'scale', 'baseline'):
            self.assertIn(phrase, text)

    def test_repair_guards_cover_semantics_and_regressions(self):
        path = SKILL / 'references/word-layout.en.md'
        self.assertTrue(path.exists())
        text = path.read_text(encoding='utf-8')
        for phrase in ('OMML', '¿', '□', 'Keep with next', 'cell margins',
                       'equation-to-code', 'every final page', 'original', 'Review draft',
                       'Do not globally', 'exact line height', 'field', 'rollback'):
            self.assertIn(phrase, text)

    def test_blank_records_are_provided(self):
        for name in ('layout-qa.md', 'equation-code-map.csv'):
            self.assertTrue((SKILL / 'assets' / name).is_file())
        self.assertIn('Not checked', (SKILL / 'assets/layout-qa.md').read_text(encoding='utf-8'))

    def test_version_is_bumped_consistently(self):
        core = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('version: "2.1.0"', core)
        for manifest in ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            path = ROOT / manifest
            self.assertTrue(path.exists(), manifest)
            self.assertEqual(json.loads(path.read_text())['version'], '2.1.0')

    def test_humanizer_original_and_writing_are_unchanged(self):
        expected = {
            'provenance/humanizer-original.md': '175bf05f45ae3bf566059a560467166d93a9599c',
        }
        for rel, digest in expected.items():
            data = (SKILL / rel).read_bytes()
            self.assertEqual(hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest(), digest)
        records = json.loads((SKILL / 'provenance/rule-map.json').read_text())['rules']
        for item in records:
            if '/writing.' not in item['file']:
                continue
            text = (SKILL / item['file']).read_text(encoding='utf-8')
            matches = list(re.finditer(r'^## (R\d\d)\b.*$', text, re.M))
            blocks = {m.group(1): text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)].strip() for i,m in enumerate(matches)}
            self.assertEqual(hashlib.sha256(blocks[item['rule']].encode()).hexdigest(), item['sha256'])

if __name__ == '__main__':
    unittest.main()
