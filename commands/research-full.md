---
name: research-full
description: Draft a full paper with ARS and the Research Humanizer research-writing contract.
disable-model-invocation: true
---

Load `research-humanizer:research-paper-craft` through the host Skill tool first, with the user's request and explicit `full-paper` mode. Read its full-paper, literature and ARS integration modules in one language. Resolve these files from this plugin's installed root, not the user's working directory. If a required file cannot be loaded, report the failure instead of substituting this summary.

Then discover the installed ARS entry. The inspected Claude entry is `academic-research-skills:academic-pipeline`. Read and invoke the actual available entry with the user's full-paper request and the Research Humanizer handoff. Do not invoke ars-full as a Skill because the inspected ars-full command disables model invocation and forwards to this pipeline. Do not invent a mode called full for the orchestrator. Select full drafting for its academic-paper WRITE phase according to the installed instructions.

If ARS is already running, attach the handoff at the next permitted checkpoint and continue its state. Never recursively invoke this command or launch a duplicate pipeline. If ARS or its required resources are unavailable, stop the ARS route, explain the missing dependency, and offer the separately identified standalone route. Do not claim ARS execution.

Keep ARS confirmation, integrity, privacy, and tool-consent gates. Pass source versions, mandatory style, literature/metric plans, original-image requirements, Word-first restrictions and pending inputs to each delegated writer, reviewer and formatter. Record actual resource loading. This is a prompt-level coordinator, not a runtime hook that intercepts other plugins.

Apply scientific humanizing during drafting. Load the punctuation review through the writing guide. Each writer and reviewer must check clause load and preserve necessary notation. Return a full source-bound manuscript when evidence supports it, not only an outline or rewritten abstract. Unknown study details remain marked and require researcher input. Never turn another paper's metrics or results into this study's observations. Review the saved artifact, figures, equations, anonymity and applicable native Word checks before assigning delivery status.

User request follows in `$ARGUMENTS`.

Within existing ARS Research, Planning and Review stages, apply the research-reasoning guide to gap/RQ fit, methods/evidence and findings/contribution/impact. Reuse the existing handoff and records. Preserve researcher confirmations.
