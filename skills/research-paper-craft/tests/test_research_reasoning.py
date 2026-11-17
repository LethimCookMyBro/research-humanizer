"""Declared-record regressions, not semantic or model-quality evaluation."""
import copy
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('reasoning_auditor', ROOT/'scripts/audit_full_paper.py')
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)

def row(kind, **extra):
    data = {'id':kind+'-1', 'criterion':kind, 'record_ref':'qa.md#'+kind,
            'status':'Verified', 'scope':'Specified study and source snapshot',
            'rationale':'Declared inspection of scoped evidence',
            'evidence_refs':['sources.md#S1'], 'review_locator':'qa.md#inspection',
            'asserted_as_fact':False}
    data.update(extra)
    return data

def record():
    checks={x:{'status':'passed','evidence_locator':'qa.md#'+x} for x in TOOL.CHECKS}
    return {'schema_version':1,'mode':'full-paper','workflow':'standalone',
      'study':{'question':'Under which assumptions does the bound hold?','source_version':'fixture'},
      'literature':{'status':'searched','searched_on':'2026-11-17','queries':['synthetic fixture only'],
        'venue':{'url':'https://example.org/venue','requirements_locator':'instructions'},
        'sources':[{'id':'S1','title':'Synthetic source','url':'https://example.org/paper',
                    'access':'full_text','locators':['Section 2']}]},
      'metrics':[], 'sections':[{'name':'Argument','status':'drafted','evidence_locator':'paper.md#proof'}],
      'docx_requested':False,'checks':checks,
      'reasoning_review':{'schema_version':1,'phase':'review','workflow_owner':'standalone',
        'rq_refs':['paper-map.csv#RQ1'], 'record_refs':{'qa_report':'qa.md','claim_ledger':'claims.md'},
        'assessments':[
          row('gap', prior_work_refs=['literature-matrix.csv#S1'], closest_work_refs=['literature-matrix.csv#S1'],
              known='Bound for case A', unknown='Case B under assumption C', importance='Limits of the bound',
              study_fit='The argument addresses case B', gap_closed=False),
          row('originality', prior_work_refs=['literature-matrix.csv#S1'], contribution_type='theoretical',
              knowledge_gain='A scoped bound for case B', novelty_basis='comparison'),
          row('impact', impact_type='Scientific Impact', impact_basis='Expected Impact',
              reported_impact='Expected Impact', beneficiaries='Researchers studying case B',
              application_limits='Assumption C'),
          row('alignment', rq_ref='paper-map.csv#RQ1', method_ref='methods.md#proof',
              data_or_argument_refs=['proof.md#lemma'], analysis_ref='proof.md#derivation',
              suitable=True),
          row('finding', finding_type='Derived Results', result_refs=['proof.md#theorem'],
              consistency='consistent', relation='theoretical', derivation_ref='proof.md#derivation'),
          row('limitation', original_answer='Scoped extension', matters_answer='Clarifies assumptions',
              knowledge_answer='Bound holds under C', limitation_refs=['proof.md#assumptions'])]}}

