# Accessibility status and learning routes

Accessibility for blind and low-vision learners is a core requirement. See the [authoring and verification policy](../../ACCESSIBILITY.md).

## Available design provisions

The reading site uses semantic headings, landmarks, descriptive links, a keyboard skip link, visible focus, and selectable code. Modules 1–5 communicate their results in named text values. Module 4 adds chart-authoring and interpretation. Its figures have short alternatives, detailed descriptions, actual HTML/CSV data tables, and marker shapes in addition to colors. Reading the figures through this text/table evidence supports the interpretation goal; authoring still requires reproducible plotting code and artifacts. No pointer gesture or color distinction is required. Module 5 also supplies exact predictions/residuals and named error values alongside optional forecast/error figures. Rendered-figure review for Module 5 remains pending because its checks were executed remotely. Feedback and practice remain available as text.

Each module’s script and notebook call the same shared functions. If a notebook interface is a barrier, the script route preserves execution, data decisions, outputs, and practice goals. This route still needs testing with a learner's actual editor/terminal and assistive technology.

## Verification status

Software checks exercise data contracts, script outputs, notebook code, generated links, and basic HTML structure. These checks do not certify accessibility.

Keyboard-only browser review, NVDA/Firefox review, VoiceOver/Safari review, zoom/reflow, and learner task-based review are **pending**. No combination has been verified for screen-reader usability in this development edition. Third-party notebook and hosting interfaces also require evaluation.

## Reporting a barrier

For a nonsensitive issue, identify the module, task, platform/browser/assistive-technology versions if you wish, observed barrier, and any attempted route. Do not disclose medical diagnoses, credentials, or personal records in a public issue. An adopting instructor should provide a private reporting/help channel. A project-maintainer private contact route must be selected before public release.

## Release expectation

A module should not be described as ready for accessible independent use while a barrier blocks its core journey through every documented route. Publish actual results, effective alternatives, and known limitations as testing proceeds.

## Modules 6–14 evidence routes

New reports provide named text values, CSV downloads, captioned tables with scoped headers, and named keyboard-focusable table regions. Notebooks explain each stage and share the script implementation. Learning-history tables carry curve information without requiring an image.

AppTest interactions and HTTP health establish execution behavior, not screen-reader usability or WCAG conformance. Manual keyboard, screen-reader, zoom/reflow, notebook/app interface, and rendered visual review remain pending. Reading-only interpretation should not be credited as execution evidence.

## Review evidence

The [task-based review log](review-log.md) distinguishes automated structural/runtime evidence from manual tasks that remain NOT RUN. The source archive includes the reusable accessibility-review template. A private accessible reporting contact must be configured before open release.
