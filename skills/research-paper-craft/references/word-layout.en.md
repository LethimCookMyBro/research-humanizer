# Word layout and typography

Load before editing an existing Word manuscript, including language-only edits inside a DOCX. Apply with writing, methods, and submission guidance as relevant. Research humanizing and evidence requirements remain unchanged. This module is a repair and verification procedure, not a guarantee of identical pagination across systems.

## R31 Keep the original Word document as the master

Use a Word-first workflow. Identify the authoritative DOCX and venue template. Keep an untouched original and make a separately named working copy. Record the file hash, Word version, operating system, compatibility mode, available fonts, and current revision-display state. Never overwrite the only copy.

Edit the existing document in Microsoft Word with a verified native editing route. Do not rebuild a formatted paper from extracted text, Markdown, HTML, PDF, screenshots, or an AI-generated replacement. Extraction is useful for analysis, not as the layout master. Do not round-trip the master through another editor or converter without explicit researcher approval.

When native Word editing is unavailable, do a read-only audit and provide a location-specific patch plan. Ask for the original DOCX, template, equation source, or native Word access when needed. A screenshot supports a visual finding, not a diagnosis of the underlying settings. Do not claim to repair a file that was never opened.

A researcher may explicitly authorize targeted programmatic edits on a copy. Then preserve unknown XML parts, relationships, fields, bookmarks, content controls, tracked changes, drawings, embedded objects, and equation objects. Replacing an entire paragraph or cell with its plain text is unsafe when these objects are present. Do not globally clear formatting or use an untested library save as a preservation guarantee. Native Word verification is still required for the final Word deliverable.

## R32 Establish a template-based format baseline

Read the actual venue template before choosing font sizes, margins, line spacing, or column widths. Record its body, heading, caption, table, equation, reference, and footnote styles. Include page size, section settings, indentation, language settings, and how styles inherit from each other. Distinguish style defaults from local overrides.

Do not invent a universal paper font, spacing value, table padding, or equation count. Correct a local defect to the approved baseline. A legitimate heading, formula, or footnote can differ from body text. Do not replace the template or change Normal for the whole document to fix one paragraph.

Inspect a baseline view of every page and make a defect list. Identify locations by heading plus a short text anchor, table or equation label, and current page or column. Page numbers alone are unstable after edits. Separate pre-existing problems from new regressions.

## R33 Inspect character spacing and word spacing separately

Check character spacing, expanded or condensed tracking, kerning, horizontal scale, baseline position, font substitution, and language-specific font settings. Check unexpected direct formatting inherited from pasted text. Reset only the affected text to the verified style. Do not compress or stretch letters simply to meet a page limit.

Check word spacing, repeated literal spaces, tabs, nonbreaking spaces, narrow spaces, and manual line breaks. Enable Word's formatting marks to distinguish stored whitespace from justification. A wide gap on screen does not prove that multiple space characters exist.

For stretched short lines, inspect justified or distributed alignment, Shift+Enter breaks, narrow columns, long unbreakable terms, and compatibility settings. Change a manual break only after checking whether it marks a real paragraph, an address, a list, or an equation. Preserve the venue's required alignment. Do not turn the whole paper left-aligned just to hide the cause. Microsoft documents character spacing, paragraph settings, and soft-line justification separately [S1, S2, S3].

Protect intentional nonbreaking relationships such as a quantity and its unit. Do not globally replace tabs, spaces, nonbreaking characters, or line breaks. Do not insert spaces between Thai letters or combining marks to imitate English spacing. Check Thai vowels, tone marks, punctuation, mixed Thai and Latin text, and permitted line-breaking behavior in the final Word view. Use approved language-aware hyphenation where applicable. Do not insert literal hyphens into scientific identifiers to force a line break.

## R34 Control line spacing and paragraph spacing through properties

Check line spacing independently from paragraph spacing before and after. Include automatic spacing, contextual spacing, indentation, tab stops, and document-grid alignment. Compare body paragraphs with the same style rather than applying one rule to headings, captions, lists, and equations.

Inspect exact line height for clipped fractions, large delimiters, subscripts, superscripts, and Thai combining marks. Where the approved template permits it, use a suitable minimum or multiple setting. Do not force every line to a fixed height just to make the page shorter. Word exposes these settings in the Paragraph dialog [S2].

