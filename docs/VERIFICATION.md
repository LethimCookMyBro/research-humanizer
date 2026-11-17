# Verification record

## 2.3.2, 17 November 2026

Source preparation executed 71 repository/documentation tests, 311 skill tests and 5 historical regressions. All 387 passed. The 90 new tool tests first ran against the exact v2.3.1 linter and produced 38 assertion failures with no test errors. New documentation contracts also failed before the corresponding patch. After implementation the complete suites passed. The release workflow reruns them on the published commit.

The original 28-case public synthetic probe is retained byte-for-byte. All seven previously unflagged gap inputs now trigger their intended review diagnostics. Previously passing probe controls and existing detection expectations are preserved. Additional tests cover source positions, valid quotations across soft wraps, technical notation, multilingual controls, CLI return codes, unchanged input bytes and deterministic malformed-text cases. Test counts are not model-quality scores.

Only the selected syntax and patterns are covered. Unusual quotation conventions, arbitrary dotted identifiers, general grammar and rendered missing-font boxes still need review. No live host installation, ARS paper run, native Word check or independent model evaluation is claimed. Core evidence, figures, methods, full-paper guidance and the original Humanizer remain unchanged apart from the main routing sentence/version and the expanded punctuation guide.

[Executed record](verification/release-v2.3.2.json) · [Before/after probes](verification/punctuation-probes.v2.3.2.json) · [Patch notes](releases/v2.3.2.md)


## 2.3.1, 17 November 2026

The patch adds context-aware punctuation candidates and bilingual drafting guidance. It does not remove punctuation automatically or certify prose as human-written.

| Local suite against the supplied v2.3.0 archive plus this patch | Result |
| --- | --- |
| Repository contracts | 58 passed |
| Skill tools and contracts | 221 passed |
| Unchanged historical regressions | 5 passed |
| Total | 284 passed |

The local archive predates the ten discovery-website tests on current main. Source-preparation CI and the publication workflow run the complete current repository, including those website tests, before publication. Read their actual logs rather than treating this local count as a claim about remote execution.

The 87 new tool cases cover positive candidates, scientific/technical exclusions, wrapped sentences, source lines, severity, unchanged inputs and CLI exits. Before implementation the initial 72-case set had 33 failures. A subsequent 13-case edge set exposed eight failures, and two citation cases exposed two more. All are now passing. Seven of eight new instruction contracts failed before their implementation.

Common citation, quote, ratio, timestamp and numeric-range false positives were repaired. Approximate grammar, unrecognized notation, unsupported citation/quotation forms and Thai sentence segmentation remain outside the tool's certification scope. New punctuation findings are advisory. Existing hard house-style rules and incomplete-parse status remain distinct. Raw inputs are not modified.

Original rule bodies R00 to R46, Word-layout guides and the bundled Humanizer remain unchanged. The writing-guide preambles and core now load the separate R47 punctuation module. ARS handoff forwards it. New behavioral scenarios are proposed only. Independent model quality, host integration and native Word repair were not tested in this patch.

[Machine-readable record](verification/release-v2.3.1.json) · [Release notes](releases/v2.3.1.md) · [English guidance](../skills/research-paper-craft/references/punctuation.en.md) · [คู่มือภาษาไทย](../skills/research-paper-craft/references/punctuation.th.md)

## 2.3.0, 17 November 2026

| Suite | Local result |
| --- | --- |
| Repository contracts, packaging and release configuration | 50 passed |
| Skill tools and contracts | 134 passed |
| Retained historical regressions | 5 passed |
| Total | 189 passed |

All three suites were executed with Python 3.13.5. The 12 new full-paper instruction contracts failed before their implementation. The 29 new record-auditor tests failed before the script existed. The four release-configuration tests failed before its workflow and notes existed. The final local suites pass. Original R00 to R40 reference modules and the bundled original Humanizer remain byte-identical to 2.2.0. The new modules add R41 to R46 plus a separate integration guide. The prior rule-map remains a fingerprint of those unchanged historical rule bodies, not the runtime package version.

The ARS full command, orchestration contract, writing entry, license and relevant setup were inspected at the source pins in the integration record. The Aboudjem skill, README and MIT notice were inspected as a design reference. The Codex sibling's README was checked separately. ARS was not vendored, installed, or run. The general Humanizer CLI and its 55-pattern catalog were not copied into this package.

The record auditor reads synthetic JSON fixtures. It tests declared completeness and relationships, not the truth of declarations. Even a consistent report always returns submission_approved false. It does not retrieve papers, select a scientifically valid metric, invoke ARS, run code, authenticate photographs, check semantic equivalence or render Word.

Live Claude Code and Codex integration, independent model evaluation, real full-paper production and native Word inspection were not performed. The 12 added full-paper acceptance scenarios are an unexecuted evaluation plan. No private manuscript, user screenshot or original study asset is published.

[Machine-readable record](verification/release-v2.3.0.json) · [Integration contract](INTEGRATION.md) · [Proposed full-paper scenarios](../evals/full-paper-scenarios.md)

The release workflow reruns all suites on the published main commit before creating a preview release and source archive. Check that workflow's actual status. Local tests and the presence of a workflow do not establish that publication has succeeded.

## Reproduce the current revision

```bash
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

## Historical 2.2.0 record

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
