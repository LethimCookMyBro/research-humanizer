# Changelog

## 2.1.0, 2026-11-16

- Added Word-first preservation guards and task-loaded English/Thai layout guidance under R31 to R40.
- Covered character and word spacing, line and paragraph spacing, Thai combining marks, table density, equation rendering and code correspondence, column gaps, fields, and final saved-file review.
- Added a read-only DOCX structural preflight with synthetic-fixture tests. It does not fix or render manuscripts.
- Added unfilled layout QA and equation-to-code records plus 20 unexecuted Word acceptance scenarios.
- Bumped both plugin manifests and the core skill to 2.1.0. Preserved all original R00 to R30 bodies, Humanizer source, and text-checker code.
- Native Word repairs and model compliance remain unverified. The five existing text-checker audit failures remain open.

## Plugin packaging 2.0.1, 2026-11-15

- Added native Claude Code and Codex plugin manifests and repository marketplace catalogs.
- Made plugin-manager installation the recommended route in both READMEs.
- Replaced installation URL placeholders with `LethimCookMyBro/research-humanizer`.
- Documented Claude Code namespacing, Codex CLI commands, migration, and management.
- Added offline packaging regression tests. Live host installation remains unverified.
- Kept the core skill at `2.0.0` and preserved all bundled skill files. The five known checker failures remain open.

## Documentation and licensing edition, 2026-11-15

- Added the Research Humanizer repository identity and English and Thai GitHub READMEs.
- Added local installation guidance for Claude Code and Codex, with safe copy commands and project-scope alternatives.
- Kept the installed skill identifier `research-paper-craft` and the core skill version `2.0.0` unchanged.
- Preserved all existing guidance modules, the original Humanizer file, and the checker implementation.
- Added an MIT license, verified upstream notices, known-issue documentation, publishing guidance, and contribution instructions.
- Retained the previous audit as history and recorded current documentation verification separately.

This is not a checker bug-fix release. The five targeted v2.0 regressions remain open. Independent model and native Word workflows are not newly validated.
