"""Synthetic punctuation regressions, not a benchmark of model prose quality."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('lint_punctuation_fixture', ROOT/'scripts/lint_manuscript.py')
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)

NEW_RULES = {
    'COMMA_DENSITY_REVIEW', 'CLAUSE_LINK_REVIEW', 'PUNCT_SPACED_HYPHEN',
    'PROSE_OPERATOR_REVIEW', 'SLASH_SHORTHAND_REVIEW', 'ELLIPSIS_REVIEW',
    'PUNCT_REPEAT_REVIEW', 'PARENTHETICAL_LOAD_REVIEW',
    'FRAGMENT_CHAIN_REVIEW', 'PUNCT_SPACING_REVIEW', 'DECORATIVE_SEPARATOR_REVIEW',
    'PUNCT_UNBALANCED_REVIEW', 'CONJUNCTION_CHAIN_REVIEW',
}

POSITIVE = [
    ('comma_chain', 'The logger records actions, tracks reference use, stores workpiece states, and exports the session log.', 'COMMA_DENSITY_REVIEW'),
    ('wrapped_comma_chain', 'The logger records actions,\ntracks reference use, stores workpiece states,\nand exports the session log.', 'COMMA_DENSITY_REVIEW'),
    ('thai_comma_chain', 'ระบบเก็บการกระทำ, การดูคำแนะนำ, สถานะชิ้นงาน, และบันทึกการทดลอง', 'COMMA_DENSITY_REVIEW'),
    ('fullwidth_comma_chain', 'The logger records actions， tracks reference use， stores states， and exports logs.', 'COMMA_DENSITY_REVIEW'),
    ('clause_link', 'The logger ran, however, the export failed.', 'CLAUSE_LINK_REVIEW'),
    ('spaced_hyphen', 'The logger - after initialization - records actions.', 'PUNCT_SPACED_HYPHEN'),
    ('equals_prose', 'More feedback = better learning.', 'PROSE_OPERATOR_REVIEW'),
    ('plus_prose', 'Feedback + practice improved the task.', 'PROSE_OPERATOR_REVIEW'),
    ('ampersand', 'We record actions & reference use.', 'PROSE_OPERATOR_REVIEW'),
    ('arrow_prose', 'More feedback -> better learning.', 'PROSE_OPERATOR_REVIEW'),
    ('unicode_arrow', 'More feedback → better learning.', 'PROSE_OPERATOR_REVIEW'),
    ('slash_shorthand', 'The display provides guidance/feedback.', 'SLASH_SHORTHAND_REVIEW'),
    ('ellipsis_ascii', 'The system worked... but the export failed.', 'ELLIPSIS_REVIEW'),
    ('ellipsis_unicode', 'The system worked… but the export failed.', 'ELLIPSIS_REVIEW'),
    ('repeated_period', 'The logger ran.. The export failed.', 'PUNCT_REPEAT_REVIEW'),
    ('repeated_comma', 'The logger ran,, then stopped.', 'PUNCT_REPEAT_REVIEW'),
    ('repeated_exclamation', 'The system worked!!', 'PUNCT_REPEAT_REVIEW'),
    ('parenthetical_load', 'The logger (in the current implementation) records actions (during each session).', 'PARENTHETICAL_LOAD_REVIEW'),
    ('nested_asides', 'The logger (after setup (when connected)) records actions.', 'PARENTHETICAL_LOAD_REVIEW'),
    ('period_fragments', 'Every. Single. Trial.', 'FRAGMENT_CHAIN_REVIEW'),
    ('missing_space', 'The logger ran,then stopped.', 'PUNCT_SPACING_REVIEW'),
    ('extra_space', 'The logger ran .', 'PUNCT_SPACING_REVIEW'),
    ('separator', 'One paragraph.\n\n---\n\nAnother paragraph.', 'DECORATIVE_SEPARATOR_REVIEW'),
    ('equals_separator', 'One paragraph.\n\n=====\n\nAnother paragraph.', 'DECORATIVE_SEPARATOR_REVIEW'),
    ('unclosed_aside', 'The logger (after initialization records actions.', 'PUNCT_UNBALANCED_REVIEW'),
    ('and_chain', 'The system records actions and it tracks reference use and it stores the workpiece state and it exports the session log and it generates a summary for the researcher to inspect.', 'CONJUNCTION_CHAIN_REVIEW'),
]
NEGATIVE = [
    ('necessary_comma', 'When the session ends, the logger saves the file.'),
    ('serial_comma', 'The sensors measure position, speed, and force.'),
    ('separate_sentences', 'We measured speed, force and position. We recorded errors, retries and time.'),
    ('separate_paragraphs', 'We measured speed, force and position\n\nWe recorded errors, retries and time'),
    ('numbers', 'The exports contain 1,000,000 rows and values of 1.25 and 0.75.'),
    ('numeric_commas', 'The medians were 1,200, 2,300, and 3,400 ms.'),
    ('negative_numbers', 'The change was -0.5 and the baseline was −0.2.'),
    ('hyphen_words', 'We used a state-of-the-art baseline in a real-time task with participant-level summaries.'),
    ('arithmetic', 'The difference is 6 - 2 = 4.'),
    ('stats', 'The sample had n = 6 and p < .05.'),
    ('stats_parentheses', 'The test yielded t(5) = 2.1 and p = .04.'),
    ('inline_math', r'The model uses $x = y + z,\; x > 0$ and \(a - b = c\).'),
    ('display_math', '$$\nx = a, b, c, d\n$$'),
    ('code', '```python\nx = a, b, c, d  # do not change\n```'),
    ('inline_code', 'Use `a = b, c, d, e` and ``x - y -> z``.'),
    ('numbers_units', 'The speed was 1.2 m/s and the dose was 2 mg/kg.'),
    ('reference_numbers', 'The method follows [1, 2, 3, 4].'),
    ('author_year', 'The method follows previous work (Smith, 2024; Doe, 2025).'),
    ('equation_reference', 'See Eq. (3) and Fig. 2 for the definition.'),
    ('acronym', 'Virtual reality (VR) and augmented reality (AR) use displays.'),
    ('version', 'Version 2.3.1 uses Python 3.13.5 and output.csv.'),
    ('url', 'See https://example.org/a-b?q=x,y,z&n=6 and doi:10.1234/a-b.'),
    ('numeric_tuple', 'The position was (1, 2, 3).'),
    ('variable_tuple', 'The coordinates are (x, y, z).'),
    ('quotes', 'The participant said "First, I looked, then paused, and tried again...".'),
    ('curly_quotes', 'The participant said “First, I looked, then paused, and tried again…”.'),
    ('blockquote', '> First, I looked, then paused, and tried again...'),
    ('references', '## References\nSmith, A., Doe, B., and Lee, C. (2025). Title - subtitle.'),
    ('table', '| Label | Value |\n| --- | --- |\n| Position | (1, 2, 3) |'),
    ('frontmatter', '---\ntitle: a, b, c, d\n---\nThe logger records actions.'),
    ('bullets', '- We recorded actions.\n- We saved logs.\n- We checked outputs.'),
    ('ordered_list', '1. We recorded actions.\n2. We saved logs.\n3. We checked outputs.'),
    ('setext_heading', 'Methods\n=======\n\nThe logger records actions.'),
    ('abbreviations', 'Dr. A. Smith reviewed Fig. 2. The results agree with Eq. 3.'),
    ('plain_statement', 'The logger records each action and the corresponding workpiece state.'),
]

class PunctuationTests(unittest.TestCase):
    def rules(self, text):
        return {x['rule'] for x in TOOL.lint_text(text)}

    def test_wrap_invariant(self):
        a=POSITIVE[0][1]; b=a.replace('tracks ', '\ntracks ').replace('and exports', '\nand exports')
        self.assertEqual(self.rules(a) & NEW_RULES, self.rules(b) & NEW_RULES)
        self.assertIn('COMMA_DENSITY_REVIEW', self.rules(b))

    def test_location_of_second_paragraph(self):
        found=TOOL.lint_text('A clear sentence.\n\n'+POSITIVE[0][1])
        match=[x for x in found if x['rule']=='COMMA_DENSITY_REVIEW']
        self.assertTrue(match)
        self.assertEqual(match[0]['line'],3)

    def test_required_rules_still_exist(self):
        codes=self.rules("It isn't clear; the explanation follows: short text — not a proof.")
        self.assertTrue({'CONTRACTION','PUNCT_SEMICOLON','PUNCT_COLON','PUNCT_LONG_DASH'} <= codes)

    def test_pending_markers_are_never_masked(self):
        for text in ('"[SOURCE REQUIRED]"', '$[RESULT UNVERIFIED]$', '## References\n[TODO]'):
            self.assertIn('DRAFT_PLACEHOLDER',self.rules(text))

    def test_incomplete_parser_survives(self):
        report=TOOL.inspect_text('$$\na = b, c, d')
        self.assertEqual(report['status'],'incomplete')

    def test_numeric_time_is_not_prose_colon(self):
        self.assertNotIn('PUNCT_COLON', self.rules('The session started at 09:30 and ended at 10:15.'))

    def test_citation_semicolon_is_not_prose(self):
        self.assertNotIn('PUNCT_SEMICOLON',self.rules(NEGATIVE[17][1]))

    def test_exact_quote_is_not_required_rewrite(self):
        found=TOOL.lint_text('The participant said "It isn\'t clear: wait; retry — slowly."')
        self.assertFalse([f for f in found if f['severity']=='required_fix'])

    def test_count_excludes_numeric_and_citation_commas(self):
        text='We measured 1,000 values (Smith, 2024), checked 2,000 records, and saved the file.'
        self.assertNotIn('COMMA_DENSITY_REVIEW', self.rules(text))

    def test_no_authorship_claim(self):
        report=TOOL.inspect_text(POSITIVE[0][1])
        self.assertFalse(report['authorship_detection'])
        self.assertIn('grammar_correctness',report['not_checked'])
        self.assertIn('punctuation_thresholds',report)

    def test_cli_advice_is_review_not_error_and_input_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'draft.md'; path.write_text(POSITIVE[0][1],encoding='utf-8')
            before=path.read_bytes()
            base=[sys.executable,'-B',str(ROOT/'scripts/lint_manuscript.py'),str(path),'--json']
            a=subprocess.run(base+['--fail-on-errors'],capture_output=True,text=True)
            b=subprocess.run(base+['--fail-on-findings'],capture_output=True,text=True)
            self.assertEqual(a.returncode,0,a.stderr)
            self.assertEqual(b.returncode,1,b.stderr)
            self.assertEqual(path.read_bytes(),before)
            self.assertTrue(all(x['severity']=='review' for x in json.loads(a.stdout)['reports'][0]['findings']))


class PunctuationEdgeCases(unittest.TestCase):
    def rules(self,text): return {f['rule'] for f in TOOL.lint_text(text)}
    def test_fullwidth_semicolon(self):
        self.assertIn('PUNCT_SEMICOLON',self.rules('The logger ran； the export failed.'))
    def test_fullwidth_colon(self):
        self.assertIn('PUNCT_COLON',self.rules('The record contains： actions.'))
    def test_numeric_ratio(self):
        self.assertNotIn('PUNCT_COLON',self.rules('The ratio is 3:1.'))
    def test_windows_path(self):
        self.assertNotIn('PUNCT_COLON',self.rules(r'The export is at C:\results\output.csv.'))
    def test_reference_definition(self):
        self.assertNotIn('PUNCT_COLON',self.rules('[source]: https://example.org/data'))
    def test_numeric_en_dash_range(self):
        self.assertNotIn('PUNCT_LONG_DASH',self.rules('See pages 3–5.'))
    def test_list_continuation_is_one_sentence(self):
        text='- The logger records actions,\n  tracks reference use, stores states,\n  and exports logs.'
        self.assertIn('COMMA_DENSITY_REVIEW',self.rules(text))
    def test_country_abbreviation_does_not_split_sentence(self):
        text='We collected logs, records from U.S. participants, timestamps, and feedback.'
        self.assertIn('COMMA_DENSITY_REVIEW',self.rules(text))
    def test_thai_no_punctuation_is_not_flagged(self):
        self.assertEqual(self.rules('ระบบบันทึกการกระทำและสถานะชิ้นงานเพื่อใช้ตรวจสอบภายหลัง') & NEW_RULES,set())
    def test_quote_still_does_not_hide_pending(self):
        self.assertIn('DRAFT_PLACEHOLDER',self.rules('The note says “Data [RESULT UNVERIFIED].”'))
    def test_correct_full_sentences_not_fragments(self):
        self.assertNotIn('FRAGMENT_CHAIN_REVIEW',self.rules('We record actions. We save logs. We check outputs.'))
    def test_scientific_comparison_unchanged(self):
        self.assertEqual(self.rules('The sample has n = 6, p = .04 and a change of -0.5.') & NEW_RULES,set())
    def test_pandoc_citation(self):
        found=TOOL.lint_text('The method is described [see @smith2024, pp. 3-5; @doe2025].')
        self.assertNotIn('PUNCT_SEMICOLON',{x['rule'] for x in found})
        self.assertFalse({x['rule'] for x in found} & NEW_RULES)
    def test_latex_citation_commas(self):
        text=r'The method follows \citep{smith2024,doe2025,lee2025,kim2026}.'
        self.assertNotIn('COMMA_DENSITY_REVIEW',self.rules(text))
    def test_alias_citation(self):
        self.assertNotIn('PUNCT_SEMICOLON',self.rules('See (Smith et al., 2024; Doe and Lee, 2025).'))


def positive_test(text, rule):
    def check(self):
        found=TOOL.lint_text(text)
        self.assertIn(rule, {x['rule'] for x in found})
        for row in found:
            if row['rule']==rule:
                self.assertEqual(row['severity'],'review')
    return check

def negative_test(text):
    def check(self):
        self.assertEqual(self.rules(text) & NEW_RULES,set())
    return check

for name,text,rule in POSITIVE:
    setattr(PunctuationTests,'test_detect_'+name,positive_test(text,rule))
for name,text in NEGATIVE:
    setattr(PunctuationTests,'test_protect_'+name,negative_test(text))

if __name__=='__main__': unittest.main()
