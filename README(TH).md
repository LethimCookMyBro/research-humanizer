<div align="center">

# Research Humanizer

**Clear research writing. Traceable claims. Real evidence.**

[![Version](https://img.shields.io/badge/version-2.2.0-2563eb?style=flat-square)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-0f766e?style=flat-square)](LICENSE)
[![Languages](https://img.shields.io/badge/guides-English%20%2B%20Thai-475569?style=flat-square)](skills/research-paper-craft/SKILL.md)
[![Status](https://img.shields.io/badge/status-preview-b45309?style=flat-square)](docs/KNOWN_ISSUES.md)

<a href="README.md">English</a> · <a href="README%28TH%29.md">ภาษาไทย</a>

[Install](#install) · [Use](#use) · [Scope](#scope) · [Validation](#validation)

</div>

Skill เขียนงานวิจัยสำหรับ Claude Code และ Codex ตัดถ้อยคำลอยโดยไม่แต่งรายละเอียด ไม่เปลี่ยนสาระ และไม่ทำให้เสียงของผู้เขียนหาย ข้อความที่ดีอยู่แล้วคงไว้ กราฟใช้ข้อมูลที่ตรวจแล้ว ส่วนภาพที่ต้องแสดงชุดทดลองจริงต้องใช้ต้นฉบับจากงานนั้น

> [!IMPORTANT]
> ขาดต้นฉบับต้องถามผู้วิจัย ประโยคที่ฟังน่าเชื่อ ภาพห้องทดลองที่สร้างขึ้น และเส้นกราฟที่ดูดี ใช้แทนหลักฐานไม่ได้

**2.2.0** เพิ่มโปรไฟล์สำนวน การเทียบข้อกล่าวอ้างก่อนหลัง ภาพจริงตามหน้าที่ และแก้ตัวตรวจข้อความ โดยยังเก็บกฎ Word-first กับ Humanizer เดิม [ดูสถานะการปิด GAP](docs/QUALITY.md)

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
/research-humanizer:research-paper-craft เกลาบทความนี้ รักษาข้อกล่าวอ้าง และถามเมื่อขาดต้นฉบับ
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
รักษาศัพท์ที่ผมยอมรับ และแก้ภาษาเฉพาะที่จำเป็น
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

<a id="scope"></a>
## ขอบเขต

| ส่วน | ข้อกำหนด |
| --- | --- |
| Humanizer | แก้เท่าที่จำเป็น รักษาสำนวนที่ยอมรับ ศัพท์คงที่ และรู้จักหยุด |
| สาระวิจัย | เชื่อมแหล่ง เทียบก่อนหลัง รักษาคำปฏิเสธ ขอบเขต และข้อความที่อ้างอิงรองรับ |
| บทความทั้งฉบับ | เชื่อมคำถาม วิธี ผล ข้อจำกัด และตัดย่อหน้าที่แค่ย้ำความสำคัญ |
| สมการ | แก้ไขได้ มีนิยาม หน่วย และส่วนโค้ดที่ตรงกัน |
| กราฟ | ข้อมูลวาดทำซ้ำได้ หน่วยตัวอย่างถูก ความไม่แน่นอนคำนวณจริง และตรวจขนาดส่งออก |
| ภาพจริง | ต้นฉบับตรงงาน มีบริบทเก็บ สิทธิ และประวัติการปรับ |
| ภาพรวมและอินโฟกราฟิก | กล่องกับลูกศรมีที่มา ลำดับอ่านชัด ไม่แต่งส่วนประกอบตกแต่ง |
| Word และการส่ง | รักษาโครงสร้าง ตรวจหน้าจริงใน Word ทุกหน้า และตรวจข้อมูลระบุตัวตน |

อ่านคู่มือภาษาเดียวตามงาน การแก้ย่อหน้าเดียวไม่ต้องโหลดคู่มือทั้งหมด เริ่มที่ [SKILL.md](skills/research-paper-craft/SKILL.md), [สำนวน](skills/research-paper-craft/references/writing.th.md), [ภาพ](skills/research-paper-craft/references/visuals.th.md) หรือ [รูปแบบ Word](skills/research-paper-craft/references/word-layout.th.md) แบบบันทึกเลือกใช้อยู่ใน [assets](skills/research-paper-craft/assets)

<a id="validation"></a>
## การทดสอบและข้อจำกัด

แก้กรณีผิดพลาดตัวตรวจข้อความเดิม 5 ข้อแล้ว เพิ่มการทดสอบสัญญาณการเปลี่ยนความหมาย ทะเบียนภาพ ข้อมูลรูปแบบผิด และการจำกัดตำแหน่งไฟล์ ดูคำสั่ง จำนวน และหลักฐานที่ [VERIFICATION.md](docs/VERIFICATION.md) คุณภาพจากโมเดลอิสระ การซ่อมผ่าน Word และการติดตั้งผ่าน host จริงยัง **ไม่ได้ยืนยัน** [ชุดประเมิน 24 กรณี](evals/README.md) เป็นข้อมูลจำลอง ไม่ใช่ผลคะแนนโมเดลที่แต่งขึ้น

| เครื่องมือ | สิ่งที่ยังไม่รับรอง |
| --- | --- |
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
