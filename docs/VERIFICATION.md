# Verification record

## 2.2.0, 16 November 2026

| Suite | Result |
| --- | --- |
| Repository contracts and evaluation-record checks | 34 passed |
| Skill tools and contracts | 105 passed |
| Retained historical regressions | 5 passed, previously all failed |
| Total | 144 passed |

These are software tests and static instruction checks, not tests of human authorship or scientific quality. The five historical tests are retained unchanged. New tool tests were first run before implementation and 34 of 38 failed. Eight new instruction contracts failed before the guide changes. Additional malformed-JSON and symbol-context regressions were reproduced and repaired.

The supplied 2.1.0 archive was reconstructed as a Git tree matching upstream `be654c513ed5401f0c9eee00351a44807c65ac34` at commit `21dfaf56da1f59fbd48d5810d8b867ec9a667cc1`. The new current rule map records deliberate changes to 20 language-specific bodies. Its prior 62-body map is archived. Both Word-layout modules and the original Humanizer are unchanged.

The 24 synthetic evaluation cases were exported for baseline and skill conditions. No model was called by that exporter. Independent model trials were **not executed**. The connected read-only delegation attempt failed before yielding a model response. No fake response or benchmark score was substituted. Native Word repair, live host installation and rendered figure workflows remain unverified.

The current code was tested with Python 3.13.5. Figure tests use synthetic local files and records. Hashes prove byte identity, not image authenticity. Revision flags are lexical candidates, not proof of semantic equivalence. All study data and screenshots remain outside this public package.

[Machine-readable record](verification/release-v2.2.0.json) · [Gap closure and tool contracts](QUALITY.md) · [Evaluation protocol](../evals/README.md)

## Reproduce

```bash
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

All three commands should succeed for this revision. A new GitHub workflow runs them with read-only repository permissions. Local success is not a claim that the remote workflow has already run.

## Historical records

- [Word-layout 2.1.0](verification/word-layout-v2.1.0.json)
- [Plugin packaging 2.0.1](verification/plugin-packaging.json)
- [Original targeted audit](audit-v2.0/README.md)

Old logs describe old revisions. They are preserved rather than rewritten as if their failures had never occurred.