Use paragraph properties for spacing. Do not create vertical layout with repeated empty paragraphs, manual line breaks, blank text boxes, or invisible characters. Remove a blank paragraph only after checking whether it carries a section break, an object anchor, a bookmark, or Word's required paragraph after a table.

Review Keep with next, Keep lines together, widow and orphan control, and Page break before as separate settings. A long chain of Keep with next settings may push content as a block. Keep a caption or heading with the appropriate content without binding the entire section together. Do not globally disable these protections [S4].

## R35 Make tables readable at the actual column width

Check each table at its final size. Inspect usable page or column width, table indentation, preferred width, AutoFit behavior, column proportions, cell margins, cell spacing, row height, vertical alignment, and text wrapping. Table padding and paragraph spacing inside cells are different controls [S5].

Look for words crowded against borders, clipped text in exactly sized rows, overwide columns, needlessly tall rows, broken units, and inconsistent numeric alignment. Rebalance column widths and simplify repetitive header wording without changing meaning or values. Repeat genuine header rows when a table spans pages. Keep units and precision consistent.

Choose row splitting according to content and the template. A short row should not split awkwardly. A row taller than the printable area cannot be fixed by forbidding every split. Check Keep with next inside cells before blaming the table's height. Check caption placement, notes, merged cells, and accessibility headers.

For a table that does not fit, propose an approved full-width placement, landscape section, split table, or appendix. Do not shrink the entire table to illegibility, drop results, alter margins, or rasterize it to conceal the problem. After any approved section change, inspect headers, footers, page numbering, columns, and adjacent pages again.

## R36 Preserve editable equations and diagnose damaged glyphs

Identify whether an equation is native Office Math Markup Language, OMML, a legacy equation or MathType object, plain text, or an image. Preserve its source and object type unless an approved conversion is required. Native Word mathematics is stored as OMML. Word supports UnicodeMath and a defined subset of LaTeX input, not arbitrary LaTeX documents [S6, S7].

Unexpected `¿`, `□`, replacement characters, or empty boxes require source inspection. Compare the stored characters, math font, object type, linear source, and rendered output. A square may be an intentional mathematical symbol. An inverted question mark can be legitimate text. Treat these as review candidates, never automatic replacements. Do not guess a lost operator or variable from the surrounding prose or screenshot.

Use an available, approved mathematical font with the necessary glyphs. Check fractions, radicals, accents, limits, brackets, minus signs, multiplication signs, Greek letters, and subscript or superscript placement. A font change cannot recover a character that was already corrupted. Ask the researcher for the original equation when the intended source is uncertain.

Check display-equation width, alignment, spacing before and after, line height, and equation-number placement. Use the template's supported equation layout rather than repeated spaces. Break a long equation at a valid mathematical boundary. Do not split a symbol, fraction, or term in a way that changes meaning. Numbering must not collide with the formula or wrap onto an isolated line. Recheck after saving and PDF export.

## R37 Reduce equation clutter without losing the method

For each displayed equation, record its purpose and whether the argument refers to it. Keep definitions, objectives, transformations, estimators, and results needed for understanding or reproduction. Use inline notation for short expressions when readable. Combine only genuinely related equations. Move a derivation to an appendix only when allowed and when the main method stays understandable. Do not set an arbitrary maximum number of equations or remove a scientific step to hide a layout defect.

Maintain an equation-to-code map using the [mapping template](../assets/equation-code-map.csv). Record the equation label, definition, units, dimensions, domain, implementation path, function, code revision, configuration, and evidence of a check. Map prose definitions too. A correctly rendered formula can still describe the wrong computation.

Check sum versus mean, weighting, signs, axis order, indexing, coordinate frames, degrees versus radians, normalization, rounding, clipping, missing-value handling, and denominator rules where relevant. Distinguish a conceptual formula from the evaluated implementation. Resolve a mismatch with the researcher before changing either. Do not silently edit scientific code while repairing format. Do not label an inspected function as an executed test.

## R38 Diagnose page and column gaps without forcing every space closed

Check page, column, and section breaks, section-start type, page vertical alignment, column widths and gutter, column balancing, footnotes, and pagination settings. Inspect wide figures or tables that legitimately interrupt two-column flow. Some bottom whitespace is required by the template or an indivisible object. Balanced columns are not automatically a requirement on every page.

