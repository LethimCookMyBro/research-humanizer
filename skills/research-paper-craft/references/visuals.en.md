# Scientific visuals and tables

Read only for the current task phase. The core rules in SKILL.md remain active.

## R18 Plan visuals by scientific function

Create a visual specification before making each figure. Record the question it answers, visual type, data or source asset, inclusion rule, transformations, units, notation, planned caption, manuscript location, and editable source format.

Use the smallest set of visuals that makes the method and evidence understandable. A full-paper request does not mean every paper needs a system overview, infographic, photograph, heatmap, and schematic. Remove a visual that repeats another without adding information.

Separate an explanatory schematic, a plot calculated from data, an observed scientific image, and a generated illustrative image. Their evidentiary roles are different. Never present a conceptual rendering as a photograph of an experiment or use generated pixels as a substitute for a measured plot.

Use reproducible data plotting for quantitative evidence and an editable diagram workflow for exact system relationships. Use image generation only for a requested, clearly labeled illustrative role when the target venue permits it. Generated scientific outputs that are themselves the subject of the research require the actual method, provenance, and evaluation, not fabricated substitutes.

Prefer a restrained visual hierarchy, clear labels, readable spacing, and consistent terminology. Do not default to glowing gradients, decorative network nodes, arbitrary icons, pseudo-3D blocks, or a poster-like marketing layout. A graphical abstract must remain faithful to the verified paper.

Before producing a planned visual, check that its required data and source assets are available and match the study. If an original environment photograph, setup image, actual screenshot, or other necessary input is missing, apply R01 and ask the researcher before searching for or generating a substitute. Do not silently change an evidence figure into an illustration.

### Real-first visual decision

When a figure must show what the experiment actually looked like, use the matching original photograph or actual system capture. Prefer a real-first panel with concise, traceable annotations over a photorealistic substitute. A photograph is not automatically better than a diagram for an abstract computation. Select the medium for the scientific question, and combine separate labeled panels when both context and logic matter.

If the original is unavailable, ask the researcher and offer the [capture checklist](../assets/capture-checklist.md). Record the missing input and continue unrelated work. Never search stock sites or generate a similar environment in its place. Never use generative fill, object removal, synthetic participants, fabricated displays or invented equipment as observed evidence. Preserve the unmodified original and an edit log. Privacy redaction must be authorized, visible where relevant and kept separate from the original.

Use [figure-manifest.json](../assets/figure-manifest.json) only as an unfilled register. Record each panel's role, claim links, source hashes, study/configuration linkage, selection rule, transformations, rights and final-size review. Mixed photo/diagram figures need panel-level provenance. A hash proves byte identity, not authenticity or permission. Source review remains a human responsibility. The default is original assets plus reproducible plots and editable vector diagrams, not generated artwork.

## R19 Make the system overview correspond to the method

Show the actual system boundary, inputs, essential processing stages, outputs, and material external dependencies. Identify training, inference, offline, online, human, and automated steps when those distinctions matter.

Give each arrow a clear meaning such as data flow, control, dependency, or feedback. Use a legend when different arrow styles carry different meanings. Do not draw a connection merely to fill space. Do not imply feedback, parallelism, or causal influence that the implementation does not contain.

Keep module names consistent with the method and implementation map. Show optional or proposed components differently from implemented ones and explain the distinction. Do not visually present a proposed extension as evaluated functionality.

Arrange the diagram with a coherent reading direction. Avoid crossing connectors, unexplained abbreviations, and long sentences inside boxes. Use a separate detail figure when an overview would otherwise become unreadable.

Inspect the rendered diagram at its actual manuscript size. Check arrow direction, labels, symbols, clipping, panel order, and grayscale readability. Keep editable source and a publication-ready export. Do not claim that a diagram has been verified against code without inspecting the relevant implementation.

Build a component-and-edge register before drawing. Each node and arrow needs a source locator in the method, code revision, configuration or confirmed researcher note. Distinguish data flow from causal inference. Label implemented, proposed and external elements. Use real screenshots or apparatus crops as separate evidence panels when they answer the figure's question. The connecting diagram remains a schematic, not a photograph. Explain one reading path with aligned labels, restrained grouping and useful whitespace. Remove decorative icons, redundant arrows and unexplained color. A graphical abstract or infographic must let the reader recover the question, operation and supported outcome without invented numbers or a marketing headline.

## R20 Produce graphs from verified data

Choose a graph for the comparison. Use lines for ordered trends, scatter plots for relationships, and appropriate distribution or interval plots for variation. Do not connect unordered categories as though they were a continuous progression. A bar chart is not a substitute for showing a distribution when distributional differences drive the claim.

