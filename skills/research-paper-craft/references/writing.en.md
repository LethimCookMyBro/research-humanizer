# Research prose and translation

Read only for the current task phase. The core rules in SKILL.md remain active.

## R07 Apply the house style to manuscript prose

Use moderately formal language that a researcher could read aloud in a lecture. Prefer familiar words and direct verbs. Introduce a technical term only when it improves precision. Keep indispensable terminology stable instead of cycling through synonyms.

Prefer short, complete sentences with one main claim. Split sentences that combine a mechanism, a result, and an interpretation. Use commas when grammar requires them, but avoid chains of loosely attached clauses. Vary sentence length naturally. Do not impose an identical sentence length or paragraph size throughout the paper.

Do not use semicolons or colons in ordinary manuscript prose. The literal label `Keywords:` and reference entries are permitted. Do not use em dashes, en dashes, or spaced double hyphens as prose separators. Express prose ranges with words such as `to`. Preserve ordinary lexical hyphens, negative signs, and mathematical operators where they belong.

Avoid explanatory parentheses inserted mid-sentence. Move the explanation into a separate sentence. Required citations, equation references, genuine mathematical grouping, and an unavoidable acronym definition are not decorative asides. Introduce an abbreviation in prose when that reads better.

Do not use English contractions. Write `is not`, `does not`, `cannot`, `we have`, and `it is`. Do not remove possessive apostrophes. Preserve exact quotations, publication titles, proper identifiers, and source metadata when changing them would falsify the source. Rephrase the surrounding manuscript or choose a faithful paraphrase instead.

Use Greek letters and symbols such as `°`, `±`, and `≤` only inside mathematical notation, numeric expressions, tables, or numeric plot labels. Inline mathematics counts as mathematics. Use the quantity's name in ordinary prose. Define the symbol at first mathematical use and keep its meaning consistent.

Separate paragraphs by purpose. Substantive sections should normally have several readable paragraphs. Do not pad a short section merely to force multiple paragraphs. Do not leave headings stranded above a page break. Keep contributions as short bullets with no numerical performance results. Use headings and bold only when they help navigation or meaning.

The prose rules do not rewrite code, YAML, LaTeX commands, equations, URLs, identifiers, bibliographic records, or exact quoted source material. The rules also cover prose in titles, captions, table notes, and figure annotations. Technical syntax is protected, not a loophole for hiding ordinary prose in code formatting.

## R08 Remove empty writing without damaging science

Rewrite at paragraph level when a passage has no clear point. Do not merely swap fashionable words for synonyms. Keep each sentence that contributes a fact, a definition, a justified inference, a necessary transition, or a consequential limitation.

| Pattern to inspect | Research-specific correction |
| --- | --- |
| Artificial contrast | State the finding directly. Retain genuine comparisons |
| Dramatic closing line | Keep only a new consequence or finding |
| Philosophical-sounding filler | Name the actual technical question |
| Staged opening | Start with the problem, condition, or result |
| Imaginary objection | Address only a relevant alternative or documented concern |
| Forced groups of three | Keep the real number of distinct ideas |
| Repeated sentence starts | Vary syntax without obscuring actors |
| Excessive separators | Rebuild complete sentences |
| Stacked uncertainty words | Use the exact qualifier the evidence requires |
| Mechanical hyphenation | Follow grammar and technical naming |
| Unclear passive voice | Identify the actor when it matters |
| Inflated vocabulary | Use precise ordinary wording |
| Unsupported significance | Name an evidenced consequence |
| Vague relationship | Specify the relationship only when known |
| Decorative participial ending | Delete the interpretation it adds without evidence |
| Promotional language | State the capability and tested conditions |
| Unnamed authority | Cite the actual source or remove the claim |
| Inflated verb phrase | Use a direct verb when meaning is unchanged |
| Repetitive bold labels | Use ordinary prose or a meaningful table |
| Decorative headings | Name the section's content |
| Inconsistent quotation marks | Follow the manuscript's convention |
| Chatbot greeting or offer | Remove it from the manuscript |
| Knowledge disclaimer followed by a guess | State the actual source gap |
| Opening sentence repeats the heading | Begin with substantive content |
| Narration of the editing process | Move it to the change log |
| Redundant background | Keep only what this paper's reader needs |

These are editorial heuristics, not evidence of AI authorship. Do not ban a scientific term because it sometimes appears in generic writing. Preserve `association` for observational findings, `robust` for an operationally defined robustness result, and `significant` for an appropriately supported statistical claim. Do not strengthen an association into causation to make the sentence more direct.

Preserve deliberate repetition needed for definitions, comparisons, and reader orientation. Preserve valid uncertainty, negative findings, exceptions, and distinctions between correlation, mechanism, prediction, and causation. When an original statement is false or unsupported, flag and correct it with evidence or remove it with a recorded reason. Fidelity does not require preserving a known error.

## R09 Keep Thai and English technically equivalent

Maintain a terminology sheet containing the preferred Thai term, preferred English term, abbreviation, definition, and prohibited ambiguous alternatives. Use natural Thai rather than English sentence structure with Thai words. Use direct academic English rather than a literal translation of Thai connectors.

Before translating, identify the controlling manuscript version. Keep numbers, units, equation numbering, citations, figure references, negation, comparison direction, uncertainty, and claim scope aligned. A translation must not convert `may` into a certainty, an association into a cause, or a tested subset into a universal result.

Explain unavoidable technical terms briefly at first use. Do not repeat English in parentheses after every Thai term. Use the same names for modules and metrics across text, equations, code mappings, and figures.

For parallel manuscripts, keep a section correspondence record. Update both versions after a scientific revision. Treat an unresolved mismatch as a verification issue rather than choosing whichever sentence sounds smoother.

## R30 Apply the rules through realistic examples

The examples below illustrate wording and decision rules. They are not findings about the user's project. Use a sentence only when the project's evidence supports its content.

| Weak or overstated wording | More defensible wording |
| --- | --- |
| The proposed framework revolutionizes real-world performance | The method combines the preprocessing and estimation stages in a single pipeline |
| The results clearly prove that the system is robust | The system was evaluated under the stated noise conditions |
| The method is not only accurate but also efficient | Report accuracy and computational cost separately with their actual evidence |
| The association demonstrates that the intervention causes improvement | The analysis found an association. The design does not establish causation |
| Extensive experiments validate the universal applicability of the method | State the experiments actually performed and restrict the conclusion to those settings |

When a table and a result export disagree, show the conflict in the working report and trace the computation. Do not silently choose a value. When code contains an untested new module, describe it as proposed or omit it from the evaluated pipeline. When raw measurements are missing, a finished-looking result plot is not an acceptable substitute.

When there is no current-best literature search, name the methods actually compared instead of asserting state of the art. When an uncertainty measure has not been calculated, do not add a shaded band for appearance. When Word was not opened, report Word layout as not checked.
