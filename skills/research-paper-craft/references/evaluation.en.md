# Evaluation and reproducibility

Read only for the current task phase. The core rules in SKILL.md remain active.

For a scientific audit or substantive research decision, load [research reasoning](research-reasoning.en.md). Reuse the records below. Language-only edits do not require the full review.

## R14 Design and report a fair evaluation

Derive the evaluation from the research questions and claims. For each experiment, identify what it tests, the experimental unit, data source, comparison, metric, operating conditions, and evidence that would contradict the claim.

Separate training, validation, and test roles when applicable. Check for overlap through participants, subjects, sessions, sites, devices, near-duplicate samples, time, and preprocessing. Fit data-dependent transformations only on the appropriate training portion. Do not tune a decision using test labels and describe the test as untouched.

Report inclusion and exclusion rules, missing-data handling, sample counts, split construction, hyperparameter selection, stochastic seeds, and stopping rules as applicable. Do not impose a universal number of runs or samples. Use a justified design and report what was actually performed.

Compare baselines under compatible conditions. Identify differences in datasets, splits, preprocessing, information available at inference, tuning budget, compute, or hardware. Distinguish reproduced baselines from published numbers and non-comparable contextual results. A table does not make unlike measurements comparable.

Use ablations to test the claimed role of components. Identify what changes and what remains fixed. Include sensitivity analysis, stress tests, failure cases, or external validation only when they answer a relevant question and are available. A missing ablation cannot be replaced by a fabricated row or a rhetorical assertion.

For latency or efficiency, specify the measured operation, workload, hardware, batch size, warm-up, synchronization, repetitions, and summary statistic where relevant. Separate training cost, inference cost, throughput, and end-to-end latency. Do not claim real-time suitability without the relevant operational deadline and measurement conditions.

## R15 Match statistics to the data and claim

Define metrics and their direction. State the unit of analysis and aggregation rule. Distinguish pooled metrics, averages of per-unit metrics, micro averages, macro averages, and weighted averages. Include the denominator and class or group composition when needed for interpretation.

Distinguish variation across observations, participants, random seeds, data splits, and repeated measurements. Do not count dependent measurements as independent experiments. Pair comparisons when the design is paired. Account for relevant clustering or repeated measures in the analysis rather than adding an unexplained error bar.

State whether uncertainty represents a standard deviation, standard error, confidence interval, prediction interval, credible interval, range, or another quantity. Give the calculation method, level where relevant, and assumptions. A single observed run does not justify inventing between-run variation.

Use a statistical test only when it answers a defined question and its assumptions are defensible. Report the comparison, test, sidedness, effect size and uncertainty where appropriate, and multiplicity treatment when needed. Distinguish a prespecified analysis from an exploratory one. Do not search among analyses solely to obtain a favorable threshold crossing.

Do not equate a small p-value with a large or useful effect. Do not equate an absence of statistical significance with proof of equivalence. Do not infer causation from an observational association alone. Use an equivalence or non-inferiority claim only with an appropriate design and justified margin.

Preserve null results, adverse results, and limitations that affect the conclusion. For qualitative work, use an appropriate account of sampling, coding, interpretation, and disconfirming cases rather than forcing numerical significance tests onto the study.

## R23 Preserve reproducibility and execution truth

Keep the analysis and plotting procedure, dependencies, environment, code revision, configuration, seeds when relevant, and commands needed to regenerate reported outputs. Document access constraints for restricted data instead of claiming public availability.

Keep raw data immutable. Write derived artifacts separately and record transformations. Use stable identifiers and content hashes when available. Link the manuscript snapshot to the result and figure snapshot used for that version.

Validate calculations with appropriate checks, such as counts, sums, units, boundary cases, invariants, a small independently computed example, or a comparison with an approved implementation. A checksum proves file identity, not scientific correctness.

Distinguish inspected code, executed code, a successful run, reproduced results, and independent replication. Report execution failures and resource limits. Do not write that tests passed, figures were regenerated, or results were reproduced unless the corresponding execution evidence exists.

If a task requires tools that are unavailable, deliver the supported source, procedure, or draft and identify the unperformed operation. A text prompt for an image is not a completed image. Plot code is not an executed plot. An exported PDF is not proof of Word pagination.
