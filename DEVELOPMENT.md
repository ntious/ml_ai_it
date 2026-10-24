# Development verification

## Increment 0.2.0: Modules 1–3 in sequence

Modules 1 and 2 now precede the existing Module 3. Each has an entry page, measurable outcomes, runnable shared-code script/notebook examples, original practice, discussion/solo reflection, public worked feedback, adaptable criteria, and a skippable extension. Modules 4–14 and the model-training/deployment cases remain future work.

Development environment: Linux, Python 3.12.14, NumPy 2.3.5, pandas 2.2.3; Node.js 24.22.1 and Marked 17.0.5 for static Markdown rendering.

## Instructional decisions

- Follow the learner sequence from Module 1 onward. The earlier Module 3 implementation was a technical pilot, retained as a usable direct-entry lesson.
- Modules 1 and 2 execute with Python's standard library before introducing dependency installation in Module 3. Operating a notebook requires installing an interface separately.
- Module 1 distinguishes an explicit rule from a trained model. Prediction and generated-response comparisons are labeled design sketches; no unavailable model is presented as implemented.
- Module 2 makes containers, loops, conditionals, functions, imports, CSV/JSON, paths, and error handling visible before NumPy/pandas abstractions.
- Preserve the planned outcome identifiers M01.1–M01.4 and M02.1–M02.5. M01.3 offers a script execution/saving route alongside notebook operation; a script does not establish notebook-interface competence. M02.5's cross-interface comparison is demonstrated by shared code and checked cell results; actual notebook-interface operation remains a separate learner activity and usability check.
- Keep original course/master documents and the course-specific crosswalk outside the public source archive. Introductory tasks are evidence opportunities, not accreditation-attainment claims.
- Keep essential explanations, results, practice, and feedback in text. Do not infer accessibility conformance from automated structural checks.

## Local checks

- Twenty behavior tests pass: the original ten data-preparation tests plus threshold boundary/invalid-input, standard-library-only script execution from another working folder, file validation, empty averages, duplicate IDs, raw preservation, and output protection.
- Eleven curated Python code cells across three notebooks execute in fresh namespaces with checked results. The files contain no saved execution outputs. This is not a notebook-interface or full notebook-format certification.
- Practice values are checked: adding a 5-minute ticket yields 5 tickets, 65 minutes, average 13, and network 3 tickets/30 minutes. Header-only tickets retain an unavailable average and unchanged event counts. Invalid minutes fail before creating outputs.
- The original Module 3 checks still produce 12 input, 6 accepted, 6 rejected, 1 accepted missing latency, and observed latency mean/median 24/20 milliseconds.
- Eighteen reading pages build, with passing local link/fragment, heading-order, main/skip-link, language/title, image-alternative, and named focusable code-block checks.
- Synthetic service-file SHA-256 checksums match. The 56-file source archive has unique paths and byte-matches the source allowlist. It excludes raw attached course documents and workspace analysis.
- Version 0.2.0 builds as an offline wheel using installed tools, with no build-isolation or dependency download.

Remote Windows/Linux CI must be inspected for this commit after pushing. The preceding 0.1 increment passed both platforms; that does not substitute for checking this expanded sequence.

## Remaining verification

Keyboard/browser interaction, rendered visual/zoom/reflow review, screen-reader task completion, notebook installation/interface operation, macOS execution, and hosted notebook routes are pending. Automated checks do not certify accessible independent use. Record actual environments and barriers during a learner pilot.

Next implementation: Module 4, exploration and visual communication, followed by Modules 5–14 in order. Named numeric/text evidence must accompany every figure.

## Increment 0.1.0 history

The initial pilot implemented Module 3, reusable NumPy/pandas data preparation, controlled downloads, eleven reading pages, ten tests, and a four-code-cell notebook. Subsequent work retains that functionality while establishing the beginner sequence.
