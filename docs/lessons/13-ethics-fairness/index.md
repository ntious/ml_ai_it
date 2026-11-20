# Module 13: Ethics and fairness across the lifecycle

## Your route through this module

1. **Read:** start with the [foundation](foundation.md) and [concepts](concepts.md); use the [guided activity](guided.md) to work through an example.
2. **Run:** follow the complete-example commands on this page and inspect the saved output.
3. **Practice:** attempt the [practice tasks](practice.md) before opening answers.
4. **Check:** compare [practice notebook answers](solutions.md) and [interpretation feedback](feedback.md), then explain any corrections.


Audit group error/selection rates on historical census-income data while questioning whether the target and task are justified.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 90–150 minutes plus practice. Small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M13.1:** Identify stakeholders, historical label limitations, and inappropriate uses.
- **M13.2:** Fit a declared training pipeline without protected audit columns.
- **M13.3:** Report group counts, confusion denominators, selection rates, TPR, and FPR.
- **M13.4:** Explain metric trade-offs, proxy effects, and uncertainty without causal/legal claims.
- **M13.5:** Write a governance recommendation, including reasons not to deploy.

## Course outcomes and evidence

<!-- OUTCOME_EVIDENCE_START -->

<details>
<summary>For instructors: course outcomes and evidence</summary>

- **Direct evidence:** CLO8 (Communication)
- **Supporting practice:** CLO2 (Applying ML/AI to IT operations), CLO5 (GenAI and LLM integration), CLO6 (Deployment and monitoring)
- **Curriculum extension:** Responsible AI practice (privacy, fairness, limits)
- **Data and tools:** <span class="data-label">Real public</span>
- **Evidence you produce:** Group error and selection-rate audit with a governance recommendation, including reasons not to deploy. See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).
- **Boundary:** Descriptive fairness reasoning only; no legal compliance claim.
- **Responsible-AI check:** Is the task itself justified, not only the metric?

See the [outcome map](../../outcome-map.md) for all modules and the label definitions. These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.

</details>
<!-- OUTCOME_EVIDENCE_END -->



## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

Fairness is a contextual normative question, not one scalar score. Excluding a protected column cannot remove proxy effects or historical label bias. Group rate differences require denominators, sample context, and uncertainty; they do not prove a causal mechanism or legal conclusion.

## Real data and its limits

UCI Adult; historical census-income records. Recorded categories and collection conditions limit interpretation. This audit is not an eligibility service. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. The reference study uses attributed public observations. Practice fixtures, derived task labels and authored evaluation controls are identified separately; they are not additional real-world observations. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The provided Adult development/evaluation files are retained. Exact full-row overlaps are removed, without claiming person identity is known. Development is split for validation. Five numeric features feed training-only imputation/scaling/logistic regression; validation selects a threshold by balanced accuracy. Final sex/race columns are used only for aggregate audit, with unavailable rates left undefined.

Age remains a model input. Excluding sex/race does not exclude all sensitive or proxy information, and does not establish fairness.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the [core environment instructions](../../../QUICKSTART.md) and install the regression extra. Commands below start with the core environment's Python, `.venv`, which you created in [first run](../../../QUICKSTART.md#module-3-add-the-data-libraries). **The first run downloads the public dataset or model, so it needs internet**; later runs reuse the verified cache. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

macOS/Linux:

~~~sh
.venv/bin/python examples/income-fairness/scripts/run.py --output runs/module13
~~~

Windows PowerShell:

~~~powershell
.\.venv\Scripts\python.exe examples/income-fairness/scripts/run.py --output runs/module13
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module13/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module13/example/index.html "site-download:module13/example/index.html") without installing an execution interface.

Key artifacts:

- validation_thresholds.csv
- group_audit.csv
- protocol.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module13/walkthrough.ipynb "site-download:module13/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [UCI Adult source documentation](https://archive.ics.uci.edu/dataset/2/adult) — collection conditions, variables, missingness, and license. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Study uncertainty intervals or a validation-only mitigation proposal with stakeholder justification and explicit error trade-offs. Do not optimize a fairness number using final labels or claim that a numerical mitigation resolves legitimacy.

## Practice and continue

Complete [original practice](practice.md), then compare [interpretation feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 14](../14-agents/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

## Optional project connection

The [optional evaluation investigation](../../advanced/evaluation.md) distinguishes seed variation, illustrative bootstrap uncertainty, calibration and assumed error costs. It does not turn benchmark metrics into a deployment or fairness approval.

## Check before continuing

You have completed this module’s core learning route when you can:

- Save and explain this evidence: Group error and selection-rate audit with a governance recommendation, including reasons not to deploy.
- Attempt the practice tasks and explain a correction or why your original answer was sound.
- Explain this limitation in your own words: Descriptive fairness reasoning only; no legal compliance claim.

Use the answer pages to resolve gaps before continuing. Optional extensions are separate from this checklist.
