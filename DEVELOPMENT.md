# Development verification

## Increment 0.6.0: repository audit and portability

The audit reads all baseline tracked source files and adds a registry-backed architecture/integrity check, complete early-module teaching pages, reusable authoring and accessibility records, instructor adoption/assessment/pacing guidance, model-use summaries, citation and contribution templates. See REPOSITORY_REVIEW.md for scope and pending original-source reconciliation.

Verification now validates notebook format and runs real Jupyter kernels, retaining executed copies separately from clean source. Source-archive membership must equal tracked files. Added HTTP prefix tests and isolated installed-wheel inference exercise packaging and writable cache placement. Reading tables gain captions, scoped headers, and named keyboard-focusable regions.

Install the verification extra in the selected environment and register that environment before kernel execution:

~~~sh
python -m pip install -e ".[visualization,regression,verification]" -c environments/constraints-tested.txt
python -m ipykernel install --user --name ml-ai-core
python scripts/check_repository.py
python scripts/check_notebook.py --group core --kernel ml-ai-core
~~~

For frameworks use the separate environment and kernel in .github/workflows/checks.yml. Do not mix tested NumPy profiles. The complete workflow gathers actual reports/executed copies before building the site.

Modules 6–14 use checkout runs/ caches by default, an installed-package user cache otherwise, or ML_AI_RUNS_DIR set before import. Existing output-directory arguments remain explicit. The wheel check verifies actual installed inference independently from editable-source imports.

Manual keyboard/screen-reader/zoom, rendered notebook/app/figure review, learner piloting, and authoritative course crosswalk confirmation remain pending. The current local terminal is unavailable; exact-commit GitHub Actions logs are the runtime evidence. Historical entries below describe their own increments, not current missing modules.


## Increment 0.5.0: Modules 6–14

All remaining implementations/teaching packages are present: five pages per module (entry, foundation, practice, feedback, instructor), a commented seven-code-cell notebook, and a public script calling shared behavior. Nine new notebooks add 63 cells to the prior 27. New lessons use actual external records, not created synthetic datasets.

The local terminal remained unavailable. Initial classical integration passed 55 tests on Windows/Linux. Initial Linux CPU framework integration passed nine actual-framework tests, including all six additional scripts, training/reload, local generation, adapter gradients/replay, app forms, and HTTP health. Final notebook/site/archive integration must pass its own commit-specific run.

## Sources and profiles

Reviewed dataset hashes/attribution are recorded in the source registry. The official SMS citation is 2011, distinct from its 2012 donation date. The attached link document could not be reread through the unavailable terminal; live official sources were checked directly rather than claiming an inaccessible attachment review.

The local model is HuggingFaceTB/SmolLM2-135M-Instruct, revision 12fd25f77366fa6b3b4b768ec3050bf629380bac (Apache-2.0 card/license). Safetensors and disabled remote code are used. No paid API/token is required.

Core retains prior Windows/Linux dependencies. The isolated Linux CPU profile uses NumPy 2.1.3, pandas 2.2.3, scikit-learn 1.8.0, TensorFlow CPU 2.19.1, PyTorch CPU 2.6.0, Transformers 4.46.3, and Streamlit 1.44.1. These are exercised choices, not a full transitive lock or latest-version claim. Other framework platforms are not inferred.

## Module decisions and initial observations

