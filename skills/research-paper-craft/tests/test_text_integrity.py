"""Retained v2.3.1 misses and synthetic guard cases. Not a grammar/model benchmark."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('lint_integrity_test', ROOT/'scripts/lint_manuscript.py')
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)
PROBES = json.loads((ROOT/'tests/fixtures/punctuation-v2.3.1-probes.json').read_text(encoding='utf-8'))
GAPS = {
    'missing_space_lower': 'PUNCT_SPACING_REVIEW',
    'short_fragments_two_words': 'FRAGMENT_CHAIN_REVIEW',
    'fullwidth_period': 'PUNCT_REPEAT_REVIEW',
    'unicode_replacement': 'UNICODE_REPLACEMENT_REVIEW',
    'square_glyph': 'GLYPH_CONTEXT_REVIEW',
    'zero_width': 'INVISIBLE_CHARACTER_REVIEW',
    'unbalanced_double_quote': 'QUOTE_BALANCE_REVIEW',
}

DETECT = [
    ('curly_open', 'We recorded “actions.', 'QUOTE_BALANCE_REVIEW'),
    ('curly_close', 'We recorded actions”.', 'QUOTE_BALANCE_REVIEW'),
    ('mixed_quotes', 'We recorded “actions".', 'QUOTE_BALANCE_REVIEW'),
    ('guillemet_open', 'We recorded «actions.', 'QUOTE_BALANCE_REVIEW'),
    ('cjk_quote_open', '記録「動作', 'QUOTE_BALANCE_REVIEW'),
    ('multiword_short', 'Low cost. High accuracy. Rapid feedback.', 'FRAGMENT_CHAIN_REVIEW'),
    ('fullwidth_ellipsis', 'The logger waited．．．', 'ELLIPSIS_REVIEW'),
    ('mixed_dots', 'The logger waited.．', 'PUNCT_REPEAT_REVIEW'),
    ('small_dots', 'The logger waited﹒﹒', 'PUNCT_REPEAT_REVIEW'),
    ('cjk_repeated_stop', '記録した。。', 'PUNCT_REPEAT_REVIEW'),
    ('isolated_fullwidth_english_stop', 'The logger waited．', 'PUNCT_WIDTH_REVIEW'),
    ('lowercase_sentence_gap', 'The logger stopped.the file was saved.', 'PUNCT_SPACING_REVIEW'),
    ('zwsp_in_word', 'The ac\u200btions were saved.', 'INVISIBLE_CHARACTER_REVIEW'),
    ('zwj_in_word', 'The ac\u200dtions were saved.', 'INVISIBLE_CHARACTER_REVIEW'),
    ('zwnj_in_word', 'The ac\u200ctions were saved.', 'INVISIBLE_CHARACTER_REVIEW'),
    ('wordjoiner_in_word', 'The ac\u2060tions were saved.', 'INVISIBLE_CHARACTER_REVIEW'),
    ('soft_hyphen', 'The ac\u00adtions were saved.', 'INVISIBLE_CHARACTER_REVIEW'),
    ('internal_bom', 'The action\ufeff was saved.', 'INVISIBLE_CHARACTER_REVIEW'),
    ('bidi_override', 'The \u202elogger ran.', 'BIDI_CONTROL_REVIEW'),
    ('bidi_isolate', 'The \u2067logger\u2069 ran.', 'BIDI_CONTROL_REVIEW'),
    ('nul_control', 'The logger\x00 ran.', 'CONTROL_CHARACTER_REVIEW'),
    ('replacement_in_quote', 'The source says "�".', 'UNICODE_REPLACEMENT_REVIEW'),
    ('object_marker', 'The export contains \ufffc.', 'UNICODE_REPLACEMENT_REVIEW'),
    ('square_in_prose', 'The export contains □ data.', 'GLYPH_CONTEXT_REVIEW'),
]

CLEAN = [
    ('normal_sentences', 'We measured time. We recorded errors. We compared scores.'),
    ('short_finite_clauses', 'It ran. We waited. They left.'),
    ('adverb_finite_clauses', 'Very few succeeded. Very few returned. Very few failed.'),
    ('thousands_decimal', 'We used 1,000 records and a threshold of 0.25.'),
    ('scientific_notation', 'The threshold was 1.2e-5.'),
    ('version', 'Version v2.3.2 uses Python 3.13.5.'),
    ('abbreviations', 'Dr. A. Smith reviewed Fig. 2 and Eq. 3.'),
    ('ascii_quote', 'The note says "No change."'),
    ('curly_quote', 'The note says “No change.”'),
    ('guillemet_quote', 'The note says «No change.»'),
    ('nested_quote', 'The note says “Use «start» now.”'),
    ('softwrapped_quote', 'The note says "First, I paused;\nthen I retried: it worked."'),
    ('softwrapped_curly_quote', 'The note says “First, I paused;\nthen I retried: it worked.”'),
    ('escaped_quote', r'The note says "Use \"start\" now."'),
    ('cjk_quote', '記録「動作」。'),
    ('cjk_punctuation', '記録した。次を確認する。'),
    ('double_inches', 'The screen measures 5" diagonally.'),
    ('numeric_quote', 'The participant entered "6".'),
    ('apostrophe_possessive', "The participants' sessions ended."),
    ('curly_possessive', 'The participant’s session ended.'),
    ('prime_math', r'The model uses $f\prime(x)$ and $x^{\prime\prime}$.'),
    ('unicode_primes', 'The rotation was 30′ and 2″.'),
    ('domain', 'The dataset is on example.org for inspection.'),
    ('email', 'Contact first.last@example.org for access.'),
    ('url', 'See https://example.org/data.csv?key=x.y.'),
    ('file', 'Read output.csv and settings.json.'),
    ('figure_files', 'Read figure.png and chart.svg.'),
    ('config_files', 'Read settings.yaml and workbook.xlsx.'),
    ('quoted_url', 'The note says "Use https://example.org/data.csv".'),
    ('wrapped_single_words', 'We record actions.\nWe save logs.\nWe check outputs.'),
    ('code_attribute', 'Use `sensor.accel` and `np.mean(values)`.'),
    ('bare_call', 'We used np.mean(values) for the mean.'),
    ('latex_math', r'The proof ends with $x = y \quad □$.'),
    ('quoted_fragments', 'The note says "Very fast. Very clear. Highly effective."'),
    ('math_dots', r'The sequence is $1, 2, \ldots, n$.'),
    ('protected_fence', '```text\nactions.it □ " \u200b\n```'),
    ('thai_boundary', 'ภาษา\u200bไทยใช้การแบ่งคำ'),
    ('persian_joiner', 'این می\u200cشود نمونه است'),
    ('emoji_joiner', 'The icon was 👩\u200d🔬.'),
    ('nbsp_unit', 'The duration was 6\u00a0s.'),
    ('narrow_space', 'The duration was 6\u202fs.'),
    ('initial_bom', '\ufeffThe logger saved the file.'),
    ('cited_numbers', 'The procedure follows (Smith, 2020; Jones, 2021).'),
    ('bracket_citation', 'See [1, 2, 3] for details.'),
]

class TextIntegrityTests(unittest.TestCase):
    def rules(self, text):
        return {f['rule'] for f in TOOL.lint_text(text)}

    def test_original_probe_file_is_identified(self):
        self.assertEqual(PROBES['git_blob_sha'], '5ec1f7e45d5745dc4b46def8701da21bb50364bd')
        self.assertEqual(len(PROBES['cases']), 28)

    def test_existing_probe_detections_remain(self):
        for case in PROBES['cases']:
            with self.subTest(case=case['case']):
                self.assertTrue(set(case['rules']) <= self.rules(case['input']))

    def test_original_clean_probe_controls_remain_clean(self):
        for case in PROBES['cases']:
            if not case['rules'] and case['case'] not in GAPS:
                with self.subTest(case=case['case']):
                    self.assertEqual(TOOL.lint_text(case['input']), [])

    def test_pending_survives_quotes_code_and_corruption(self):
        for text in ('"[SOURCE REQUIRED]"', '“[RESULT UNVERIFIED]', '`[TODO]`', 'ac\u200btions [SOURCE REQUIRED]'):
            with self.subTest(text=text):
                self.assertIn('DRAFT_PLACEHOLDER', self.rules(text))

    def test_unclosed_quote_does_not_hide_following_errors(self):
        rules = self.rules('The note says "unfinished\n\nIt is not done; retry: tomorrow.')
        self.assertTrue({'QUOTE_BALANCE_REVIEW', 'PUNCT_COLON', 'PUNCT_SEMICOLON'} <= rules)

    def test_locations_and_codepoints(self):
        findings = TOOL.lint_text('Clear text.\n\nac\u200btions �')
        rows = {f['rule']: f for f in findings}
        self.assertIn('INVISIBLE_CHARACTER_REVIEW', rows)
        self.assertIn('UNICODE_REPLACEMENT_REVIEW', rows)
        self.assertEqual(rows['INVISIBLE_CHARACTER_REVIEW']['line'], 3)
        self.assertEqual(rows['INVISIBLE_CHARACTER_REVIEW']['column'], 3)
        self.assertEqual(rows['INVISIBLE_CHARACTER_REVIEW']['codepoint'], 'U+200B')
        self.assertEqual(rows['UNICODE_REPLACEMENT_REVIEW']['codepoint'], 'U+FFFD')
        self.assertNotIn('\u200b', rows['INVISIBLE_CHARACTER_REVIEW']['excerpt'])

    def test_quotation_location_on_wrapped_line(self):
        findings = TOOL.lint_text('The logger ran\nand saved "actions.')
        found = [f for f in findings if f['rule'] == 'QUOTE_BALANCE_REVIEW']
        self.assertTrue(found)
        self.assertEqual(found[0]['line'], 2)

    def test_valid_quote_does_not_hide_following_rule(self):
        self.assertIn('PUNCT_SEMICOLON', self.rules('It says "done"; inspect the log.'))

    def test_link_quote_column_matches_source(self):
        text = 'Read [the file](https://example.org) and "unfinished.'
        rows = [f for f in TOOL.lint_text(text) if f['rule']=='QUOTE_BALANCE_REVIEW']
        self.assertTrue(rows)
        row = rows[0]
        self.assertEqual(row['column'], text.index('"')+1)

    def test_bidi_is_escaped_in_all_report_excerpts(self):
        rows = TOOL.lint_text('The \u202elogger ran..')
        self.assertTrue(rows)
        self.assertTrue(all('\u202e' not in row['excerpt'] for row in rows))

    def test_random_inputs_do_not_crash_or_change_results(self):
        import random
        rng=random.Random(232)
        alphabet='abc x.y,;()[]$`"“”«»\n\t．□�ก่日\u200b\u200d\u2066\u2069'
        for _ in range(300):
            text=''.join(rng.choice(alphabet) for _ in range(rng.randint(0,120)))
            self.assertEqual(TOOL.inspect_text(text),TOOL.inspect_text(text))

    def test_existing_incomplete_status_stays(self):
        self.assertEqual(TOOL.inspect_text('$$\nunclosed')['status'], 'incomplete')

    def test_cli_preserves_bytes_and_review_exit(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'sample.md'
            raw=b'\xef\xbb\xbfThe ac\xe2\x80\x8btions were saved..\r\n'
            path.write_bytes(raw)
            cmd=[sys.executable,'-B',str(ROOT/'scripts/lint_manuscript.py'),str(path),'--json']
            for option, expected in (('--fail-on-errors',0),('--fail-on-findings',1)):
                run=subprocess.run(cmd+[option],capture_output=True,text=True)
                self.assertEqual(run.returncode, expected, run.stderr)
                report=json.loads(run.stdout)['reports'][0]
                self.assertFalse(report['authorship_detection'])
                self.assertEqual(path.read_bytes(),raw)

    def test_invalid_utf8_is_not_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'sample.md'; path.write_bytes(b'bad\xfftext')
            run=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/lint_manuscript.py'),str(path),'--json'],capture_output=True)
            self.assertEqual(run.returncode,2)
            self.assertEqual(path.read_bytes(),b'bad\xfftext')

    def test_unsupported_single_quote_grammar_is_disclosed(self):
        report=TOOL.inspect_text('The logger ran.')
        self.assertIn('all citation/quotation/notation forms',report['not_checked'])
        self.assertIn('grammar_correctness', report['not_checked'])


def positive(text, rule):
    def test(self):
        matches=[f for f in TOOL.lint_text(text) if f['rule']==rule]
        self.assertTrue(matches, (text,rule))
        self.assertTrue(all(f['severity']=='review' for f in matches))
    return test

def negative(text):
    def test(self):
        self.assertEqual(TOOL.lint_text(text), [], text)
    return test

for case in PROBES['cases']:
    if case['case'] in GAPS:
        setattr(TextIntegrityTests,'test_original_gap_'+case['case'],positive(case['input'],GAPS[case['case']]))
for name,text,rule in DETECT:
    setattr(TextIntegrityTests,'test_detect_'+name,positive(text,rule))
for name,text in CLEAN:
    setattr(TextIntegrityTests,'test_preserve_'+name,negative(text))

if __name__=='__main__': unittest.main()
