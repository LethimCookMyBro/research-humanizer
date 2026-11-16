# Research Paper Craft 2.2.0

The skill inside Research Humanizer. Start with SKILL.md. Load one language and only the guidance needed for the current task. The core stays under 1,000 English whitespace-delimited words. Detailed Word, scientific and language rules are task-loaded.

Research humanizing preserves sources, terminology, scope and uncertainty. Real evidence images stay real. Quantitative graphs come from approved data. Overview diagrams map components and arrows to the implemented method. Existing DOCX files stay Word-first.

## New in this version

Optional author voice profile, minimal-edit and stop rules, before/after claim review, source-bound examples, whole-paper coherence checks, real-first figure provenance and explicit checker coverage. Five historical text-checker regressions are fixed. Independent model quality and native Word execution are not established.

## Local tools

Run from this skill folder. Python 3.10 or later is required only for the tools. No network requests or research-input edits occur.

```bash
python scripts/lint_manuscript.py manuscript.md --json --fail-on-errors
python scripts/review_revision.py before.md after.md --terms terms.json
python scripts/audit_figures.py figure-manifest.json --root /path/to/project
python scripts/audit_docx.py manuscript.docx --json
```

terms.json contains a JSON list of exact terms. The voice-profile is optional and is not automatically loaded by these tools. Figure manifest documentation is in the repository quality guide. Empty templates do not pass an audit.

Text checks flag selected house-style rules and generic wording candidates. Revision checks flag selected lexical differences. Figure checks validate records, local hashes and selected CSV values. DOCX checks inspect XML structure. None proves authorship, truth, statistical validity, visual quality or Word pagination. An incomplete text parse returns exit 2 and cannot be reported as a pass.

## Records

assets contains the project brief, author profile, claim revision ledger, paper map, figure manifest, capture checklist, graph review, equation-code map and layout/submission QA templates. Keep only the records required by the task. All start unverified.

## ไทย

ใช้ SKILL.md เป็นจุดเริ่ม แล้วอ่านคู่มือภาษาเดียวตามงาน เก็บศัพท์และความหมายของเจ้าของงาน แก้เฉพาะที่มีเหตุผล ภาพหลักฐานใช้ต้นฉบับจริง กราฟใช้ข้อมูลที่ตรวจแล้ว สมการต้องตรงกับโค้ด และเอกสาร Word ต้องแก้จากสำเนาต้นฉบับ ไม่สร้างไฟล์จัดหน้าใหม่จากข้อความที่ดึงออกมา

เครื่องมือช่วยชี้จุดตรวจ ไม่รับรองว่าข้อความเป็นของมนุษย์หรือบทความถูกต้องทั้งหมด อ่าน [ข้อจำกัด](KNOWN_ISSUES.md) และเก็บบันทึกตรวจแยกจากบทความ
