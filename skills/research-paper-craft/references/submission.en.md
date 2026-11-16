# Verification and submission

Read only for the current task phase. The core rules in SKILL.md remain active.

## R24 Handle ethics, disclosure, and anonymous review

Confirm the applicable ethics, consent, licensing, data-protection, funding, conflict-of-interest, and AI-disclosure requirements. Do not invent approvals, registration numbers, consent statements, authorship contributions, or funding acknowledgments. Keep author verification items explicit.

An anonymous version must remove identifying material from the manuscript and all files intended for submission. Inspect author names, affiliations, emails, acknowledgments, grants, logos, institution-specific phrasing, headers, footers, watermarks, hyperlinks, repository ownership, filenames, and supplemental material.

Inspect document properties, custom metadata, comments, tracked changes, hidden text, alt text, embedded objects, chart data, attachments, image EXIF or XMP, PDF metadata, bookmarks, and source paths where applicable. Search the package for known names and identifiers. A text search alone is not a complete anonymity audit.

Make a separate anonymous copy. Preserve a private identified master and necessary rights records. Resolve tracked changes deliberately instead of accepting them blindly. Inspect again after the final save or export, since a saved file can differ from the inspected working state.

Follow the venue's treatment of self-citations and anonymized artifacts. Do not delete legitimate prior-work attribution or falsify bibliographic metadata merely to make the paper appear anonymous. Check what links reveal to a reviewer without author privileges. Do not publish a repository or upload a submission without explicit authorization.

## R25 Verify the final rendered document

Use the actual target template. Maintain editable equations, figures, tables, references, and cross-references where the format supports them. Preserve the original files and write new versions with clear names.

When the requested deliverable is Word, open the final DOCX in Microsoft Word, refresh fields and cross-references, repaginate, save, and record the actual page count. Inspect every page in Word Print Layout or a PDF exported from that exact final Word version. Record which route was used. Check the opening and closing of every page rather than inspecting only a thumbnail overview.

Check headings, paragraph spacing, widows and orphans, page breaks, columns, equations, subscripts, superscripts, Greek glyphs, Thai glyphs, tables, repeated table headers, captions, references, image resolution, and object anchors. Look for clipping, overlap, unexpected blank pages, substituted fonts, detached captions, and unreadable figure labels.

Compare page limits according to the venue's counting rules, including whether references, appendices, or supplementary material are included. Verify both the DOCX and exported PDF when both are deliverables. Recheck after any change that can alter layout.

Do not claim native Word verification based on a word-count estimate, a page-count property, python-docx, LibreOffice, another renderer, or a PDF from an unidentified source. Alternative rendering can provide a provisional layout check, but record the renderer and leave Word verification pending.

For a LaTeX-only or other explicitly chosen workflow, compile with the intended template and inspect every page of the actual output. Do not require an unnecessary Word conversion. When native Word verification is a mandatory deliverable and Word is unavailable, deliver a review draft with that blocker recorded. Do not label it submission-ready.

## R26 Work through observable checkpoints

| Checkpoint | Required evidence before advancing the relevant claim |
| --- | --- |
| Scope | Task mode, sources, output language, and unresolved decisions recorded |
| Source snapshot | Relevant source versions linked and conflicts identified |
| Required inputs | Missing project-specific inputs raised with the researcher under R01 and their status recorded |
| Scientific basis | Core claims connected to evidence and unsupported claims removed or marked |
| Methods and numbers | Method, equations, implementation, and approved results reconciled |
| Visuals | Each visual traced to its source and checked at final size |
| Language | Meaning preserved, house style checked, bilingual alignment checked when applicable |
| Submission | Required disclosures, references, anonymity, and rendered pages verified |

Use these checkpoints proportionally. A paragraph edit does not require creating an entire paper package. A full-paper task does require checking all applicable areas. Mark a checkpoint not applicable with a reason. Never mark an unperformed check as passed.

When blocked by a missing required input, ask the researcher whether the original exists under R01 and explain its consequence. Recording a gap is not a substitute for asking. Continue the independent parts. Keep placeholders visible in a working draft, using explicit markers such as `[SOURCE REQUIRED]`, `[RESULT UNVERIFIED]`, or `[AUTHOR DECISION]`. Never turn placeholders into plausible-looking content to make a paper appear finished.

Run the humanizing pass after the scientific account is stable. Compare the rewrite with the evidence-bearing version. Recheck quantities, scope, causality, uncertainty, exceptions, citations, and technical terms after any substantial rewrite.

## R27 Deliver the manuscript and its audit trail separately

Deliver the requested manuscript and actually created assets. Include the editable source, figures and their sources, bibliography, necessary analysis or plotting code, and the requested rendered document when available. Do not create empty files merely to simulate a complete package.

Keep internal records in a separate working or audit folder. These may include the source manifest, claim ledger, number ledger, figure register, notation sheet, reference verification log, decision log, and QA report. Do not accidentally include private raw data, identity mappings, API keys, hidden author information, or internal comments in a submission archive.

The final message should identify the completed deliverables, verified checks, remaining blockers, and decisions requiring the author's review. Keep the manuscript itself free of chatbot wrappers, process narration, and irrelevant audit notes. Do not send both a rough draft and a final rewrite unless requested.

Use explicit delivery status. `Working draft` means unresolved scientific inputs remain. `Review draft` means supported content is assembled but required checks or author approval remain. `Submission candidate` means applicable technical and formatting checks have passed and the author still decides whether to submit. Avoid a promise of acceptance or universal compliance.

## R28 Audit with pass, fail, not checked, and not applicable

Before delivery, inspect scientific support, methods, mathematics, statistics, references, visuals, style, reproducibility, anonymity, and rendered layout. Record the check, artifact, evidence, result, and required action.

A blocking failure includes an invented source or result, a central unsupported claim, an unreconciled method-result mismatch, a misleading visual, an incorrect central calculation, a missing mandatory disclosure, or an identity leak in a required anonymous submission. Pending mandatory Word pagination or uninspected final pages also block a submission-candidate claim for that workflow.

A warning can include a minor style issue, a supported but wordy passage, or a nonessential visual improvement. Classify by impact on scientific interpretation and submission requirements, not by how easy the item is to fix.

Do not assign an AI-likeness percentage or an arbitrary quality score. Report specific defects and fixes. An automated text check can flag punctuation or placeholders. It cannot certify scientific validity, plagiarism freedom, anonymity, native Word layout, or human authorship.

Use independent review when a suitable reviewer or tool is actually available. Otherwise perform a separate self-review pass and identify it honestly. Do not fabricate a second reviewer, a completed agent test, or a tool execution.

Check that every required missing input was raised with the researcher, that previous answers were respected, and that no unauthorized substitute entered the text or visuals. An unresolved required input blocks a submission-candidate claim. A recorded author decision can resolve a nonessential illustration choice, but cannot validate invented study evidence.

For language QA, explicit house-style prohibitions are `required_fix`, not optional cosmetic warnings. A supported but verbose phrase is a review candidate. An incomplete parse or inaccessible source is not a style pass. Record checked scope and not-checked scope separately. Pending-source markers remain visible to integrity checks even inside code or mathematics. A checker cannot approve a manuscript by hiding a region it could not parse.
