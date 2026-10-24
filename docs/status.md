# Development status

Development edition 0.2.0 implements Modules 1–3. It is not the complete 14-module course.

## Implemented

- Module 1: terminology, method choice, first Python run, a saved threshold-rule result, original practice and feedback.
- Module 2: a beginner bridge, reusable functions, CSV/JSON processing, invalid-input investigation, original practice and feedback.
- Module 3: NumPy/pandas data preparation, accepted/rejected outputs, quality reporting, original practice and feedback.
- A shared implementation, a command-line script and curated notebook per module, synthetic data and provenance.
- Static reading pages, controlled source/data/notebook downloads, automated behavior/code/link/structure checks, and Windows/Linux CI.

## Verification boundaries

Exact local results are recorded in `DEVELOPMENT.md` in the repository. Remote CI is separate evidence for each commit. Windows and Linux passed for the earlier 0.1 increment; the expanded sequence must pass its own run. macOS has not been exercised.

Notebook code checks do not test notebook UI. HTML structure/link checks do not establish WCAG conformance. Browser/keyboard, screen-reader, visual/zoom/reflow review, and hosted execution routes remain pending. No accessible-use certification is claimed.

## Next development

Develop Module 4, exploration and visual communication, with named numerical/text evidence for every figure. Continue in order through Module 14. Each increment needs its own usable example, prerequisites, practice, feedback, and verification. Accessibility piloting remains part of development across modules.

GitHub Pages publication and repository visibility changes are separate release actions, not performed by this increment.
