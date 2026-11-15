> [!IMPORTANT]
> Repository documentation edition, 2026-11-15. Core v2.0 instructions and checker code are unchanged. Read [KNOWN_ISSUES.md](KNOWN_ISSUES.md) before relying on the checker. Five targeted audit regressions remain open. MIT and upstream notices are included in [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

# Research paper craft 2.0

## ใช้แพ็กเกจนี้ชุดเดียว

ชุดนี้ใช้แทน v1.1 ได้ ไม่ต้องติดตั้งไฟล์รวมไทยและอังกฤษเพิ่ม และไม่ควรเปิดใช้สองเวอร์ชันพร้อมกัน

หากระบบรองรับการนำเข้า skill ด้วย ZIP ให้นำเข้า ZIP นี้ หากระบบใช้โฟลเดอร์ skills ให้แตกไฟล์แล้ววางโฟลเดอร์ `research-paper-craft` ทั้งโฟลเดอร์ไว้ในตำแหน่ง skills ของระบบนั้น เก็บโครงสร้างภายในไว้ครบ

ไฟล์ [SKILL.md](SKILL.md) คือจุดเริ่มของ AI คู่มือ 8 หมวดใน `references` มีทั้งไทยและอังกฤษ แต่กำหนดให้อ่านภาษาเดียวและอ่านเฉพาะช่วงงานที่ต้องใช้ ภาษาในคู่มือไม่ได้บังคับภาษาของบทความ

ทดสอบการเรียกใช้ด้วยข้อความนี้

```text
ใช้ skill research-paper-craft กับไฟล์ที่แนบเพื่อเขียนบทความวิจัย
อ่านคำสั่งหลักและเปิดคู่มือเฉพาะส่วนที่กำลังทำ
ตรวจไฟล์และคำตอบเดิมก่อนถาม
หากขาดข้อมูลหรือภาพจริงที่จำเป็น ให้ถามผมก่อนว่ามีต้นฉบับหรือไม่
ห้ามเดาหรือใช้สิ่งอื่นแทนเอง
แยกต้นฉบับออกจากรายงานสิ่งที่ตรวจแล้วและสิ่งที่ยังค้าง
```

การแนบเฉพาะ SKILL.md โดยไม่มีไฟล์คู่มือไม่เท่ากับติดตั้งแพ็กเกจนี้ครบ ระบบต้องอ่านไฟล์ที่อ้างถึงได้ด้วย การนำเข้า ZIP และตำแหน่งติดตั้งขึ้นกับเครื่องมือที่ใช้งาน ไม่ได้อ้างว่าทดสอบติดตั้งแล้วในบัญชีหรือเครื่องของผู้ใช้

## English quick start

Use this package instead of version 1.1. Import the ZIP if the host supports skill ZIP import. Otherwise extract the complete `research-paper-craft` folder into that host's configured skills directory. Keep the relative paths intact. Do not activate both versions.

Invoke `research-paper-craft` with the actual project files and requested deliverable. SKILL.md is the entry point. Guidance is available in Thai and English. Read one language of the relevant module at the appropriate phase. Reading the instructions does not require producing a bilingual manuscript.

The host must support reading bundled reference files. Attaching only SKILL.md does not supply those references. Host installation and model behavior still require testing in the actual environment.

## สิ่งที่อยู่ในชุด

| ส่วน | หน้าที่ |
| --- | --- |
| SKILL.md | กฎหลักและการเลือกคู่มือ |
| references | คู่มือ 8 หมวด แยกไทยและอังกฤษ |
| assets | แบบบันทึกโจทย์และรายงานตรวจที่ยังไม่กรอกผล |
| scripts | ตัวตรวจข้อความแบบอ่านอย่างเดียว |
| tests | การทดสอบเครื่องมือ โครงสร้างแพ็กเกจ และโจทย์ทดสอบโมเดล |
| provenance | ไฟล์ต้นทางและบันทึกที่มา ไม่ใช่คำสั่งให้โหลดทุกงาน |

## Optional records

Use [assets/project-brief.yaml](assets/project-brief.yaml) only when establishing or updating the brief. Fill from existing files and decisions first. Unknown values stay unknown.

Use [assets/qa-report.md](assets/qa-report.md) when recording applicable verification. It is an unfilled template, not a completed audit. Working-record fields are in the records module.

## Optional text checker

Requires Python 3.10 or newer. It uses only the standard library and does not edit manuscript files. Run from the skill directory. Use the actual manuscript path.

```bash
python scripts/lint_manuscript.py manuscript.md --json
python scripts/lint_manuscript.py manuscript.md --fail-on-findings
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

The environment-variable prefix on the test command is for POSIX shells. On other shells, run `python -B -m unittest discover -s tests -v`.

The checker flags common prose punctuation, contractions, draft markers, HTML comments, and quotations needing review. It preserves common code, YAML frontmatter, URLs, mathematical notation, and reference sections. It is a heuristic scanner, not a complete Markdown or LaTeX parser. Review every finding. Some valid strings may be flagged and some defects may be missed.

It does not verify numerical provenance, citations, scientific validity, statistical assumptions, symbol meaning, scientific image integrity, authorship, anonymity, or page layout. It cannot open Word or inspect DOCX metadata. A clean report is not scientific or submission approval. Do not lint the instruction guides as though their examples were manuscript prose.

## การตรวจรุ่นนี้

ดูผลที่รันจริงใน [tests/verification-report.md](tests/verification-report.md) และ [tests/unit-test-results.txt](tests/unit-test-results.txt)

การทดสอบโครงสร้างและตัวตรวจข้อความไม่ใช่การทดสอบว่าโมเดลปฏิบัติตามกฎครบทุกข้อ โจทย์ใน [tests/acceptance-scenarios.md](tests/acceptance-scenarios.md) ยังต้องทดลองกับโมเดลและระบบที่ใช้งานจริง

## Changes and origin

Version 2.0 replaces the monolithic-guide loading rule with eight task-specific modules. R00 through R30 are preserved from both version 1.1 guides. R31 and the historical source notes are retained separately in provenance. The missing-input requirement remains directly in SKILL.md.

The uploaded humanizer source is preserved unchanged with its original license metadata. Its original instructions are historical material and do not override this skill. House style is the user's requirement, not a universal publishing standard. See [provenance/change-notes.md](provenance/change-notes.md) for packaging references and verification scope.
