# Research Humanizer v2.3.3 upgrade review

> บันทึกต่อท้ายสถานะวันที่ 17 พฤศจิกายน 2026 ผู้ดูแลอนุมัติให้นำชุดนี้ขึ้น main แล้ว รายงานด้านล่างเก็บสถานะเดิมของช่วงเตรียม candidate ไว้ ดู [บันทึกการเผยแพร่](VERIFICATION.md) และผล workflow สำหรับสถานะล่าสุด


**สถานะ Unpublished review candidate**

พัฒนาบนสำเนาที่ตรงกับ v2.3.2 ที่ commit `dc9819514ea24abea5e924d9545de6b3ebfbe709` และ Git tree `1e7dd35abf8e52e3e53392b61841764b46f0416e` ไม่ได้ push สร้าง tag เผยแพร่ GitHub Release หรือ deploy เว็บไซต์

ขยาย `research-paper-craft` เดิม ไม่เพิ่ม skill หรือ pipeline ใหม่ ชื่อ plugin และคำสั่งเดิมยังใช้ต่อได้ บันทึกก่อนแก้อยู่ใน [Architecture audit](plans/v2.3.3-architecture-audit.md)

## 1. Existing vs new capabilities

| ส่วน | สิ่งที่มีอยู่ใน v2.3.2 | สิ่งที่เพิ่มในฉบับนี้ |
| --- | --- | --- |
| Research Gap | แยกปัญหาหน้างานจากช่องว่างและมีขั้นค้นวรรณกรรม | ตรวจสิ่งที่รู้ สิ่งที่ยังไม่รู้ งานใกล้ที่สุด หลักฐาน ความสำคัญ และความสามารถของงานที่จะตอบ แยก Gap existence จาก Gap closure |
| Originality | เชื่อม Contribution กับหลักฐานและจำกัดคำว่า first | เทียบความรู้ที่เพิ่มกับงานเดิม ตรวจการเปลี่ยนเครื่องมือหรือบริบท และรองรับคุณค่าของ replication กับผลเชิงลบ |
| Impact | จำกัดนัยของผลและการอ้างข้ามบริบท | แยกด้านความรู้ วิธี และการใช้จริง พร้อมแยก Expected จาก Demonstrated |
| RQ alignment | มี Paper map การตรวจแบบวิจัย หน่วยอิสระ และ Metric plan | ตรวจทุก RQ ผ่านวิธี ข้อมูลหรือข้อพิสูจน์ การวิเคราะห์ และ Findings โดยเลือกเกณฑ์ตามประเภทงาน |
| Evidence to findings | มีประเภทหลักฐาน ตัวเลขย้อนกลับ และตัวตรวจ revision | ตรวจผลสังเกต ผลคำนวณ การตีความ สมมติฐาน และข้อกล่าวอ้างที่ยังไม่มีหลักฐาน พร้อมจัดประเภทปัญหา |
| Feedback | มี Decision log และบริบทผู้เขียน | แบ่งความเห็นสี่ประเภท ตรวจขอบเขตและข้อยกเว้นก่อนบันทึกหลักการใช้ซ้ำ |
| Humanizer | สำนวนวิจัย การรักษาความหมาย และเครื่องหมายตามบริบท | คงกฎเดิม งานแก้ภาษาอย่างเดียวไม่เปิดการตรวจวิจัยเต็มชุด |
| Full paper และ ARS | มีโหมดและ handoff เดียว | เพิ่มเกณฑ์วิจัยในขั้นวางแผน ตรวจหลักฐาน และ review ของกระบวนการเดิม |
| ตัวตรวจบันทึก | ตรวจ full-paper JSON schema 1 แบบไม่แก้ไฟล์ | รองรับ `reasoning_review` แบบสมัครใจ ตรวจข้อมูลที่ประกาศว่าขัดกันหรือขาดหรือไม่ |

## 2. Files changed

รายการเต็มพร้อมค่าแฮชอยู่ใน [บันทึกตรวจ v2.3.3](verification/release-v2.3.3.json)

