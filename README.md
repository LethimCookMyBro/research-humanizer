<div align="center">

# Research Humanizer

**Clear research writing. Traceable claims. Real evidence.**

[![Version](https://img.shields.io/badge/version-2.2.0-2563eb?style=flat-square)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-0f766e?style=flat-square)](LICENSE)
[![Languages](https://img.shields.io/badge/guides-English%20%2B%20Thai-475569?style=flat-square)](skills/research-paper-craft/SKILL.md)
[![Status](https://img.shields.io/badge/status-preview-b45309?style=flat-square)](docs/KNOWN_ISSUES.md)

<a href="README.md">English</a> · <a href="README%28TH%29.md">ภาษาไทย</a>

[Install](#install) · [Use](#use) · [Scope](#scope) · [Validation](#validation)

</div>

A research-writing skill for Claude Code and Codex. Remove generic filler without inventing specificity, changing the science or replacing the author's voice. Keep good text unchanged. Build graphs from verified data and use actual study photographs when the figure must show the real setup.

> [!IMPORTANT]
> Missing originals? Ask the researcher. A plausible sentence, a synthetic lab image or an attractive curve is not evidence.

**2.2.0** adds author voice profiles, before/after claim review, real-first figures and a repaired text checker. Word-first safeguards and the original Humanizer remain. [See the gap-closure record](docs/QUALITY.md).

<a id="install"></a>
## Install

### Claude Code

Run inside Claude Code, one line at a time.

```text
/plugin marketplace add LethimCookMyBro/research-humanizer
/plugin install research-humanizer@research-humanizer
```

Then invoke the skill.

```text
/research-humanizer:research-paper-craft Revise this manuscript. Preserve my claims and ask for missing originals.
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

Check the installed version in `/plugins`. Restart the host session. A refreshed catalog or a GitHub push does not prove the installed cache changed. If a desktop app still shows an older version, check that its installation and the CLI use the same account/configuration. Back up local customizations before reinstalling. Do not delete the entire host configuration directory.

For a standalone installation, copy the complete `skills/research-paper-craft` folder into `~/.claude/skills/` or `~/.agents/skills/`, or the corresponding project directory. Do not enable both standalone and plugin copies. Keep references, scripts and license notices together.

</details>

Commands follow the [Claude plugin guide](https://code.claude.com/docs/en/discover-plugins) and [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference). Live host installation remains unverified in the development environment.

<a id="use"></a>
## Use

```text
Use research-paper-craft on the files in this project.
Preserve my accepted terminology and make only necessary language changes.
Compare changed claims with their sources, including scope and uncertainty.
Use real originals for evidence images and verified data for graphs.
Map overview components and arrows to the actual method.
Ask me for missing study inputs. Do not substitute them.
Keep the original Word document and edit a copy.
Separate the manuscript from the verification report.
```

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
| Humanizing | Minimal edits, author-approved voice, stable terminology and explicit stopping rules |
| Scientific meaning | Trace sources, compare before/after claims, preserve negation, scope and citation attachment |
| Whole papers | Link questions, methods, results and limitations; remove paragraphs that only repeat importance |
| Mathematics | Editable equations, defined symbols and units, implementation mapping |
| Graphs | Reproducible plot data, independent units, calculated uncertainty and final-size review |
| Real images | Matching originals, capture context, consent and disclosed processing |
| Overview / infographic | Evidence-linked nodes and arrows, readable hierarchy, no decorative invented components |
| Word and submission | Preserve DOCX structure, inspect native Word pagination and every final page, audit anonymity |

Guidance is task-loaded in one language. An ordinary paragraph edit does not load all guides. Start with [SKILL.md](skills/research-paper-craft/SKILL.md), [writing](skills/research-paper-craft/references/writing.en.md), [visuals](skills/research-paper-craft/references/visuals.en.md) or [Word layout](skills/research-paper-craft/references/word-layout.en.md). Optional record templates are in [assets](skills/research-paper-craft/assets).

<a id="validation"></a>
## Validation and limits

The five historical text-checker regressions are fixed. New tests cover revision signals, figure contracts, malformed inputs and path confinement. Full commands, counts and evidence are in [VERIFICATION.md](docs/VERIFICATION.md). Independent model quality, native Word repair and live host installation remain **not established**. The [24-case evaluation bank](evals/README.md) contains synthetic fixtures, not fabricated benchmark results.

| Tool | What it does not certify |
| --- | --- |
| Text checker | Scientific truth, every syntax form, or AI authorship |
| Revision reviewer | Semantic equivalence or correct citation attachment |
| Figure audit | Photo authenticity, permissions, statistical recomputation or rendered quality |
| DOCX preflight | Native Word pagination or visual layout |

All checks are local and non-mutating. [Tool usage and schemas](docs/QUALITY.md). A no-flags report is not submission approval. Follow the venue's AI-disclosure policy. This project does not promise detector evasion, paper acceptance or a particular number of stars.

## Contribute

[CONTRIBUTING.md](CONTRIBUTING.md) · [Known limits](docs/KNOWN_ISSUES.md) · [Changelog](CHANGELOG.md) · [Publishing](docs/PUBLISHING.md)

Useful contributions are reproducible edge cases, source-bounded bilingual examples and recorded host/model trials. Never submit private manuscripts, participant data or credentials without authorization.

## License and attribution

[MIT](LICENSE). The original Humanizer by [Siqi Chen](https://github.com/blader/humanizer) is retained with its [MIT notice](licenses/humanizer-MIT.txt) and [provenance](THIRD_PARTY_NOTICES.md). This is an independent project, not an endorsement by the providers of Claude Code or Codex.
