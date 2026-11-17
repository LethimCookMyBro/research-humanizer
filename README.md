<div align="center">

# Research Humanizer

**Clear research writing. Traceable claims. Real evidence.**

[![Version](https://img.shields.io/badge/version-2.3.3-2563eb?style=flat-square)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-0f766e?style=flat-square)](LICENSE)
[![Languages](https://img.shields.io/badge/guides-English%20%2B%20Thai-475569?style=flat-square)](skills/research-paper-craft/SKILL.md)
[![Status](https://img.shields.io/badge/status-preview-b45309?style=flat-square)](docs/KNOWN_ISSUES.md)

<a href="README.md">English</a> · <a href="README%28TH%29.md">ภาษาไทย</a>

[Install](#install) · [Use](#use) · [Scope](#scope) · [Validation](#validation)


**[Project website](https://research-humanizer.vercel.app/)** · [Release v2.3.2](https://github.com/LethimCookMyBro/research-humanizer/releases/tag/v2.3.2)

</div>

**2.3.3 Preview.** It adds scoped research-gap, originality, impact and RQ/evidence review to the existing skill. Language-only humanizing stays lightweight. [Upgrade notes](docs/releases/v2.3.3.md) · [Architecture audit](docs/plans/v2.3.3-architecture-audit.md). Refresh the marketplace and update the plugin to load this version. [Release and downloads](https://github.com/LethimCookMyBro/research-humanizer/releases/tag/v2.3.3).

**2.3.2** closes the seven retained punctuation-probe misses and adds contextual quotation and Unicode checks. It preserves scientific notation and never rewrites inputs automatically. [Patch notes](docs/releases/v2.3.2.md) · [Executed checks](docs/VERIFICATION.md).



Research Humanizer is an academic writing skill and full-paper research companion for Claude Code and Codex. Pair it with ARS `ars-full` to apply research-specific humanizing from the first draft through literature, metrics, figures and final document checks. Use it for different researchers and fields, with private author context when available. Revision and read-only audit modes remain available.

> [!IMPORTANT]
> Missing originals? Ask the researcher. A plausible sentence, a synthetic lab image or an attractive curve is not evidence.

**2.3.0** adds full-paper mode, an ARS coordinator, mandatory literature/venue reconnaissance, metric-to-data planning and scoped author context. Existing humanizing, graph, equation, evidence and Word safeguards remain. [Integration and limits](docs/INTEGRATION.md) · [2.3.0 release notes](docs/releases/v2.3.0.md).

**2.3.1 punctuation patch** reviews comma-heavy sentences and symbolic shorthand without deleting scientific notation. New findings are advisory. [Punctuation guide](skills/research-paper-craft/references/punctuation.en.md) · [Release notes](docs/releases/v2.3.1.md)

<a id="install"></a>
## Install

### Claude Code

Run inside Claude Code, one line at a time.

```text
/plugin marketplace add LethimCookMyBro/research-humanizer
/plugin install research-humanizer@research-humanizer
```

Then invoke the skill in the requested mode.

```text
/research-humanizer:research-paper-craft Draft a full paper from these materials. Apply the research style from the first paragraph and ask for missing evidence.
```

### Codex CLI

Run in your terminal, not the chat.

```bash
codex plugin marketplace add LethimCookMyBro/research-humanizer
codex plugin add research-humanizer@research-humanizer
```

Start a new session and use `/plugins` to check installation. Select `research-paper-craft` with `$` or ask Codex to use it. The plugin is named `research-humanizer`; its bundled skill is `research-paper-craft`. A compatible host with plugin support and Git is required. Python 3.10+ is optional for local checks. No hooks or MCP servers are added.

<details>
<summary><strong>Update, migration and standalone installation</strong></summary>

Claude Code terminal update.

```bash
claude plugin marketplace update research-humanizer
claude plugin update research-humanizer@research-humanizer
claude plugin list
```

Codex marketplace refresh.

```bash
codex plugin marketplace upgrade research-humanizer
```

Check the installed version in `/plugins`. Restart the host session. A refreshed catalog, a GitHub push or a GitHub Release does not prove the installed cache changed. Releases identify downloadable revisions; plugin updates still depend on their configured source and version. If a desktop app still shows an older version, check that its installation and the CLI use the same account/configuration. Back up local customizations before reinstalling. Do not delete the entire host configuration directory.

For a standalone installation, copy the complete `skills/research-paper-craft` folder into `~/.claude/skills/` or `~/.agents/skills/`, or the corresponding project directory. Do not enable both standalone and plugin copies. Keep references, scripts and license notices together.

</details>

Commands follow the [Claude plugin guide](https://code.claude.com/docs/en/discover-plugins) and [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference). Live host installation remains unverified in the development environment.

<a id="use"></a>
## Use

```text
Use research-paper-craft on the files in this project.
Use full-paper mode. Draft every applicable section, not only an outline.
Inspect the actual study and search related papers, official venue instructions and metric definitions.
Use accessible author-approved context without inventing memory.
Apply the research style from the first draft and preserve accepted terminology.
Compare changed claims with their sources, including scope and uncertainty.
Use real originals for evidence images and verified data for graphs.
Map overview components and arrows to the actual method.
Ask me for missing study inputs. Do not substitute them.
Keep the original Word document and edit a copy.
Separate the manuscript from the verification report.
```

### Full paper with ARS

Install ARS separately in Claude Code. Its own license is **CC BY-NC 4.0**. Our MIT license does not relicense that dependency. This package does not copy or install ARS for you.

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

After both plugins are loaded, invoke the new coordinator in Claude Code.

```text
/research-humanizer:research-full Draft a full paper from this project's actual materials with ARS. Apply research-paper-craft from the first draft. Search primary papers, official venue requirements and metric definitions. Ask for missing originals and preserve ARS confirmation points.
```

The existing `ars-full` entry can be used too.

```text
/academic-research-skills:ars-full Draft the complete applicable manuscript. Load research-humanizer:research-paper-craft first and carry its full-paper, literature, style, real-image and Word-first contract to every writer, reviewer and formatter.
```

The coordinator loads the actual installed ARS pipeline, not a copy of it. Missing ARS stops the ARS route. It is a **prompt-level adapter**, not an enforcement hook, and it preserves ARS's researcher confirmations. It does not submit a paper or fabricate a finished experiment from a topic.

For Codex, install the upstream [ARS-Codex distribution](https://github.com/Imbad0202/academic-research-skills-codex) and select its installed `academic-research-suite` skill alongside `research-paper-craft`. Ask for ARS full-paper orchestration and our contract in the same request. Claude slash commands and hooks do not transfer automatically. See the [integration guide](skills/research-paper-craft/references/ars-integration.en.md) for the exact source versions, permissions and known conflicts.

<details>
<summary><strong>Without ARS or when revising only</strong></summary>

Use `research-paper-craft` with an explicit `full-paper` request for the standalone procedure. This must not be reported as an ARS run. Select `revise` for existing text and `audit` for a read-only report. Existing Word masters still require the Word-first path.

</details>

### What a useful edit looks like

*An authored teaching example, not a model benchmark.* The supplied note states only that the method combines sensor readings. No evaluation results are supplied.

| Draft | Source-bounded revision |
| --- | --- |
| Our groundbreaking framework seamlessly integrates sensor measurements and demonstrates robust real-world performance. | The method combines sensor readings. |

The performance claim is flagged as unsupported, not silently treated as true. A clear sentence such as “The logger records each action and the corresponding workpiece state” can stay unchanged.

<a id="scope"></a>
## Scope

| Area | Contract |
| --- | --- |
| Humanizing | Source-bound prose from the first draft, private author context, minimal changes during revision |
| Scientific meaning | Trace sources, compare before/after claims, preserve negation, scope and citation attachment |
| Whole papers | Draft all applicable sections with ARS or standalone. Link questions, literature, metrics, results and limitations |
| Mathematics | Editable equations, defined symbols and units, implementation mapping |
| Graphs | Reproducible plot data, independent units, calculated uncertainty and final-size review |
| Real images | Matching originals, capture context, consent and disclosed processing |
| Overview / infographic | Evidence-linked nodes and arrows, readable hierarchy, no decorative invented components |
| Word and submission | Preserve DOCX structure, inspect native Word pagination and every final page, audit anonymity |

Guidance is task-loaded in one language. An ordinary paragraph edit does not load all guides. Start with [SKILL.md](skills/research-paper-craft/SKILL.md), [writing](skills/research-paper-craft/references/writing.en.md), [visuals](skills/research-paper-craft/references/visuals.en.md) or [Word layout](skills/research-paper-craft/references/word-layout.en.md). Optional record templates are in [assets](skills/research-paper-craft/assets).

<a id="validation"></a>
## Validation and limits

Version 2.3.0 local checks pass **50 repository + 134 skill + 5 historical regression tests**. These are software and instruction contracts, not a model-quality benchmark.

The 2.3.0 tests add full-paper and ARS instruction contracts plus synthetic record checks. These do not establish live ARS integration or whole-paper quality. The five historical text-checker regressions remain fixed. New tests cover revision signals, figure contracts, malformed inputs and path confinement. Full commands, counts and evidence are in [VERIFICATION.md](docs/VERIFICATION.md). Independent model quality, native Word repair and live host installation remain **not established**. The [24-case evaluation bank](evals/README.md) contains synthetic fixtures, not fabricated benchmark results.

| Tool | What it does not certify |
| --- | --- |
| Full-paper record audit | Whether sources were actually read, the study is valid, or the paper is ready |
| Text checker | Scientific truth, every syntax form, or AI authorship |
| Revision reviewer | Semantic equivalence or correct citation attachment |
| Figure audit | Photo authenticity, permissions, statistical recomputation or rendered quality |
| DOCX preflight | Native Word pagination or visual layout |

The bundled Python audits are local and do not modify research inputs. Host-led literature searches use the authorized network tools. [Tool usage and schemas](docs/QUALITY.md). A no-flags report is not submission approval. Follow the venue's AI-disclosure policy. This project does not promise detector evasion, paper acceptance or a particular number of stars.

## Contribute

[CONTRIBUTING.md](CONTRIBUTING.md) · [Known limits](docs/KNOWN_ISSUES.md) · [Changelog](CHANGELOG.md) · [Publishing](docs/PUBLISHING.md) · [Website and search setup](docs/DISCOVERY.md)

Useful contributions are reproducible edge cases, source-bounded bilingual examples and recorded host/model trials. Never submit private manuscripts, participant data or credentials without authorization.

## License and attribution

[MIT](LICENSE). The original Humanizer by [Siqi Chen](https://github.com/blader/humanizer) is retained with its [MIT notice](licenses/humanizer-MIT.txt) and [provenance](THIRD_PARTY_NOTICES.md). This is an independent project, not an endorsement by the providers of Claude Code or Codex.


ARS is separately installed under CC BY-NC 4.0. The inspected Aboudjem Humanizer informs a research-specific compatibility policy, not a bundled AI detector or an unrestricted rewrite pass. Its [MIT notice](skills/research-paper-craft/licenses/aboudjem-humanizer-MIT.txt) and [source record](skills/research-paper-craft/provenance/integrations.json) are retained.

## Research reasoning review

Use the same `research-paper-craft` skill. Request a Scientific Audit or Research Gap Review to inspect gap evidence, originality, impact, RQ alignment and finding support without editing the manuscript. In revise mode separate scientific proposals from language edits and obtain researcher approval for substantive changes. The optional extension of `audit_full_paper.py` checks declarations, not scientific truth. [Guide](skills/research-paper-craft/references/research-reasoning.en.md) · [Examples and compatibility](docs/UPGRADE-v2.3.3.md).
