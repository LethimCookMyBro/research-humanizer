# Word layout acceptance scenarios

Proposed manual and model trials. None of these scenarios has been executed as an independent AI or native Word trial in the 2.1.0 packaging run. The synthetic XML unit tests are separate. Use shareable fixtures, not private manuscripts or the researcher's screenshots, in public evidence.

Record the model, host, Word build, operating system, template, input and output hashes, exact prompt, observed behavior, pages inspected, and pass or fail reasoning for each actual trial. A claim in an agent reply is not evidence that Word was opened.

| ID | Scenario | Required behavior and evidence |
| --- | --- | --- |
| W01 | A formatted DOCX is supplied for language-only humanizing | Load writing and Word layout guidance. Preserve the original. Edit locally within the existing document and verify the saved copy |
| W02 | Native Word access is unavailable but the user asks for a final paper | Offer a read-only audit and anchored patch plan. Keep native pagination pending and label Review draft |
| W03 | A screenshot shows stretched short English lines | Ask for the original DOCX if absent. Check justification, manual breaks, literal spaces, and character settings without asserting a cause from the screenshot |
| W04 | Condensed tracking was used to meet a page limit | Compare the template. Do not use character compression or reduced margins to hide overflow |
| W05 | A mixed Thai-English paragraph has clipped tone marks | Inspect fonts, line height, grid, and language settings. Preserve combining characters and verify in native Word |
| W06 | A quantity and its unit are separated by a nonbreaking space | Preserve the relationship. Do not run a global whitespace replacement |
| W07 | A justified paragraph contains intentional and accidental Shift+Enter breaks | Classify each break before editing. Preserve required paragraph and equation boundaries |
| W08 | Table text touches borders and a row is clipped | Check cell margins, paragraph settings, column width, exact row height, and final-size reading. Do not rasterize or shrink to illegibility |
| W09 | An unsplittable table row is taller than the printable page | Choose a template-approved split or alternate placement. Do not forbid every row split globally |
| W10 | A formula contains ¿, a square, and a legitimate proof-ending square | Compare stored characters and original mathematical source. Do not replace all squares or guess missing operators |
| W11 | Native OMML, a legacy equation object, and an equation image coexist | Inventory object types. Preserve editable sources and ask before conversion. Verify any approved conversion |
| W12 | Formula displays correctly but code uses mean while the paper says sum | Mark a scientific mismatch. Ask the researcher and record the equation-to-code map. Do not silently edit code |
| W13 | Many equations crowd a method section | Keep scientifically necessary equations. Use inline notation or an appendix only when justified and allowed |
| W14 | A chain of Keep with next settings leaves a large gap | Identify the chain. Retain appropriate heading/caption ties and remove only the unintended ties |
| W15 | A two-column paper has legitimate bottom whitespace beside a full-width table | Do not force all column bottoms to align. Document whether the gap is intentional or a repairable defect |
| W16 | A floating image has a hidden anchor and its caption moves | Inspect anchor, wrapping, text distance, and reading order. Check downstream pages after a local fix |
| W17 | A citation-manager field and bookmark lie inside text being rewritten | Preserve fields and references. Do not replace the entire paragraph with plain text |
| W18 | Reviewer comments and tracked changes are present | Preserve review state unless explicit decisions authorize changes. Do not accept everything as a layout shortcut |
| W19 | The DOCX passed review before anonymity cleanup and final export | Reopen the final saved copy. Recheck every Word/PDF page and anonymity. Earlier inspection does not cover the modified artifact |
| W20 | The structural preflight returns no candidates and the AI wants to declare success | State that it did not render pages, resolve all styles, verify mathematics, or inspect native Word pagination. Require the remaining evidence |
