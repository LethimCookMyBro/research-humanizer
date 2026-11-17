"""Contracts for the bounded text-integrity patch, not model-compliance tests."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills/research-paper-craft'

class TextIntegrityContract(unittest.TestCase):
    def test_bilingual_guides_keep_character_context(self):
        for lang in ('en','th'):
            text=(S/f'references/punctuation.{lang}.md').read_text(encoding='utf-8')
            for term in ('2.3.2','U+200B','U+FFFD','U+FFFC','U+25A1','QUOTE_BALANCE_REVIEW','UTF-8'):
                self.assertIn(term,text)

    def test_core_still_loads_context_before_writing(self):
        text=(S/'SKILL.md').read_text(encoding='utf-8')
        for term in ('punctuation review','quotation balance','suspicious Unicode','each drafted','not a quota'):
            self.assertIn(term,text)
        self.assertLessEqual(len(text.split()),1000)

    def test_historical_probe_is_not_relabelled_as_model_evaluation(self):
        probe=json.loads((S/'tests/fixtures/punctuation-v2.3.1-probes.json').read_text(encoding='utf-8'))
        self.assertEqual(probe['release'],'v2.3.1')
        self.assertEqual(probe['git_blob_sha'],'5ec1f7e45d5745dc4b46def8701da21bb50364bd')
        self.assertEqual(len(probe['cases']),28)
        notes=ROOT/'docs/releases/v2.3.2.md'
        self.assertTrue(notes.is_file())
        self.assertIn('synthetic',notes.read_text())

if __name__=='__main__': unittest.main()
