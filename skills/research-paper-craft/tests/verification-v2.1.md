# Version 2.1.0 verification

Checked on 16 November 2026. These results are from executable local tests, not a repaired research manuscript.

| Check | Result |
| --- | --- |
| Repository plugin and instruction contracts | 19 passed, including 8 new Word-layout contracts |
| Skill package and checker suite | 58 passed, including 27 synthetic DOCX preflight tests |
| Historical targeted text-checker regressions | 5 failed, unchanged and still open |
| Original R00 to R30 language-specific rule bodies | All 62 preserved |
| Original Humanizer and text-checker source | Unchanged |
| New bilingual Word guidance | R31 to R40 in each language, loaded only for relevant tasks |
| Main skill size | 61 lines and 901 whitespace-delimited words, not a tokenizer count |
| Native Microsoft Word rendering or repair | Not performed |
| Independent AI behavior and live plugin installation | Not performed |

The new preflight tests first failed because the implementation was absent. Seven of eight new instruction contracts first failed on missing Word guidance or the old version. All new executable tests passed after implementation. These are static and synthetic-fixture tests, not an AI baseline experiment.

Run `python -B -m unittest discover -s tests -v` from this skill folder. Run the repository-level tests separately from the repository root. The known failing historical audit remains separate and must not be reported as passing.

The twenty scenarios in [word-layout-scenarios.md](word-layout-scenarios.md) are proposed native Word/model trials. They are unexecuted. A clean DOCX preflight does not certify layout, scientific meaning, anonymity, or submission readiness. User screenshots and manuscript content are not included in the public package.
