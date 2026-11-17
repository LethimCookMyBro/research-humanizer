"""Synthetic record tests only. The tool cannot prove that research was conducted."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/audit_full_paper.py'

def record():
    return {
        'schema_version':1,'mode':'full-paper','workflow':'ars',
        'dependencies':{'ars':{'loaded':True,'version':'3.24.3','entry':'academic-research-skills:academic-pipeline','confirmations_preserved':True}},
        'study':{'question':'Synthetic test question','source_version':'fixture-v1'},
        'literature':{'status':'searched','searched_on':'2026-11-17','queries':['synthetic query'],
            'venue':{'url':'https://example.org/venue','requirements_locator':'fixture p1'},
            'sources':[{'id':'S1','url':'https://example.org/paper','title':'Synthetic fixture','access':'full_text','locators':['methods p2']}]},
        'metrics':[{'id':'M1','decision':'selected','source_ids':['S1'],'definition':'mean duration','independent_unit':'participant','raw_fields':['elapsed_seconds'],
            'code_locator':'fixture.py::mean','approval':'fixture author decision','result_status':'not_measured','validation_locator':None}],
        'sections':[{'name':'Methods','status':'drafted','evidence_locator':'fixture.md#method'}],
        'docx_requested':True,
        'checks':{k:{'status':'passed','evidence_locator':'fixture-check-log'} for k in ('numbers','citations','meaning','style','visuals','equations','anonymity','word_layout')}
    }

class FullPaperAuditTests(unittest.TestCase):
    def audit(self,d):
        self.assertTrue(SCRIPT.exists(), 'Missing full-paper record auditor')
        spec=importlib.util.spec_from_file_location('full_audit',SCRIPT)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module.audit_record(d)
    def codes(self,d): return {f['code'] for f in self.audit(d)['findings']}
    def test_consistent_record_not_submission_certificate(self):
        result=self.audit(record())
        self.assertEqual(result['record_status'],'consistent')
        self.assertFalse(result['submission_approved'])
        self.assertEqual(result['scientific_verification'],'not_performed_by_this_tool')
    def test_input_is_not_mutated(self):
        d=record();old=copy.deepcopy(d);self.audit(d);self.assertEqual(d,old)
    def test_absent_ars_is_not_simulated(self):
        d=record();d['dependencies']['ars']['loaded']=False;self.assertIn('ARS_UNAVAILABLE',self.codes(d))
    def test_string_true_is_not_confirmation(self):
        d=record();d['dependencies']['ars']['confirmations_preserved']='true';self.assertIn('ARS_CONFIRMATIONS',self.codes(d))
    def test_missing_ars_version(self):
        d=record();d['dependencies']['ars']['version']=None;self.assertIn('ARS_VERSION',self.codes(d))
    def test_standalone_does_not_require_ars(self):
        d=record();d['workflow']='standalone';d['dependencies']={};self.assertNotIn('ARS_UNAVAILABLE',self.codes(d))
    def test_offline_is_incomplete(self):
        d=record();d['literature']['status']='offline';self.assertIn('SEARCH_PENDING',self.codes(d))
    def test_missing_query(self):
        d=record();d['literature']['queries']=[];self.assertIn('SEARCH_LOG',self.codes(d))
    def test_impossible_search_date(self):
        d=record();d['literature']['searched_on']='2026-02-31';self.assertIn('SEARCH_DATE',self.codes(d))
    def test_venue_not_inferred_from_sample(self):
        d=record();d['literature']['venue']={};self.assertIn('VENUE_PENDING',self.codes(d))
    def test_duplicate_source(self):
        d=record();d['literature']['sources']*=2;self.assertIn('SOURCE_DUPLICATE',self.codes(d))
    def test_metadata_is_not_metric_evidence(self):
        d=record();d['literature']['sources'][0]['access']='metadata_only';self.assertIn('METRIC_SOURCE_ACCESS',self.codes(d))
    def test_abstract_only_is_not_metric_evidence(self):
        d=record();d['literature']['sources'][0]['access']='abstract_only';self.assertIn('METRIC_SOURCE_ACCESS',self.codes(d))
    def test_unknown_metric_source(self):
        d=record();d['metrics'][0]['source_ids']=['S2'];self.assertIn('METRIC_SOURCE_UNKNOWN',self.codes(d))
    def test_incomplete_metric_definition(self):
        d=record();d['metrics'][0]['definition']=None;self.assertIn('METRIC_DEFINITION',self.codes(d))
    def test_missing_independent_unit(self):
        d=record();d['metrics'][0]['independent_unit']=None;self.assertIn('METRIC_DEFINITION',self.codes(d))
    def test_selected_metric_without_data(self):
        d=record();d['metrics'][0]['raw_fields']=[];self.assertIn('METRIC_DATA',self.codes(d))
    def test_selected_metric_without_author_approval(self):
        d=record();d['metrics'][0]['approval']=None;self.assertIn('METRIC_APPROVAL',self.codes(d))
    def test_not_measured_is_not_fabricated_result(self):
        self.assertNotIn('RESULT_UNVERIFIED',self.codes(record()))
    def test_reported_metric_needs_validation(self):
        d=record();d['metrics'][0]['result_status']='reported';self.assertIn('RESULT_UNVERIFIED',self.codes(d))
    def test_empty_checks_are_not_pass(self):
        d=record();d['checks']={};self.assertIn('CHECK_PENDING',self.codes(d))
    def test_pass_without_evidence(self):
        d=record();d['checks']['style']['evidence_locator']=None;self.assertIn('CHECK_EVIDENCE',self.codes(d))
    def test_docx_requires_native_word_check(self):
        d=record();d['checks']['word_layout']={'status':'not_applicable','reason':'no Word here'};self.assertIn('WORD_PENDING',self.codes(d))
    def test_non_docx_can_mark_word_not_applicable(self):
        d=record();d['docx_requested']=False;d['checks']['word_layout']={'status':'not_applicable','reason':'LaTeX only'};self.assertNotIn('WORD_PENDING',self.codes(d))
    def test_blocked_section_is_not_final(self):
        d=record();d['sections'][0]['status']='blocked';self.assertIn('SECTION_PENDING',self.codes(d))
    def test_no_sections(self):
        d=record();d['sections']=[];self.assertIn('SECTIONS_PENDING',self.codes(d))
    def test_malformed_structure_reports_incomplete(self):
        for d in ([],None,{'schema_version':True},{'schema_version':1,'literature':[]}):
            with self.subTest(d=d):self.assertNotEqual(self.audit(d)['record_status'],'consistent')
    def test_cli_bad_json_is_not_pass(self):
        self.assertTrue(SCRIPT.exists())
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bad.json';p.write_text('{bad')
            run=subprocess.run([sys.executable,'-B',str(SCRIPT),str(p),'--json'],capture_output=True,text=True)
            self.assertEqual(run.returncode,2);self.assertEqual(json.loads(run.stdout)['record_status'],'incomplete')
    def test_cli_never_modifies_input(self):
        self.assertTrue(SCRIPT.exists())
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'record.json';p.write_text(json.dumps(record()));before=p.read_bytes()
            run=subprocess.run([sys.executable,'-B',str(SCRIPT),str(p),'--json'],capture_output=True,text=True)
            self.assertEqual(run.returncode,0);self.assertEqual(before,p.read_bytes())
            self.assertFalse(json.loads(run.stdout)['submission_approved'])

if __name__=='__main__': unittest.main()
