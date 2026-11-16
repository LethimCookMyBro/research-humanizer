"""Tests of records, not model-generated answers."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('evaluation_records',ROOT/'evals/evaluate.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class EvaluationRecords(unittest.TestCase):
    def test_export_does_not_reveal_reference_response(self):
        c={'id':'x','topic':'writing','language':'en','source':'Source content','draft':'Draft','task':'Task','acceptable_example':'SECRET_REFERENCE'}
        j=m.jobs([c],'baseline',ROOT)[0]
        self.assertNotIn('SECRET_REFERENCE',j['prompt'])
        self.assertIn('Source content',j['prompt'])
    def test_empty_response_set_fails(self):
        self.assertTrue(m.check([{'case_id':'x','prompt_sha256':'a'}],[])['errors'])
    def test_missing_execution_metadata_fails(self):
        self.assertTrue(m.check([{'case_id':'x','prompt_sha256':'a'}],[{'case_id':'x','response':'hello'}])['errors'])
    def test_duplicates_fail(self):
        r={'case_id':'x','model':'synthetic','host':'synthetic','run_id':'fixture','executed_at':'fixture','prompt_sha256':'a','response':'not a model result'}
        self.assertTrue(m.check([{'case_id':'x','prompt_sha256':'a'}],[r,r])['errors'])
    def test_complete_records_are_not_quality_approval(self):
        r={'case_id':'x','model':'synthetic','host':'synthetic','run_id':'fixture','executed_at':'fixture','prompt_sha256':'a','response':'not a model result'}
        result=m.check([{'case_id':'x','prompt_sha256':'a'}],[r])
        self.assertEqual(result['errors'],[])
        self.assertEqual(result['human_review'],'not_rated')
        self.assertEqual(result['quality_improvement'],'not_established')
if __name__=='__main__': unittest.main()
