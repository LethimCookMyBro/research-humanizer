# Grounded openings and concise research writing

Status: unpublished local amendment to the v2.3.3 payload at commit `664cf952cfa6854ccf4fcc67145e4b9492226207`. No release version was assigned. No remote files were changed.

## Architecture audit

| Requirement | Present before this amendment | Specific addition |
| --- | --- | --- |
| An engaging opening without invented facts | R10 already asks for concrete problems and forbids invented statistics and stories | A reader check and a traceable premise. Check the opening promise against what the study actually addresses |
| Research substance | R06 and R48 already connect questions, evidence and contributions | Distinguish a research argument from a feature inventory or development diary. Keep methods detail needed for replication |
| Concision | R07 and R08 already prefer complete short sentences and remove filler | A task-scoped compression pass. Remove duplication before losing evidence and record necessary relocation |
| Suitable length | R06 already uses the actual template and a provisional budget | No universal word count, forced reduction percentage or font shrinking to meet the target |
| Scope and meaning | Existing claim/revision ledgers already preserve meaning and uncertainty | Explicitly preserve denominators, exclusions, proof assumptions, qualitative interpretive procedure and citation attachment |
| Existing useful writing | Minimal editing and unchanged controls already exist | An adequate opening may remain unchanged. Interestingness is not a reason to invent drama |

No new skill, script, pipeline, claim ledger or quality score is introduced. Guidance is inserted before the frozen numbered rules in the existing paper module. Writing links to it only for opening/length work. Original numbered rule bodies remain unchanged. Examples O01 to O03 are authored synthetic fixtures in both languages, not real study evidence or observed model responses.

## Proposed operating checks

The opening should help the intended reader identify the concrete research object and the reason to examine it. The reason must be supported or explicitly framed as a question or expected implication. The paper need not begin with a statistic, a surprise or a dramatic story.

Keep the scale of the opening consistent with the evidence. A study of reported preferences does not establish improved learning, safety or deployment benefit. Broad context is permitted when the actual studied population and scope become clear. An overbroad promise should be narrowed rather than completed through selective reporting.

Shortening is an information-preservation task. Remove redundant explanation and unrelated history before cutting method definitions, adverse findings, uncertainty or reproducibility detail. Supplementary material is an option only when the venue allows it and the supplement is actually delivered. A decisive limitation must not be hidden there.

Keep implementation information that defines or justifies the research. Do not turn the paper into a product description. Do not erase implementation detail that allows replication. Qualitative and theoretical papers use appropriate evidence rather than a mandatory quantitative template.

## Remaining gaps and limits

| Issue | Evidence in the inspected project | Practical next step | Status |
| --- | --- | --- | --- |
| Whether readers actually find the opening clearer | Existing evaluation records explicitly do not report independent model/reader results | Compare matched old/new outputs with supplied sources. Have readers describe the question, motivation and actual evidence. Record misunderstandings rather than inventing an engagement score | Not Run |
| Meaning lost during compression | `review_revision.py` checks selected lexical signals and disclaims semantic equivalence | Evaluate omitted conditions, denominator changes, lost uncertainty and citation scope with source-level review | Procedure strengthened, outcome not demonstrated |
| Cross-section consistency in generated full papers | Existing paper map is a procedure, not evidence of an executed whole-paper review | Inspect title, abstract, Introduction and conclusion against the same result and argument records after final assembly | Required review, runtime outcome unverified |
| Cross-discipline and bilingual behavior | Thai/English guides exist but broad agent evaluation is not established | Include theoretical, qualitative, replication and negative-result papers. Judge each against its actual article type and sources | Not Run |
| ARS handoff and actual Word layout | Existing integration/Word documents disclose these limits | Run a real host workflow with authorized project files, then inspect the saved artifact. Do not infer success from static tests | Not Run |
| Publication-status wording in older documents | Published v2.3.3 `docs/QUALITY.md` still has an “unpublished” section heading and the skill README ends “This candidate is not published.” | In a separate publication cleanup, distinguish the archived candidate stage from the released plugin. Historical verification records should not be rewritten as later executions | Observed documentation issue, not changed here |

## Verification boundary

The local baseline came from the supplied v2.3.3 candidate. Its skill README title was aligned with the inspected published version before forming the patch base. The complete payload was checked against the published SHA256SUMS identity. All seven modified existing payload files have base Git blob hashes matched to the pinned GitHub commit. Root documentation not touched by this patch was not represented as a fresh remote checkout.

The eight new static tests first failed against the baseline instructions and then passed after the amendment. These are checks for instruction content, routing and examples. They do not demonstrate that an AI follows the instructions. Existing software tests and all numbered rule bodies remain intact. Verification details and run logs are provided alongside this patch.

No model, reader, live host, native Word or new GitHub CI evaluation was executed. There is no measured improvement in interest, naturalness or publication readiness.

## Reading used for the review

The controlling requirements are the user's research-writing instructions and the repository's existing rules. The following source supplies editorial background, not a validated quality scale or a universal manuscript template.

Mensh B, Kording K. Ten simple rules for structuring papers. PLOS Computational Biology. 2017;13(9):e1005619. https://doi.org/10.1371/journal.pcbi.1005619. Inspected the HTML article on 18 November 2026, especially the sections on reader needs, the Introduction and allocating writing effort. It supports attention to a central question and the reader's ability to follow the evidence. Its prescribed structures are not imposed on all disciplines here.

The original bundled Humanizer supports removing staged openings while retaining source claims and varying sentence structure. Its exact original file is unchanged. Search results for Nature editorials were checked, but the opened pages exposed only previews. No inaccessible full-text guidance was treated as inspected evidence.

## สรุปภาษาไทย

เพิ่มขั้นตรวจในคู่มือเดิม ให้บทเปิดน่าสนใจจากปัญหาและคำถามที่มีหลักฐาน ไม่แต่งสถิติหรือประโยชน์ให้ดูสำคัญ เนื้อหาต้องอธิบายข้อค้นพบและวิธีที่รองรับ ไม่กลายเป็นรายการคุณสมบัติของระบบ

เมื่อลดความยาว ให้ตัดคำซ้ำและพื้นหลังที่ไม่ช่วยตอบคำถามก่อน ห้ามตัดตัวหาร เกณฑ์คัดออก ความไม่แน่นอน ผลขัดแย้ง หรือรายละเอียดที่ทำซ้ำจำเป็น ไม่กำหนดว่าทุกบทความต้องสั้นเท่ากัน

นี่เป็นชุดแก้ไขสำหรับตรวจทาน ไม่ใช่รุ่นที่เผยแพร่แล้ว เวอร์ชันใน marketplace ยังไม่เปลี่ยน การผ่านชุดทดสอบหมายถึงคำสั่งและโปรแกรมยังตรงตามข้อกำหนดที่ทดสอบ ไม่ได้พิสูจน์ว่า paper อ่านดีขึ้นแล้วในสายตาผู้วิจัย
