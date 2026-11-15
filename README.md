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

[Install](#install) · [Use](#use) · [Scope](#scope) · [Validation](#validation) · [Contribute](CONTRIBUTING.md)

</div>

Research Humanizer combines research-specific editing rules with evidence checks. It tells the agent to preserve scientific meaning, trace numerical claims, and ask the researcher for missing originals before filling a gap.

**Missing a real environment photo, raw record, or experimental setting? Ask the researcher first. Do not invent it or quietly replace it.**

> [!NOTE]
> This repository packages the existing Research Paper Craft v2.0 skill. The installed skill is still named `research-paper-craft`. The repository name is `research-humanizer`. Core instructions and checker code have not been rewritten for this documentation edition. Known checker defects and untested workflows are listed under [Validation](#validation).

<a id="install"></a>
## Install

These instructions target **local Claude Code and Codex CLI**. Install and sign in to the host separately. The optional text checker requires Python 3.10 or later. The skill instructions themselves do not require Python.

### Get the repository

Replace `YOUR_USERNAME` with the repository owner's GitHub username. Run the remaining installation commands from the cloned repository root.

```bash
git clone https://github.com/YOUR_USERNAME/research-humanizer.git
cd research-humanizer
```

A downloaded ZIP works too. Extract it and open a terminal in the folder that contains this README and `skills/`.

### Claude Code

Install for your user account on macOS, Linux, or WSL.

```bash
destination="$HOME/.claude/skills/research-paper-craft"
if [ -e "$destination" ] || [ -L "$destination" ]; then
  printf '%s\n' "Already installed. Back up the existing folder before updating."
else
  mkdir -p "$(dirname "$destination")" &&
    cp -R skills/research-paper-craft "$destination"
fi
```

In Claude Code, type the following **in the chat input**, not in your shell.

```text
/research-paper-craft Revise the manuscript in this workspace. Preserve the evidence and ask me about missing study inputs.
```

The personal skill directory and slash invocation follow the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

### Codex

Install for your user account on macOS, Linux, or WSL.

```bash
destination="$HOME/.agents/skills/research-paper-craft"
if [ -e "$destination" ] || [ -L "$destination" ]; then
  printf '%s\n' "Already installed. Back up the existing folder before updating."
else
  mkdir -p "$(dirname "$destination")" &&
    cp -R skills/research-paper-craft "$destination"
fi
```

In Codex, type the following **in the chat input**, not in your shell.

```text
$research-paper-craft Revise the manuscript in this workspace. Preserve the evidence and ask me about missing study inputs.
```

The user skill directory is `~/.agents/skills/`. This follows the [Codex skills documentation](https://developers.openai.com/codex/skills/). The separate `~/.codex/` directory is not the destination used by this guide.

<details>
<summary><strong>Windows PowerShell</strong></summary>

After cloning the repository, run this from its root. Choose `.claude` for Claude Code or `.agents` for Codex. For a host running inside WSL, use the Linux instructions inside that WSL environment instead.

```powershell
# Use .claude for Claude Code or .agents for Codex.
$skillsRoot = ".claude"
$destination = Join-Path $HOME "$skillsRoot/skills/research-paper-craft"
if (Test-Path -LiteralPath $destination) {
    throw "Already installed. Back up the existing folder before updating."
}
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
Copy-Item -LiteralPath "skills/research-paper-craft" -Destination $destination -Recurse -ErrorAction Stop
```

This copies files only. It does not install Claude Code, Codex, or Python. The PowerShell example has not been executed in this packaging environment.

</details>

<details>
<summary><strong>Install for one research project</strong></summary>

Copy the complete `skills/research-paper-craft` folder into the appropriate directory **inside the research project**, keeping the final folder name unchanged.

| Host | Final entry point relative to the research project root |
| --- | --- |
| Claude Code | `.claude/skills/research-paper-craft/SKILL.md` |
| Codex | `.agents/skills/research-paper-craft/SKILL.md` |

Keep the adjacent references, templates, scripts, and license notices. Do not copy only `SKILL.md`. Choose a user-level or project-level installation for each host, rather than keeping competing versions at both scopes.

</details>

### Verify discovery and update safely

Open your research project in the host. Start a new session if the skill does not appear, then invoke it explicitly. Confirm that the agent can read a referenced module, not just the entry point. A local file copy is not an end-to-end host test.

To update a Git clone, review local changes and run `git pull --ff-only` from the repository root. Back up the installed skill folder **outside the host's skills directory**, move the old folder out, then repeat the copy step. The copy commands intentionally do not overwrite existing installations. A copied installation does not update automatically when the source repository changes.

To uninstall, move the installed `research-paper-craft` folder outside the skills directory and start a new session. Do not move or delete your manuscript files.

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

The eight guidance modules are available in [English](skills/research-paper-craft/references/writing.en.md) and [Thai](skills/research-paper-craft/references/writing.th.md). The full routing table is in [SKILL.md](skills/research-paper-craft/SKILL.md).

<details>
<summary><strong>Default manuscript style</strong></summary>

Use short, complete, moderately formal sentences. Avoid comma chains and crowded paragraphs. Keep necessary terminology stable.

The default house style prohibits prose semicolons, colons, long dashes, and English contractions. `Keywords:` and reference punctuation are exceptions. Code, equations, URLs, identifiers, required citations, and exact quotations remain protected. Use Greek letters and restricted symbols in mathematical or numerical contexts rather than decorative prose.

These are this project's defaults, not universal publishing rules. Report conflicts with a verified venue template or the researcher's explicit requirements. Never change scientific meaning to satisfy a style checker.

</details>

### Boundaries

This is a set of agent instructions with an optional heuristic checker. It does not itself provide browsing, image generation, document rendering, or Microsoft Word. Those capabilities depend on the host and its tools.

It does not certify scientific correctness, guarantee publication acceptance, or promise to evade AI detectors. Follow the venue's AI-use disclosure requirements. Without native Word access, Word pagination remains unchecked rather than being inferred from another renderer.

<a id="validation"></a>
## Validation

**Preview status is deliberate.** Instruction coverage, executable tests, and real-model behavior are different forms of evidence.

| Check | Current evidence |
| --- | --- |
| Bundled checker and package tests | 31 tests pass in the documented local run |
| Targeted v2.0 audit regressions | 5 tests fail and remain open |
| Independent model trials | 40 scenarios are defined. They have not been executed |
| Claude Code and Codex integration | Installation paths checked against official documentation. Live host invocation not tested here |
| Native Word and full submission workflow | Not tested end to end on a research manuscript |

See [known issues](docs/KNOWN_ISSUES.md), the [original audit](docs/audit-v2.0/README.md), and the [current verification record](docs/VERIFICATION.md). The documentation edition does not claim to fix the v2.0 checker.

### Optional checker and tests

Run from the repository root. Replace the manuscript path with your own file. Use `python` in place of `python3` when that is your Python 3 command.

```bash
python3 skills/research-paper-craft/scripts/lint_manuscript.py /path/to/manuscript.md --json
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
```

The checker reads UTF-8 Markdown or plain text and does not edit files. It does not validate DOCX, PDF, mathematics, citations, image authenticity, anonymity, or scientific claims. A clean report does not approve a manuscript.

To reproduce the **currently failing** targeted audit checks, run the following separately. A nonzero exit is expected on the unchanged v2.0 checker and must not be reported as a pass.

```bash
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

## Repository layout

```text
research-humanizer/
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
