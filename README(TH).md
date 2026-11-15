<div align="center">

# Research Humanizer

**ภาษาที่เป็นธรรมชาติ ข้อกล่าวอ้างที่ตรวจสอบได้**

Skill สำหรับเขียนและปรับบทความวิจัยใน Claude Code และ Codex<br>
ครอบคลุมสำนวน สมการ ภาพ และการตรวจก่อนส่ง

[![License MIT](https://img.shields.io/badge/License-MIT-2563eb?style=flat-square)](LICENSE)
[![Guides English and Thai](https://img.shields.io/badge/Guides-English%20%2B%20Thai-0f766e?style=flat-square)](skills/research-paper-craft/references/writing.th.md)
[![Format Agent Skills](https://img.shields.io/badge/Format-Agent%20Skills-475569?style=flat-square)](skills/research-paper-craft/SKILL.md)
[![Status Preview](https://img.shields.io/badge/Status-Preview-b45309?style=flat-square)](docs/KNOWN_ISSUES.md)

[English](README.md) · **ภาษาไทย**

[ติดตั้ง](#install) · [เริ่มใช้](#use) · [ขอบเขต](#scope) · [การทดสอบ](#validation) · [ร่วมพัฒนา](CONTRIBUTING.md)

</div>

Research Humanizer รวมกฎเกลาสำนวนสำหรับงานวิจัยกับการตรวจหลักฐาน โดยกำหนดให้ AI รักษาความหมายทางวิทยาศาสตร์ ตรวจที่มาของตัวเลข และถามผู้วิจัยก่อนเติมส่วนที่ขาด

**ขาดภาพสภาพแวดล้อมจริง ข้อมูลดิบ หรือค่าตั้งการทดลอง ต้องถามผู้วิจัยก่อน ห้ามแต่งขึ้นหรือหาสิ่งอื่นมาแทนเอง**

> [!NOTE]
> Repository นี้บรรจุ Research Paper Craft v2.0 เป็น plugin ชื่อ `research-humanizer` สำหรับ Claude Code และ Codex ตัว plugin ใช้เวอร์ชัน `2.0.1` ส่วนชื่อ skill และเวอร์ชันแกนหลักยังเป็น `research-paper-craft` และ `2.0.0` กฎวิจัยกับตัวตรวจข้อความไม่ได้เปลี่ยน ดูข้อจำกัดในหัวข้อ [การทดสอบ](#validation)

<a id="install"></a>
## ติดตั้ง

แนะนำให้ติดตั้ง **Research Humanizer เป็น plugin** ซึ่งบรรจุ skill `research-paper-craft` และคู่มือไทยกับอังกฤษไว้แล้ว วิธีหลักนี้ไม่ต้อง clone repository หรือคัดลอกโฟลเดอร์ skill เอง

ใช้ **Claude Code CLI หรือ Codex CLI รุ่นที่รองรับ plugin** และมี Git ในเครื่อง ต้องติดตั้งและเข้าสู่ระบบเครื่องมือหลักก่อน Python 3.10 ขึ้นไปจำเป็นเฉพาะตัวตรวจข้อความเสริม ชุดนี้ไม่เพิ่ม MCP server, hook หรือการเชื่อมต่อบัญชีอื่น

### Claude Code

พิมพ์คำสั่งต่อไปนี้ **ในช่องแชตของ Claude Code** ทีละคำสั่ง

```text
/plugin marketplace add LethimCookMyBro/research-humanizer
/plugin install research-humanizer@research-humanizer
```

เลือกขอบเขตติดตั้งเมื่อระบบถาม แล้วทำตามข้อความแจ้งการเปิดใช้งาน หากยังไม่ทำงานให้ใช้ `/reload-plugins` หรือเริ่ม session ใหม่ จากนั้นเรียก skill ด้วยชื่อที่มีชื่อ plugin นำหน้า

```text
/research-humanizer:research-paper-craft ปรับบทความจากไฟล์ในโปรเจกต์นี้ รักษาหลักฐานเดิม และถามผมก่อนเมื่อข้อมูลของงานยังขาด
```

<details>
<summary><strong>ทางเลือกสำหรับ Claude Code ผ่าน terminal</strong></summary>

รันใน terminal ไม่ใช่ช่องแชต ค่าเริ่มต้นติดตั้งสำหรับบัญชีผู้ใช้ หากต้องการให้ใช้ร่วมกันในโปรเจกต์วิจัย ให้เพิ่ม `--scope project` ท้ายคำสั่งติดตั้ง

```bash
claude plugin marketplace add LethimCookMyBro/research-humanizer
claude plugin install research-humanizer@research-humanizer
```

</details>

การเพิ่ม marketplace กับการติดตั้ง plugin เป็นคนละขั้น ในชุดนี้ทั้งสองชื่อคือ `research-humanizer` อ้างอิงจาก [คู่มือติดตั้งทางการ](https://code.claude.com/docs/en/discover-plugins) และ [คู่มือชื่อเรียก skill ใน plugin](https://code.claude.com/docs/en/plugins)

### Codex CLI

รันคำสั่งต่อไปนี้ **ใน terminal ไม่ใช่ช่องแชตของ Codex**

```bash
codex plugin marketplace add LethimCookMyBro/research-humanizer
codex plugin add research-humanizer@research-humanizer
```

เริ่ม Codex session ใหม่ แล้วพิมพ์ `/plugins` เพื่อตรวจว่า **Research Humanizer** ติดตั้งและเปิดใช้งานแล้ว อีกวิธีคือเพิ่ม marketplace ด้วยคำสั่งแรก จากนั้นเปิด `/plugins` แล้วเลือกติดตั้ง Research Humanizer จาก marketplace นี้

สั่งให้ Codex ใช้ skill `research-paper-craft` กับไฟล์งานของคุณ หรือพิมพ์ `$` เพื่อเลือก skill จากรายการ

```text
ใช้ skill research-paper-craft จาก Research Humanizer ปรับบทความในโปรเจกต์นี้ รักษาหลักฐานเดิม และถามผมก่อนเมื่อข้อมูลของงานยังขาด
```

Codex ใช้ `codex plugin add` เพื่อติดตั้ง และใช้ `/plugins` เพื่อเปิดหน้าจัดการ ไม่ใช่คำสั่งเดียวกับ Claude Code อ้างอิงจาก [คู่มือ Codex CLI](https://learn.chatgpt.com/docs/cli/reference) และ [คู่มือ plugin](https://developers.openai.com/codex/plugins)

> [!TIP]
> หากเคยติดตั้งด้วยวิธีคัดลอกไฟล์ ให้สำรองและย้ายโฟลเดอร์ `research-paper-craft` แบบเดี่ยวออกจาก `~/.claude/skills/`, `~/.agents/skills/` หรือโฟลเดอร์ skills ในโปรเจกต์ก่อนเปลี่ยนมาใช้ plugin ไม่ต้องย้ายไฟล์บทความ และไม่ควรเปิดใช้สำเนาแบบเดี่ยวกับแบบ plugin ซ้ำกัน

<details>
<summary><strong>ตรวจ อัปเดต หรือถอนการติดตั้ง plugin</strong></summary>

ตรวจรายการที่ติดตั้งจาก terminal

```bash
claude plugin list
codex plugin list
```

สำหรับ Claude Code ให้รีเฟรช marketplace แล้วอัปเดต plugin

```bash
claude plugin marketplace update research-humanizer
claude plugin update research-humanizer@research-humanizer
```

สำหรับ Codex ให้รีเฟรชรายการใน marketplace

```bash
codex plugin marketplace upgrade research-humanizer
```

การรีเฟรชรายการยังไม่ยืนยันว่าสำเนาที่ติดตั้งอัปเดตแล้ว ตรวจเวอร์ชันใน `/plugins` หากยังเป็นฉบับเก่า ให้สำรองสิ่งที่เคยแก้เองและติดตั้งใหม่ผ่านหน้าจัดการนั้น จากนั้นเริ่ม session ใหม่

ถอนการติดตั้งจาก terminal หาก Claude Code ติดตั้งแบบเฉพาะโปรเจกต์ ให้เพิ่ม `--scope project`

```bash
claude plugin uninstall research-humanizer@research-humanizer
codex plugin remove research-humanizer@research-humanizer
```

คำสั่งเหล่านี้จัดการ plugin ไม่ใช่ไฟล์บทความ หากระบบไม่รู้จักคำสั่ง plugin ให้อัปเดตเครื่องมือหลักตามคู่มือทางการ นโยบายขององค์กรอาจจำกัด marketplace ภายนอกด้วย ไม่ควรข้ามข้อจำกัดนั้น

</details>

<details>
<summary><strong>ทางเลือกสำหรับติดตั้ง skill แบบเดี่ยว</strong></summary>

ใช้เฉพาะกรณีต้องการ skill แบบเดี่ยวแทน plugin ไม่ต้องทำเพิ่มหากติดตั้ง plugin ตามวิธีหลักแล้ว

```bash
git clone https://github.com/LethimCookMyBro/research-humanizer.git
cd research-humanizer
```

คัดลอกโฟลเดอร์ `skills/research-paper-craft` ทั้งโฟลเดอร์ไปยังปลายทางแห่งเดียว หากมีฉบับเดิม ให้สำรองและย้ายออกนอกโฟลเดอร์ skills ก่อน ห้ามเขียนทับหรือคัดลอกเฉพาะ `SKILL.md`

| เครื่องมือ | ติดตั้งสำหรับผู้ใช้ | ติดตั้งเฉพาะโปรเจกต์ |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/research-paper-craft/` | `.claude/skills/research-paper-craft/` |
| Codex | `~/.agents/skills/research-paper-craft/` | `.agents/skills/research-paper-craft/` |

ตำแหน่งแบบโปรเจกต์เริ่มจากโฟลเดอร์หลักของงานวิจัย บน Windows ให้ใช้โฟลเดอร์ผู้ใช้แทน `~` หากเครื่องมือรันใน WSL ให้ใช้ตำแหน่งภายใน WSL นั้น เก็บคู่มือ สคริปต์ แบบบันทึก และข้อความสิทธิไว้ครบ

Claude Code แบบ skill เดี่ยวเรียกด้วย `/research-paper-craft` โดยไม่มีชื่อ plugin นำหน้า ส่วน Codex เลือก skill โดยพิมพ์ `$` เริ่ม session ใหม่หลังเปลี่ยนไฟล์ที่ติดตั้ง

สำเนาแบบนี้ไม่อัปเดตผ่าน plugin manager ให้ตรวจการเปลี่ยนแปลงต้นทาง รัน `git pull --ff-only` สำรองสำเนาที่ติดตั้ง แล้วเปลี่ยนเป็นฉบับใหม่โดยตั้งใจ ถอนการติดตั้งโดยย้ายโฟลเดอร์ skill ออกนอกตำแหน่งที่ระบบค้นหา ไม่ต้องย้ายไฟล์บทความ

อ้างอิงจาก [คู่มือ skills ของ Claude Code](https://code.claude.com/docs/en/skills) และ [คู่มือ skills ของ Codex](https://developers.openai.com/codex/skills/)

</details>

<a id="use"></a>
## เริ่มใช้

ให้ AI เข้าถึงไฟล์งานจริง ระบุภาษาของบทความ แหล่งตีพิมพ์ และชุดผลที่ถือเป็นหลักเมื่อทราบข้อมูลแล้ว ตัว skill กำหนดให้อ่านไฟล์และคำตอบเดิมก่อนถามซ้ำ

```text
ใช้ research-paper-craft กับไฟล์ในโปรเจกต์นี้
เขียนบทความเป็นภาษาอังกฤษ และคุยเรื่องที่ต้องตัดสินใจกับผมเป็นภาษาไทย
ตรวจต้นฉบับ โค้ด ชุดผลที่ยืนยันแล้ว และข้อมูลต้นทางก่อน
หากขาดข้อมูล ภาพจริง หรือรายละเอียดของงาน ให้ถามผมก่อน
ทำสมการและภาพเฉพาะจุดที่งานวิจัยจำเป็นต้องใช้
แยกต้นฉบับออกจากรายงานตรวจ
ห้ามอ้างว่าตรวจสิ่งที่ยังไม่ได้ตรวจจริง
```

หากต้องการแก้เฉพาะภาษา ให้ระบุขอบเขตนั้น ไม่ควรออกแบบการทดลองใหม่ระหว่างเกลาย่อหน้า ตัว skill เลือกอ่านคู่มือภาษาเดียวเฉพาะช่วงงานที่ใช้ ไม่ได้โหลดคู่มือเต็มสองภาษาตั้งแต่เริ่ม

### ตัวอย่างเล็ก ๆ

*ตัวอย่างสมมติสำหรับอธิบายการแก้ภาษา ไม่ใช่ผลทดสอบโมเดลที่รันแล้ว*

สมมติว่าบันทึกที่ให้มายืนยันเพียงว่าวิธีนี้รวมค่าจากเซนเซอร์ โดยไม่มีผลประเมินหรือภาพสถานที่จริง

| ขั้น | ข้อความ |
| --- | --- |
| ร่างที่กล่าวเกินหลักฐาน | กรอบวิธีที่ล้ำหน้านี้ผสานค่าจากเซนเซอร์อย่างไร้รอยต่อ และแสดงประสิทธิภาพที่แข็งแกร่งในสภาพจริง |
| ฉบับที่มีหลักฐานรองรับ | วิธีนี้รวมค่าที่อ่านได้จากเซนเซอร์ |
| คำถามถึงผู้วิจัย | มีผลประเมินและภาพสภาพแวดล้อมจริงจากการทดลองชุดนี้ไหมครับ |

ข้อกล่าวอ้างเรื่องประสิทธิภาพยังรอหลักฐาน ไม่ควรทำให้แรงขึ้น เติมคำเดา หรือถือว่าได้รับการยืนยันแล้ว

<a id="scope"></a>
## ขอบเขต

| ส่วน | สิ่งที่คำสั่งกำหนด |
| --- | --- |
| เกลาภาษาวิจัย | ตัดคำฟุ่มเฟือยและสำนวนเป็นสูตร โดยรักษาความหมาย ตัวเลข อ้างอิง คำปฏิเสธ และระดับความแน่ใจ |
| หลักฐานและเวอร์ชัน | ถ้าเอกสารกับโค้ดขัดกันให้ถามผู้วิจัย เชื่อมผลกับชุดผลที่กำหนดและข้อมูลดิบ |
| โครงสร้างบทความ | Introduction เล่าภาพรวมให้อ่านเข้าใจ Contributions เป็น bullet สั้นและไม่มีตัวเลขผล |
| วิธีและสมการ | นิยามตัวแปร หน่วย มิติ สมมติฐาน และกรณีขอบเขต พร้อมตรวจความตรงกับโค้ด |
| การประเมินและสถิติ | ตรวจความเป็นธรรมของการเปรียบเทียบ การรวมผล ความไม่แน่นอน และการทำซ้ำ |
| ภาพและตาราง | สร้างกราฟจากข้อมูลที่ตรวจแล้ว ภาพระบบต้องตรงกับวิธีจริง ระบุภาพแนวคิดให้ชัด |
| ก่อนส่ง | ตรวจข้อมูลระบุตัวตน metadata หัวกระดาษ และไฟล์เสริม ตรวจจำนวนหน้าจริงใน Word และดูทุกหน้าเมื่อกำหนดให้ใช้ Word |
| บันทึกการทำงาน | แยกไฟล์บทความออกจากทะเบียนแหล่งข้อมูล ข้อกล่าวอ้าง และรายงานตรวจ |

คู่มือทั้งแปดหมวดมีฉบับ [อังกฤษ](skills/research-paper-craft/references/writing.en.md) และ [ไทย](skills/research-paper-craft/references/writing.th.md) ตารางเลือกอ่านแต่ละหมวดอยู่ใน [SKILL.md](skills/research-paper-craft/SKILL.md)

<details>
<summary><strong>สำนวนตั้งต้นของบทความ</strong></summary>

ใช้ประโยคสั้นที่สมบูรณ์ ภาษาระดับกลางค่อนทางการ ไม่ร้อยลูกน้ำหรืออัดหลายประเด็นในย่อหน้าเดียว รักษาศัพท์เฉพาะที่จำเป็นให้คงที่

กฎตั้งต้นห้ามใช้ semicolon, colon, ขีดยาว และคำย่อภาษาอังกฤษอย่าง `isn't` ในเนื้อความ ยกเว้น `Keywords:` และเครื่องหมายในเอกสารอ้างอิง ต้องรักษาโค้ด สมการ URL ตัวระบุ การอ้างอิงที่บังคับ และข้อความอ้างตรง ใช้อักษรกรีกและสัญลักษณ์ที่จำกัดในบริบทคณิตศาสตร์หรือตัวเลข ไม่ใช้ตกแต่งเนื้อความ

กฎเหล่านี้เป็นข้อกำหนดของโปรเจกต์ ไม่ใช่มาตรฐานตายตัวของทุกวารสาร หากขัดกับรูปแบบของแหล่งตีพิมพ์ที่ตรวจแล้วหรือคำสั่งชัดเจนของผู้วิจัย ให้แจ้งข้อขัดแย้ง ห้ามเปลี่ยนความหมายทางวิทยาศาสตร์เพียงเพื่อให้ตัวตรวจสำนวนผ่าน

</details>

### ข้อจำกัด

ชุดนี้เป็นคำสั่งสำหรับ AI พร้อมตัวตรวจข้อความเบื้องต้น ไม่ได้ติดตั้งเครื่องมือค้นเว็บ สร้างภาพ จัดหน้า หรือ Microsoft Word ให้เอง ความสามารถเหล่านั้นขึ้นกับเครื่องมือและสิทธิที่มีในระบบ

ไม่รับรองความถูกต้องทางวิทยาศาสตร์ ไม่รับประกันการตอบรับตีพิมพ์ และไม่สัญญาว่าจะหลบเครื่องมือตรวจ AI ต้องทำตามนโยบายเปิดเผยการใช้ AI ของแหล่งตีพิมพ์ หากไม่มี Microsoft Word ให้บันทึกว่าการตรวจจำนวนหน้าใน Word ยังไม่เสร็จ ห้ามอ้างแทนจากโปรแกรมอื่น

<a id="validation"></a>
## การทดสอบ

**สถานะยังเป็นรุ่นทดลองใช้** การมีกฎครบ การรันสคริปต์ผ่าน และการทำงานจริงของโมเดลเป็นหลักฐานคนละประเภท

| ส่วนที่ตรวจ | หลักฐานปัจจุบัน |
| --- | --- |
| การทดสอบตัวตรวจข้อความและโครงสร้างที่มากับชุดเดิม | ผ่าน 31 ข้อในการรันที่บันทึกไว้ |
| กรณีทดสอบเจาะจงจากการตรวจ v2.0 | ยังไม่ผ่าน 5 ข้อ และยังไม่ได้แก้ |
| การทดลองกับโมเดลอิสระ | มีโจทย์ 40 สถานการณ์ แต่ยังไม่ได้รัน |
| ไฟล์ plugin และวิธีติดตั้ง | เพิ่มไฟล์สำหรับทั้งสองระบบและชุดทดสอบแบบไม่เรียก host จริง ดูผลล่าสุดในบันทึกการตรวจ |
| การใช้งานใน Claude Code และ Codex | ตรวจคำสั่งกับเอกสารทางการแล้ว ยังไม่ได้ติดตั้งและเรียกผ่านโปรแกรมจริงในสภาพแวดล้อมนี้ |
| Word และขั้นตอนส่งบทความทั้งชุด | ยังไม่ได้ทดสอบครบตั้งแต่ต้นจนจบกับบทความวิจัยจริง |

ดู [ปัญหาที่ทราบ](docs/KNOWN_ISSUES.md), [รายงานตรวจเดิม](docs/audit-v2.0/README.md) และ [บันทึกการตรวจรอบนี้](docs/VERIFICATION.md) ชุดเอกสารนี้ไม่ได้อ้างว่าแก้ตัวตรวจข้อความ v2.0 แล้ว

### ตัวตรวจข้อความและชุดทดสอบเสริม

รันจากโฟลเดอร์หลักของ repository เปลี่ยนตำแหน่งบทความเป็นไฟล์ของคุณ หากเครื่องใช้คำสั่ง `python` สำหรับ Python 3 ให้ใช้แทน `python3`

```bash
python3 skills/research-paper-craft/scripts/lint_manuscript.py /path/to/manuscript.md --json
python3 -B -m unittest discover -s skills/research-paper-craft/tests -v
python3 -B -m unittest discover -s tests -v
```

ตัวตรวจอ่าน Markdown หรือข้อความธรรมดาแบบ UTF-8 และไม่แก้ไฟล์ให้เอง ไม่ได้ตรวจ DOCX, PDF, ความถูกต้องของสมการ อ้างอิง ความแท้ของภาพ anonymous หรือข้อกล่าวอ้างทางวิทยาศาสตร์ ผลที่ไม่พบปัญหาจึงไม่ใช่การอนุมัติบทความ

คำสั่งต่อไปนี้ใช้ทำซ้ำกรณีเจาะจงที่ **ยังไม่ผ่าน** ให้รันแยกจากชุดเดิม ตัวตรวจ v2.0 ที่ยังไม่แก้จะคืนค่าจบแบบมีข้อผิดพลาด ห้ามรายงานผลนั้นว่าเป็นการทดสอบที่ผ่าน

```bash
python3 -B docs/audit-v2.0/audit_regressions.py skills/research-paper-craft
```

## โครงสร้าง repository

```text
research-humanizer/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── .agents/plugins/
│   └── marketplace.json
├── tests/
│   └── test_plugin_packaging.py
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

## ร่วมพัฒนา

เริ่มจากรายงานปัญหาที่ทำซ้ำได้หรือ pull request ขนาดเล็ก งานที่มีประโยชน์คือแก้ตัวตรวจให้ผ่านกรณีที่พบปัญหา เพิ่มตัวอย่างตรวจการรักษาความหมายสองภาษา และบันทึกการใช้งานจริงในแต่ละระบบ ใช้ข้อมูลสมมติหรือข้อมูลที่มีสิทธิเปิดเผย ห้ามแนบต้นฉบับส่วนตัว ข้อมูลผู้เข้าร่วม รหัสลับ หรือผลที่ยังไม่เผยแพร่โดยไม่ได้รับอนุญาต

อ่าน [CONTRIBUTING.md](CONTRIBUTING.md) ส่วนชื่อ repository คำอธิบาย Topics และขั้นตอนขึ้น GitHub อยู่ใน [PUBLISHING.md](docs/PUBLISHING.md)

## สิทธิการใช้และเครดิต

เผยแพร่ด้วย [MIT License](LICENSE) การแจกต่อให้เก็บข้อความลิขสิทธิ์และการอนุญาตที่แนบไว้ครบ

Humanizer ต้นทางเป็นผลงานใน [โครงการ Humanizer ของ Siqi Chen](https://github.com/blader/humanizer) ไฟล์ต้นฉบับที่เก็บในชุดนี้ตรงกับ Git blob ของ upstream v4.0.0 และเก็บ MIT notice ไว้ใน [licenses/humanizer-MIT.txt](licenses/humanizer-MIT.txt) ที่มาของส่วนปรับสำหรับงานวิจัยอยู่ใน [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

Claude Code และ Codex เป็นผลิตภัณฑ์ของผู้ให้บริการแต่ละราย โปรเจกต์นี้เป็นงานอิสระ ไม่ได้แสดงว่าผู้ให้บริการเหล่านั้นรับรอง

<sub>ตรวจคู่มือติดตั้งเมื่อวันที่ 15 พฤศจิกายน 2026 พฤติกรรมของผลิตภัณฑ์อาจเปลี่ยนได้</sub>
