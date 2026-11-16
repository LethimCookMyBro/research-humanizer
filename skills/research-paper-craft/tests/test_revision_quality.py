"""Synthetic regressions. These are tool tests, not model or authorship tests."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    path = ROOT / 'scripts' / (name + '.py')
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

class LintSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tool = load('lint_manuscript')
    def codes(self, text):
        return {i['rule'] for i in self.tool.lint_text(text)}
    def test_here_contractions(self):
        for text in ("Here's the result.", "Here’s the result.", "This's provisional."):
            self.assertIn('CONTRACTION', self.codes(text))
    def test_possessives_are_not_contractions(self):
        self.assertEqual(self.codes("The author's model uses Student's t distribution."), set())
    def test_hidden_pending_markers(self):
        for text in ('`[RESULT UNVERIFIED]`', '$[RESULT UNVERIFIED]$',
                     '```text\n[SOURCE REQUIRED]\n```', '---\nnote: "[TBD]"\n---',
                     '## References\n[CITATION NEEDED]', '$$\n[AUTHOR DECISION]\n$$'):
            self.assertIn('DRAFT_PLACEHOLDER', self.codes(text))
    def test_malformed_regions_are_not_clean(self):
        for text in ('---\nx: y', '```\nx', '$$\nx', r'\[x', 'Use `x', 'Use $x'):
            self.assertTrue(any(x.startswith('PARSE_') for x in self.codes(text)), text)
    def test_fence_tail_does_not_close(self):
        self.assertIn('PARSE_UNCLOSED_FENCE', self.codes('```text\nx\n```bad'))
    def test_multi_backtick_inline_code(self):
        self.assertEqual(self.codes('Use ``a`b: c;d`` in code.'), set())
    def test_blockquote_preserved(self):
        self.assertEqual(self.codes('> It isn\'t clear: retain it.'), {'QUOTATION_REVIEW'})
    def test_vague_promotional_review(self):
        text = ('This study provides a comprehensive framework that plays a crucial role '
                'in advancing the field. The findings offer valuable insights and pave the way for future research.')
        self.assertIn('STYLE_CANDIDATE', self.codes(text))
    def test_technical_terms_are_not_banned(self):
        self.assertEqual(self.codes('We used robust regression. The association was statistically significant.'), set())
    def test_severity_and_coverage(self):
        self.assertTrue(hasattr(self.tool, 'inspect_text'))
        report = self.tool.inspect_text('The model ran; output was saved.')
        self.assertEqual(report['status'], 'needs_review')
        self.assertEqual(report['findings'][0]['severity'], 'required_fix')
        self.assertIn('scientific_validity', report['not_checked'])
        self.assertFalse(report['authorship_detection'])
    def test_incomplete_exit_is_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'draft.md'; p.write_text('$$\nunclosed', encoding='utf-8')
            result=subprocess.run([sys.executable, '-B', str(ROOT/'scripts/lint_manuscript.py'), str(p), '--json'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['reports'][0]['status'], 'incomplete')

class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.tool = load('review_revision')
        self.assertIsNotNone(self.tool, 'Revision reviewer not implemented')
    def codes(self, a, b, terms=()):
        return {x['rule'] for x in self.tool.review(a, b, terms)['findings']}
    def test_only_all(self):
        self.assertIn('SCOPE_CHANGED', self.codes('Only successful trials were included.', 'All trials were included.'))
    def test_negation(self):
        self.assertIn('NEGATION_CHANGED', self.codes('The difference was not significant.', 'The difference was significant.'))
    def test_uncertainty(self):
        self.assertIn('UNCERTAINTY_CHANGED', self.codes('The result may indicate an association.', 'The result demonstrates an association.'))
    def test_number(self):
        self.assertIn('NUMBER_CHANGED', self.codes('The test used 12 trials.', 'The test used 21 trials.'))
    def test_unit(self):
        self.assertIn('UNIT_CHANGED', self.codes('The duration was 12 ms.', 'The duration was 12 s.'))
    def test_citation(self):
        self.assertIn('CITATION_CHANGED', self.codes('The method was reported [3].', 'The method was reported [4].'))
    def test_equation(self):
        self.assertIn('MATH_CHANGED', self.codes('Use $x+y$.', 'Use $x-y$.'))
    def test_term_lock(self):
        self.assertIn('LOCKED_TERM_CHANGED', self.codes('Use the reference viewer.', 'Use the guidance panel.', ['reference viewer']))
    def test_thai_scope(self):
        self.assertIn('SCOPE_CHANGED', self.codes('คำนวณเฉพาะงานที่สำเร็จ', 'คำนวณทุกงาน'))
    def test_thai_negation(self):
        self.assertIn('NEGATION_CHANGED', self.codes('ไม่พบความแตกต่าง', 'พบความแตกต่าง'))
    def test_same_text_is_valid(self):
        text='The logger records each action and the corresponding workpiece state.'
        result=self.tool.review(text,text)
        self.assertTrue(result['unchanged'])
        self.assertEqual(result['findings'], [])
    def test_no_flags_is_not_semantic_proof(self):
        result=self.tool.review('The logger records actions.', 'Actions are recorded by the logger.')
        self.assertEqual(result['semantic_equivalence'], 'not_established')
    def test_no_auto_rewrite(self):
        a='The mean is 3.'; b='The median is 3.'
        self.assertIn('ESTIMAND_CHANGED', self.codes(a,b))
    def test_causal_inflation(self):
        self.assertIn('CAUSALITY_CHANGED', self.codes('The outcome was associated with treatment.', 'Treatment caused the outcome.'))

class FigureTests(unittest.TestCase):
    def setUp(self):
        self.tool=load('audit_figures')
        self.assertIsNotNone(self.tool, 'Figure reviewer not implemented')
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.root.joinpath('data.csv').write_text('group,value\na,1\na,2\nb,3\n', encoding='utf-8')
        self.root.joinpath('plot.py').write_text('# synthetic fixture, never executed\n', encoding='utf-8')
    def source(self, path, role, origin='researcher_original'):
        return {'id':role, 'path':path, 'sha256':hashlib.sha256((self.root/path).read_bytes()).hexdigest(), 'role':role, 'origin':origin}
    def figure(self):
        return {'id':'F1','kind':'graph','purpose':'Compare measured values', 'caption':'Synthetic test example.',
                'evidence_status':'derived','claim_refs':['C1'], 'pending_inputs':[],
                'sources':[self.source('data.csv','plot_data'),self.source('plot.py','generation_script')],
                'graph':{'x':{'label':'Group','unit':'category','scale':'categorical'}, 'y':{'label':'Value','unit':'s','scale':'linear'},
                'chart_type':'scatter','aggregation':'none','independent_unit':'participant','missing_values':'none',
                'exclusions':'none','uncertainty':{'type':'none','reason':'Raw observations only'},
                'numeric_columns':['value'],'transformations':'none'},
                'review':{'source_verified_by':None,'final_size_checked_by':None}}
    def report(self, f):
        return self.tool.audit({'schema_version':1,'figures':[f]}, self.root)
    def codes(self, f):
        return {x['rule'] for x in self.report(f)['findings']}
    def test_valid_contract_not_authenticity(self):
        report=self.report(self.figure())
        self.assertEqual(report['errors'],0)
        self.assertEqual(report['source_authenticity'],'not_verified_by_tool')
        self.assertFalse(report['submission_ready'])
    def test_missing_data(self):
        f=self.figure(); f['sources']=[]
        self.assertIn('GRAPH_SOURCES_REQUIRED',self.codes(f))
    def test_hash_mismatch(self):
        f=self.figure(); f['sources'][0]['sha256']='0'*64
        self.assertIn('SOURCE_HASH_MISMATCH',self.codes(f))
    def test_missing_file(self):
        f=self.figure(); f['sources'][0]['path']='absent.csv'
        self.assertIn('SOURCE_MISSING',self.codes(f))
    def test_path_escape(self):
        f=self.figure(); f['sources'][0]['path']='../private.csv'
        self.assertIn('UNSAFE_SOURCE_PATH',self.codes(f))
    def test_generated_photo_rejected(self):
        f=self.figure(); f['kind']='photo'; f['evidence_status']='observed'
        f['sources'][0]['origin']='generative_ai'; f['capture_context']='Claimed lab'; f['permissions']='claimed permission'
        self.assertIn('GENERATED_EVIDENCE',self.codes(f))
    def test_photo_needs_capture_context(self):
        f=self.figure(); f['kind']='photo'; f['evidence_status']='observed'
        self.assertIn('CAPTURE_CONTEXT_REQUIRED',self.codes(f))
    def test_unknown_origins_not_pass(self):
        f=self.figure(); f['sources'][0]['origin']='unknown'
        self.assertIn('SOURCE_ORIGIN_UNVERIFIED',self.codes(f))
    def test_nan_not_plotted(self):
        self.root.joinpath('data.csv').write_text('group,value\na,NaN\n',encoding='utf-8')
        self.assertIn('NONFINITE_PLOT_VALUE',self.codes(self.figure()))
    def test_uncertainty_requires_method(self):
        f=self.figure(); f['graph']['uncertainty']={'type':'confidence_interval'}
        self.assertIn('UNCERTAINTY_METHOD_REQUIRED',self.codes(f))
    def test_no_empty_manifest_pass(self):
        report=self.tool.audit({'schema_version':1,'figures':[]},self.root)
        self.assertGreater(report['errors'],0)
    def test_overview_dangling_arrow(self):
        f=self.figure(); f['kind']='overview'; f['evidence_status']='conceptual'
        f['diagram']={'nodes':[{'id':'A','label':'Logger','status':'implemented','source_id':'generation_script','locator':'line 1'}],
                      'edges':[{'from':'A','to':'B','meaning':'recorded data','source_id':'generation_script','locator':'line 1'}]}
        self.assertIn('DANGLING_EDGE',self.codes(f))
    def test_source_validation_is_readonly(self):
        before={p.name:p.read_bytes() for p in self.root.iterdir()}
        self.report(self.figure())
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})

if __name__ == '__main__': unittest.main()