| กลุ่ม | ไฟล์สำคัญและเหตุผล |
| --- | --- |
| คู่มือใหม่ | `references/research-reasoning.en.md` และ `.th.md` เพิ่ม R48–R50 ส่วน `research-reasoning-records.md` อธิบายฟิลด์เสริมเมื่อใช้ตัวตรวจ |
| จุดเรียกคู่มือ | `SKILL.md` และส่วนเกริ่นของ paper, literature, evidence, evaluation, full-paper, ars-integration, records ทั้งสองภาษา |
| แบบบันทึกเดิม | `assets/qa-report.md` เพิ่มตารางและสรุป audit ส่วน `assets/ars-handoff.md` ส่งต่อเกณฑ์และเรื่องที่รออนุมัติ |
| เครื่องมือ | `scripts/audit_full_paper.py` ตรวจส่วนเสริมเมื่อมีเท่านั้น ไม่เพิ่ม CLI หรือพึ่งพาแพ็กเกจใหม่ |
| คำสั่ง ARS | `commands/research-full.md` เพิ่มเกณฑ์ในขั้นเดิม ไม่เปลี่ยนเจ้าของ workflow |
| ชุดทดสอบ | `tests/test_research_reasoning_contract.py` และ `skills/research-paper-craft/tests/test_research_reasoning.py` |
| การประเมินโมเดล | `evals/research-reasoning-scenarios.md` เป็นแผน 14 สถานการณ์ที่ยังไม่ได้รัน |
| เอกสารและรุ่น | README ไทยและอังกฤษ, CHANGELOG, QUALITY, KNOWN_ISSUES, VERIFICATION, VERSION, manifest ทั้งสองระบบ, บันทึกที่มาและ checksum |
| เว็บไซต์ในสำเนา | อัปเดตเฉพาะ `softwareVersion` ในข้อมูลโครงสร้างให้ตรง candidate ไม่ได้ deploy หน้าเว็บ ปุ่มดาวน์โหลดยังคงชี้รุ่นที่เผยแพร่แล้ว |

ไม่ได้แก้เนื้อหา Humanizer ต้นทาง กฎสำนวนและเครื่องหมายเดิม คู่มือ Word สคริปต์ตรวจอีกสี่ตัว หรือ Header ของ CSV เดิม ตัวเลขรุ่นในไฟล์ประวัติการทดสอบไม่ถูกเขียนทับ

## 3. Rules added or modified

เพิ่มสามกฎในโมดูลที่อ่านเมื่อจำเป็น

| กฎ | หน้าที่ |
| --- | --- |
| R48 | ตรวจ Gap, Originality, Impact, RQ alignment, Evidence-to-finding และ Contribution/Limitations ตามประเภทงาน |
| R49 | แปลง Feedback เป็นข้อเสนอที่ตรวจที่มา เหตุผล ขอบเขต ข้อยกเว้น และการอนุมัติก่อนบันทึกใช้ซ้ำ |
| R50 | ใช้บันทึกเดิม แยกสถานะหลักฐานจากสถานะรันตรวจ และกำหนดรายงาน audit |

เนื้อหากฎเดิม R00–R47 ไม่เปลี่ยน ส่วนที่ปรับคือคำสั่งเรียกคู่มือและเส้นทางส่งงาน หลักฐานของงานต้องมาจากแหล่งที่อ่านจริง ความลื่นไหลของภาษาไม่ทำให้ข้อกล่าวอ้างกลายเป็นจริง

สถานะหลักฐานมี Verified, Partially Supported, Unverified, Proposed, Contradicted และ Not Applicable ส่วน Passed, Failed และ Not Run ใช้กับการดำเนินการ ไม่ใช่หลักฐานความถูกต้องของข้อสรุป

การเก็บ Feedback ใช้ Decision log เดิม โดยแยก Universal Research Principle, Domain-Specific Principle, Project-Specific Correction และ Unverified Recommendation ความเห็นจากผู้เชี่ยวชาญคนเดียวไม่กลายเป็นหลักสากลอัตโนมัติ ไม่คัดลอกความเห็นลับหรือข้อมูลผู้เข้าร่วมไปเผยแพร่สาธารณะ

## 4. Compatibility with ARS and existing records

ARS ยังเป็นเจ้าของลำดับงานและสถานะ เพิ่มเกณฑ์ผ่าน handoff ที่ใช้อยู่ รักษาจุดยืนยันของผู้วิจัยและไม่เริ่มกระบวนการอีกชุด ไม่มีการอ้างว่าการประสานงานจริงระหว่าง agent ผ่านการทดสอบแล้ว