| Module | Evidence and limits |
| --- | --- |
| 6 | Grouped real chemistry profiles; baseline/logistic/trees; validation-only choice. Logistic at threshold 0.3 initially gave TP19/FP30/FN10/TN184 and balanced accuracy about 0.7575 on 243 final rows. Classroom label, not certification. |
| 7 | Training scaling, predefined K, validation silhouette, original-unit profiles. Initially K=2. Quality excluded; cluster IDs are not ranks. Static observations do not validate an RL policy. |
| 8 | Actual TensorFlow training/checkpoint/reload. Initial neural balanced accuracy about 0.5927 versus 0.6295 for the fixed-threshold linear reference; more complexity is not presumed better. |
| 9 | Training vocabulary, embedding/pooling, lexical reference. Initial neural model missed all 30 positives: balanced accuracy 0.5 despite 87.5% accuracy. Lexical reference recovered six positives. |
| 10 | Actual local generation and strict parsing on eight balanced real messages. Initial schema success 0/8 is retained, not repaired into credited success. |
| 11 | Eight actual gradient steps; 2,304 rank-2 adapter parameters; prompt masking; real disjoint text IDs; numeric replay. Initial base/adapted final completion loss about 2.5106/2.5081 is mechanics evidence, not validated behavior. |
| 12 | Shared checked inference, actual-record defaults, two app forms, measured durations, four-batch replay. Source order of 243 real rows is not event time, so no temporal-drift/SLA claim is made. |
| 13 | Historic benchmark, full-row overlap removal, five numeric inputs including age, validation threshold, group audit. Income labels/categories do not justify decisions about people or establish fairness. |
| 14 | Actual model scoring over three legal plans, strict read-only tools, one-call budget, outside-model checks, source evidence. Legal plans can still misunderstand intent; unrestricted autonomy is not claimed. |

## Verification design

Both curated notebook groups execute in fresh namespaces. Their actual reports are copied to generated folders. Site assembly depends on both jobs and fails if evidence is missing; no placeholder result files are invented.

All new public scripts execute from another working directory. Trained neural models and adapters replay after save/load. AppTest exercises both forms; a separate server must return HTTP health. Error controls mutate actual records or authored requests, not training datasets.

Final assembly checks links/semantic structure, original-source ZIP byte matching, external-cache digests/attribution, extracted CLI, and package build. App source is included; external records/model caches remain separate.

The first complete assembly passed notebooks/site/archive checks but its final wheel step failed because a clean Python 3.12 runner lacked setuptools while build isolation was disabled. The step now uses the declared PEP 517 build environment; no offline-build claim is made for this release check.

## Remaining readiness work

Manual keyboard, screen-reader, zoom/reflow, rendered visual, notebook/app interface, macOS, Windows framework, and hosted routes remain pending. Automated checks are not accessibility conformance or production validation.

Domain transfer does not by itself demonstrate genuine IT-record application. Instructor mappings are evidence opportunities; no unseen original wording or master's-level ABET attainment is invented. Learner piloting, formal assessment review, merging, publication, and visibility changes remain separate.

## Increment 0.4.0: regression and reliable evaluation

Module 5 adds a real-data one-day-ahead forecasting study, a separately labeled synthetic fixture, explicit stage scripts, a commented notebook, foundation support, original practice/feedback, and instructor adaptation/alignment.

The local execution environment was unavailable. Development used GitHub's file/commit APIs and actual Windows/Linux GitHub Actions runs. Do not describe these as local executions. The initial implementation at d62e7b6 passed all 46 tests, including real UCI acquisition and the complete workflow. Scikit-learn 1.8.0 is added to the tested constraints.

## Module 5 decisions and observations

- The forecast is issued after a fully observed day for the next calendar day. Only prior-day/prior-week counts are included. Target-day weather/components/target are unavailable and excluded.
- UCI Bike Sharing supplies real, historical public data under CC BY 4.0. Original ZIP/CSV/README, attribution, retrieval time, and hashes remain together. The reviewed archive SHA-256 is b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401; original day.csv SHA-256 is a6bcf826782d3c0fbfdcbeead17cd0884185a0dafe8ff10cd48a874ee7ba18be.
- The original attached ZIP's dataset-link document could not be reread through the unavailable terminal in this increment. UCI's live official page was checked directly for source/rights rather than claiming a review of inaccessible attachment contents.
- The 731 daily records produce 724 examples after warm-up: 504 train, 110 validation, 110 final test. Fixed parameters are evaluated at rolling one-day-ahead origins; newly observed past holdout counts can become later lag features.
- Training fits only training rows. Validation chooses among dummy mean, daily/weekly persistence, and two simple linear pipelines. A baseline can win; alphabetical tie breaking is explicit. Final evaluation never refits or changes the choice.
- In the initial actual-data run, validation selected previous-day persistence. Final MAE was 926.572727 rentals/day, versus 2330.675325 for the training mean and 1382.1 for weekly persistence. Mean residual was -46.736364. The synthetic study instead selected weekly linear regression with MAE 17.438715. Neither result is generalized to current operations.
- The invalid identity/leakage demonstration is isolated from valid candidate selection. Training-only expanding-window folds illustrate where fitting belongs.
- Numeric JSON exposes the narrow supported model parameters and avoids executable model deserialization. It is not a general model interchange format.
- Text, captioned/scoped tables, CSV predictions/residuals, and descriptions accompany optional figures. Manual rendered-figure and assistive-technology review are pending, not inferred from remote execution.

