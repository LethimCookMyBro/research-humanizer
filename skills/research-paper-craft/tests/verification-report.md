# Version 2.0 verification record

Checked on 12 November 2026 using Python 3.13.5.

## Completed checks

| Check | Result | Evidence |
| --- | --- | --- |
| Core frontmatter | Passed | YAML parsed. Name matches the folder. Required fields and version checked |
| Main-file size | Passed | 59 lines and 802 whitespace-delimited words including metadata and the route table. This is not a tokenizer count |
| Focused routing | Passed | Eight topics with direct links to Thai and English files. No requirement to read the whole guide at startup |
| Runtime rule preservation | Passed | All 62 R00 through R30 language-specific blocks match version 1.1 after trimming outer whitespace. Fingerprints are in provenance/rule-map.json |
| Origin notes | Passed | Both R31 sections retained in provenance/origin-v1.1.md |
| Original humanizer source | Passed | Byte-for-byte match to the supplied humanizer.md |
| Existing checker and working templates | Passed | Byte-for-byte match to the version 1.1 package |
| Automated test suite | Passed | 31 tests consisting of 18 existing checker tests and 13 packaging checks. See unit-test-results.txt |
| Command-line smoke checks | Passed | Clean input accepted, four intended style findings detected, unsupported DOCX rejected. Inputs unchanged. See smoke-results.json |

The original version 1.1 package was first checked against the new routing and packaging requirements. The static baseline reported failures because the old entry point required a full-guide read and lacked the new topic files. This was a structural baseline, not an experiment on model behavior.

The first version 2 build exposed two absent report-file links. The report files were added and the complete suite was rerun. No failed check is represented as a pass from that initial run.

## Not checked

No installation test has been performed in the user's actual AI host. The 40 acceptance scenarios are a proposed behavioral evaluation set, not executed model trials. No cross-model reliability estimate is available. A matching sentence in a guide does not prove an AI will obey it.

No research manuscript was created or scientifically validated as part of packaging this skill. No native Word pagination, scientific image validation, or anonymization of a real submission was performed. Those remain requirements for future paper tasks when applicable.

Publisher policies cited in the historical source notes were not rechecked for this packaging change. Only the two packaging references listed in provenance/change-notes.md were inspected for this version.
