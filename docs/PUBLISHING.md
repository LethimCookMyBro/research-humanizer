# GitHub publishing setup

## Repository identity

| Field | Value |
| --- | --- |
| Repository name | `research-humanizer` |
| Display title | Research Humanizer |
| Installed skill name | `research-paper-craft` |
| License | MIT |
| Suggested visibility | Public, after reviewing the files for private material |
| Initial status | Preview |

### About description

```text
Evidence-first research writing skill for Claude Code and Codex. Humanize academic prose, check equations and figures, and flag missing sources. English + Thai.
```

### Suggested topics

```text
research academic-writing scientific-writing agent-skills claude-code codex humanizer research-integrity reproducible-research markdown thai
```

### Short announcement

```text
Research Humanizer is an open-source research-writing skill for Claude Code and Codex. It combines prose editing with evidence checks and requires the agent to ask for missing original study materials. English and Thai guides are included. Preview release with known limitations documented.
```

## ก่อนอัปโหลด

เปลี่ยน `YOUR_USERNAME` ใน README ทั้งสองไฟล์ให้เป็นชื่อบัญชี GitHub ของคุณ ชื่อนี้เป็นช่องแทนที่ในคำสั่งดาวน์โหลด ไม่ใช่ repository ที่สร้างให้แล้ว

ใช้ชื่อ repository เป็น `research-humanizer` และใช้คำอธิบายด้านบน ชื่อ skill ที่เรียกในแชตยังเป็น `research-paper-craft` เพื่อให้ตรงกับไฟล์เดิมและโฟลเดอร์ติดตั้ง

นำเนื้อหาภายในโฟลเดอร์ `research-humanizer` ไปไว้ที่รากของ repository อย่าซ้อนเป็น `research-humanizer/research-humanizer` และอย่าอัปโหลดเพียง README โดยไม่มีโฟลเดอร์ `skills/`

เก็บไฟล์ LICENSE ที่เตรียมให้พร้อม THIRD_PARTY_NOTICES และ license ของต้นทาง อย่าให้หน้าสร้าง repository สร้าง LICENSE หรือ README อีกชุดที่ทับของนี้

ตรวจว่าไม่มีต้นฉบับส่วนตัว ข้อมูลผู้เข้าร่วม รหัสลับ หรือไฟล์ผลวิจัยที่ยังไม่ได้รับอนุญาตให้เปิดเผยในชุดที่จะอัปโหลด

## Publish with Git

Create an empty repository under your own GitHub account first. Leave automatic README and license creation off because the files are already supplied. Run from the extracted repository root, replacing `YOUR_USERNAME`.

```bash
git init -b main
git add README.md 'README(TH).md' LICENSE THIRD_PARTY_NOTICES.md CONTRIBUTING.md CHANGELOG.md .gitignore docs licenses skills
git diff --cached --stat
git diff --cached --check
```

Review the staged files before committing. Then run the following.

```bash
git commit -m "Add Research Humanizer skill, bilingual docs, and MIT notices"
git remote add origin https://github.com/YOUR_USERNAME/research-humanizer.git
git push -u origin main
```

These commands assume a new local repository and an empty remote. For an existing repository, inspect its branch, remotes, and changes first. Do not use force push to work around a mismatch.

No repository has been created, and none of these publish commands has been run against a remote as part of generating this bundle.

## What to show on the project page

Keep the before-and-after writing example labeled as illustrative. Keep the preview badge and known-issue link until there is new evidence supporting a stronger status. Add screenshots or demonstrations only after running the corresponding workflow. Never use a fabricated chat transcript or green CI badge as proof of compatibility.

A useful first contribution list is the three checker defect groups in KNOWN_ISSUES, meaning-preservation tests in both languages, and recorded host installation trials. Do not claim a release fixes issues that remain open.

MIT was selected to allow broad reuse with a short notice requirement. License choice alone does not guarantee GitHub stars. The package makes the purpose, installation path, example behavior, and current limitations visible so readers can decide whether to use it.

## Sources checked on 2026-11-15

| Source | Purpose |
| --- | --- |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | User and project directories, explicit invocation |
| [Codex skills](https://developers.openai.com/codex/skills/) | Local discovery paths and explicit invocation |
| [Agent Skills specification](https://agentskills.io/specification) | Portable skill directory and metadata |
| [MIT License](https://opensource.org/license/mit) | Permission text and notice requirement |
| [Humanizer v4.0.0 license](https://github.com/blader/humanizer/blob/v4.0.0/LICENSE) | Upstream permission and copyright notice |