## Module 5 outcome evidence

| Outcome | Original alignment | Course alignment | Advisory ABET opportunity | Evidence |
| --- | --- | --- | --- | --- |
| M05.1 | O05.1 | CLO1/CLO4 support | A1 | Equation/residual/loss arithmetic |
| M05.2 | O05.2 | CLO2, CLO4 | A2 | Trained pipeline and baselines |
| M05.3 | O05.3 | CLO2, CLO4 | A1, A2 | Feature availability and leakage audit |
| M05.4 | O05.4; explicit evaluation added | CLO4, CLO8 | A1, A2 | Chronological/frozen evaluation |
| M05.5 | O05.4 | CLO2, CLO8 | A3 | Reproducibility and stakeholder memo |

This follows the separate planning register. Advisory mappings are evidence opportunities, not attainment or accreditation claims.

## Increment 0.4.0 verification record

The final commit's CI must verify all 46 behavior tests (including 15 regression checks), five curated notebooks/27 plain-Python cells, the generated reading/report site, links/structure, and the extracted source CLI. The build records its actual page/archive counts. The initial core implementation already passed Windows/Linux; that does not substitute for checking the final integration commit. No local wheel build or manual figure review is claimed for this increment.

The source archive excludes downloaded external data; a separate attributed cache ZIP supports offline replay. Checks compare every source-archive entry with checked-out bytes, run the extracted CLI, and verify external cache digests. CI runs for pull requests and main updates, avoiding redundant push/PR runs for one branch change.


## Increment 0.3.0: exploration and visual communication

Module 4 is implemented with four measurable outcomes, a foundation bridge, shared script/notebook exploration, original practice/discussion, worked feedback, and adaptable criteria. Modules 1–3 remain available in sequence or by direct link. Module 5 is next; Modules 5–14 remain future work.

The local environment adds Matplotlib 3.10.8 and Seaborn 0.13.2 to Python 3.12.14, NumPy 2.3.5, and pandas 2.2.3. Node.js 24.22.1/Marked 17.0.5 build the reading site. Plotting uses the headless Agg backend and local data; no display server or dataset download is required. The optional `visualization` extra is exercised by CI and required for a complete site build.

## Module 4 observations and decisions

- Observation unit is one service-day. Supplied p95 values are already aggregated; their mean/median is not an overall request-level percentile.
- Normalize only documented service case/whitespace, retain the first exact duplicate, reject conflicting keys, and preserve raw bytes.
- Keep the missing-latency observation for request totals. Whole-row deletion would discard 130 known requests. Omit it only from latency-specific views.
- Retain the deliberately constructed 160 ms spike. An IQR flag invites investigation; sensitivity analysis demonstrates the effect of removal without establishing an error.
- Preserve raw fixture bytes through Git checkout using `.gitattributes`; the Module 4 checksum is also asserted in CI to expose data/provenance drift.
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
- The data SHA-256 checksum matches. All 68 allowlisted-source ZIP entries byte-match the source, with no private attached documents or workspace analysis. The documented CLI also runs from a freshly extracted archive outside the repository. Version 0.3.0 builds as an offline wheel without dependency downloads.

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

## Notebook verification references

The kernel execution/checking path follows the [nbclient execution API](https://nbclient.readthedocs.io/en/latest/client.html) and [IPython environment-specific kernel registration](https://ipython.readthedocs.io/en/stable/install/kernel_install.html). Source notebooks are validated with nbformat before execution; saved executed copies are distinct build artifacts. Their visual presentation still needs the manual inspection recorded in the review log.
