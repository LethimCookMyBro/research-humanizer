# Full-paper integration

Research Humanizer 2.3.0 is a research-specific writing contract for whole manuscripts, revision and audits. Pair it with ARS to keep the same contract across research, writing, review and formatting. It is not a fork of ARS and does not install external dependencies automatically.

## Entry points

Claude Code user command `research-humanizer:research-full` loads the Research Humanizer core and then the discovered `academic-research-skills:academic-pipeline` entry. The inspected upstream ars-full command uses that pipeline and disables model invocation of the command itself. Do not invoke the command recursively.

Codex uses the upstream ARS-Codex distribution and its academic-research-suite router. Ask for full-paper mode and research-paper-craft together. No Claude hooks or command machinery is claimed to transfer.

[English adapter](../skills/research-paper-craft/references/ars-integration.en.md) · [คู่มือภาษาไทย](../skills/research-paper-craft/references/ars-integration.th.md) · [Inspected upstream sources](../skills/research-paper-craft/provenance/integrations.json)

## Contract and defaults

- Full-paper drafting is explicit. Revision-only minimal-edit rules do not stop new sections being written.
- Research decisions, uncertain versions and missing original study inputs still require the researcher. ARS confirmation and privacy gates stay in force.
- Literature is searched from the actual study. Open sources and retain locations. Official venue requirements outrank a published exemplar for formatting.
- A metric from another paper is a candidate, not an observed result. Verify definitions, raw fields, denominators, repeated measures and analysis permission before using it.
- Style uses available author-approved context without inventing memory. Profiles stay separate per researcher and outside the installed plugin.
- Real study images, reproducible graphs and actual code mappings remain required. Word master preservation is not replaced by ARS format conversion.

## Read-only record audit

From the repository root, run the following on a private completed record.

```bash
python3 skills/research-paper-craft/scripts/audit_full_paper.py /path/to/full-paper-run.json --json
```

The blank template in assets is deliberately incomplete. The auditor checks schema, ARS resource declarations, search records, source access and locators, metric-data decisions, section records and final-check declarations. Exit 0 means consistent declarations, 1 means review findings, 2 means unreadable/unsupported input. It performs no web retrieval, source execution, semantic verification, image authentication or Word rendering. submission_approved is always false. It cannot decide whether all sections required by the actual discipline are present.

## Release and installation

A release identifies a tagged downloadable revision. Plugin discovery and updates still depend on the configured marketplace or imported snapshot, manifest version, enabled plugin and new-session loading. An old Desktop display is not diagnosed by creating a new release alone. Refresh the correct marketplace and inspect the installed source before deleting or reinstalling anything. Never delete the entire .claude directory.

## Licensing

Research Humanizer additions remain MIT. ARS is installed separately under CC BY-NC 4.0; our license does not remove its restrictions. Aboudjem Humanizer is an inspected MIT reference, with its notice retained. The existing blader Humanizer original and notice remain. No provider or upstream endorsement is implied.

## What is and is not verified

The source interfaces were inspected and local contracts tested. These tests do not establish live ARS/Claude/Codex interoperability, a complete real-paper workflow, stronger prose quality, or successful native Word repair. See the current verification record and the proposed full-paper scenarios before making stronger claims.
