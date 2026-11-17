# Optional reasoning fields in existing records

Maintenance/reference contract for v2.3.3. Load only when preparing or checking a reasoning record. Use the same existing claim, source, literature, metric, paper-map, decision and QA records. These fields add scoped references and assessments, not another evidence database. They do not migrate any CSV header or the existing blank `full-paper-run.json`.

## Where to record decisions

| Existing record | Optional annotations when needed |
| --- | --- |
| Literature matrix | gap/closest-work IDs, what is known, uncertainty reason, counterevidence, scope |
| Claim ledger | RQ ID, claim role, support status, impact type and basis, result/derivation/limitation locators |
| Metric plan | RQ ID and references to the existing definition, measurement, selection rationale and limitations |
| Paper map | gap/RQ IDs, method, data or argument, analysis and finding references |
| Decision log | approval locator, scientific-change scope, feedback classification, validation basis, exceptions and superseded version |
| Source manifest | actual inspected version and location; reuse existing fields |
| QA report | the scientific-audit table, six summaries, inspection evidence and pending decisions |

Use notes keyed by existing row IDs where a legacy format has no suitable field. Support states do not replace the existing evidence classes, metric decisions or execution statuses. Existing records without the optional extension retain their previous script behavior. The core scientific review must still disclose pending checks even when the optional script was not run.

## Optional `reasoning_review` member

Add this member only to an existing full-paper schema-1 JSON record when the machine-readable review is useful. Do not turn an audit/revise task into a full-paper job just to run the tool. The tool does not open referenced files or follow URLs.

| Key | Type and meaning |
| --- | --- |
| schema_version | Integer 1 for the extension |
| phase | `planning`, `evidence` or `review` |
| workflow_owner | Same `ars` or `standalone` value as the parent record |
| rq_refs | Nonempty list of unique locators for the declared questions |
| record_refs | Object with a `qa_report` locator; other existing record locators are optional |
| assessments | List of the scoped assessment declarations below |

Each assessment has a unique nonempty `id`, `criterion`, `record_ref`, `scope`, `rationale` and `status`. Status is exactly one of Verified, Partially Supported, Unverified, Proposed, Contradicted or Not Applicable. Verified additionally needs a nonempty `evidence_refs` list and a `review_locator` identifying the actual inspection record. These strings are declarations and are not verified by the tool. Not Applicable requires the scope and reason and bypasses criterion-specific requirements, but cannot hide an unanswered declared RQ or be used to claim gap closure.

`asserted_as_fact` is an optional boolean, default false. It identifies a claim being presented as established. It conflicts with Proposed, Unverified, Contradicted and Not Applicable. Partially Supported needs a `qualification_ref` when used as a finding. It does not suppress missing source or method warnings.

| Criterion | Fields checked in applicable assessments |
| --- | --- |
| gap | `prior_work_refs`, `closest_work_refs`, `known`, `unknown`, `importance`, `study_fit`. Optional booleans `absence_claim`, `search_only`, `gap_closed`. True closure additionally needs Verified support, `closure_evidence_refs`, `closure_scope` and `remaining_uncertainty`. |
| originality | `prior_work_refs`, `contribution_type`, `knowledge_gain`. A `novelty_basis` of `tool_or_context_change` also needs `change_rationale_ref`. Negative results and replication are accepted contribution types. |
| impact | `impact_type` is Scientific Impact, Methodological Impact or Practical Impact. `impact_basis` and `reported_impact` are Expected Impact or Demonstrated Impact. Include `beneficiaries`, `application_limits` and, for demonstrated impact, `observed_support_refs`. |
| alignment | `rq_ref` from `rq_refs`, `method_ref`, `data_or_argument_refs`, `analysis_ref`, boolean `suitable`. Theoretical argument locators can replace empirical data. No mandatory statistics or numerical baseline. |
| finding | `finding_type` is Observed Results, Derived Results, Interpretation, Hypothesis or Unsupported Claim. Include `result_refs` and `consistency` as consistent, partial, unverified or contradicted. Derived results need `derivation_ref`. Verified cannot coexist with a partial or unverified result comparison. Hypothesis and Unsupported Claim cannot be Verified. A `relation` of causal needs `causal_basis_ref` and cannot coexist with `association_only` true. The RQ link is reviewed in the existing paper map. |
| limitation | `original_answer`, `matters_answer`, `knowledge_answer`, `limitation_refs` for the three contribution questions and boundaries. |
| metric | `definition_ref`, `measurement_ref`, `selection_rationale`, `limitations`, pointing to the existing metric plan rather than copying its data. |
| revision | Boolean `scientific_change`. True requires `approval_ref` before implementing scientific changes. |
| feedback | `classification` is one of the four feedback classes. Optional boolean `promote_to_general`. Promotion requires Verified support, Universal Research Principle, a `validation_basis` of independent_sources or methodological_argument, plus `validation_ref`, `exceptions` and `approval_ref`. A single opinion alone is insufficient. |

Planning requires gap, originality and alignment assessments. Evidence review requires alignment and finding assessments. Review requires all six dimensions including impact and limitation. Every declared RQ needs an alignment row. An explained Not Applicable decision can satisfy a genuinely irrelevant dimension. Metric, revision and feedback rows are conditional on the task.

## Read-only check

Use the existing command on the existing record. Resolve the installed skill path before running it.

```bash
python -B skills/research-paper-craft/scripts/audit_full_paper.py full-paper-run.json --json
```

The API, CLI options and return shape remain compatible. No extension means the previous checks only. An extension with missing or conflicting declarations adds `REASONING_*` findings and gives a nonzero CLI exit. No network, manuscript edit, source execution or approval is performed. A consistent record keeps `scientific_verification` set to `not_performed_by_this_tool` and `submission_approved` false. The script does not render the scientific-audit table; the agent creates that report from actually inspected evidence.

## Feedback example

Authored teaching example, not an executed expert review. A reviewer says that every study needs a numeric baseline. Record the comment and its context in the Decision log as Unverified Recommendation. Inspect whether the particular question needs a comparator. For a theorem, a comparison with existing assumptions or bounds may be relevant without an experimental baseline. Keep the resulting recommendation scoped to the appropriate design. Do not promote the original sentence to a universal rule or silently redesign the study.
