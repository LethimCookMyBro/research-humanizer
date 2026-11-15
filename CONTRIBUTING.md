# Contributing

English and Thai contributions are welcome. Keep changes small enough to review and preserve the distinction between a rule, an automated check, and a result observed in a model trial.

## Report an issue

Include the host and version, operating system, model identifier when available, repository commit, a minimal input, expected behavior, actual behavior, and reproduction steps. Redact credentials and identifying information. Use synthetic text or material you are allowed to share.

For prose edits, show both versions and identify any changes in numbers, units, citations, negation, assumptions, or uncertainty. Do not submit private manuscripts or raw participant records in public issues.

## Change the skill

Keep the English and Thai guidance aligned. Do not weaken the requirement to ask the researcher for missing original study inputs. Never add invented results, references, participant approvals, or host-testing claims.

A rule change may legitimately require updating the rule fingerprints. Explain the changed meaning and review both language versions before updating the manifest. Do not modify tests only to hide a regression.

## Test a change

Run from the repository root.

```bash
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

The second command currently fails on five targeted cases. Report baseline failures separately from any newly introduced failure. For a checker fix, first reproduce the defect, then add or retain its regression test and show it passing after the fix.

For a host trial, record the actual host, model, input, outputs, and checks performed. Use the existing acceptance scenarios. A text change or a green unit-test suite does not establish model compliance.

Update the relevant documentation and checksum manifest when changing packaged files. Do not commit caches, secrets, or private research data.

## Licensing

By submitting a contribution, you agree to license your contribution under this project's MIT License and confirm that you have the right to submit it. Preserve third-party notices and disclose the source and license of reused material. This does not require transferring copyright ownership.
