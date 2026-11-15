# Known issues

Documentation packaging date 2026-11-15. Core skill version 2.0.0.

## Checker defects still open

The optional `lint_manuscript.py` remains unchanged from v2.0. The audit reproduces five targeted failures in three groups.

| ID | Failure | Consequence |
| --- | --- | --- |
| K01 | `Here's the result.` is not detected as a contraction | The contraction rule can be missed |
| K02 | `[RESULT UNVERIFIED]` is masked inside inline math or inline code | An unresolved result marker can disappear from the report |
| K03 | An unclosed YAML-like opening or display-math delimiter masks later text without warning | A malformed document can look clean |

These are selected edge cases, not a measured population failure rate. Check unresolved placeholders manually across the entire manuscript. Check protected regions for balanced delimiters. Never use a zero-finding report as scientific or submission approval.

## Coverage not implemented in the checker

Greek-symbol context, numerical results inside contribution bullets, scientific meaning, mathematical correctness, source verification, real-image provenance, and anonymity require separate review. The checker is not a Markdown or LaTeX parser, does not render documents, and cannot inspect native Word pagination.

## Behavioral evidence not yet collected

Forty acceptance scenarios are supplied but have not been executed as independent model trials. Live discovery and invocation inside Claude Code or Codex were not tested in this documentation environment. No full research-paper, anonymization, or native Word workflow was validated here.

A bilingual rule-ID alignment check does not prove semantic translation equivalence. Review meaning-preservation examples in both languages before making broader reliability claims.

## Instruction clarification still pending

The existing style prohibition rules are strong, but the submission guidance also mentions minor style warnings. A future instruction revision should explicitly distinguish mandatory house-style failures from optional refinements before claiming style compliance. This documentation edition does not silently rewrite those rule blocks.

## Licensing status updated

The earlier audit could not identify a complete upstream copyright notice within the supplied package. This documentation edition identifies the Humanizer v4.0.0 source by Git blob SHA and includes the matching MIT notice. That specific provenance gap has been addressed. The earlier audit is retained as a historical record, not rewritten to imply the license was already present.

The remaining checker defects and missing behavioral tests have not been closed by adding documentation or a license.
