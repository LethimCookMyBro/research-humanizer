# Methods and mathematics

Read only for the current task phase. The core rules in SKILL.md remain active.

## R12 Describe the method that exists

Define the task, inputs, outputs, assumptions, system boundary, and operating conditions. Separate the proposed design from the implemented and evaluated version. State material differences between them.

Describe each necessary component by its input, operation, output, and purpose. Explain design choices with evidence or an explicit rationale. Avoid calling a routine block intelligent, adaptive, optimized, or robust without defining the relevant behavior.

Specify preprocessing, calibration, initialization, state updates, stopping rules, failure handling, and postprocessing when they affect reproducibility. For geometric or physical systems, define coordinate frames, reference directions, units, synchronization, and calibration conventions. For computational models, define architecture, objectives, optimization details, and inference behavior as relevant.

Keep a method-to-code map when implementation is available. Link manuscript modules and equations to functions, configuration fields, and relevant tests. Document mismatches. Do not edit the described method to fit a desired result or silently change scientific code during a prose task.

Use pseudocode only when it makes a procedure clearer. Define inputs, outputs, initialization, loops, conditions, and termination. It must agree with both the mathematics and implementation. Do not invent a complexity bound or claim the pseudocode has been executed.

## R13 Make mathematics necessary and checkable

Introduce equations only when they define the problem, method, objective, estimator, constraint, metric, or argument. Explain their scientific role. Decorative equations do not improve rigor.

For every symbol, define its meaning, domain, units where relevant, shape or dimensionality, indexing convention, and whether it is a scalar, vector, matrix, set, or random variable. Distinguish observed values, model parameters, estimates, and latent quantities. Do not reuse a symbol for unrelated meanings.

Check that additions have compatible units, matrix products have compatible shapes, probabilities meet their stated domain, logarithms have valid arguments, denominators are handled, and boundary cases are defined. State the convention for angles, normalization, missing values, ties, empty sets, and zero denominators when the method needs it.

Keep the derivation consistent with the implemented computation. Track sums versus means, loss weights, sign conventions, normalization constants, and reduction axes. A correct-looking equation that describes different code is a substantive error.

Separate definitions, assumptions, derived identities, hypotheses, and theorems. Give a theorem its conditions and a complete argument appropriate to the claim. Numerical checks can expose errors but do not establish a general proof. Do not present an intuitive explanation as a proof or a borrowed derivation as a new result.

Use editable mathematical source such as LaTeX or Word equations. Number equations that are referenced. Explain non-obvious steps and cite external derivations. Preserve the mathematical source with the delivered figure or manuscript assets. Record symbolic or numerical checks as performed checks only when they were actually run.