ไฟล์ schema 1 ที่ไม่มี `reasoning_review` ยังคงใช้ API และ CLI เดิม ได้รูปแบบผลรายงานเดิม ไม่บังคับแก้ `full-paper-run.json` หรือย้าย CSV งาน scientific audit แบบอ่านอย่างเดียวใช้ QA report เดิมได้โดยไม่ต้องสร้าง full-paper record

ส่วนเสริมที่กรอกครบยังเป็นเพียงคำประกาศ ตัวตรวจไม่เปิดไฟล์หรือ URL ที่อ้าง ไม่คำนวณผลใหม่ และไม่ตรวจความหมายของ paper โดยอัตโนมัติ ผลรายงานยังคง `scientific_verification = not_performed_by_this_tool` และ `submission_approved = false`

## 5. Test results

ผลที่รันจริงอยู่ใน [VERIFICATION](VERIFICATION.md) และ [บันทึก JSON](verification/release-v2.3.3.json) พร้อมคำสั่งและสภาพแวดล้อม

ก่อนแก้ ฐาน v2.3.2 ผ่าน 387 ข้อ ชุดทดสอบบันทึกใหม่ 34 ข้อพบ 21 ข้อไม่ผ่านเมื่อใช้ตัวตรวจเดิม ส่วน static contracts ใหม่ 11 ข้อพบ 9 ข้อไม่ผ่าน ก่อนเพิ่มเงื่อนไขขอบเขตอีก 10 ข้อได้ตรวจพบปัญหา 4 ข้อเพิ่มเติมในโค้ดระหว่างพัฒนา

หลังแก้ ชุดทดสอบมี repository 82 ข้อ เครื่องมือและ skill 355 ข้อ และกรณีบั๊กเก่า 5 ข้อ รวม 442 ข้อ ดูผลสุดท้ายและผลจาก ZIP/patch ในบันทึกการตรวจ ไม่ตีความจำนวนข้อเป็นคะแนนคุณภาพการวิจัย

การทดสอบที่ครอบคลุมมี unsupported novelty, Gap ไม่มีวรรณกรรม, RQ ไม่มีข้อมูลที่เหมาะ, metric ขาดนิยามหรือเหตุผล, ความสัมพันธ์ถูกอ้างเป็นเหตุผล, expected impact ถูกอ้างว่า demonstrated, finding ขัด result, replication และผลเชิงลบ, งานเชิงคุณภาพและทฤษฎี, scientific revision ที่ไม่มีอนุมัติ, lightweight routing และ ARS owner เดียว

**Not Run** สำหรับการประเมินโมเดลอิสระ การร่าง paper จริงครบกระบวนการด้วย ARS/Claude/Codex และการเปิดตรวจหรือซ่อม Word จริง ชุดทดสอบคำสั่งเป็น static checks ไม่ใช่การสังเกต agent ทำตามจริง

## 6. Remaining limitations

การตรวจคุณภาพทางวิทยาศาสตร์ยังต้องเปิดอ่านแหล่งจริงและใช้เกณฑ์ที่เหมาะกับสาขา ตัวตรวจบันทึกไม่สามารถรับรองความใหม่ ความเพียงพอของกลุ่มตัวอย่าง ความตรงของการวัด ความถูกต้องของบทพิสูจน์ หรือความสัมพันธ์เชิงเหตุผล การมี locator ไม่ได้ยืนยันว่าเอกสารนั้นมีอยู่หรือรองรับข้อความ

สถานะ Verified ใช้ได้เฉพาะข้อความที่มีหลักฐานรองรับในขอบเขตที่บันทึก ไม่ใช่ความจริงสากลหรือการรับรองพร้อมตีพิมพ์ การปิดช่องว่างต้องมีหลักฐานเพียงพอ ไม่ใช่การกรอกทุกช่อง ชุดทดสอบผ่านก็ยังไม่ยืนยันคุณภาพสำนวนหรือการยอมรับของวารสาร

ค่าความสำคัญ Critical, Major และ Minor ช่วยเรียงงานแก้ ไม่ใช่คะแนนคุณภาพที่ผ่านการตรวจความเที่ยงตรง แผนประเมินพฤติกรรม 14 สถานการณ์ยังไม่ใช่ผลทดลอง

## 7. Examples of using the upgraded skill

