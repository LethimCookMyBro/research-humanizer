# Research reasoning and gap validation

Load for a Scientific Audit, Research Gap Review, full-paper planning/review or a substantive revision. Language-only humanizing does not trigger a full research review. Keep the existing evidence, literature, evaluation and writing rules. This module adds questions and decisions, not a second workflow or a scientific quality score.

## R48 Check the scientific argument within its scope

First establish the article type, research stage, actual question and authoritative sources. Inspect cited passages and study records before judging support. Record access limits and unresolved conflicts. An unavailable source means unverified support, not a disproved claim. A working draft can proceed on independent supported parts while a scientific blocker remains visible.

### Research Gap validity

Separate the Practical Problem, Research Gap and Proposed Solution. A practical difficulty motivates research but does not itself establish a missing piece of knowledge. A proposed system is a candidate response, not evidence that a gap exists.

Locate what previous work establishes, what remains unknown or inadequately supported, and the closest work addressing the same question. For each gap record the source passage, search scope/date, reason for uncertainty, importance and how this study can address it. Check counterevidence and competing terminology. Distinguish absent reporting, inaccessible evidence, conflicting evidence and evidence of absence. Finding no paper is not proof that nobody has done the work. Qualify any novelty statement to the inspected literature and its coverage.

Judge gap existence separately from gap closure. Closure needs adequate evidence under an explicit scope, an explanation of how it answers the gap and remaining uncertainty. Complete prose, a completed experiment or a checked box does not close a gap. A smaller defensible claim may remain valuable without claiming closure of the whole field's problem.

### Originality and contribution

Compare the proposed contribution directly with the closest prior work. Identify a theoretical, methodological, empirical, system, replication or negative-result contribution as applicable. Explain what knowledge or capability changes and which evidence supports that difference. Changing a tool, language, sample or context alone is not sufficient. A context change can matter when it tests a justified boundary or mechanism. Do not force every contribution to be a new invention. A well-designed replication, confirmation or negative finding can add knowledge. Keep contributions within what was actually tested, observed or proved.

### Research Impact

Ask what becomes possible or better understood if the finding is true. Separate Scientific Impact, Methodological Impact and Practical Impact. Then label each as Expected Impact or Demonstrated Impact. State the users of the knowledge, the application conditions and transfer limits. A functioning prototype, a preference rating or a laboratory improvement is not by itself demonstrated real-world benefit. Do not change a prediction into an achieved impact when polishing prose.

### Research question and method alignment

Trace Research Gap → RQ → Method → Data or argument → Analysis → Findings. Every RQ needs an appropriate evidence path. Map findings back to the question they answer. Examine design, sampling and independent unit, measurement validity, operational definitions, metric rationale and limits, applicable comparators, analysis, confounding factors and alternative explanations. Repeated events from one participant are not automatically independent participants.

Select criteria appropriate to the inquiry. Quantitative work may require an estimand, uncertainty, assumptions and comparable baselines. Qualitative work may require justified sampling, an inspectable interpretive procedure, reflexivity and disconfirming cases. Theoretical work may require definitions, assumptions, proof obligations, counterexamples and comparison with existing results. Historical, conceptual, review and mixed-method work need suitable source or synthesis criteria. Do not require statistical significance, numeric baselines, experiments or a particular qualitative procedure for every study. Explain Not Applicable decisions. Use the existing metric plan rather than inventing a second metric register.

### Evidence to Findings

Label Observed Results, Derived Results, Interpretation, Hypothesis and Unsupported Claim separately. For every principal finding inspect its raw/result/argument locator, derivation where needed, RQ link, population, comparator, uncertainty and exceptions. Check whether the same result admits other explanations. Association cannot become causation without a defensible design and identification argument. Keep negative and contradictory results. Do not equate a nonsignificant test with proof of no effect or a reported preference with demonstrated performance. Recheck claims in the abstract, contribution bullets, captions and conclusion against the same evidence.

### Contribution and limitation decision

Require defensible answers to “What is original about this research?”, “Why does this research matter?” and “What new knowledge does the evidence provide?”. A valid replication can answer through confirmation or boundary evidence. Classify an inadequate answer as conceptual, evidential, methodological or writing-related. Do not repair a scientific defect by polishing its wording. Propose a feasible repair such as narrowing the RQ, inspecting closer literature, recomputing a supported analysis or collecting a missing measure. Show dependencies and limits. Changes to RQs, design, endpoints, analysis or scientific conclusions require researcher approval and a decision record before implementation. Keep such proposals separate from language edits.

## R49 Learn from feedback without inventing universal rules

Record each actual professor/reviewer comment in the existing Decision log. Preserve the comment's source and context. Classify it as Universal Research Principle, Domain-Specific Principle, Project-Specific Correction or Unverified Recommendation. These labels state the proposed scope, not the authority of the speaker.

