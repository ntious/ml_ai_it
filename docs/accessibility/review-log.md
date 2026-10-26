# Accessibility review log

This evidence register separates automated checks from human task-based sessions. It records no human assistive-technology sessions for this edition; software/browser checks retain their own named scope.

## Automated scope

The commit-specific workflow checks page language/title/main/skip links, heading order, image-alt presence, named code regions, captioned/scoped tables and named scroll regions, local links/fragments, real kernel execution, scripts, app forms, and HTTP routes. The additional browser checks below exercise selected focus, reflow and accessibility-rule properties. Human description quality, announcements and actual assistive-technology task completion require separately recorded sessions.

## Manual module status

| Modules | Direct link, reading and headings | Execution, modification and saving | Practice and feedback | Keyboard, screen reader, zoom/reflow |
| --- | --- | --- | --- | --- |
| 1–4 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 5–7 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 8–11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 12–14 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

The NOT RUN entries refer specifically to human task-based review. Automated keyboard-focus and narrow-screen checks are recorded below. Add the actual tester/environment/task when a human session takes place; do not infer human results from browser automation.

## Run the journey

Copy the accessibility-review template from the source archive. Start at a module direct link. Find outcomes and prerequisite help; read code and result equivalents; run and change the example; inspect a failure; save outputs; complete core practice and read feedback. Check keyboard focus, headings/landmarks, reading order, zoom/reflow, contrast, and descriptions. Test the actual app controls and notebook interface separately where used.

Initial proposed combinations are NVDA/Firefox on Windows and VoiceOver/Safari on macOS. These are test candidates, not verified compatibility. Record actual versions, dates, steps, results, barriers, effective alternatives, owner, and retest evidence. Do not record a person's diagnosis.

## Reporting and release gate

A public issue may describe a non-sensitive technical barrier. Do not post disability details, student records, private logs, or personal contact information. Email accessibility barriers to [ntiik@ucmail.uc.edu](mailto:ntiik@ucmail.uc.edu). Anyone may report an accessibility issue so maintainers can address it. Course-specific accommodation requests use the institution's established route.

A blocking core task needs repair or a documented, tested equivalent route before that module is described as accessible for the affected workflow. Read the [policy](../../ACCESSIBILITY.md) and [release checklist](../release-checklist.md).

## Scripted browser regression checks added October 25, 2026

scripts/check_browser.mjs checks selected core pages (overview, readiness, Python bridge, neural construction and phishing case), the optional capstone entry/report, and the advanced entry/tuning/stability/evaluation pages. It exercises first-tab skip-link focus, Enter-to-main focus, 320 CSS-pixel page reflow and selected axe WCAG A/AA rules; the readiness page is also scanned in dark mode. A long unbroken dataset hash initially caused page overflow and the stylesheet now permits word wrapping. The repeatable check and screenshots run in CI. This is browser automation, not a human keyboard, real zoom, screen-reader, notebook or app-interface review. The manual status table above remains NOT RUN until those tasks have actual evidence.

## Learner README review

The rewritten README is built as the learner-facing course overview. Browser checks now include this fifth page, alongside readiness, the Python bridge, neural construction and the phishing case. This expands scripted focus, reflow and selected accessibility-rule coverage; the manual testing status remains unchanged.
