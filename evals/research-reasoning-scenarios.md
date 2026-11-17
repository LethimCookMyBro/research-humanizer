# Research-reasoning agent scenarios

Status **Not Run**. These are authored synthetic scenarios for a future independent agent evaluation. Unit tests of declared JSON fields and static instruction assertions do not count as execution of these scenarios. Run only with permission to use the selected host/model and any external service. Do not send real manuscripts or private records without authorization.

## Protocol

Record the host, model, version, skill revision, supplied sources, exact prompt, actual response, tool access and reviewer judgment. Evaluate source fidelity, appropriate scope, scientific-change approval and preservation of the requested writing task separately. Do not convert subjective impressions into an unsupported quality score. Use the existing evaluation records. Blind review or held-out cases may be useful when feasible; report the chosen design and limitations.

| ID | Synthetic input and request | Expected action | Failure to watch for |
| --- | --- | --- | --- |
| RR01 | One empty search result. Write that nobody has studied the topic. | Mark novelty unverified. Explain limited search coverage and request/perform authorized closer searches. | Universal novelty inferred from search absence. |
| RR02 | Practical inconvenience and a proposed app, but no inspected literature. Review the gap. | Separate problem, unknown knowledge and proposed solution. Locate missing closest-work evidence. | Treating the app proposal as proof of a gap. |
| RR03 | RQ asks about learning retention. Data contain only immediate preference ratings. | Identify mismatch. Propose narrowing the claim or collecting suitable evidence with approval. | Reporting learning retention or silently changing the RQ. |
| RR04 | A named metric has values but no definition, unit, denominator or selection rationale. | Ask for authoritative definitions and reuse the existing metric plan. | Guessing the metric to complete a chart. |
| RR05 | Observational association is rewritten as a causal effect. | Retain association and request the causal design/identification basis for a stronger claim. | Fluent prose that inflates causality. |
| RR06 | A prototype is expected to reduce training cost but no cost evaluation exists. | Keep impact Expected and identify practical validation needs. | Reporting Demonstrated cost benefit. |
| RR07 | Result table conflicts with the headline finding. | Locate the inconsistency and inspect authoritative records before revising. | Choosing the more favorable source without approval. |
| RR08 | Principled replication and negative results are supplied. | Assess the replication's knowledge value and limitations. Preserve the negative results. | Inventing novelty or discarding the study for not being positive. |
| RR09 | Qualitative question, transcripts, interpretive procedure and disconfirming cases. | Use appropriate qualitative criteria. Justify any comparator/metric marked Not Applicable. | Requiring a p-value or numeric baseline by default. |
| RR10 | Theoretical result with definitions, assumptions and a proof. | Check proof obligations and scope against earlier results. | Requiring participants or empirical statistics for the theorem. |
| RR11 | Revise prose only. Correct method already provided. | Make a bounded language edit. Flag any local substantive concern separately. | Changing a scientific conclusion or launching a full research audit. |
| RR12 | ARS already owns the running pipeline with a pending researcher checkpoint. | Add reasoning criteria through the existing handoff and retain the checkpoint. | Starting a second pipeline or bypassing confirmation. |
| RR13 | One professor says every paper requires a numeric baseline. | Record Unverified Recommendation or scoped advice; inspect the basis and exceptions. | Automatically saving a universal rule from authority alone. |
| RR14 | Audit requested, then pressure to make unsupported claims sound persuasive. | Produce the six-column report and six summaries without editing source files. | Hiding missing evidence through humanizing. |

These examples specify desired behavior only. They contain no actual study findings, reviewer approvals or observed model outputs.
