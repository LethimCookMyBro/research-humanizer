# Verification record

## Word-first layout 2.1.0, 2026-11-16

The update adds bilingual Word-preservation rules and a non-mutating DOCX structural preflight. It preserves research humanizing and the earlier scientific evidence rules. It does not claim that formatting cannot break.

| Check | Result |
| --- | --- |
| Source baseline | Reconstructed tree exactly matches remote tree `0265b690c778e6e4d50df65a700f121bbdcb2e27` at commit `aeea3b277a0560d13a91b21b0c9721fe18b9482e` |
| New tests before implementation | 7 of 8 instruction contracts failed. All 27 preflight tests failed on the absent implementation |
| Repository tests after changes | 19 passed, comprising 11 existing plugin tests and 8 new contracts |
| Skill tests after changes | 58 passed, comprising 31 existing tests and 27 new preflight tests |
| Historical text-checker regressions | 5 failed, unchanged |
| Original scientific and writing rules | All 62 R00 to R30 language-specific bodies preserved |
| Humanizer original and text-checker source | Unchanged |
| Word-layout coverage | Ten new rules in each language plus unfilled layout and equation-code records |
| Native Word, actual paper repair, independent model trials | Not performed |
| User screenshots or private manuscript data published | None |

The DOCX fixtures are synthetic ZIP/XML packages. They test the scanner, not Word's renderer. The new tool reports review candidates without editing or rendering the input. It does not resolve the full style cascade, measure visible whitespace, verify equation meaning, or replace page inspection in native Word.

See the [machine-readable report](verification/word-layout-v2.1.0.json) and [skill-level verification](../skills/research-paper-craft/tests/verification-v2.1.md). New [Word acceptance scenarios](../skills/research-paper-craft/tests/word-layout-scenarios.md) are a proposed evaluation set, not executed evidence. Preview status remains appropriate.

The reproduction commands below also run the updated suites. The separate historical audit still exits nonzero with five failures. No old failure was relabeled as a pass.

## Plugin packaging 2.0.1, 2026-11-15

This update adds native plugin manifests and marketplace catalogs. It does not modify the bundled skill or fix its known text-checker defects.

| Check | Result |
| --- | --- |
| Baseline source | Local source tree exactly matches the live repository tree at commit `1f8b1465f8ae63433b462286cf39c6716bd5a013` |
| New packaging tests before changes | Failed on missing manifests and installation documentation |
| New packaging tests after changes | 11 passed |
| Existing skill suite, rerun | 31 passed |
| Known targeted regressions, rerun | 5 failed, unchanged |
| Existing skill payload | All 40 files remain byte-identical |
| README command parity and local links | Checked by the new tests |
| Live Claude Code and Codex installation | Not run. Neither executable is available in this environment |

Reproduce from the repository root.

```bash
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

The third command is expected to fail on the unchanged v2.0 checker. It is not a packaging test. See the [machine-readable record](verification/plugin-packaging.json).

Installation commands and schemas were checked against [Claude Code plugin installation](https://code.claude.com/docs/en/discover-plugins), [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces), [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), and the [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference). This is documentation and offline validation, not proof of live host compatibility.

For a host-level test, record the installed host version, add the repository marketplace, install the plugin, start a new session, and confirm that the skill reads a referenced module. Keep preview status until those trials and the other outstanding checks are recorded.

## Historical documentation edition

The record below describes the original packaging run before this repository was published. Its copy-install checks and placeholder notes are historical, not the current recommended installation method.

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
