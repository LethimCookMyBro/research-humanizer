# Research Paper Craft 2.3.1

The skill inside Research Humanizer. Start with SKILL.md. Load one language and only the guidance needed for the current task. The core stays under 1,000 English whitespace-delimited words. Detailed Word, scientific and language rules are task-loaded.

Research humanizing preserves sources, terminology, scope and uncertainty. Real evidence images stay real. Quantitative graphs come from approved data. Overview diagrams map components and arrows to the implemented method. Existing DOCX files stay Word-first.

## New in 2.3.1

Context-aware punctuation review now runs through the existing text checker. Soft-wrapped prose is reviewed as a sentence. New advisory candidates cover comma load, symbolic shorthand, ellipses, repeated marks and overloaded asides. Common numerical, citation and quoted contexts are protected. Load [English punctuation guidance](references/punctuation.en.md) or [ภาษาไทย](references/punctuation.th.md) with writing. No automatic edits, grammatical certification or AI score are added. Thresholds are review triggers, not writing quotas.

## Added in 2.3.0

Full-paper mode, ARS handoff and a Claude research-full command, literature/venue reconnaissance, metric-data planning, private multi-author context, and a read-only record-completeness audit. See [full-paper](references/full-paper.en.md), [literature](references/literature.en.md), and [integration](references/ars-integration.en.md). ARS is installed separately under CC BY-NC 4.0. Host invocation has not been tested here.

## Retained from 2.2.0

Optional author voice profile, minimal-edit and stop rules, before/after claim review, source-bound examples, whole-paper coherence checks, real-first figure provenance and explicit checker coverage. Five historical text-checker regressions are fixed. Independent model quality and native Word execution are not established.

## Local tools

Run from this skill folder. Python 3.10 or later is required only for the tools. No network requests or research-input edits occur.

```bash
python scripts/lint_manuscript.py manuscript.md --json --fail-on-errors
python scripts/review_revision.py before.md after.md --terms terms.json
python scripts/audit_figures.py figure-manifest.json --root /path/to/project
python scripts/audit_docx.py manuscript.docx --json
python scripts/audit_full_paper.py full-paper-run.json --json
```

terms.json contains a JSON list of exact terms. The voice-profile is optional and is not automatically loaded by these tools. Figure manifest documentation is in the repository quality guide. Empty templates do not pass an audit.

Text checks flag selected house-style rules and generic wording candidates. Revision checks flag selected lexical differences. Figure checks validate records, local hashes and selected CSV values. DOCX checks inspect XML structure. None proves authorship, truth, statistical validity, visual quality or Word pagination. An incomplete text parse returns exit 2 and cannot be reported as a pass.

## Records

assets contains the project brief, author profile, claim revision ledger, paper map, figure manifest, capture checklist, graph review, equation-code map and layout/submission QA templates. Keep only the records required by the task. All start unverified.

## ไทย

ใช้ SKILL.md เป็นจุดเริ่ม แล้วอ่านคู่มือภาษาเดียวตามงาน เก็บศัพท์และความหมายของเจ้าของงาน แก้เฉพาะที่มีเหตุผล ภาพหลักฐานใช้ต้นฉบับจริง กราฟใช้ข้อมูลที่ตรวจแล้ว สมการต้องตรงกับโค้ด และเอกสาร Word ต้องแก้จากสำเนาต้นฉบับ ไม่สร้างไฟล์จัดหน้าใหม่จากข้อความที่ดึงออกมา

เครื่องมือช่วยชี้จุดตรวจ ไม่รับรองว่าข้อความเป็นของมนุษย์หรือบทความถูกต้องทั้งหมด อ่าน [ข้อจำกัด](KNOWN_ISSUES.md) และเก็บบันทึกตรวจแยกจากบทความ

The full-paper auditor checks declared record consistency only. Exit 0 means consistent declarations, 1 means unresolved record findings, and 2 means unreadable or unsupported input. It never approves submission or fetches sources. Blank templates are deliberately incomplete. Private run records belong in the research project, not the installed skill.
