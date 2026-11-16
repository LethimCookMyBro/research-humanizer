"""Instruction and provenance contracts, not evidence of independent model quality."""
from pathlib import Path
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/research-paper-craft'

class QualityContracts(unittest.TestCase):
    def test_voice_profile_has_no_invented_author(self):
        p=SKILL/'assets/voice-profile.json'
        self.assertTrue(p.exists())
        profile=json.loads(p.read_text())
        self.assertEqual(profile['approved_samples'],[])
        self.assertEqual(profile['locked_terms'],[])
        self.assertIsNone(profile['approved_by'])
    def test_workflow_is_in_existing_writing_module(self):
        text=(SKILL/'references/writing.en.md').read_text()
        for phrase in ('minimal edit','unchanged','claim ledger','citation attachment','stop','voice-profile'):
            self.assertIn(phrase,text.casefold())
    def test_visual_originals_and_overview_mapping(self):
        text=(SKILL/'references/visuals.en.md').read_text()
        for phrase in ('real-first','capture checklist','source locator','independent unit','numerical tolerance','generative fill'):
            self.assertIn(phrase,text.casefold())
    def test_qa_distinguishes_required_style_and_incomplete(self):
        text=(SKILL/'references/submission.en.md').read_text()
        self.assertIn('incomplete',text)
        self.assertIn('required_fix',text)
        self.assertIn('not a style pass',text)
    def test_evaluation_set_is_not_faked_results(self):
        p=ROOT/'evals/cases.jsonl'
        self.assertTrue(p.exists())
        rows=[json.loads(x) for x in p.read_text().splitlines()]
        self.assertGreaterEqual(len(rows),16)
        self.assertEqual(len({r['id'] for r in rows}),len(rows))
        self.assertEqual({r['language'] for r in rows},{'en','th'})
        for r in rows:
            self.assertEqual(r['provenance'],'synthetic_fixture')
            self.assertIn(r['split'],{'development','evaluation'})
            self.assertTrue(r['source'])
            self.assertNotIn('observed_model_output',r)
        self.assertTrue((ROOT/'evals/evaluate.py').exists())
    def test_baseline_fingerprints_retained(self):
        p=SKILL/'provenance/rule-map.v2.1.0.json'
        self.assertTrue(p.exists())
        self.assertEqual(len(json.loads(p.read_text())['rules']),62)
        current=json.loads((SKILL/'provenance/rule-map.json').read_text())
        self.assertEqual(current['version'],'2.2.0')
    def test_templates_fail_closed(self):
        p=SKILL/'assets/figure-manifest.json'
        self.assertTrue(p.exists())
        self.assertEqual(json.loads(p.read_text())['figures'],[])
    def test_repository_keeps_honest_status(self):
        text=(ROOT/'docs/VERIFICATION.md').read_text()
        self.assertIn('2.2.0',text)
        self.assertIn('not executed',text)

if __name__=='__main__': unittest.main()
