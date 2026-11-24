"""Static editorial contract checks, not observed model compliance or prose scoring."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'skills/research-paper-craft'

class OpeningConcisionContracts(unittest.TestCase):
    def text(self, name):
        return (S / 'references' / name).read_text(encoding='utf-8')

    def test_opening_is_traceable_and_proportionate(self):
        text = self.text('paper.en.md')
        for term in ('opening promise', 'traceable premise', 'unmeasured benefit', 'population and setting'):
            self.assertIn(term, text)

    def test_reader_test_is_not_a_fixed_template(self):
        text = self.text('paper.en.md')
        for term in ('reader can identify', 'not a fixed paragraph template', 'no engagement score'):
            self.assertIn(term, text)

    def test_shorter_does_not_mean_less_reproducible(self):
        text = self.text('paper.en.md')
        for term in ('compression pass', 'denominators', 'exclusions', 'proof assumptions', 'interpretive procedure', 'no universal word count'):
            self.assertIn(term, text)

    def test_research_substance_is_not_feature_inventory(self):
        text = self.text('paper.en.md')
        for term in ('feature inventory', 'development diary', 'research question', 'theoretical', 'qualitative'):
            self.assertIn(term, text)

    def test_existing_records_and_approval_are_used(self):
        text = self.text('paper.en.md')
        for term in ('existing paper map', 'QA report', 'researcher approval', 'do not conceal'):
            self.assertIn(term, text)

    def test_task_scoped_route_in_both_languages(self):
        for lang, marker in [('en', 'Only for opening or length work'), ('th', 'เฉพาะงานปรับบทเปิดหรือความยาว')]:
            text = self.text(f'writing.{lang}.md')
            self.assertIn(f'paper.{lang}.md', text)
            self.assertIn(marker, text)

    def test_thai_has_equivalent_decision_checks(self):
        text = self.text('paper.th.md')
        for term in ('ประเด็นที่เปิดไว้', 'หลักฐานตรวจย้อนกลับ', 'ไม่กำหนดจำนวนคำตายตัว', 'ตัวหาร', 'สมมติฐานของบทพิสูจน์', 'ไม่ใช่คะแนนความน่าสนใจ'):
            self.assertIn(term, text)

    def test_examples_include_source_limits_and_do_not_imply_model_runs(self):
        for lang in ('en', 'th'):
            text = self.text(f'editing-examples.{lang}.md')
            for case in ('O01', 'O02', 'O03'):
                self.assertIn(f'## {case}', text)
        self.assertIn('not recorded model responses', self.text('editing-examples.en.md'))
        self.assertIn('ไม่มีหลักฐานว่ารูปแบบใดช่วยให้ทำงานได้ดีขึ้น', self.text('editing-examples.th.md'))

if __name__ == '__main__':
    unittest.main()