Generate quantitative graphics from the verified data or result export through a recorded script or equivalent reproducible workflow. Retain the plotted data and transformations. Do not redraw a more attractive trend by hand, invent points, smooth a curve without disclosure, or hide unsuccessful runs.

Label axes with the measured quantity and units. State normalization, logarithmic scaling, aggregation, uncertainty, sample size where relevant, and missing or excluded values. Use comparable axis ranges for direct comparisons or clearly explain differences. Magnitude-encoding bars ordinarily need a meaningful baseline. Any truncation or axis break must be visible and justified.

Use the same visual encoding for the same method across the paper. Make groups distinguishable through labels, line styles, markers, or patterns as well as color. Check grayscale readability. Do not use a misleading color scale, unnecessary 3D effects, or background decoration that interferes with the data.

Show uncertainty only when it is actually calculated and defined. A shaded band must not imply a confidence interval if it represents a range or standard deviation. Explain nonlinear transformations and the scale on which intervals were computed when relevant.

Use the venue's actual font, size, resolution, and format requirements. Prefer vector output for line art when the venue supports it. Retain suitable raster originals for image data. Do not invent a universal resolution requirement or shrink labels below readability to fit a page.

If the data, units, conditions, or transformation needed for a plot are missing or unverified, ask the researcher for the correct source under R01. Do not estimate unseen measurements or borrow another study's data to finish the figure.

Record the independent unit before plotting. Repeated frames, trials or folds are not automatically independent participants. Preserve pairing and clustering. Define the displayed estimand, weighting, denominator and inclusion rule. Choose uncertainty appropriate to that unit. Do not use within-trial variation as participant-level uncertainty or treat SD, SE and confidence intervals as interchangeable. Show distributional information when a summary conceals the relevant structure. Do not imply significance from error-bar overlap alone.

Reconcile the plotted values with the approved result export using an explicit numerical tolerance justified by precision. Keep raw data, plot-ready data, filters, aggregation, code revision, random seed if used, environment and output hashes. Recompute a spot check independently where feasible. Check nonfinite values, missing groups, duplicate records, reversed labels, unit conversions and excluded failures. Declared hashes and a successful script run are not a statistical validation.

Inspect graph exports at the actual single- or double-column size, in grayscale and at readable zoom. Check tick density, label collisions, legend order, numerical precision, clipping, contrast and distinguishable markers. Keep axis ranges comparable when needed, justify any break, and disclose smoothing or jitter. Do not impose a single aesthetic on every dataset. Use [graph-review.md](../assets/graph-review.md) for evidence of the checks. `audit_figures.py` checks local contracts and selected CSV values, not rendered quality or the analysis itself.

## R21 Protect scientific image integrity

For photographs, screenshots, microscopy, maps, sensor imagery, or other observed images, record the source, acquisition context, sample identifier where appropriate, permissions, and processing history. Keep the original unmodified asset.

Use only justified transformations. Disclose cropping, contrast adjustments, denoising, registration, compositing, or annotation when they affect interpretation. Apply comparison processing consistently. Do not remove inconvenient features, duplicate evidence panels, move objects, or add an apparent experimental result.

Explain scale bars, orientation, color mappings, and annotations. Do not invent a scale bar without calibration. Document the sample-selection rule for representative images and show failure examples when they matter to the claim.

Check copyright, consent, privacy, and the target venue's current image and AI policy. Label illustrative renders and synthetic examples clearly. An illustration cannot establish that a device was built or an experiment occurred. Do not upload confidential source images to an external service without authorization.

For a real-world environment or apparatus figure, establish that the asset belongs to this study and corresponds to the described setup. When the file or that connection is missing, ask the researcher under R01. A similar-looking scene is not a verified scene from this experiment.

If generated images are themselves the object of the study, preserve the actual experimental outputs, model/configuration and evaluation provenance. This is a distinct research-output case, not permission to manufacture a missing experiment photo. The optional figure checker does not certify that case and may flag it for manual review. Check the target venue's current policy instead of assuming one publisher's rules apply everywhere.

## R22 Make tables and captions independently interpretable

Use a table when readers need exact values, multiple conditions, or structured comparisons. Keep column names short and put units in headers or notes. Separate incomparable protocols rather than ranking them as though they were equivalent.

Distinguish zero, missing, not measured, not applicable, and not reported. Explain all abbreviations and uncertainty notation. Use consistent precision within a meaningful comparison without concealing a relevant difference.

Emphasize a best value only after defining the direction, comparison set, tie policy, and relevant uncertainty. Do not imply that a numerically larger value is statistically better. Do not use checkmarks for an unverified capability.

A caption should explain what is shown, the relevant data or conditions, the meaning of panels and encodings, and any essential uncertainty or processing convention. Include a source credit when needed. Do not repeat the entire results paragraph or introduce an unsupported interpretation. Apply the prose punctuation rules to captions and notes.