class ResearchReasoningTests(unittest.TestCase):
    def codes(self, data): return {r['code'] for r in TOOL.audit_record(data)['findings']}
    def item(self, data, kind):
        return next(r for r in data['reasoning_review']['assessments'] if r['criterion']==kind)
    def test_legacy_record_without_extension_is_unchanged(self):
        d=record(); del d['reasoning_review']
        self.assertEqual(TOOL.audit_record(d), {'record_status':'consistent','findings':[],
          'scientific_verification':'not_performed_by_this_tool','submission_approved':False,
          'scope':'Declared record consistency only. No source retrieval, tool execution, semantic verification or rendered-layout inspection.'})
    def test_theoretical_work_without_numeric_metrics(self):
        self.assertEqual(self.codes(record()),set())
    def test_qualitative_without_numeric_baseline_or_statistics(self):
        d=record(); self.item(d,'originality')['contribution_type']='empirical'
        r=self.item(d,'alignment'); r.update(method_ref='methods.md#interpretive',data_or_argument_refs=['transcripts.md#T1'],analysis_ref='coding.md#interpretation')
        self.assertEqual(self.codes(d),set())
    def test_unsupported_novelty_not_asserted_as_fact(self):
        d=record(); self.item(d,'originality').update(status='Unverified',asserted_as_fact=True)
        self.assertIn('REASONING_UNSUPPORTED_ASSERTION',self.codes(d))
    def test_gap_needs_literature_and_closest_work(self):
        d=record(); self.item(d,'gap').update(prior_work_refs=[],closest_work_refs=[])
        self.assertIn('REASONING_GAP_BASIS',self.codes(d))
    def test_empty_search_is_not_absence_proof(self):
        d=record(); self.item(d,'gap').update(absence_claim=True,search_only=True)
        self.assertIn('REASONING_ABSENCE',self.codes(d))
    def test_completed_text_does_not_close_gap(self):
        d=record(); self.item(d,'gap').update(gap_closed=True)
        self.assertIn('REASONING_GAP_CLOSURE',self.codes(d))
    def test_gap_existence_and_closure_are_separate(self):
        self.assertNotIn('REASONING_GAP_CLOSURE',self.codes(record()))
    def test_rq_needs_suitable_data_or_argument(self):
        d=record(); self.item(d,'alignment').update(data_or_argument_refs=[],suitable=False)
        self.assertIn('REASONING_ALIGNMENT',self.codes(d))
    def test_every_declared_question_is_covered(self):
        d=record(); d['reasoning_review']['rq_refs'].append('paper-map.csv#RQ2')
        self.assertIn('REASONING_RQ_COVERAGE',self.codes(d))
    def test_tool_change_is_not_automatic_contribution(self):
        d=record(); self.item(d,'originality').update(novelty_basis='tool_or_context_change',knowledge_gain='')
        self.assertIn('REASONING_ORIGINALITY',self.codes(d))
    def test_expected_impact_not_demonstrated(self):
        d=record(); self.item(d,'impact')['reported_impact']='Demonstrated Impact'
        self.assertIn('REASONING_IMPACT_INFLATION',self.codes(d))
    def test_demonstrated_impact_requires_observed_support(self):
        d=record(); self.item(d,'impact').update(impact_basis='Demonstrated Impact',reported_impact='Demonstrated Impact')
        self.assertIn('REASONING_IMPACT_EVIDENCE',self.codes(d))
    def test_metric_needs_definition_measurement_rationale_limits(self):
        d=record(); d['reasoning_review']['assessments'].append(row('metric'))
        self.assertIn('REASONING_METRIC',self.codes(d))
    def test_complete_metric_review(self):
        d=record(); d['reasoning_review']['assessments'].append(row('metric',definition_ref='metric-plan.csv#M1-definition',measurement_ref='metric-plan.csv#M1-measurement',selection_rationale='metric-plan.csv#M1-reason',limitations='metric-plan.csv#M1-limits'))
        self.assertNotIn('REASONING_METRIC',self.codes(d))
    def test_correlation_is_not_causation(self):
        d=record(); self.item(d,'finding').update(relation='causal',association_only=True,causal_basis_ref='methods.md#assertion')
        self.assertIn('REASONING_CAUSAL',self.codes(d))
    def test_causal_claim_needs_identification_argument(self):
        d=record(); self.item(d,'finding').update(relation='causal')
        self.assertIn('REASONING_CAUSAL',self.codes(d))
    def test_finding_cannot_conflict_with_results(self):
        d=record(); self.item(d,'finding')['consistency']='contradicted'
        self.assertIn('REASONING_RESULT_CONFLICT',self.codes(d))
    def test_negative_result_contribution_valid(self):
        d=record(); self.item(d,'originality')['contribution_type']='negative_result'
        self.assertEqual(self.codes(d),set())
    def test_replication_contribution_valid(self):
        d=record(); self.item(d,'originality')['contribution_type']='replication'
        self.assertEqual(self.codes(d),set())
    def test_revision_requires_scientific_approval(self):
        d=record(); d['reasoning_review']['assessments'].append(row('revision',scientific_change=True))
        self.assertIn('REASONING_APPROVAL',self.codes(d))
    def test_authorized_revision_and_language_only_revision(self):
        for changed in (True,False):
            d=record(); d['reasoning_review']['assessments'].append(row('revision',scientific_change=changed,approval_ref='decisions.md#D1'))
            self.assertNotIn('REASONING_APPROVAL',self.codes(d))
    def test_single_expert_not_universal(self):
        d=record(); d['reasoning_review']['assessments'].append(row('feedback',classification='Universal Research Principle',promote_to_general=True,validation_basis='expert_opinion_only',validation_ref='notes.md#opinion',exceptions='scope-bound',approval_ref='decisions.md#D2'))
        self.assertIn('REASONING_FEEDBACK_PROMOTION',self.codes(d))
    def test_unverified_feedback_can_remain_a_proposal(self):
        d=record(); d['reasoning_review']['assessments'].append(row('feedback',classification='Unverified Recommendation',status='Proposed',promote_to_general=False))
        self.assertNotIn('REASONING_FEEDBACK_PROMOTION',self.codes(d))
    def test_no_duplicate_ars_owner(self):
        d=record(); d['workflow']='ars'; d['dependencies']={'ars':{'loaded':True,'entry':'installed-entry','version':'fixture','confirmations_preserved':True}}
        self.assertIn('REASONING_WORKFLOW_OWNER',self.codes(d))
        d['reasoning_review']['workflow_owner']='ars'
        self.assertNotIn('REASONING_WORKFLOW_OWNER',self.codes(d))
    def test_na_requires_a_reason(self):
        d=record(); self.item(d,'impact').update(status='Not Applicable',rationale='')
        self.assertIn('REASONING_CONTEXT',self.codes(d))
    def test_verified_needs_actual_review_locator(self):
        d=record(); self.item(d,'gap').update(review_locator='',evidence_refs=[])
        self.assertIn('REASONING_VERIFICATION',self.codes(d))
    def test_no_score_or_automatic_scientific_approval(self):
        r=TOOL.audit_record(record()); self.assertIs(r['submission_approved'],False)
        self.assertEqual(r['scientific_verification'],'not_performed_by_this_tool'); self.assertNotIn('score',r)
    def test_all_six_support_states_recognized(self):
        for status in ('Verified','Partially Supported','Unverified','Proposed','Contradicted','Not Applicable'):
            d=record(); self.item(d,'impact')['status']=status
            self.assertNotIn('REASONING_STATUS',self.codes(d))
    def test_missing_review_dimensions_are_visible(self):
        d=record(); d['reasoning_review']['assessments']=[]
        self.assertIn('REASONING_COVERAGE',self.codes(d))
    def test_planning_does_not_require_completed_results(self):
        d=record(); d['reasoning_review']['phase']='planning'; d['reasoning_review']['assessments']=[x for x in d['reasoning_review']['assessments'] if x['criterion'] in ('gap','originality','alignment')]
        self.assertNotIn('REASONING_COVERAGE',self.codes(d))
    def test_input_is_not_changed(self):
        d=record(); original=copy.deepcopy(d); TOOL.audit_record(d); self.assertEqual(d,original)
    def test_malformed_optional_extension_is_not_ignored(self):
        for value in (None,False,[],42,'review',{'schema_version':1,'phase':[], 'assessments':[None,{},[],{'criterion':[]}]}):
            d=record(); d['reasoning_review']=value
            self.assertTrue(any(c.startswith('REASONING_') for c in self.codes(d)))
    def test_cli_no_mutation(self):
        d=record(); self.item(d,'gap')['prior_work_refs']=[]
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'record.json'; p.write_text(json.dumps(d),encoding='utf-8'); before=p.read_bytes()
            r=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/audit_full_paper.py'),str(p),'--json'],capture_output=True,text=True)
            self.assertEqual(r.returncode,1,r.stderr); self.assertEqual(p.read_bytes(),before)
            self.assertIn('REASONING_GAP_BASIS',{x['code'] for x in json.loads(r.stdout)['findings']})

    def test_na_cannot_hide_gap_closure_claim(self):
        d=record(); self.item(d,'gap').update(status='Not Applicable',gap_closed=True)
        self.assertIn('REASONING_GAP_CLOSURE',self.codes(d))
    def test_verified_finding_cannot_declare_unverified_result_match(self):
        d=record(); self.item(d,'finding')['consistency']='unverified'
        self.assertIn('REASONING_RESULT_CONFLICT',self.codes(d))
    def test_verified_finding_cannot_declare_only_partial_result_match(self):
        d=record(); self.item(d,'finding')['consistency']='partial'
        self.assertIn('REASONING_RESULT_CONFLICT',self.codes(d))
    def test_hypothesis_is_not_verified_finding(self):
        d=record(); self.item(d,'finding')['finding_type']='Hypothesis'
        self.assertIn('REASONING_UNSUPPORTED_ASSERTION',self.codes(d))
    def test_partial_finding_can_remain_qualified(self):
        d=record(); self.item(d,'finding').update(status='Partially Supported',consistency='partial',asserted_as_fact=True,qualification_ref='claims.md#qualified')
        self.assertEqual(self.codes(d),set())
    def test_na_cannot_hide_missing_rq_path(self):
        d=record(); self.item(d,'alignment')['status']='Not Applicable'
        self.assertIn('REASONING_RQ_COVERAGE',self.codes(d))
    def test_promoted_feedback_has_scoped_approval(self):
        d=record(); d['reasoning_review']['assessments'].append(row('feedback',classification='Universal Research Principle',promote_to_general=True,validation_basis='methodological_argument',validation_ref='decisions.md#argument',exceptions='decisions.md#scope',approval_ref='decisions.md#approval'))
        self.assertNotIn('REASONING_FEEDBACK_PROMOTION',self.codes(d))
    def test_duplicate_assessment_id(self):
        d=record(); d['reasoning_review']['assessments'].append(copy.deepcopy(self.item(d,'gap')))
        self.assertIn('REASONING_ID',self.codes(d))
    def test_declared_closure_has_scoped_evidence(self):
        d=record(); self.item(d,'gap').update(gap_closed=True,closure_scope='Only case B under C',closure_evidence_refs=['proof.md#theorem'],remaining_uncertainty='Assumption D remains untested')
        self.assertNotIn('REASONING_GAP_CLOSURE',self.codes(d))
        self.assertIs(TOOL.audit_record(d)['submission_approved'],False)
    def test_random_field_types_do_not_crash_or_mutate_input(self):
        rng=random.Random(233)
        choices=[None,False,True,0,1,[],{},['x'],{'x':1},'', 'unknown']
        keys=('id','criterion','status','scope','record_ref','rationale','evidence_refs','asserted_as_fact','rq_ref','impact_type','consistency','classification')
        for _ in range(200):
            d=record(); item=rng.choice(d['reasoning_review']['assessments']); item[rng.choice(keys)]=copy.deepcopy(rng.choice(choices))
            before=copy.deepcopy(d); a=TOOL.audit_record(d); b=TOOL.audit_record(d)
            self.assertEqual(a,b); self.assertEqual(before,d)

if __name__=='__main__': unittest.main()