Check the reasoning, relevant methodological sources, counterexamples and applicability before promoting a comment. A single expert opinion does not automatically establish a universal principle. Keep unresolved disagreements and untested recommendations visible. Do not apply a project-specific preference as a rule for all researchers or research types.

A reusable principle needs a source locator, rationale, scope, exceptions, validation basis, support status, approving researcher/maintainer and the version it supersedes. Reuse a matching existing rule instead of creating a duplicate. Persist only an approved and appropriately de-identified principle in an actual version-controlled project record or a reviewed change to the relevant reference module. Keep confidential feedback and participant material outside a public repository. Record the real file and change reference. A conversation, memory claim or drafted patch is not a saved or published update. Do not commit, push, release or publish without the necessary authorization.

## R50 Reuse records and report decisions

Use the existing Source manifest for inspected versions and locations, Claim ledger for support and counterevidence, `literature-matrix.csv` for closest work, `metric-plan.csv` for measurement choices, `paper-map.csv` for RQ/evidence paths, Decision log for approvals/feedback, and QA report for review issues. Do not copy all source text into new ledgers. Reuse existing IDs. For legacy CSV headers put optional reasoning annotations in the existing structured notes or QA record and cross-reference row IDs. No mandatory CSV migration is required.

Add only fields needed by the review. Useful optional annotations are RQ reference, closest-work reference, claim role, impact domain/basis, support status, limitation locator and approval reference. Do not replace legacy evidence classes or execution states with support states.

| Support status | Meaning within the recorded scope |
| --- | --- |
| Verified | Inspected evidence supports the specific assertion. Record the operation, locator and limits. This is not universal truth or automatic approval. |
| Partially Supported | Some components or conditions are supported. State exactly what remains unresolved. |
| Unverified | Required evidence has not been inspected or is insufficient to judge. |
| Proposed | A planned method, interpretation, benefit or action not yet established. |
| Contradicted | Inspected evidence conflicts with the assertion. Keep the conflicting evidence. |
| Not Applicable | The criterion does not fit this task/type. Give the reason. |

Execution states such as Passed, Failed and Not Run answer a different question. A successful script or complete record cannot promote a claim to Verified. Gap closure has its own scoped evidence decision.

For a Scientific Audit or Research Gap Review use this table. Populate only actual issues. If there are none within a checked area, identify what was inspected and what was not.

| Issue | Evidence | Why It Matters | Recommended Fix | Status | Priority |
| --- | --- | --- | --- | --- | --- |

Evidence must contain a precise locator or an explicit missing-evidence statement. Status uses the support states above for the claim under review, not a claimed repair completion. Priority is Critical, Major or Minor with a stated reason. Critical blocks a central conclusion. Major affects support or reproducibility. Minor is a local reporting defect. These are triage labels, not a validated research-quality scale.

Then summarize Critical Research Problems, Verified Contributions, Unsupported Claims, Missing Evidence, Feasible Gap-Closure Actions and Decisions Requiring Researcher Approval. State none identified or not checked as appropriate. Verified Contributions require inspected support. Do not fabricate a positive entry to fill the report.

### Integration and optional record checking

In audit mode inspect and report without editing source files. In revise mode preserve approved RQs, methods, findings and contribution scope. Check changed meaning locally and separate proposed scientific changes. Do not expand a language-only job into a full audit. In full-paper mode review gap/RQ fit while planning, method/evidence before result claims, and findings/originality/impact at review. Apply Humanizer from the first draft throughout.

When ARS is active, it remains the workflow and state owner. Attach these checks to its existing Research, Planning and Review boundaries using the existing handoff. Preserve confirmations, register IDs and pending issues. Do not spawn another pipeline or assume child agents inherited the guide. This is a prompt-level contract, not a tested enforcement mechanism.

`audit_full_paper.py` optionally checks `reasoning_review` inside an existing schema-1 run record. The extension contains locators and declared assessments only. See the [record field contract](research-reasoning-records.md). Omit it for legacy or language-only work. It checks declared consistency, not literature truth, suitability, causality or genuine approval. Audit/revise jobs can use their existing QA report without creating a full-paper record. Human judgment and actual source inspection remain necessary.

### Sources and applicability

The review procedure and status labels are project requirements, not an externally validated universal instrument. Two inspected background sources inform bounded examples. The AHRQ framework concerns gaps in systematic reviews and distinguishes reasons for inadequate evidence. Its PICOS structure is not imposed on every discipline. The National Academies discussion treats replication in the context of a body of evidence rather than treating one success or failure as conclusive. Neither source validates this skill or its software.

- [AHRQ 2011, structured abstract and stated limits](https://www.ncbi.nlm.nih.gov/sites/books/NBK62478/)
- [National Academies 2019, chapter 5, opening discussion](https://www.ncbi.nlm.nih.gov/books/NBK547524/)
