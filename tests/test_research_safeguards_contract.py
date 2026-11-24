"""Static safeguard coverage and authored scenario checks, not model evaluation."""
import hashlib
import json
from pathlib import Path
import re
import unittest
R=Path(__file__).resolve().parents[1]; S=R/'skills/research-paper-craft'
class SafeguardContracts(unittest.TestCase):
    def guide(self,lang='en'):
        p=S/f'references/research-safeguards.{lang}.md'
        self.assertTrue(p.exists(),'Task-loaded safeguards module missing')
        return p.read_text(encoding='utf-8')
    def test_bilingual_route(self):
        t=(S/'SKILL.md').read_text()
        for lang in ('en','th'): self.assertIn(f'research-safeguards.{lang}.md',t)
    def test_bilingual_rule_identity(self):
        for lang in ('en','th'):
            self.assertEqual(re.findall(r'^## (R\d+)\b',self.guide(lang),re.M),['R51','R52','R53','R54','R55','R56'])
    def test_reading_marks_is_not_arbitrary_deletion(self):
        t=self.guide()
        for k in ('commented version','heading is not permission to delete','author-confirmed','assistant inference','replacement','duplicate photographs'):
            self.assertIn(k,t)
    def test_write_upload_publish_are_separate(self):
        t=self.guide()
        for k in ('edit','upload','submit','publication','authorization','concurrent','read-back'):
            self.assertIn(k,t)
    def test_sample_and_evidence_states(self):
        t=self.guide()
        for k in ('recruited','analyzed','independent unit','development','pilot','actual sessions','deployed','experienced'):
            self.assertIn(k,t)
    def test_event_and_clock_semantics(self):
        t=self.guide()
        for k in ('visible feedback','clock','timestamp ties','automatic','first-opening latency','equal time bins','join cardinality','precision'):
            self.assertIn(k,t)
    def test_aggregation_is_not_opportunity_zero(self):
        t=self.guide()
        for k in ('mean of individual ratios','pooled ratio','no opportunity','missing','zero','percentage points','unrounded','sensitivity'):
            self.assertIn(k,t)
    def test_measurement_interpretation(self):
        t=self.guide()
        for k in ('displayed','read','scale anchors','randomized','culture','designed difficulty','measured difficulty','interaction','exploratory'):
            self.assertIn(k,t)
    def test_graph_and_reference_dependencies(self):
        t=self.guide()
        for k in ('caption','legend','panel','DOI','cross-artifact','independent verification','component render','backend','exported'):
            self.assertIn(k,t)
    def test_ethics_and_data_minimization(self):
        t=self.guide().lower()
        for k in ('exemption','approval','consent','funding','re-identification','least','hidden sheets','recipient'):
            self.assertIn(k,t)
    def test_scope_not_universal_venue_policy(self):
        t=self.guide()
        for k in ('not universal','qualitative','theoretical','only relevant','Language-only','no fixed','not a direct transcript'):
            self.assertIn(k,t)
    def test_existing_records_are_reused(self):
        t=self.guide()
        for k in ('Decision log','Number ledger','Source manifest','QA report','paper-map.csv','metric-plan.csv','no parallel ledger'):
            self.assertIn(k,t)
    def test_full_paper_and_ars_handoff(self):
        for lang in ('en','th'):
            for name in ('full-paper','ars-integration','evidence','evaluation','visuals','submission','records'):
                self.assertIn(f'research-safeguards.{lang}.md',(S/f'references/{name}.{lang}.md').read_text())
        self.assertIn('Research safeguards',(S/'assets/ars-handoff.md').read_text())
    def mapping(self):
        p=S/'provenance/safeguards-map.v2.3.4.json'; self.assertTrue(p.exists())
        return json.loads(p.read_text())
    def test_all_72_source_items_mapped(self):
        d=self.mapping(); self.assertEqual([x['source_item'] for x in d['items']],list(range(1,73)))
        for x in d['items']:
            self.assertTrue(x['scope']); self.assertTrue(x['adaptation']);self.assertTrue(x['existing_rules'])
            for lang in ('en','th'):
                self.assertTrue((S/x['targets'][lang]).exists())
    def test_source_provenance_and_limits(self):
        d=self.mapping(); self.assertEqual(d['source_kind'],'user-supplied synthesis')
        self.assertFalse(d['private_linked_sources_inspected']);self.assertFalse(d['universal_validation_claimed'])
        self.assertRegex(d['source_sha256'],r'^[0-9a-f]{64}$')
    def test_no_private_paths_or_project_constants_copied(self):
        text=self.guide()+self.guide('th')+json.dumps(self.mapping())
        self.assertNotIn('/Users/',text)
        self.assertNotIn('C:\\Users\\',text)
        self.assertFalse(self.mapping()['raw_private_source_redistributed'])
    def cases(self):
        p=R/'evals/research-safeguards-cases.jsonl';self.assertTrue(p.exists())
        return [json.loads(x) for x in p.read_text().splitlines() if x]
    def test_pressure_cases_are_authored_not_measured(self):
        cases=self.cases(); self.assertGreaterEqual(len(cases),18)
        self.assertEqual(len(cases),len({c['id'] for c in cases}))
        for c in cases:
            self.assertEqual(c['provenance'],'authored synthetic fixture'); self.assertEqual(c['execution_status'],'Not Run')
            for key in ('source_note','request','expected_checks','must_not'):
                self.assertTrue(c[key])
    def test_every_new_rule_has_pressure_cases(self):
        rules={r for c in self.cases() for r in c['rules']}
        self.assertTrue(set('R51 R52 R53 R54 R55 R56'.split()).issubset(rules))
    def test_old_auditors_remain_identical(self):
        p=S/'provenance/safeguards-map.v2.3.4.json';self.assertTrue(p.exists())
        for name,sha in json.loads(p.read_text())['unchanged_auditor_hashes'].items():
            self.assertEqual(hashlib.sha256((S/'scripts'/name).read_bytes()).hexdigest(),sha)
    def test_new_rule_fingerprints(self):
        rows=self.mapping()['new_rule_fingerprints']
        self.assertEqual(len(rows),12)
        for r in rows:
            t=(S/r['file']).read_text();ms=list(re.finditer(r'^## (R\d\d)\b.*$',t,re.M))
            blocks={m[1]:t[m.start():ms[i+1].start() if i+1<len(ms) else len(t)].strip() for i,m in enumerate(ms)}
            self.assertEqual(hashlib.sha256(blocks[r['rule']].encode()).hexdigest(),r['sha256'])
    def test_runtime_budget(self):
        self.assertLessEqual(len((S/'SKILL.md').read_text().split()),1000)
if __name__=='__main__': unittest.main()
