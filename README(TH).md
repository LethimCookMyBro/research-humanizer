<div align="center">

# Research Humanizer

**Clear research writing. Traceable claims. Real evidence.**

[![Version](https://img.shields.io/badge/version-2.3.2-2563eb?style=flat-square)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-0f766e?style=flat-square)](LICENSE)
[![Languages](https://img.shields.io/badge/guides-English%20%2B%20Thai-475569?style=flat-square)](skills/research-paper-craft/SKILL.md)
[![Status](https://img.shields.io/badge/status-preview-b45309?style=flat-square)](docs/KNOWN_ISSUES.md)

<a href="README.md">English</a> · <a href="README%28TH%29.md">ภาษาไทย</a>

[Install](#install) · [Use](#use) · [Scope](#scope) · [Validation](#validation)


**[เว็บไซต์โครงการ](https://research-humanizer.vercel.app/th/)** · [Release v2.3.2](https://github.com/LethimCookMyBro/research-humanizer/releases/tag/v2.3.2)

</div>

**2.3.2** เพิ่มการตรวจจุด อัญประกาศ และอักขระแฝงตามบริบท ครอบคลุมกรณีที่หลุดทั้งเจ็ดข้อจากการตรวจเดิม โดยรักษาสูตรและไม่แก้ไฟล์อัตโนมัติ [สิ่งที่แก้](docs/releases/v2.3.2.md) · [ผลตรวจ](docs/VERIFICATION.md)



Skill สำหรับให้ AI ร่าง paper ทั้งฉบับใน Claude Code และ Codex ใช้คู่กับ `ars-full` ของ ARS เพื่อกำกับสำนวนวิจัยตั้งแต่ร่างแรก ผ่านการค้นงานอ้างอิง เลือก metric สร้างภาพ และตรวจไฟล์สุดท้าย ใช้ได้กับผู้วิจัยหลายคนและหลายสาขา พร้อมบริบทผู้เขียนแบบส่วนตัวเมื่อมี ยังใช้แก้ต้นฉบับหรือตรวจอย่างเดียวได้

> [!IMPORTANT]
> ขาดต้นฉบับต้องถามผู้วิจัย ประโยคที่ฟังน่าเชื่อ ภาพห้องทดลองที่สร้างขึ้น และเส้นกราฟที่ดูดี ใช้แทนหลักฐานไม่ได้

**2.3.0** เพิ่ม full-paper ตัวประสาน ARS ขั้นค้นงานและแม่แบบ แผน metric ที่เชื่อมกับข้อมูลจริง และบริบทผู้เขียนแยกต่อโครงการ โดยเก็บกฎ Humanizer กราฟ สมการ หลักฐาน และ Word เดิมครบ [การเชื่อมระบบและข้อจำกัด](docs/INTEGRATION.md)

**2.3.1** เพิ่มการตรวจลูกน้ำและสัญลักษณ์ตามบริบท แบ่งประโยคตามความหมายโดยรักษาสูตรและตัวเลข คำเตือนใหม่ต้องทบทวน ไม่ลบอัตโนมัติ [คู่มือเครื่องหมาย](skills/research-paper-craft/references/punctuation.th.md) · [บันทึกรุ่น](docs/releases/v2.3.1.md)

<a id="install"></a>
## ติดตั้ง

### Claude Code

พิมพ์ในช่องแชต Claude Code ทีละคำสั่ง

```text
/plugin marketplace add LethimCookMyBro/research-humanizer
/plugin install research-humanizer@research-humanizer
```

จากนั้นเรียก skill

```text
/research-humanizer:research-paper-craft ร่าง paper ทั้งฉบับจากข้อมูลนี้ ใช้สำนวนวิจัยตั้งแต่ย่อหน้าแรก และถามเมื่อขาดหลักฐาน
```

### Codex CLI

รันใน terminal ไม่ใช่ช่องแชต

```bash
codex plugin marketplace add LethimCookMyBro/research-humanizer
codex plugin add research-humanizer@research-humanizer
```

เปิด session ใหม่และตรวจการติดตั้งด้วย `/plugins` เลือก `research-paper-craft` ด้วย `$` หรือสั่งให้ Codex ใช้ skill นี้ ชื่อ plugin คือ `research-humanizer` ส่วน skill คือ `research-paper-craft` ต้องมี host ที่รองรับ plugin และ Git ใช้ Python 3.10 ขึ้นไปเฉพาะเมื่อต้องรันตัวตรวจ ชุดนี้ไม่เพิ่ม hook หรือ MCP server

<details>
<summary><strong>อัปเดต ย้ายจากฉบับเดิม และติดตั้งแบบ skill เดี่ยว</strong></summary>

อัปเดต Claude Code จาก terminal

```bash
claude plugin marketplace update research-humanizer
claude plugin update research-humanizer@research-humanizer
claude plugin list
```

รีเฟรช marketplace ของ Codex

```bash
codex plugin marketplace upgrade research-humanizer
```

ตรวจเวอร์ชันที่ติดตั้งใน `/plugins` แล้วเปิด session ใหม่ การรีเฟรชรายการหรือ push GitHub ไม่ได้ยืนยันว่าสำเนาที่ติดตั้งเปลี่ยนแล้ว หากแอปยังแสดงเวอร์ชันเก่าให้ตรวจว่าแอปกับ CLI ใช้บัญชีและชุดการตั้งค่าเดียวกัน สำรองสิ่งที่แก้เองก่อนติดตั้งใหม่ ห้ามลบโฟลเดอร์การตั้งค่าทั้งชุด

ติดตั้งแบบ skill เดี่ยวได้โดยคัดลอกโฟลเดอร์ `skills/research-paper-craft` ทั้งชุดไปไว้ใน `~/.claude/skills/` หรือ `~/.agents/skills/` หรือโฟลเดอร์โปรเจกต์ที่ตรงกัน อย่าเปิดสำเนาเดี่ยวกับ plugin ซ้ำกัน เก็บคู่มือ สคริปต์ และข้อความสิทธิไว้ครบ

</details>

คำสั่งอ้างอิง [คู่มือ Claude plugin](https://code.claude.com/docs/en/discover-plugins) และ [คู่มือ Codex CLI](https://learn.chatgpt.com/docs/cli/reference) การติดตั้งผ่านโปรแกรมจริงยังไม่ได้ทดสอบในสภาพแวดล้อมพัฒนานี้

<a id="use"></a>
## เริ่มใช้

```text
ใช้ research-paper-craft กับไฟล์ในโปรเจกต์นี้
ใช้โหมด full-paper ร่างทุกส่วนที่เกี่ยวข้อง ไม่ใช่เพียงโครงร่าง
ตรวจสิ่งที่ทำจริง แล้วค้นงานใกล้เคียง ข้อกำหนดแหล่งตีพิมพ์ และนิยามตัวชี้วัด
ใช้บริบทสำนวนที่ผู้เขียนยอมรับและที่เข้าถึงได้จริง ห้ามแต่งความจำ
เขียนตามสำนวนวิจัยตั้งแต่ร่างแรกและรักษาศัพท์ที่ตกลงไว้
เทียบข้อกล่าวอ้างที่แก้กับแหล่งจริง รวมขอบเขตและความไม่แน่นอน
ใช้ต้นฉบับจริงกับภาพหลักฐาน และข้อมูลที่ตรวจแล้วกับกราฟ
ให้กล่องและลูกศรในภาพรวมตรงกับวิธีจริง
ถามผมเมื่อข้อมูลของงานขาด ห้ามหาสิ่งอื่นแทนเอง
เก็บ Word ต้นฉบับและแก้บนสำเนา
แยกบทความออกจากรายงานตรวจ
```

### ตัวอย่างการแก้ที่มีหน้าที่

*ตัวอย่างสำหรับสอน ไม่ใช่ผลทดสอบโมเดล* บันทึกต้นทางระบุเพียงว่าวิธีนี้รวมข้อมูลเซนเซอร์ ยังไม่มีผลประเมิน

| ร่าง | ฉบับที่มีหลักฐานรองรับ |
| --- | --- |
| ระบบอัจฉริยะนี้พลิกโฉมวงการด้วยสมรรถนะเหนือชั้นในการรวมข้อมูลเซนเซอร์ | วิธีนี้รวมข้อมูลเซนเซอร์ |

ข้ออ้างด้านประสิทธิภาพต้องถูกแจ้งว่ายังไม่มีหลักฐาน ไม่ถือว่าจริงเงียบ ๆ ประโยคที่ชัดอยู่แล้ว เช่น “ตัวบันทึกเก็บการกระทำและสถานะชิ้นงาน” คงไว้ได้

### ร่างทั้ง paper ร่วมกับ ARS

ติดตั้ง ARS แยกใน Claude Code ต้นทางใช้ **CC BY-NC 4.0** ส่วน MIT ของเราไม่เปลี่ยนสิทธิ dependency นั้น แพ็กเกจนี้ไม่คัดลอกหรือติดตั้ง ARS ให้เอง

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

เมื่อโหลดทั้งสอง plugin แล้ว เรียกตัวประสานงานใหม่ใน Claude Code

```text
/research-humanizer:research-full ใช้ ARS ร่าง paper ทั้งฉบับจากสิ่งที่ทำจริงในโปรเจกต์ ใช้ research-paper-craft ตั้งแต่ร่างแรก ค้น paper ต้นทาง ข้อกำหนดแหล่งตีพิมพ์ และนิยาม metric ถามเมื่อขาดต้นฉบับและรักษาจุดยืนยันของ ARS
```

หรือใช้จุดเริ่ม `ars-full` เดิม

```text
/academic-research-skills:ars-full ร่างบทความให้ครบทุกส่วนที่เกี่ยวข้อง โหลด research-humanizer:research-paper-craft ก่อน แล้วส่งข้อกำหนด full-paper วรรณกรรม สำนวน ภาพจริง และ Word-first ให้ writer reviewer และ formatter ทุกตัว
```

ตัวประสานงานโหลด ARS ที่ติดตั้งจริง ไม่ใช่สำเนาที่เขียนเลียนแบบ เมื่อไม่มี ARS ต้องหยุดส่วน ARS ระบบนี้เชื่อมผ่านคำสั่ง ไม่ใช่ hook บังคับ และยังรักษาจุดยืนยันของผู้วิจัย ไม่ส่งบทความเองหรือแต่งการทดลองให้เสร็จจากหัวข้อเพียงอย่างเดียว

สำหรับ Codex ให้ติดตั้ง [ARS-Codex ของต้นทาง](https://github.com/Imbad0202/academic-research-skills-codex) แล้วเลือก `academic-research-suite` ที่ติดตั้งคู่กับ `research-paper-craft` ขอให้ใช้ ARS ทำ full-paper และใช้ข้อกำหนดของเราในคำขอเดียวกัน คำสั่งกับ hook ของ Claude ไม่ได้ย้ายมาใช้ตรง ๆ อ่าน [คู่มือใช้ร่วมกัน](skills/research-paper-craft/references/ars-integration.th.md) เพื่อดูรุ่นต้นทาง สิทธิ และข้อขัดแย้งที่ตรวจพบ

<details>
<summary><strong>กรณีไม่ใช้ ARS หรือขอแก้ต้นฉบับอย่างเดียว</strong></summary>

ใช้ `research-paper-craft` พร้อมระบุ `full-paper` เพื่อทำตามขั้นตอนแบบเดี่ยว ห้ามเรียกว่าได้รัน ARS เลือก `revise` เมื่อแก้ข้อความเดิม และ `audit` เมื่อต้องการรายงานแบบอ่านอย่างเดียว ถ้ามี Word ต้นฉบับยังต้องรักษา Word-first

</details>

<a id="scope"></a>
## ขอบเขต

| ส่วน | ข้อกำหนด |
| --- | --- |
| Humanizer | ใช้สำนวนที่มีหลักฐานตั้งแต่ร่างแรก แยกบริบทผู้เขียน และแก้เท่าที่จำเป็นเมื่อทบทวน |
| สาระวิจัย | เชื่อมแหล่ง เทียบก่อนหลัง รักษาคำปฏิเสธ ขอบเขต และข้อความที่อ้างอิงรองรับ |
| บทความทั้งฉบับ | ร่างทุกส่วนที่เกี่ยวข้องผ่าน ARS หรือแบบเดี่ยว เชื่อมคำถาม วรรณกรรม metric ผล และข้อจำกัด |
| สมการ | แก้ไขได้ มีนิยาม หน่วย และส่วนโค้ดที่ตรงกัน |
| กราฟ | ข้อมูลวาดทำซ้ำได้ หน่วยตัวอย่างถูก ความไม่แน่นอนคำนวณจริง และตรวจขนาดส่งออก |
| ภาพจริง | ต้นฉบับตรงงาน มีบริบทเก็บ สิทธิ และประวัติการปรับ |
| ภาพรวมและอินโฟกราฟิก | กล่องกับลูกศรมีที่มา ลำดับอ่านชัด ไม่แต่งส่วนประกอบตกแต่ง |
| Word และการส่ง | รักษาโครงสร้าง ตรวจหน้าจริงใน Word ทุกหน้า และตรวจข้อมูลระบุตัวตน |

อ่านคู่มือภาษาเดียวตามงาน การแก้ย่อหน้าเดียวไม่ต้องโหลดคู่มือทั้งหมด เริ่มที่ [SKILL.md](skills/research-paper-craft/SKILL.md), [สำนวน](skills/research-paper-craft/references/writing.th.md), [ภาพ](skills/research-paper-craft/references/visuals.th.md) หรือ [รูปแบบ Word](skills/research-paper-craft/references/word-layout.th.md) แบบบันทึกเลือกใช้อยู่ใน [assets](skills/research-paper-craft/assets)

<a id="validation"></a>
## การทดสอบและข้อจำกัด

รุ่น 2.3.0 ทดสอบในเครื่องผ่าน **50 ข้อของ repository + 134 ข้อของ skill + 5 กรณีบั๊กเดิม** เป็นการตรวจซอฟต์แวร์และคำสั่ง ไม่ใช่คะแนนคุณภาพการเขียนของ AI

รุ่น 2.3.0 เพิ่มการทดสอบข้อกำหนด full-paper กับ ARS และบันทึกจำลอง ยังไม่ใช่ผลรัน ARS จริงหรือคะแนนคุณภาพทั้งบทความ กรณีผิดพลาดตัวตรวจข้อความเดิม 5 ข้อยังผ่านเหมือนเดิม เพิ่มการทดสอบสัญญาณการเปลี่ยนความหมาย ทะเบียนภาพ ข้อมูลรูปแบบผิด และการจำกัดตำแหน่งไฟล์ ดูคำสั่ง จำนวน และหลักฐานที่ [VERIFICATION.md](docs/VERIFICATION.md) คุณภาพจากโมเดลอิสระ การซ่อมผ่าน Word และการติดตั้งผ่าน host จริงยัง **ไม่ได้ยืนยัน** [ชุดประเมิน 24 กรณี](evals/README.md) เป็นข้อมูลจำลอง ไม่ใช่ผลคะแนนโมเดลที่แต่งขึ้น

| เครื่องมือ | สิ่งที่ยังไม่รับรอง |
| --- | --- |
| ตัวตรวจบันทึก full-paper | แหล่งถูกอ่านจริงหรือไม่ งานถูกต้องหรือพร้อมส่งหรือไม่ |
| ตัวตรวจข้อความ | ความจริงทางวิจัย ไวยากรณ์ทุกแบบ หรือผู้เขียนเป็น AI หรือไม่ |
| ตัวเทียบฉบับแก้ | ความหมายเทียบเท่าหรือการวางอ้างอิงถูกข้อ |
| ตัวตรวจทะเบียนภาพ | ภาพจริงหรือไม่ สิทธิ สถิติที่คำนวณซ้ำ หรือความสวยที่จัดแล้ว |
| ตัวตรวจ DOCX | จำนวนหน้า Word จริงหรือรูปแบบที่มองเห็น |

เครื่องมือตรวจในเครื่องและไม่เขียนทับต้นทาง [วิธีใช้และรูปแบบข้อมูล](docs/QUALITY.md) การไม่พบปัญหาไม่ใช่การอนุมัติส่งบทความ ปฏิบัติตามนโยบายเปิดเผย AI ของแหล่งตีพิมพ์ ไม่รับประกันการหลบ detector การรับตีพิมพ์ หรือจำนวนดาว

## ร่วมพัฒนา

[แนวทางร่วมพัฒนา](CONTRIBUTING.md) · [ข้อจำกัด](docs/KNOWN_ISSUES.md) · [ประวัติรุ่น](CHANGELOG.md) · [การเผยแพร่](docs/PUBLISHING.md)

ส่งกรณีผิดพลาดที่ทำซ้ำได้ ตัวอย่างสองภาษาที่มีแหล่ง และผลทดสอบ host หรือโมเดลที่รันจริง ห้ามส่งต้นฉบับส่วนตัว ข้อมูลผู้เข้าร่วม หรือรหัสลับโดยไม่ได้รับอนุญาต

## สิทธิและเครดิต

ใช้ [MIT](LICENSE) เก็บ Humanizer ต้นฉบับของ [Siqi Chen](https://github.com/blader/humanizer) พร้อม [ข้อความสิทธิ](licenses/humanizer-MIT.txt) และ [ที่มา](THIRD_PARTY_NOTICES.md) โปรเจกต์นี้เป็นงานอิสระ ไม่ได้อ้างการรับรองจากผู้ให้บริการ Claude Code หรือ Codex


ARS ต้องติดตั้งแยกและใช้ CC BY-NC 4.0 ส่วน Humanizer ของ Aboudjem ใช้เป็นแนวคิดสำหรับกฎวิจัยเฉพาะ ไม่ได้บรรจุ detector หรือรันการเขียนใหม่แบบไม่จำกัด เก็บ [ข้อความ MIT](skills/research-paper-craft/licenses/aboudjem-humanizer-MIT.txt) และ [บันทึกต้นทาง](skills/research-paper-craft/provenance/integrations.json) ไว้ครบ


[เว็บไซต์โครงการและการตั้งค่าการค้นหา](docs/DISCOVERY.md)
