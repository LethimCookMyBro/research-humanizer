# Working-record schemas

Read only for the current task phase. The core rules in SKILL.md remain active.

## R29 Use explicit working-record schemas

The following field sets are templates, not populated research findings. Keep a compact representation appropriate to the project. CSV, JSON, YAML, a spreadsheet, or a structured note is acceptable when the fields stay inspectable.

| Record | Required fields |
| --- | --- |
| Project brief | task mode, research question, article type, venue, language, template, limits, anonymity, authoritative sources, requested outputs, unresolved decisions |
| Source manifest | source ID, path or URL, source kind, version or hash, role, inspected location, access date when relevant, status |
| Claim ledger | claim ID, claim text, evidence class, source IDs, precise locations, scope, counterevidence, verification status, manuscript destinations |
| Number ledger | number ID, quantity, raw value, displayed value, unit, evidence class, raw source, approved result source, configuration or run ID, formula, filters, denominator, aggregation, rounding, verification status, destinations |
| Notation sheet | symbol, name, definition, domain, shape, unit, first use, code mapping |
| Figure register | figure ID, scientific purpose, visual class, source IDs, selection rule, transformations, encoding, caption, editable source, export, rights, anonymity check, final-size check |
| Reference log | reference ID, verified metadata, source identifier, version, inspected passage, supported claims, access limits, correction status when relevant |
| QA report | check ID, artifact and version, operation performed, evidence location, status, issue, action, reviewer or tool, date |
| Decision log | issue, alternatives, evidence, chosen decision, decision owner, affected artifacts, unresolved dependencies |
| Missing-input register | request ID, missing item, affected section or figure, reason needed, sources already checked, question sent, researcher reply, source received or approved alternative, evidence class, unresolved dependency, status |
