# ARS and research-specific humanizing

This is a prompt-level interoperability contract, not a runtime hook, automatic plugin merger, or measured end-to-end integration. Read the installed dependencies before using them. Their source versions and inspected paths are pinned in [integrations.json](../provenance/integrations.json). ARS is a separate dependency and is not copied into this package.

## Entry and responsibility

For Claude Code, the inspected ARS command `ars-full` loads `academic-research-skills:academic-pipeline` using the host Skill tool. Its command disables model invocation. Do not invoke the command itself as a Skill or replace the actual pipeline with its short command summary. Discover the exact installed identifier before dispatch. Our user command `/research-humanizer:research-full` loads research-paper-craft first and coordinates the handoff. The original `/academic-research-skills:ars-full` can also be used with an explicit instruction to apply research-paper-craft from the first stage.

When ARS is not installed or a required resource cannot be read, stop ARS execution and identify the missing dependency. Do not silently run a homemade pipeline under the ARS name. Offer an explicitly named standalone full-paper run. Do not install packages, enable hooks, change global memory or send manuscripts to another model without authorization.

For Codex, ARS publishes the separate `Imbad0202/academic-research-skills-codex` distribution with the `academic-research-suite` entry and ars-* aliases. Use its installed router and instructions, not Claude-specific command files, environment assumptions, subagent names or hooks. An account-imported skill, plain chat, desktop plugin and local CLI do not have identical capabilities. Record which tools and controls are actually available. No live host compatibility is claimed by this adapter.

ARS owns research orchestration, stage state, integrity checks, review and confirmation. Research Humanizer supplies the manuscript contract and checks within those stages. Do not open two competing workflows, duplicate ARS registers, write fake checkpoint approvals, or mark unexecuted optional audits as enabled. Full drafting is selected for the WRITE phase. It does not remove ARS user confirmation points. Reviewer simulation is not peer acceptance.

## Carry the contract through every stage

Prepare a private [handoff](../assets/ars-handoff.md) that points to source versions, user decisions, mandatory style, the authoritative Word master or template, permitted output paths, literature and metric decisions, original-asset requests, author context, and unresolved inputs. Resolve its actual path and give it to every delegated writer, visualization agent, reviewer and formatter. Include the relevant module paths and require an acknowledgement of what was loaded. Do not assume a child agent inherits the entire parent conversation or memory. If a host cannot propagate the contract, retain that limitation and review the returned artifact yourself rather than claiming enforcement.

| ARS boundary | Research Humanizer obligation |
| --- | --- |
| Research and intake | Confirm study versions, source access, actual question, venue, privacy and author's style context. Search primary literature and inspect exemplars. |
| Before drafting | Set evidence/metric/figure plans. Ask for missing originals and substantive decisions. Load required writing rules before the first paragraph. |
| Writing and visualization | Draft complete applicable sections. Keep claims, notation and images grounded. Use original captures and reproducible graphs. |
| Integrity and review | Preserve ARS checks and confirmations. Compare changed claims with sources and code. Record missing or unsupported material. |
| Revision and re-review | Recheck every affected number, reference, metric, diagram and summary. Keep valid uncertainty. |
| Final formatting | Preserve Word-first safeguards, inspect saved outputs, verify anonymity and mark pending checks. |
| Process record and delivery | Document actual tools, approvals, sources, searches and limits separately from the manuscript. |

Before delegating, pass the full-paper mode and source contract. After receiving work, check the output against them. A writer's statement that a check passed is not independent evidence. At each stage, preserve ARS's actual confirmation behavior rather than forging a transition to satisfy a request for speed.

## Resolve known conflicts explicitly

ARS supports Markdown, LaTeX and DOCX via Pandoc. For an existing Word master, do not use conversion as a replacement for native editing. Route finalization through the approved Word-first path, or deliver a review draft with a location-specific patch plan. New DOCX creation from an approved template may use an authorized conversion, but it is provisional until native Word review. For LaTeX-only work, inspect the actual compiled output. Do not convert an existing master merely to fit a tool's default output.

Read the target's actual citation requirements. The inspected ARS main includes an interim restriction on automatic corrections outside APA. Its Codex sibling may vendor an earlier revision. Do not claim IEEE/Vancouver correctness from a generic citation check. Review source metadata and the target style directly. Record the actual dependency version rather than inferring it from this adapter.

## Adapting Aboudjem Humanizer for research

[Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) is an inspected design reference, not a required runtime dependency. Its general-purpose rewriting defaults are not enabled by this package. Its source is MIT; a notice is preserved in [aboudjem-humanizer-MIT.txt](../licenses/aboudjem-humanizer-MIT.txt). The original blader Humanizer and its credit remain separate.

| General-purpose direction | Research-specific treatment |
| --- | --- |
| Concrete rather than inflated prose | Supply detail only from actual evidence. Ask when it is missing. |
| Voice and context | Use attributable author-approved context, separate for each researcher. Never invent personality, anecdotes or opinions. |
| Contractions, fragments and punchy prose | No contractions or theatrical fragments in the default manuscript style. Use complete, moderately formal sentences. |
| Aggressive removal of hedging | Preserve justified uncertainty, negative findings, population limits and observational language. |
| Burstiness or perplexity targets | Do not optimize sentence-length variation, rare synonyms or AI-tell score. Meaning and readability govern. |
| Repetition and passive voice | Keep consistent technical terms, needed repetition and appropriate scientific passive constructions. |
| Citation-token and placeholder cleanup | Resolve citations to actual sources. Preserve unresolved markers in working drafts rather than deleting evidence of a gap. |
| Unicode cleanup | Review within language and math context. Never strip Greek letters, Thai marks, nonbreaking units or intentional math symbols globally. |
| Generic conclusion and interchangeable paragraphs | Give each paragraph a role in the study's argument. End with a supported conclusion and scope, not promotional certainty. |

If the generic humanizer is also installed, do not run an unrestricted final rewrite after research verification. Treat its suggestions as candidates, reapply the research contract, and recheck affected claims. A 0–100 style score is not a probability of human authorship, a scientific quality grade or a reason to change evidence.

## Licensing and evidence boundary

ARS is licensed CC BY-NC 4.0 by its author. Install it separately and follow its terms. Our MIT license does not relicense ARS or remove its noncommercial condition. No ARS workflow source, scripts or figures are vendored here. The integration describes interfaces and adds independently written research requirements. No endorsement by either upstream author is implied.

Local contract tests validate files and records, not a live ARS run. To evaluate integration, use an authorized host, record both plugin versions, confirm resource loading, run a shareable full-paper fixture with actual tools, preserve checkpoint transcripts and inspect all produced artifacts. Test missing data, unavailable sources, conflicting code, broken math, absent Word and missing real photographs. Never fill an evaluation log with an ideal response and call it an observed result.
