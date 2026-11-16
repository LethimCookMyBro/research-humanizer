# Repository checks

Run from the repository root.

```bash
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
```

The first command checks plugin packaging and Word-layout instruction contracts. The second checks the heuristic text linter, original rule preservation, and the read-only DOCX preflight. DOCX fixtures are synthetic ZIP/XML data, not rendered Word documents. These tests do not establish scientific correctness or model compliance.

The historical targeted audit is separate and still fails on the unchanged v2.0 text checker.

```bash
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

Do not report those five failures as passes. Native Word and model trials are described in `skills/research-paper-craft/tests/word-layout-scenarios.md` and remain unexecuted until actual evidence is recorded.
