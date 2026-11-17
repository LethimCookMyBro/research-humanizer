# Punctuation with a scientific purpose

Load with the writing guide before drafting or revising manuscript prose. Also review captions, graph annotations, table notes and overview labels. The existing house-style bans remain. These are project writing rules, not an authorship test.

## R47 Review punctuation by function

Prefer one main scientific point per sentence. A sentence that mixes a procedure, a finding and its interpretation usually needs restructuring. Draft that structure first. Do not wait until the final pass to remove commas. Keep the condition and uncertainty attached to the claim they qualify.

Do not remove every comma. Keep grammar-required commas and genuine lists. A restrictive clause can change meaning when commas are inserted or removed. Do not replace all commas with and. Do not substitute semicolons, colons, dashes or explanatory parentheses to retain the same overloaded sentence. Those substitutions do not solve the structural problem and may violate the house style.

### Decide what the mark is doing

| Mark or pattern | Review in prose | Preserve when meaningful |
| --- | --- | --- |
| Commas | Chains of clauses, stacked asides and long lists with several scientific roles | Necessary grammar, real list items, source citations and numeric separators |
| Hyphens and dashes | Spaced hyphens used as pauses or punctuation-heavy labels | Lexical compounds, identifiers, negative values such as -0.5, subtraction and required technical ranges |
| Equals, plus and ampersands | Shorthand that replaces an unexplained verbal relationship | Equations such as n = 6, defined notation and exact names |
| Arrows | Implied causality or unsupported transitions in body text | Defined system flows and actual mathematical relations with source support |
| Slashes | Ambiguous alternatives such as and/or or guidance/feedback | Units, ratios, paths, URLs and fixed technical labels |
| Periods | Repeated dots, dramatic single-word fragments or inconsistent sentence endings | Complete sentences, decimals, versions, file extensions and abbreviations such as e.g. |
| Parentheses and brackets | Repeated or nested explanatory asides | Citations, equation references, necessary acronym definitions and mathematical grouping |
| Ellipses and repeated emphasis | Vague omission, trailing suspense and !! or ?? | Quoted omissions, mathematical sequences and exact source strings |
| Separators and markup | Decorative horizontal lines, repeated bold or symbols that replace an explanation | Actual Markdown structure, source syntax and required template elements |

Use complete sentences in body prose. A label in a graph or overview can be a short noun phrase. Do not turn every label into a full sentence. Conversely, do not reduce body prose to disconnected labels. A period ends a sentence; it is not a character to eliminate. Preserve simultaneous actions, temporal order, negation, comparator, population, units and citation attachment when splitting a sentence. Do not add a temporal or causal link just to make the prose flow.

For Thai prose, do not insert English-style commas or periods mechanically. Use natural Thai phrase boundaries and paragraphs. Keep Thai letters and combining marks intact. Do not normalize scientific Unicode or strip invisible characters throughout a Word file. Inspect a suspected encoding problem against its source first.

### Review loop

Read a whole paragraph. Mark its claims and their qualifying conditions. Rewrite only where a punctuation-heavy construction makes the relationship hard to follow. Compare the new sentences against those claims and sources. Read aloud once for completeness and continuity. Stop when the identified problem is resolved. Good text may stay unchanged.

Perform this check after each drafted or revised section and again on the assembled manuscript. Apply it to ARS writer, reviewer and formatter handoffs. It does not replace Word-first review or authorize changing a scientific formula. A missing original still requires the researcher.

### Example with no result invented

Synthetic source note. The system records actions and reference use. It stores workpiece states and exports a session log. No ordering or performance finding is supplied.

Before

> The system records actions, tracks reference use, stores workpiece states, and exports the session log.

One acceptable revision

> The system records actions and reference use. It also stores workpiece states and exports the session log.

Preserve the four operations. Do not add “then” because their order was not provided. Do not turn “Feedback = successful learning” into a factual causal sentence unless the source supports that relationship. Flag the unsupported assertion instead.

### Read-only checker and its limits

The existing `lint_manuscript.py` now returns selected punctuation review candidates. `COMMA_DENSITY_REVIEW` triggers at 3 or more prose commas in an approximate sentence. A threshold crossing is not a grammatical error and is not a quota. Four items can be necessary. Numeric punctuation such as 1,000 is excluded when recognized. Soft-wrapped lines in one paragraph are joined for sentence review.

