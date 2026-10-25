# Accessibility review log

This is an evidence register, not a conformance statement. Manual task-based checks have not been performed in this audit. Do not infer a pass from an HTML checker, a successful kernel, or a launch configuration.

## Automated scope

The commit-specific workflow checks page language/title/main/skip links, heading order, image-alt presence, named code regions, captioned/scoped tables and named scroll regions, local links/fragments, real kernel execution, scripts, app forms, and HTTP routes. These checks cannot judge equivalent descriptions, focus behavior, announcements, contrast, rendered reflow, or actual assistive-technology use.

## Manual module status

| Modules | Direct link, reading and headings | Execution, modification and saving | Practice and feedback | Keyboard, screen reader, zoom/reflow |
| --- | --- | --- | --- | --- |
| 1–4 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 5–7 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 8–11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 12–14 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

No platform/browser/assistive-technology version or tester is recorded because those tasks have not run. Record each module separately when tested; grouping here is only a compact view of identical pending status.

## Run the journey

Copy the accessibility-review template from the source archive. Start at a module direct link. Find outcomes and prerequisite help; read code and result equivalents; run and change the example; inspect a failure; save outputs; complete core practice and read feedback. Check keyboard focus, headings/landmarks, reading order, zoom/reflow, contrast, and descriptions. Test the actual app controls and notebook interface separately where used.

Initial proposed combinations are NVDA/Firefox on Windows and VoiceOver/Safari on macOS. These are test candidates, not verified compatibility. Record actual versions, dates, steps, results, barriers, effective alternatives, owner, and retest evidence. Do not record a person's diagnosis.

## Reporting and release gate

A public issue may describe a non-sensitive technical barrier. Do not post disability details, student records, private logs, or personal contact information. A private accessible reporting contact has not yet been configured; the maintainer must supply it before open release. Adopting instructors should provide their established private help route.

A blocking core task needs repair or a documented, tested equivalent route before that module is described as accessible for the affected workflow. Read the [policy](../../ACCESSIBILITY.md) and [release checklist](../release-checklist.md).
