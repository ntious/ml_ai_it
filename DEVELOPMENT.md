# Development verification

## Increment 0.3.0: exploration and visual communication

Module 4 is implemented with four measurable outcomes, a foundation bridge, shared script/notebook exploration, original practice/discussion, worked feedback, and adaptable criteria. Modules 1–3 remain available in sequence or by direct link. Module 5 is next; Modules 5–14 remain future work.

The local environment adds Matplotlib 3.10.8 and Seaborn 0.13.2 to Python 3.12.14, NumPy 2.3.5, and pandas 2.2.3. Node.js 24.22.1/Marked 17.0.5 build the reading site. Plotting uses the headless Agg backend and local data; no display server or dataset download is required. The optional `visualization` extra is exercised by CI and required for a complete site build.

## Module 4 observations and decisions

- Observation unit is one service-day. Supplied p95 values are already aggregated; their mean/median is not an overall request-level percentile.
- Normalize only documented service case/whitespace, retain the first exact duplicate, reject conflicting keys, and preserve raw bytes.
- Keep the missing-latency observation for request totals. Whole-row deletion would discard 130 known requests. Omit it only from latency-specific views.
- Retain the deliberately constructed 160 ms spike. An IQR flag invites investigation; sensitivity analysis demonstrates the effect of removal without establishing an error.
- Do not infer zero workload for absent dates/services. Daily tables state coverage, and absent dates break the time line.
- Generate four analytical figures and one labeled misleading-axis demonstration. Each figure has a short alternative, a detailed description, and the exact CSV/HTML table used to plot it. Scatter text notes overlap and avoids causal claims.
- Include a notebook variation that authors a horizontal comparison, rather than asking learners only to run a finished report. Core practice requests a purposeful modification and its reproducible evidence.
- Keep GenAI optional. The same critique checklist and public feedback support learners without an assistant. Final-test data must stay outside later model-directed exploratory choices.

## Module 4 alignment and evidence

This implements the existing curriculum proposal, using its identifiers. Original-outcome references point to the supplied private M4 source register; that source is not published. Course and ABET labels retain the advisory definitions in the separate planning crosswalk. They are evidence opportunities, not attainment or accreditation claims.

| Module outcome | Original alignment | Course alignment | Planned advisory ABET opportunity | Evidence |
| --- | --- | --- | --- | --- |
| M04.1: preprocessing rationale | O04.1 | CLO3 | A1 | Row accounting and sensitivity explanation |
| M04.2: labeled, appropriate plots | O04.2 | CLO8 | A2, A3 | Plotting code, three figures, matching tables and scales |
| M04.3: evidence-based interpretation | O04.3 | CLO3, CLO8 | A1, A3 | Exact values, anomaly discussion, causal limits |
| M04.4: stakeholder communication | O04.2–O04.3 | CLO8 | A3 | Memo, useful descriptions, and limitations |

## Increment 0.3.0 verification

- All 31 behavior tests pass, including 11 exploration tests covering reconciliation, missingness, retained flags, sensitivity, conflicts, invalid values, exact grouped-count bounds, empty input, absent dates, all-missing latency, artifact pairs, and raw/output preservation.
- Four curated notebooks execute 17 code cells in fresh namespaces with expected results. Notebook-interface operation is not tested by this executor.
- The documented CLI produces 25 raw rows → 24 observations, 4,180 requests, 23 observed latencies/1 unavailable, mean daily service p95 about 38.70 ms, median 34 ms, and one retained IQR flag.
- Practice changes are checked: dropping the unavailable-latency row gives 4,050 requests and 23 normalized rows; excluding only the flagged latency gives 22 observed values, mean about 33.18 ms, median 33 ms.
- All five generated PNGs were inspected for legible labels, units, scales, clipping, and the axis demonstration. This figure-file review is not browser/zoom/screen-reader testing.
- The build produces 22 reading pages plus the generated evidence report: 23 HTML pages pass local link/fragment and basic structural checks. The evidence report includes five captioned tables with scoped column headers and named keyboard-focusable table regions.
- The data SHA-256 checksum matches. All 67 allowlisted-source ZIP entries byte-match the source, with no private attached documents or workspace analysis. The documented CLI also runs from a freshly extracted archive outside the repository. Version 0.3.0 builds as an offline wheel without dependency downloads.

Remote Windows/Linux results must be inspected after pushing this increment. Manual keyboard/browser, screen-reader, zoom/reflow, notebook-interface, macOS, and hosted-route testing remain pending; no conformance is claimed.

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
