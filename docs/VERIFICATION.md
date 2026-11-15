# Documentation edition verification

Checked on 2026-11-15 using Python 3.13.5.

This record covers repository packaging and documentation. It is not a scientific validation report or an executed behavioral evaluation of an AI model.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Existing skill tests | 31 passed | [Unit-test output](verification/unit-tests.txt) |
| Targeted v2.0 regressions | 5 failed, still open | [Regression output](verification/audit-regressions.txt) |
| Local README links | Resolved in the packaged tree | [Document checks](verification/document-checks.json) |
| English and Thai shell examples | Identical commands | [Document checks](verification/document-checks.json) |
| Claude Code installation copy | All files copied correctly into an isolated temporary home | [Document checks](verification/document-checks.json) |
| Codex installation copy | All files copied correctly into an isolated temporary home | [Document checks](verification/document-checks.json) |
| Existing-installation guard | A second copy attempt left existing files and a local-change sentinel unchanged | [Document checks](verification/document-checks.json) |
| Original skill behavior files | Compared against the supplied v2.0 ZIP | [Package checks](verification/package-checks.json) |
| Humanizer source identification | Local Git blob hash matches upstream v4.0.0 | [Source record](../skills/research-paper-craft/provenance/upstream-license.json) |
| Upstream MIT notice | Complete license copy matches the upstream Git blob hash | [Source record](../skills/research-paper-craft/provenance/upstream-license.json) |
| README presentation | English and Thai opening sections inspected in a local Chromium preview | Local Markdown rendering with simplified GitHub-like styling. External badges were represented by text labels in this preview |

The original skill name and runtime version remain unchanged. The only existing skill files edited by this documentation edition are the local README and the refreshed checksum manifest. Added notices and known-issue files are listed in the package check record.

## Not established

The actual Claude Code and Codex executables are not available in this packaging environment. No live skill discovery or invocation was tested in either host. The PowerShell copy example was inspected but not executed.

The local preview is not GitHub's production renderer. Remote badge images and a published GitHub page were not tested. No repository was created or pushed, and the `YOUR_USERNAME` placeholder must be replaced before publishing the installation URL.

The forty acceptance scenarios remain unexecuted as independent model trials. No native Word, anonymization, real scientific-image, or complete paper-production workflow was newly validated. The five targeted checker failures were not fixed or converted into passing checks.

## Reproduce

Run these separately from the repository root.

```bash
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

The first command currently passes 31 tests. The second currently exits nonzero with five failures. Report those outcomes separately.