Other candidates cover clause-linking words, spaced hyphens, symbolic shorthand, slash alternatives, repeated marks, ellipses, nested asides and selected period-separated single words. An and-chain is reviewed when it contains at least four occurrences of “and” and at least 30 English-style word tokens. These are conservative triage rules, not a grammar parser or a measured model-quality metric.

The checker protects supported code, math, reference sections, common numeric and citation forms, double-quoted passages and selected technical syntax. It does not understand every quotation, field-specific name, citation style, Markdown form or language. Thai sentence segmentation and rendered Word typography are not checked. Consult `not_checked` in the JSON report. Review an unfamiliar technical expression manually rather than changing it to satisfy a flag.

New heuristic findings have severity `review`. Existing explicit house-style violations retain `required_fix`. `--fail-on-findings` also exits nonzero for review candidates. `--fail-on-errors` keeps its existing required-fix-only behavior. An exit of zero is not editorial approval. Inspect reported candidates and document either the revision or the reason for retaining the expression before marking the prose review complete. The tool makes no automatic edits and assigns no AI score.

### Sources and scope

Reviewed on 17 November 2026. These sources describe punctuation roles and editorial practice. The thresholds and restrictions above are this project's choices, not validated detection criteria or endorsement by the sources.

- [Microsoft punctuation guidance](https://learn.microsoft.com/en-us/style-guide/punctuation/)
- [Purdue OWL comma rules](https://owl.purdue.edu/owl/general_writing/punctuation/commas/index.html)
- [Microsoft dashes, hyphens and minus signs](https://learn.microsoft.com/en-us/style-guide/punctuation/dashes-hyphens)

### Text integrity in 2.3.2

Review missing spaces after periods even when the next English word begins in lowercase. Check repeated fullwidth or small full stops as well as ASCII dots. An isolated fullwidth stop in Latin prose merits review. Japanese sentence-ending punctuation is not an error by itself. The checker recognizes common addresses, file extensions and function calls. Other unmarked dotted identifiers can still need manual classification.

Review selected short phrase chains such as “Very fast. Very clear. Highly effective.” and “Low cost. High accuracy. Rapid feedback.” Do not combine correct short sentences merely because they are short. Figure labels and exact quotations may deliberately use fragments. This is a finite pattern check rather than a complete English or Thai grammar analysis.

Check quotation balance before changing punctuation inside a quotation. The checker recognizes straight double quotes, English curly double quotes, guillemets and Japanese corner brackets. It can protect a complete quotation across soft-wrapped lines within one paragraph. It does not pair across blank paragraphs or omitted code/reference regions. Unmatched marks trigger QUOTE_BALANCE_REVIEW and do not hide the remaining manuscript. Single-quote conventions, primes and unusual nested quotations still require manual review. Never invent the missing quoted words or silently move quotation boundaries.

Inspect U+FFFD and U+FFFC against the original source. They may reflect replacement or embedded-object export issues, but a deliberately quoted character is also possible. Inspect literal U+25A1 squares in prose without guessing what they should be. A square stored in the text differs from a missing-font box shown only by a renderer. Mathematical proof symbols, checkboxes and exact quoted text may be intentional. The text checker cannot inspect rendered glyph appearance. Use native Word and the actual fonts for that check.

Review zero-width characters, soft hyphens or word joiners inserted between Latin letters or digits. Report the code point and source position. Do not remove all invisible characters. U+200B can provide Thai word-break opportunities. Joining characters can be necessary in other scripts and emoji. Nonbreaking spaces may deliberately keep a number and unit together. Direction controls and internal byte-order marks are review findings rather than blanket errors. Never apply global Unicode normalization to scientific text or a Word file.

Source-character diagnostics can appear inside code, quotations or reference sections. Their purpose is to expose possible source corruption or directional controls, not authorize rewriting protected content. Report excerpts escape invisible controls for inspection. The original input remains unchanged. New diagnostic severities are review. Invalid UTF-8 input and the previously supported incomplete-parse cases still cannot count as passes.

After a contextual repair, compare numbers, units, formulae, scope, quotations and citation attachment against the original. Re-run the checker on the saved manuscript and inspect final pages. Resolving a warning means recording either the correction or the reason for keeping a legitimate expression. A clean report is not proof of grammar, human authorship or scientific correctness.

Unicode background is documented by the [Unicode character and format-control specification](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-23/) and the [unsupported-character FAQ](https://www.unicode.org/faq/unsup_char.html). These sources do not validate this project's heuristic detectors.
