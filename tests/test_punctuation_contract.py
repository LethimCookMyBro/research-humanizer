"""Punctuation instructions are source contracts, not model-behavior evidence."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills/research-paper-craft'

class PunctuationContract(unittest.TestCase):
    def test_bilingual_guides_are_linked(self):
        for language in ('en','th'):
            guide=S/f'references/punctuation.{language}.md'
            self.assertTrue(guide.exists())
            self.assertIn(f'(punctuation.{language}.md)',(S/f'references/writing.{language}.md').read_text())
    def test_core_requires_drafting_review(self):
        text=(S/'SKILL.md').read_text()
        self.assertIn('punctuation review',text)
        self.assertIn('each drafted',text)
        self.assertIn('not a quota',text)
    def test_guide_separates_roles_and_preserves_math(self):
        path=S/'references/punctuation.en.md'; self.assertTrue(path.exists())
        text=path.read_text()
        for fragment in ('3 or more','not a grammatical error','-0.5','n = 6','1,000','e.g.','and/or','automatic','caption','citation','simultaneous'):
            self.assertIn(fragment,text)
    def test_no_blanket_sentence_or_punctuation_ban(self):
        path=S/'references/punctuation.en.md'; self.assertTrue(path.exists())
        text=path.read_text()
        self.assertIn('Do not remove every comma',text)
        self.assertIn('complete sentences',text)
        self.assertIn('Do not replace all commas with and',text)
    def test_thresholds_are_documented_as_review(self):
        path=S/'references/punctuation.en.md'; self.assertTrue(path.exists())
        text=path.read_text()
        for fragment in ('COMMA_DENSITY_REVIEW','30','four','not an authorship','not_checked'):
            self.assertIn(fragment,text)
    def test_patch_notes_exist(self):
        path=ROOT/'docs/releases/v2.3.1.md'; self.assertTrue(path.exists())
        text=path.read_text()
        self.assertIn('Preview',text)
        self.assertIn('not',text)
        self.assertIn('Word',text)
    def test_runtime_main_budget(self):
        self.assertLessEqual(len((S/'SKILL.md').read_text().split()),1000)
    def test_full_pipeline_forwards_punctuation(self):
        self.assertIn('punctuation',(ROOT/'commands/research-full.md').read_text())

if __name__=='__main__': unittest.main()
