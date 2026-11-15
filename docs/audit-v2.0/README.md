# Research Paper Craft v2.0 audit

Audited 2026-11-15. This is an audit bundle, not an updated or installable skill.

## Verdict

The requested research-writing rules are present in the inspected instructions. The current package does not justify a claim that all gaps are closed or that AI behavior has been validated end to end.

The original 31 tests pass on Python 3.13.5. All 32 listed file hashes match. The preserved Humanizer source matches the supplied file byte for byte. Five added targeted regression checks fail on unchanged v2.0. These are deliberately selected edge cases, not a representative failure rate.

## Reproduced checker defects

- `Here's the result.` is not flagged as a contraction.
- `[RESULT UNVERIFIED]` disappears from the draft-marker check inside inline math or inline code.
- An unclosed YAML-like opening or display-math delimiter can suppress all later checks without a warning.

Greek-letter context and numerical contribution statements are additional unimplemented checks, not defects in a claimed semantic validator. The README already documents the checker as heuristic. A clean report is not manuscript approval.

## Remaining validation and release work

The package defines 40 behavioral scenarios but contains no executed independent model trials or target-host installation test. The audit did not run those trials. Full-paper, native Word, and anonymity workflows were not exercised on a real manuscript. Bilingual rule-ID alignment tests do not prove semantic translation equivalence.

Clarify that explicit user prohibitions must be fixed before claiming house-style compliance, while optional prose refinements may remain warnings.

The package has no package-wide LICENSE. The preserved original says MIT in metadata, but a full upstream copyright and permission notice and an identified upstream rights holder were not found in the inspected package. Confirm upstream provenance and licensing before public redistribution. Do not invent copyright holders. Absence of a LICENSE is not an Agent Skills format failure.

## Evidence and reproduction

See AUDIT.th.md for the requirement matrix, source locations, root causes, proposed remedies, limitations, and external specification references. See audit-evidence.json for exact probe inputs and outputs. unit-tests.txt records the existing suite. regression-tests.txt records the newly added checks.

Run the audit regression checks against an extracted skill directory with

```bash
python -B audit_regressions.py /path/to/research-paper-craft
```

Run the original test suite from the skill directory with

```bash
python -B -m unittest discover -s tests -v
```

No original package file was edited. No new skill release was built, no installation was performed, and nothing was published to GitHub.
