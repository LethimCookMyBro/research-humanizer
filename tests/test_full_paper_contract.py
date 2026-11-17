"""Source contracts, not model-behavior or native host integration tests."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'skills/research-paper-craft'

class FullPaperContracts(unittest.TestCase):
    def text(self, rel):
        path = ROOT / rel
        self.assertTrue(path.is_file(), rel)
        return path.read_text(encoding='utf-8')

    def test_modes_and_scope(self):
        text = self.text('skills/research-paper-craft/SKILL.md')
        for phrase in ('full-paper', 'revise', 'audit', 'ars-full', 'from the first draft'):
            self.assertIn(phrase, text)
        self.assertNotIn('Default to a minimal edit and keep good text unchanged.', text)

    def test_full_paper_routes_and_parity(self):
        core = self.text('skills/research-paper-craft/SKILL.md')
        for topic, ids in [('full-paper', ['R41', 'R42', 'R43']), ('literature', ['R44', 'R45', 'R46'])]:
            for lang in ('en','th'):
                path = f'references/{topic}.{lang}.md'
                self.assertIn(f']({path})', core)
                text = self.text('skills/research-paper-craft/' + path)
                self.assertEqual(re.findall(r'^## (R\d+)\b', text, re.M), ids)

    def test_native_entry_loads_ours_before_ars(self):
        text = self.text('commands/research-full.md')
        self.assertIn('research-humanizer:research-paper-craft', text)
        self.assertIn('academic-research-skills:academic-pipeline', text)
        self.assertLess(text.index('research-humanizer:research-paper-craft'),text.index('academic-research-skills:academic-pipeline'))
        self.assertIn('Do not invoke ars-full as a Skill', text)
        self.assertIn('stop the ARS route', text)

    def test_ars_adapter_guards(self):
        text = self.text('skills/research-paper-craft/references/ars-integration.en.md')
        for phrase in ('confirmation', 'not a runtime hook', 'not installed', 'Pandoc', 'Word-first', 'CC BY-NC 4.0', 'version', 'agent'):
            self.assertIn(phrase, text)

    def test_no_generic_voice_or_score_override(self):
        text = self.text('skills/research-paper-craft/references/ars-integration.en.md')
        for phrase in ('contractions', 'uncertainty', 'AI-tell score', 'burstiness', 'Unicode', 'Aboudjem'):
            self.assertIn(phrase.casefold(), text.casefold())

    def test_draft_is_not_just_outline(self):
        text = self.text('skills/research-paper-craft/references/full-paper.en.md')
        for phrase in ('not just an outline', 'source-bound', 'Working draft', 'not measured', 'memory', 'author-approved', 'different researchers', 'existing Word'):
            self.assertIn(phrase, text)

    def test_search_and_metric_rules(self):
        text = self.text('skills/research-paper-craft/references/literature.en.md')
        for phrase in ('official venue', 'primary sources', 'abstract-only', 'locator', 'independent unit', 'not measured', 'post hoc', 'retraction', 'PDF', 'not a study result', 'permission'):
            self.assertIn(phrase, text)

    def test_shared_state_is_not_installed_private_profile(self):
        text = self.text('skills/research-paper-craft/references/full-paper.en.md')
        for phrase in ('.research-humanizer/', 'not inside the plugin', 'not evidence', 'not author approval', 'already-running'):
            self.assertIn(phrase, text)
        self.assertIn('.research-humanizer/', self.text('.gitignore'))

    def test_templates_are_unfilled(self):
        record = json.loads(self.text('skills/research-paper-craft/assets/full-paper-run.json'))
        self.assertEqual(record['literature']['sources'], [])
        self.assertEqual(record['metrics'], [])
        self.assertFalse(record['dependencies']['ars']['loaded'])
        self.assertIsNone(record['study']['question'])
        for name in ('literature-matrix.csv','metric-plan.csv','search-log.csv','ars-handoff.md'):
            self.text('skills/research-paper-craft/assets/' + name)

    def test_upstream_reference_record_is_pinned(self):
        record=json.loads(self.text('skills/research-paper-craft/provenance/integrations.json'))
        for item in record['sources']:
            self.assertRegex(item['ref'], r'^[0-9a-f]{40}$')
            self.assertTrue(item['paths'])
        self.assertFalse(record['ars_vendored'])
        self.assertFalse(record['live_host_tested'])

    def test_readmes_have_full_paper_and_honest_integration(self):
        for file in ('README.md','README(TH).md'):
            text=self.text(file)
            for fragment in ('research-full','ars-full','2.3.0','CC BY-NC','full-paper'):
                self.assertIn(fragment,text)

    def test_license_notice_is_local(self):
        text=self.text('skills/research-paper-craft/licenses/aboudjem-humanizer-MIT.txt')
        self.assertIn('Copyright (c) 2026 Adam Boudjemaa',text)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"',text)

if __name__=='__main__': unittest.main()
