"""Version and intentional-rule-change checks, separate from model evaluation."""
import hashlib
import json
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'skills/research-paper-craft'
class ReleaseIntegrity(unittest.TestCase):
    def test_changed_rules_are_an_explicit_allowlist(self):
        changes=json.loads((S/'provenance/rule-changes.v2.2.0.json').read_text())['changed_rules']
        self.assertEqual({(r['language'],r['rule']) for r in changes},
                         {(l,r) for l in ('en','th') for r in ('R06','R07','R08','R18','R19','R20','R21','R28','R29','R30')})
        old=json.loads((S/'provenance/rule-map.v2.1.0.json').read_text())['rules']
        now=json.loads((S/'provenance/rule-map.json').read_text())['rules']
        old={(r['language'],r['rule']):r['sha256'] for r in old}
        now={(r['language'],r['rule']):r['sha256'] for r in now}
        for row in changes:
            key=(row['language'],row['rule'])
            self.assertEqual(old[key],row['before']); self.assertEqual(now[key],row['after'])
        changed={(r['language'],r['rule']) for r in changes}
        for key in set(old)-changed: self.assertEqual(old[key],now[key])
    def test_checksums_cover_every_payload_file(self):
        declared=set()
        for line in (S/'SHA256SUMS.txt').read_text().splitlines():
            if line.strip() and not line.startswith('#'): declared.add(line.split(maxsplit=1)[1].lstrip('*'))
        actual={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'}
        self.assertEqual(declared,actual)
if __name__=='__main__': unittest.main()