Inspect floating-object anchors, text wrapping, distance from text, positioning relative to the page or column, and locked anchors. A hidden or transparent object can occupy space. Keep an image and its caption in reading order. Use inline placement where suitable, but do not convert every float to inline without examining the approved layout.

Classify each gap as an intentional layout choice, a constraint of an object, or a correctable defect. Repair the cause and record the tradeoff. Do not fill gaps with invented text, invisible characters, negative spacing, arbitrary breaks, reduced margins, or distorted images. After a local fix, inspect the following pages because pagination may cascade.

## R39 Protect fields, citations, revisions, and document structure

Preserve heading hierarchy, list numbering, bookmarks, hyperlinks, cross-references, figure and table captions, footnotes, endnotes, citation-manager fields, content controls, and embedded chart data. Check broken-reference messages, duplicate numbers, missing targets, and detached captions. Do not flatten these objects into text to make a warning disappear.

Update applicable fields in the main text, headers, footers, notes, and other relevant document areas. Check citation-manager behavior separately. Do not refresh external links, enable macros, install fonts or add-ins, or contact remote services without appropriate permission. Do not accept all tracked changes or delete reviewer comments as a formatting shortcut.

After a save or approved conversion, compare object counts and relationships with the baseline. Inspect every unexplained deletion or change. Equal counts alone do not prove preservation. Restore the backup and perform a smaller patch if an unrelated structure changes. Re-run anonymity checks on the final saved copy after layout and metadata work.

## R40 Close the repair with evidence from the saved artifact

Work in small batches with a rollback point. After each batch, save a new working version, inspect changed regions and downstream pagination, and compare content against the evidence-checked text. Keep the researcher informed about any needed scientific decision. Maintain the [layout QA record](../assets/layout-qa.md) outside the submission manuscript.

For final Word delivery, open the saved DOCX in Microsoft Word, update permitted fields, repaginate, save, and record the actual page count. Inspect every final page at readable size, including column tops and bottoms. Check text density, character and word spacing, line and paragraph spacing, tables, equations, figures, captions, references, headers, footers, and page numbers. Thumbnails are an overview, not a substitute for reading each page.

When delivering a PDF too, export it from that same verified Word version and inspect every PDF page. Check selectable text, missing glyphs, font substitution, equations, cropping, links, and page correspondence. Record the exact DOCX and PDF hashes, renderer or application, pages inspected, and review result. Reopen after the last save. Any later layout-affecting edit invalidates that final inspection and requires a new check.

A structural preflight or a clean text-linter report does not verify visual layout. LibreOffice or another renderer provides provisional evidence only for a Word-required task. Without native Word verification, keep the file at `Review draft` and list pending checks. Unresolved equation meaning or missing source evidence requires `Working draft`. Do not promise that a skill makes Word formatting impossible to break.

### Optional read-only preflight

Run from the skill directory. The tool does not write to the manuscript, launch Word, or render pages.

```bash
python scripts/audit_docx.py manuscript.docx --json
```

The output lists structural review candidates and object inventories. It does not resolve the full style cascade, font availability, actual whitespace geometry, scientific meaning, or Word pagination. A report without candidates is not a layout pass. Exit code zero means the inspection completed. Use `--fail-on-findings` for a nonzero exit when review candidates exist. Store reports privately because filenames and structure can reveal research information.

### Technical sources

Checked on 16 November 2026. These sources explain Word behavior. The preservation workflow and review gates above are this project's policy, not a claim that Microsoft certifies this skill.

- [S1 Microsoft character spacing](https://support.microsoft.com/en-us/word/change-the-spaces-between-text-in-word)
- [S2 Microsoft paragraph spacing and indentation](https://support.microsoft.com/en-us/word/adjust-indents-and-spacing)
- [S3 Microsoft soft-line justification setting](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.donotexpandshiftreturn)
- [S4 Microsoft line and page breaks](https://support.microsoft.com/en-us/word/line-and-page-breaks)
- [S5 Microsoft table widths and cell margins](https://support.microsoft.com/en-us/word/resize-a-table-column-or-row)
- [S6 Microsoft Office mathematics and OMML](https://learn.microsoft.com/en-us/office/math/)
- [S7 Microsoft UnicodeMath and LaTeX input](https://support.microsoft.com/en-us/word/linear-format-equations-using-unicodemath-and-latex-in-word)
