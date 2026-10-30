# Accessibility and learning routes

The resource supplies reading, script, notebook and text/table routes to support learners with different interface needs. The [authoring policy](../../ACCESSIBILITY.md) defines the design target; the [evidence log](review-log.md) records the tested scope.

## Available design provisions

The reading site uses semantic headings, landmarks, descriptive links, a keyboard skip link, visible focus and selectable code. Reports provide named results, CSV downloads and captioned tables with scoped headers. Charts include descriptions and numerical equivalents; series/groups use labels or marker/line distinctions alongside color.

Scripts and notebooks call the same shared functions. If a notebook interface presents a barrier, the script route preserves execution, data decisions, outputs and practice goals. Interpretation uses the same numerical evidence; plotting-authoring or implementation outcomes still require code and execution evidence.

## Display preferences and repository counts

Use the header’s **Theme** control to choose Light, Dark or System. The choice is stored in this browser; System follows your device setting. With JavaScript disabled, the site follows the device setting automatically.

The **Course repository** link opens the main branch. Its star and fork counts come from GitHub’s public API, with a 30-minute cache in the current browser tab. This request contacts GitHub without credentials or a referrer; it does not send exercise answers or search terms. These are repository statistics, not visitor analytics. If GitHub is unavailable or rate-limits the request, the link remains usable without counts.

## Verification scope

CI validates source/generated links, defined HTML properties, real notebook kernels, software behavior, app forms and HTTP health. Scripted Chromium checks cover the course overview, readiness, Python bridge, neural construction and phishing case, including skip-link focus, 320px page reflow and selected axe rules. The readiness page also has a dark-mode scan.

These checks establish their named automated properties. They do not establish WCAG conformance or human screen-reader/keyboard/real-zoom task completion in every reading, notebook or app interface. No human assistive-technology test sessions are recorded for this edition; use the [task log](review-log.md) to document findings and effective alternatives during independent review or adoption.

## Reporting a barrier

**Email accessibility reports to [ntiik@ucmail.uc.edu](mailto:ntiik@ucmail.uc.edu).** This address is for anyone reporting accessibility issues so maintainers can investigate and address them. A nonsensitive reproducible barrier may also be reported through a [repository issue](https://github.com/ntious/ml_ai_it/issues).

Include the module/link, version or commit if known, task attempted, expected result, observed barrier and any effective alternative. Browser/OS/assistive-technology versions can help when relevant; sharing a diagnosis, student record, password or personal medical information is unnecessary. A screenshot is optional. Course assessment/accommodation decisions remain with the institution's established support process.

## Review evidence and repairs

The [review log](review-log.md) separates browser automation from human sessions. Record actual tasks, barriers, owners, effective alternatives and retest evidence. Use the accessibility-review template in the source archive. A core task blocked in every documented route requires a repair or a tested equivalent route; a successful software run alone cannot establish accessible task completion.
