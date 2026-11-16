<div align="center">

# Research Humanizer

**Natural prose. Verifiable claims.**

A research-writing skill for Claude Code and Codex.<br>
From manuscript revisions to equations, figures, and submission checks.

[![License MIT](https://img.shields.io/badge/License-MIT-2563eb?style=flat-square)](LICENSE)
[![Guides English and Thai](https://img.shields.io/badge/Guides-English%20%2B%20Thai-0f766e?style=flat-square)](skills/research-paper-craft/references/writing.en.md)
[![Format Agent Skills](https://img.shields.io/badge/Format-Agent%20Skills-475569?style=flat-square)](skills/research-paper-craft/SKILL.md)
[![Status Preview](https://img.shields.io/badge/Status-Preview-b45309?style=flat-square)](docs/KNOWN_ISSUES.md)

**English** · <a href="README%28TH%29.md">ภาษาไทย</a>

[Install](#install) · [Use](#use) · [Word layout](#word-layout) · [Scope](#scope) · [Validation](#validation) · [Contribute](CONTRIBUTING.md)

</div>

Research Humanizer combines research-specific editing rules with evidence checks. It tells the agent to preserve scientific meaning, trace numerical claims, and ask the researcher for missing originals before filling a gap.

**Missing a real environment photo, raw record, or experimental setting? Ask the researcher first. Do not invent it or quietly replace it.**

> [!NOTE]
> Version `2.1.0` adds Word-first layout and typography safeguards to the `research-humanizer` plugin and `research-paper-craft` skill. Original research humanizing rules remain unchanged. The optional DOCX preflight is read-only, not a rendering validator. The five known text-checker regressions remain open. See [Word layout](#word-layout) and [Validation](#validation).

<a id="install"></a>
## Install

Install **Research Humanizer as a plugin**. The plugin bundles the existing `research-paper-craft` skill and its English and Thai guides. You do not need to clone the repository or copy skill folders for the recommended installation.

Use a current **Claude Code CLI or Codex CLI** with plugin support and Git available. Install and sign in to the host separately. Python 3.10 or later is needed only for the optional text checker. This package adds no MCP servers, hooks, or extra account connection.

### Claude Code

Run these commands **inside the Claude Code chat**, one at a time.

```text
/plugin marketplace add LethimCookMyBro/research-humanizer
/plugin install research-humanizer@research-humanizer
```

Choose the installation scope when prompted. Follow the activation message. If needed, run `/reload-plugins` or start a new session. Then invoke the bundled skill with its plugin namespace.

```text
/research-humanizer:research-paper-craft Revise the manuscript in this workspace. Preserve the evidence and ask me about missing study inputs.
```

<details>
<summary><strong>Claude Code terminal alternative</strong></summary>

Run these in your terminal, not in the chat. The default scope is your user account. Add `--scope project` to the install command for a shared research project.

```bash
claude plugin marketplace add LethimCookMyBro/research-humanizer
claude plugin install research-humanizer@research-humanizer
```

</details>

The marketplace registration and plugin installation are separate steps. The plugin name and marketplace name are both `research-humanizer`. See the official [installation guide](https://code.claude.com/docs/en/discover-plugins) and [plugin namespace guide](https://code.claude.com/docs/en/plugins).

### Codex CLI

Run these commands **in your terminal**, not in the Codex chat.

```bash
codex plugin marketplace add LethimCookMyBro/research-humanizer
codex plugin add research-humanizer@research-humanizer
```

Start a new Codex session. Enter `/plugins` to confirm that **Research Humanizer** is installed and enabled. The interactive alternative is to register the marketplace with the first command above, then open `/plugins` and install Research Humanizer from that marketplace.

Ask Codex to use the `research-paper-craft` skill on your project files. You can also select it from the skill picker by typing `$`.

```text
Use the research-paper-craft skill from Research Humanizer to revise the manuscript in this workspace. Preserve the evidence and ask me about missing study inputs.
```

Codex uses `codex plugin add` for installation and `/plugins` for its browser. These are different from Claude Code's commands. See the official [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference) and [plugin guide](https://developers.openai.com/codex/plugins).

> [!TIP]
> Migrating from the earlier manual installation? Back up and move your standalone `research-paper-craft` folder outside `~/.claude/skills/`, `~/.agents/skills/`, or the corresponding project skills directory before switching to the plugin. Keep your manuscript files untouched. Do not leave competing standalone and plugin copies enabled.

<details>
<summary><strong>Verify, update, or uninstall the plugin</strong></summary>

Check installed plugins from your terminal.

```bash
claude plugin list
codex plugin list
```

For Claude Code, refresh the marketplace and update the plugin.

```bash
claude plugin marketplace update research-humanizer
claude plugin update research-humanizer@research-humanizer
```

For Codex, refresh the marketplace catalog.

```bash
codex plugin marketplace upgrade research-humanizer
```

A refreshed catalog is not proof that the installed cache changed. Check the installed version in `/plugins`. If the installed copy is still old, back up any local customizations and reinstall it through that browser. Start a new session afterward.

Uninstall from your terminal. For a Claude Code project-scope install, add `--scope project`.

```bash
claude plugin uninstall research-humanizer@research-humanizer
codex plugin remove research-humanizer@research-humanizer
```

These commands manage plugins, not manuscript files. If plugin commands are not recognized, update the host using its official installation instructions. Organization policies may also restrict custom marketplaces. Do not bypass those policies.

</details>

<details>
<summary><strong>Manual alternative for a standalone skill</strong></summary>

Use this only when you need a plain skill instead of a plugin. Do not perform it in addition to the recommended plugin installation.

```bash
git clone https://github.com/LethimCookMyBro/research-humanizer.git
cd research-humanizer
```

Copy the complete `skills/research-paper-craft` directory to one destination. Back up and move an existing installation outside the skills directory first. Do not overwrite it or copy only `SKILL.md`.

| Host | User-level destination | Project-level destination |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/research-paper-craft/` | `.claude/skills/research-paper-craft/` |
| Codex | `~/.agents/skills/research-paper-craft/` | `.agents/skills/research-paper-craft/` |

Project paths are relative to the research project's root. On Windows, use your home directory for `~`. If the host runs in WSL, use the paths inside that WSL environment. Keep all references, scripts, templates, and license notices.

A standalone Claude Code skill uses `/research-paper-craft` rather than the plugin-namespaced command. In Codex, select the skill by typing `$`. Start a new session after changing the installed files.

Manual copies do not update through the plugin manager. Review source changes, run `git pull --ff-only`, back up the installed copy, and replace it deliberately. To uninstall, move the installed skill folder outside the discovery directory. Leave manuscript files untouched.

See the official [Claude Code skills guide](https://code.claude.com/docs/en/skills) and [Codex skills guide](https://developers.openai.com/codex/skills/).

</details>

<a id="use"></a>
## Use

Give the agent access to the actual project files. State the output language, target venue, and which result exports are authoritative when these are known. It must read existing decisions before asking again.

```text
Use research-paper-craft on the files in this workspace.
Write the manuscript in English and discuss open questions with me in Thai.
Inspect the manuscript, code, approved results, and source records first.
Ask me for any missing original data, images, or study details.
Create equations and visuals only where the research needs them.
Keep the manuscript separate from the verification report.
Do not claim checks that were not actually performed.
```

For a language-only edit, ask for that narrower scope. The skill should not redesign the study while polishing a paragraph. It loads relevant guidance progressively in one language, rather than reading both complete language sets at startup.

### A small example

*Illustrative writing example, not an executed model benchmark.*

The supplied note states only that a method combines sensor readings. It includes no evaluation results or field photographs.

| Stage | Text |
| --- | --- |
| Inflated draft | Our groundbreaking framework seamlessly integrates sensor measurements and demonstrates robust real-world performance. |
| Supported rewrite | The method combines sensor readings. |
| Researcher question | Do you have the evaluation results and original environment photographs for this study? |

The performance claim stays unresolved until evidence is supplied. It is not strengthened, replaced with a guess, or silently treated as established.

<a id="word-layout"></a>
## Word-first layout checks

**Humanize the prose without rebuilding the formatted paper.** Version 2.1.0 adds a task-loaded Word layout module in [English](skills/research-paper-craft/references/word-layout.en.md) and [Thai](skills/research-paper-craft/references/word-layout.th.md). The original research-writing and evidence rules remain intact.

| Problem | Required review |
| --- | --- |
| Stretched words or letters | Character tracking, scale, kerning, justification, tabs, nonbreaking spaces, manual line breaks |
| Uneven or clipped lines | Line height, paragraph before/after spacing, styles, grid, Thai combining marks |
| Cramped tables | Column width, cell margins, row height, wrapping, header repetition, row splitting |
| Broken or crowded equations | Original symbols, OMML or legacy objects, fonts, numbering, spacing, necessity, equation-to-code consistency |
| Empty column bottoms or page gaps | Keep chains, section and column breaks, floating anchors, footnotes, legitimate whitespace |
| Formatting drift after editing | Original-copy preservation, targeted Word edits, field and object checks, saved-file and PDF review |

The agent must keep an untouched original and use a working copy. It must not recreate the DOCX from Markdown, extracted text, or screenshots. Without native Word editing access, it provides a read-only audit and a location-specific patch plan. Programmatic edits require explicit approval and final verification in Word.

```text
Use research-paper-craft in Word-first mode on the original DOCX.
Preserve research meaning, equation objects, fields, and the venue template.
Audit character, word, line, paragraph, table, equation, and page spacing.
Ask before replacing uncertain symbols or changing scientific definitions.
Keep a backup and verify every final page in Microsoft Word.
If Word access is unavailable, return an anchored patch plan rather than a rebuilt document.
```

An optional read-only preflight finds structural review candidates. Run it from a local repository checkout. It does not fix files or render pages.

```bash
python3 skills/research-paper-craft/scripts/audit_docx.py /path/to/manuscript.docx --json
```

Use the [layout QA record](skills/research-paper-craft/assets/layout-qa.md) and [equation-to-code map](skills/research-paper-craft/assets/equation-code-map.csv) when applicable. These are unfilled templates. A clean preflight does not prove that the layout is correct. Native Word access, every-page inspection, and the final saved artifact remain required.

<a id="scope"></a>
## Scope

| Area | What the instructions require |
| --- | --- |
| Research humanizing | Remove filler and formulaic prose while preserving meaning, numbers, citations, negation, and uncertainty |
| Evidence and versions | Resolve conflicting documents and code with the researcher. Trace study results to approved exports and raw records |
| Paper structure | Keep the Introduction accessible. Use concise contribution bullets without numerical results |
| Methods and equations | Define variables, units, dimensions, assumptions, and boundary cases. Check consistency with implementation |
| Evaluation and statistics | Review comparison fairness, aggregation, uncertainty, and reproducibility |
| Figures and tables | Plot verified data. Match system diagrams to the real method. Label conceptual illustrations |
| Submission | Check identity leakage, metadata, headers, and supplements. Verify Word pagination and every final page when required |
| Working records | Separate manuscript deliverables from source, claim, and verification records |

The nine guidance modules are available in [English](skills/research-paper-craft/references/writing.en.md) and [Thai](skills/research-paper-craft/references/writing.th.md). The full routing table is in [SKILL.md](skills/research-paper-craft/SKILL.md).

<details>
<summary><strong>Default manuscript style</strong></summary>

Use short, complete, moderately formal sentences. Avoid comma chains and crowded paragraphs. Keep necessary terminology stable.

The default house style prohibits prose semicolons, colons, long dashes, and English contractions. `Keywords:` and reference punctuation are exceptions. Code, equations, URLs, identifiers, required citations, and exact quotations remain protected. Use Greek letters and restricted symbols in mathematical or numerical contexts rather than decorative prose.

These are this project's defaults, not universal publishing rules. Report conflicts with a verified venue template or the researcher's explicit requirements. Never change scientific meaning to satisfy a style checker.

</details>

### Boundaries

This is a set of agent instructions with optional read-only text and DOCX structural checkers. It does not itself provide browsing, image generation, document rendering, or Microsoft Word. Those capabilities depend on the host and its tools.

It does not certify scientific correctness, guarantee publication acceptance, or promise to evade AI detectors. Follow the venue's AI-use disclosure requirements. Without native Word access, Word pagination remains unchecked rather than being inferred from another renderer.

<a id="validation"></a>
## Validation

**Preview status is deliberate.** Instruction coverage, executable tests, and real-model behavior are different forms of evidence.

| Check | Current evidence |
| --- | --- |
| Bundled checker and package tests | 31 tests pass in the documented local run |
| Targeted v2.0 audit regressions | 5 tests fail and remain open |
| DOCX structural preflight | 27 tests on synthetic ZIP/XML fixtures pass. No native Word rendering |
| Word layout instruction contracts | 8 static tests pass. They do not establish model compliance |
| Independent model trials | 40 research scenarios and 20 Word layout scenarios are defined. They have not been executed |
| Plugin packaging and install docs | Both host manifests and catalogs added. Offline contract tests are recorded in the verification report |
| Claude Code and Codex integration | Commands checked against official documentation. Live install and invocation not tested here |
| Native Word and full submission workflow | Not tested end to end on a research manuscript |

See [known issues](docs/KNOWN_ISSUES.md), the [original audit](docs/audit-v2.0/README.md), and the [current verification record](docs/VERIFICATION.md). Version 2.1.0 does not claim to fix the v2.0 text checker.

### Optional checker and tests

Run from the repository root. Replace the manuscript path with your own file. Use `python` in place of `python3` when that is your Python 3 command.

```bash
python3 skills/research-paper-craft/scripts/lint_manuscript.py /path/to/manuscript.md --json
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B -m unittest discover -s tests -v
```

The checker reads UTF-8 Markdown or plain text and does not edit files. It does not validate DOCX, PDF, mathematics, citations, image authenticity, anonymity, or scientific claims. A clean report does not approve a manuscript.

To reproduce the **currently failing** targeted audit checks, run the following separately. A nonzero exit is expected on the unchanged v2.0 checker and must not be reported as a pass.

```bash
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

## Repository layout

```text
research-humanizer/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── .agents/plugins/
│   └── marketplace.json
├── tests/
│   └── test_plugin_packaging.py
├── README.md
├── README(TH).md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── CONTRIBUTING.md
├── docs/
│   ├── PUBLISHING.md
│   ├── KNOWN_ISSUES.md
│   ├── VERIFICATION.md
│   └── audit-v2.0/
└── skills/
    └── research-paper-craft/
        ├── SKILL.md
        ├── references/
        ├── assets/
        ├── scripts/
        ├── tests/
        ├── provenance/
        └── licenses/
```

## Contribute

Start with a reproducible issue or a small pull request. Useful contributions include checker regression fixes, bilingual meaning-preservation examples, and documented host trials. Use synthetic or shareable fixtures. Do not upload private manuscripts, participant data, credentials, or unpublished results without permission.

Read [CONTRIBUTING.md](CONTRIBUTING.md). For repository setup, the About description, and suggested topics, see [PUBLISHING.md](docs/PUBLISHING.md).

## License and attribution

Released under the [MIT License](LICENSE). Preserve the included copyright and permission notices when redistributing this work.

The Humanizer source is credited to [Siqi Chen's Humanizer project](https://github.com/blader/humanizer). The bundled original matches the upstream v4.0.0 Git blob. Its MIT notice is retained in [licenses/humanizer-MIT.txt](licenses/humanizer-MIT.txt). Research-specific adaptations and provenance are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Claude Code and Codex are products of their respective providers. This repository is an independent project and does not imply their endorsement.

<sub>Installation documentation checked on 15 November 2026. Product behavior can change.</sub>
