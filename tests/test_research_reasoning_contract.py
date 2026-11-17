"""Static instructions and packaging, not observed agent compliance."""
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'skills/research-paper-craft'
class ReasoningContracts(unittest.TestCase):
    def guide(self,lang='en'):
        p=S/f'references/research-reasoning.{lang}.md'
        self.assertTrue(p.is_file(),str(p)); return p.read_text(encoding='utf-8')
    def test_existing_skill_bilingual_route(self):
        text=(S/'SKILL.md').read_text()
        for lang in ('en','th'): self.assertIn(f'references/research-reasoning.{lang}.md',text)
        self.assertIn('name: research-paper-craft',text)
    def test_bilingual_rules_match(self):
        self.assertEqual(re.findall(r'^## (R\d+)\b',self.guide('en'),re.M),re.findall(r'^## (R\d+)\b',self.guide('th'),re.M))
    def test_all_research_dimensions(self):
        text=self.guide()
        for term in ('Practical Problem','Research Gap','Proposed Solution','closest','Originality','Scientific Impact','Methodological Impact','Practical Impact','Expected Impact','Demonstrated Impact','Observed Results','Derived Results','Interpretation','Hypothesis','Unsupported Claim'):
            self.assertIn(term,text)
    def test_lightweight_is_not_full_audit(self):
        text=(S/'SKILL.md').read_text(); self.assertIn('Language-only',text); self.assertIn('do not trigger',text)
    def test_approval_and_no_cosmetic_science(self):
        text=self.guide()
        for term in ('researcher approval','Do not repair a scientific defect by polishing','statistical','theoretical','qualitative','replication','negative'):
            self.assertIn(term,text)
    def test_feedback_classes_and_persistence(self):
        text=self.guide()
        for term in ('Universal Research Principle','Domain-Specific Principle','Project-Specific Correction','Unverified Recommendation','single expert','version-controlled','exceptions'):
            self.assertIn(term,text)
    def test_output_contract(self):
        text=self.guide()
        self.assertIn('| Issue | Evidence | Why It Matters | Recommended Fix | Status | Priority |',text)
        for term in ('Critical Research Problems','Verified Contributions','Unsupported Claims','Missing Evidence','Feasible Gap-Closure Actions','Decisions Requiring Researcher Approval'):
            self.assertIn(term,text)
    def test_existing_records_not_parallel_ledgers(self):
        text=self.guide()
        for term in ('literature-matrix.csv','metric-plan.csv','paper-map.csv','Claim ledger','Decision log','Source manifest','QA report','reasoning_review'):
            self.assertIn(term,text)
    def test_ars_owns_workflow(self):
        for lang in ('en','th'):
            self.assertIn(f'research-reasoning.{lang}.md',(S/f'references/ars-integration.{lang}.md').read_text())
        self.assertIn('Research reasoning',(S/'assets/ars-handoff.md').read_text())
    def test_new_optional_schema_does_not_migrate_templates(self):
        import json
        template=json.loads((S/'assets/full-paper-run.json').read_text())
        self.assertEqual(template['schema_version'],1)
        self.assertNotIn('reasoning_review',template)
    def test_old_rules_remain_intact(self):
        import hashlib,json
        manifest=json.loads((S/'provenance/rule-map.json').read_text())
        for r in manifest['rules']:
            text=(S/r['file']).read_text(); matches=list(re.finditer(r'^## (R\d\d)\b.*$',text,re.M))
            blocks={m[1]:text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)].strip() for i,m in enumerate(matches)}
            self.assertEqual(hashlib.sha256(blocks[r['rule']].encode()).hexdigest(),r['sha256'])
if __name__=='__main__': unittest.main()
