# Accessibility
## Design and verification requirements for the ML and AI resource

Version 1.0 · October 24, 2026 · ML_AI_IT project

**Accessibility is a core requirement for every module, example, application, and release.** Blind and low-vision learners should be able to enter a module through a direct link, understand its concepts, run and modify code, interpret results, complete practice, and obtain feedback with an effective access route.

This is a development specification. The repository/site and execution routes have not yet been implemented or tested for accessibility. Publish actual test results and known limitations as development proceeds. The design target for the web content we control is **WCAG 2.2 Level AA**; meeting a short checklist or passing an automated scan does not establish conformance. [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)

## 1. Reading and navigation

Use semantic HTML, meaningful page titles, a logical heading hierarchy, descriptive links, and a skip-to-content mechanism. Keep essential explanations in selectable text. Prefer native controls over custom widgets. Do not require a mouse, visual position, or an unexplained icon to navigate or reveal core content. These choices follow WAI's [heading guidance](https://www.w3.org/WAI/tutorials/page-structure/headings/) and [design guidance](https://www.w3.org/WAI/tips/designing/).

For low-vision use, plan checks for text contrast, text enlargement, reflow, visible focus, and high-contrast/forced-color settings. Use the applicable WCAG criteria rather than assuming a dark theme is accessible. Initial manual checks include 200% text enlargement and a narrow/reflow view corresponding to 320 CSS pixels; code/data requiring two-dimensional layout needs careful handling rather than indiscriminate shrinking. Full keyboard operation and focus visibility must remain usable at the tested zoom settings. These are selected checks, not the full AA requirements. [WCAG quick reference](https://www.w3.org/WAI/WCAG22/quickref/)

Use tables for genuine comparisons/data, with clear captions and associated headers. Keep them small where possible; offer a linear explanation of complex outcome mappings. Verify rendered HTML semantics rather than assuming Markdown produces everything needed. [WAI tables tutorial](https://www.w3.org/WAI/tutorials/tables/)

## 2. Charts and visual explanations

Every instructional chart needs an equivalent explanation of what a learner is expected to infer. Add a short alternative identifying the visual, a nearby description of important relationships, and accessible numerical evidence where relevant. WAI's [complex-image guidance](https://www.w3.org/WAI/tutorials/images/complex/) explains the role of short and detailed alternatives.

Our ML-specific authoring requirements are:

- Name the task, axes/variables, units, groups, and intended comparison.
- Explain important patterns, exceptions, uncertainty, and limitations in text.
- Provide a small labeled HTML table or structured text for key values; supply the full data download when useful.
- For a confusion matrix, identify which dimension is actual versus predicted and explain error counts/costs in words.
- For learning curves, describe which series improves or diverges and the evidence for an overfitting interpretation.
- For trees, pipelines, neural architectures, and agent diagrams, provide a readable description of components, relationships, and decisions.
- Use labels, line styles, symbols, or patterns alongside color. Do not ask learners to identify the answer from color alone.

A CSV download alone does not explain the pattern, and a short alt label alone does not communicate a complex chart. Describe visual information without giving away an exercise's answer when independent interpretation is the goal: provide equivalent raw relationships/data and keep worked-answer feedback separate.

## 3. Code and execution

Teach the same concepts through an HTML reading path and a runnable code path. Keep code selectable/copyable, identify filenames and commands clearly, use meaningful variable names, and explain critical indentation, shapes, and expected outputs. Screenshots of code, mouse-only notebook instructions, or unexplained syntax colors cannot be the sole instruction.

Notebooks are one interface, not the only execution route. Provide scripts calling the shared Python implementation, written execution steps, text summaries of results, and explicit saving/recovery instructions. Keep outputs bounded and label metric names/units. Make verbose progress displays optional where they interfere with reading; test console behavior rather than assuming a terminal is accessible.

Evaluate the actual tool/version/browser/assistive-technology combination. JupyterLab's accessibility statement, last updated in July 2024 on the page inspected, recommends evaluating the simpler Jupyter Notebook interface in preference to JupyterLab for accessibility. This does not establish that either interface or every hosted environment meets our learners' needs. [Jupyter accessibility statement](https://jupyterlab.readthedocs.io/en/latest/getting_started/accessibility.html)

Do not claim Codespaces, Colab, Binder, or local notebook accessibility from the existence of a launch badge. Document a verified route and any barriers. If a third-party interface blocks the core task, provide an effective route to the same code, data, and learning evidence; do not offer an observation-only substitute for required execution.

## 4. Apps and multimedia

For applications, use programmatically associated labels, clear instructions/errors, keyboard-operable inputs, predictable focus, and readable/announced results where updates occur. Test charts, table widgets, upload controls, and downloads in the rendered app. Prefer a simple text/table result alongside any interactive visualization. Framework defaults require verification. [WAI forms guidance](https://www.w3.org/WAI/tutorials/forms/)

For recordings, narrate meaningful visual actions and code changes, identify the relevant file/section, and provide a descriptive transcript. Include captions for broader access. A transcript must explain essential visual information rather than merely repeat “as you can see here.” Do not make an undescribed video demonstration the only way to learn a workflow. [WAI media guidance](https://www.w3.org/WAI/media/av/)

Render equations as accessible text/math supported by the chosen output, and include a plain-language explanation of symbols and relationships. Do not rely on equation screenshots; verify the resulting reading order with assistive technology.

## 5. Practice and feedback

Practice must measure ML/AI reasoning and implementation rather than sight or mouse precision. Provide keyboard/text routes to selecting features, interpreting evaluation, tracing a pipeline, and receiving feedback. Avoid required drag-and-drop, drawing-only responses, inaccessible time limits, or location/color-only prompts.

For example, a Module 4 learner can analyze the labeled chart data and explain the same trend, uncertainty, and limitation. A Module 12 learner can operate the app through labeled controls and read the prediction/validation result. A Module 14 learner can inspect a structured text tool trace instead of depending on an animated diagram.

Provide feedback and worked examples in readable text. Optional challenges should meet the same accessibility standard as the core. Adopting instructors retain their accommodation processes, but our default materials should already support independent access.

## 6. Release checks and evidence

Combine automated checks with manual task-based review. Automated tools cannot establish the quality of chart descriptions, learning equivalence, or an entire screen-reader workflow. [WAI evaluation overview](https://www.w3.org/WAI/test-evaluate/)

For each released module, verify this journey:

1. Open its direct link, locate the title/outcomes, and navigate by headings and keyboard.
2. Access prerequisite help and read its code, data descriptions, and visual explanations.
3. Launch a tested execution route, run/change the example, inspect errors/results, and save work.
4. Complete core practice and access feedback without a visual-only or mouse-only step.
5. Test zoom/reflow and contrast, then record remaining barriers and their effective alternatives.

The initial screen-reader test plan should include NVDA with Firefox on Windows and VoiceOver with Safari on macOS where available. These are proposed test combinations, not verified compatibility claims. Add combinations relevant to learners and publish exact versions and dates. Invite voluntary review by blind/low-vision users without requiring diagnosis disclosure or making them responsible for all quality assurance.

Record module/release, platform/browser, assistive technology, task, observed result, barrier, workaround/equivalent route, owner, and retest status. Automated scans can assist with labels, names, contrast, and structural issues; keyboard/screen-reader and content reviews remain required.

**Acceptance rule:** do not mark a core module ready while an unresolved barrier prevents completing the learning journey through any documented effective route. Publish an accessibility statement with scope, verified combinations, known limitations, and a private reporting option. Report only tests actually performed. Learners should not have to post personal information in public GitHub issues.

## 7. Repository integration

Keep this policy at repository root as `ACCESSIBILITY.md`. Add `docs/accessibility/` for learner instructions, tested routes, known limitations, and reporting; `templates/accessibility-review.md` for the task record; and accessibility checks alongside site/app tests. Include accessibility review in lesson/case templates, contribution guidance, pull-request review, and release criteria.

Apply these requirements across Modules 1–3 and all subsequent modules. Accessibility work is part of implementation and maintenance, not a final visual review after the content is complete.

Sources checked October 24, 2026. The references inform our design; they do not certify this planned resource or replace testing its actual implementation.