คำสั่งต่อไปนี้ใช้ชื่อเดิม หลังติดตั้งหรือโหลดสำเนา candidate นี้ในเครื่องแล้ว การอัปเดตจาก marketplace ตอนนี้ยังไม่ดึง v2.3.3 เพราะยังไม่ได้เผยแพร่

### ตรวจเหตุผลวิจัยโดยไม่แก้ต้นฉบับ

```text
/research-humanizer:research-paper-craft
ใช้โหมด audit ตรวจ Research Gap ความใหม่ Impact และเส้นทาง RQ ถึง Findings
อ่านงานใกล้เคียงกับหลักฐานจริงก่อนตัดสิน
รายงานตาราง Issue, Evidence, Why It Matters, Recommended Fix, Status, Priority
ตามด้วยสรุปหกส่วนตามคู่มือ research-reasoning
ห้ามแก้ไฟล์หรือเปลี่ยนคำถามวิจัย
```

### ร่างบทความทั้งฉบับกับ ARS

```text
/research-humanizer:research-full
ร่างบทความทั้งฉบับจากโปรเจกต์นี้ร่วมกับ ARS
ใช้ Humanizer ตั้งแต่ร่างแรก
ตรวจ Gap และ RQ ตอนวางแผน ตรวจวิธีกับหลักฐานก่อนอ้างผล
ตรวจ Findings Contribution และ Impact ในขั้น Review
ใช้ workflow และ handoff เดิม เก็บจุดยืนยันของผู้วิจัย
```

### เกลาภาษาโดยไม่เปิดการตรวจเต็มชุด

```text
/research-humanizer:research-paper-craft
ใช้โหมด revise เกลาภาษาเฉพาะย่อหน้านี้
ไม่เปิด scientific audit เต็มชุด
รักษา RQ วิธี ผล Contribution และระดับความแน่ใจ
หากพบปัญหาวิทยาศาสตร์ ให้รายงานแยกและถามก่อนแก้สาระ
```

### ตรวจ Feedback จากอาจารย์

```text
/research-humanizer:research-paper-craft
จำแนก Feedback ที่แนบตาม research-reasoning
ใช้ Decision log เดิม เก็บเหตุผล ที่มา ขอบเขต และข้อยกเว้น
อย่ายกระดับความเห็นเฉพาะงานเป็นกฎทั่วไป
เสนอการแก้คู่มือหรือไฟล์ความรู้ให้ตรวจ แต่ยังไม่ commit หรือ push
```

### ตรวจบันทึกแบบอ่านอย่างเดียว

```bash
python -B skills/research-paper-craft/scripts/audit_full_paper.py full-paper-run.json --json
```

ไฟล์ต้องเป็น full-paper schema 1 เดิม ส่วน `reasoning_review` เป็นตัวเลือก ดู [สัญญาฟิลด์](../skills/research-paper-craft/references/research-reasoning-records.md) ตัวตรวจไม่สร้าง scientific-audit table ให้เอง Agent ต้องสร้างตารางจากหลักฐานที่ตรวจจริง

## ใช้แพ็กเกจนี้ก่อนเผยแพร่

แตก ZIP ลงโฟลเดอร์ใหม่ อย่าเขียนทับ repository ที่มีงานค้าง หรือแทน plugin ที่ใช้งานอยู่โดยไม่สำรอง เปรียบเทียบ diff ก่อนนำเข้า การสั่งให้ AI อ่าน `skills/research-paper-craft/SKILL.md` จากสำเนานี้เป็นการทดสอบในเครื่อง ไม่ใช่การอัปเดต marketplace

Patch ใช้กับ baseline commit ที่ระบุด้านบน ให้ตรวจว่า working tree สะอาดและรันจาก root ของ repository

```bash
git apply --check /path/to/research-humanizer-v2.3.3.patch
git apply /path/to/research-humanizer-v2.3.3.patch
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s skills/research-paper-craft/tests -v
python -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

อย่า push รุ่นนี้ไป main จนกว่าจะอนุมัติการเผยแพร่ด้วย เพราะ workflow เดิมตั้งให้สร้าง Release เมื่อ VERSION เปลี่ยนบน main รอบนี้คง workflow เดิมไว้ ไม่แก้พฤติกรรมการเผยแพร่โดยพลการ
