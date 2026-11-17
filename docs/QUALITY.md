# Quality contract and gap closure

Version 2.3.0 adds whole-paper drafting and ARS coordination to the 2.2.0 quality work. It does not claim every possible failure is eliminated.

## Whole-paper additions

| Requirement | Implementation | Evidence boundary |
| --- | --- | --- |
| Draft a whole paper, not only polish | Explicit modes, first-draft style and complete applicable deliverables | Static guide contracts, not a successful real manuscript run |
| Pair with ars-full | Dedicated Claude coordinator and host-specific adapter | Source interface inspected. No enforcement hook or live compatibility claim |
| Read related papers before drafting | Actual-study search, source access/locators, official venue and exemplar matrix | Procedure and blank records. Agent still needs real retrieval tools |
| Select relevant metrics | Definition, independent unit, input/code mapping and author decision | Suggestions are not measured outcomes. Auditor checks declarations only |
| Serve many researchers | Scoped accessible memory and approved context outside the plugin | No automatic access to other chats, no inferred personal identity |
| Adapt general humanizing to research | Compatibility matrix for uncertainty, terms, notation, Unicode and scores | No classifier or publication guarantee |
| Publish a versioned download | Main-only tested preview-release workflow | GitHub Release does not refresh an installed host cache |

The older revision-quality changes below remain available. Use minimal editing for existing text, not as a restriction on writing missing sections in full-paper mode.

| Gap | Change | Evidence boundary |
| --- | --- | --- |
| G01 Real-model quality | Public bilingual evaluation cases, prompt exporter and execution-record validator | Infrastructure delivered. Independent model and author evaluation not executed |
| G02 Author voice | Optional approved-sample profile and locked terminology in R07 | Guidance and blank contract, not learned author identity |
| G03 Semantic drift | Before/after claim ledger and lexical review tool | Detects selected candidates, not semantic equivalence |
| G04 Overediting | Minimal-edit default, unchanged controls and stopping rule | Examples and explicit contract, not a model quality score |
| G05 Whole-paper coherence | Reverse outline linking questions, methods, results and scope | Source-level review still required |
| G06 Weak examples | Source-bound English/Thai examples and 24 synthetic cases | Authored teaching fixtures, not recorded benchmark wins |
| G07 Checker defects | All five retained regressions pass; explicit severity and incomplete status | Supported syntax only, no universal parser |
| G08 Frozen instructions | Archived baseline, current fingerprints and explicit changed-rule manifest | Intentional changes are visible, not silently skipped |
| Real images and overview | Real-first selection, capture request, panel provenance and node/edge mapping | Hash identity is not study authenticity |
| Graphs | Independent units, uncertainty, data-to-export reconciliation and final-size review | No automatic certification of statistics or appearance |

## Working loop

```text
Study snapshot → literature / metric / author context → source-bound drafting or revision
        → before-after and source checks → actual-size / saved-artifact inspection
        → author decisions and explicit delivery status
```

Keep records proportional. A one-sentence edit needs no folder of empty CSVs. A full paper needs inspectable evidence for each material claim and visual. Missing originals trigger a researcher question, not a substitute.

## Tool contracts

Run from the repository root. All tools are local and read-only with respect to research inputs. The bundled Python auditors make no API calls and do not upload sources. The full-paper workflow separately requires authorized web or scholarly retrieval by the host; it is not an offline-only writing service.

```bash
python3 skills/research-paper-craft/scripts/lint_manuscript.py manuscript.md --json --fail-on-errors
python3 skills/research-paper-craft/scripts/review_revision.py before.md after.md --terms terms.json
python3 skills/research-paper-craft/scripts/audit_figures.py figure-manifest.json --root /path/to/project
python3 skills/research-paper-craft/scripts/audit_docx.py manuscript.docx --json
python3 skills/research-paper-craft/scripts/audit_full_paper.py full-paper-run.json --json
```

terms.json is a JSON list of exact protected phrases. It is not the entire voice-profile object. Text exports are analysis inputs only, never a reason to recreate a formatted DOCX. Reports can reveal filenames or draft details. Keep them outside public submission packages unless disclosure is authorized.

The text checker keeps the v2 lint_text list API and existing report keys. JSON schema_version is now 2, with status, severity and checked/not_checked scope. Exit 2 means a parse was incomplete or input could not be read. Exit 1 is selected by the failure flags. A zero exit never means scientific or authorship approval. Figure audit exits 1 for contract errors and can exit 0 with human-review candidates. Revision review reports findings without approving semantics.

## Figure manifest

Use schema_version 1 and a nonempty figures array. Every figure has id, kind, purpose, caption, evidence_status, claim_refs, pending_inputs, sources and review. Sources have id, relative path, sha256, role and origin. Paths are confined to the selected project root. The tool does not execute generation scripts or read outside that root. The current per-source limit is 64 MiB.

Graph records need plot_data and generation_script sources, x/y labels, units and scales, chart_type, aggregation, independent_unit, missing_values, exclusions, transformations, numeric_columns and uncertainty. Declare none with a reason or name the actual interval method and unit_of_replication. Photo/screenshot records need original_image, capture_context and permissions. Overview nodes and edges map to source_id and locator. Conceptual figures need an explicit illustration_approval. Each mixed panel should be its own record.

Review source_verified_by and final_size_checked_by only after the corresponding review. Empty fields remain pending. A named reviewer is a declaration to inspect, not executable proof. Research outputs made by a generative model are a separate provenance case requiring manual review, not a loophole for replacing absent photographs.

## External sources

Checked 16 November 2026. These motivate source preservation and reporting checks; they do not certify this software or impose one journal's format on every paper. Recheck the selected venue before submission.

- [Nature image integrity](https://www.nature.com/nature/editorial-policies/image-integrity) describes original-data retention and constraints on image manipulation.
- [PLOS Biology submission guidance](https://journals.plos.org/plosbiology/s/submission-guidelines) gives journal-specific figure and data-presentation requirements.
- [Nature AI policy](https://www.nature.com/nature/editorial-policies/ai) distinguishes assistive use, accountability and unverifiable outputs.
- [Agent Skills specification](https://agentskills.io/specification) describes metadata and progressive disclosure.
