# Module 13: Ethics and fairness across the lifecycle

Audit group error/selection rates on historical census-income data while questioning whether the target and task are justified.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 90–150 minutes plus practice. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M13.1:** Identify stakeholders, historical label limitations, and inappropriate uses.
- **M13.2:** Fit a declared training pipeline without protected audit columns.
- **M13.3:** Report group counts, confusion denominators, selection rates, TPR, and FPR.
- **M13.4:** Explain metric trade-offs, proxy effects, and uncertainty without causal/legal claims.
- **M13.5:** Write a governance recommendation, including reasons not to deploy.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

Fairness is a contextual normative question, not one scalar score. Excluding a protected column cannot remove proxy effects or historical label bias. Group rate differences require denominators, sample context, and uncertainty; they do not prove a causal mechanism or legal conclusion.

## Real data and its limits

UCI Adult; historical census-income records. Recorded categories and collection conditions limit interpretation. This audit is not an eligibility service. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The provided Adult development/evaluation files are retained. Exact full-row overlaps are removed, without claiming person identity is known. Development is split for validation. Five numeric features feed training-only imputation/scaling/logistic regression; validation selects a threshold by balanced accuracy. Final sex/race columns are used only for aggregate audit, with unavailable rates left undefined.

Age remains a model input. Excluding sex/race does not exclude all sensitive or proxy information, and does not establish fairness.

## Run and inspect

Download the [complete source](../../setup/student-workspace.md#reading-reports-from-github "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the [core environment instructions](../../../QUICKSTART.md) and install the regression extra. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/income-fairness/scripts/run.py --output runs/module13
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module13/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](../../setup/student-workspace.md#reading-reports-from-github "site-download:module13/example/index.html") without installing an execution interface.

Key artifacts:

- validation_thresholds.csv
- group_audit.csv
- protocol.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](../../setup/student-workspace.md#reading-reports-from-github "site-download:module13/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [UCI Adult source documentation](https://archive.ics.uci.edu/dataset/2/adult) — collection conditions, variables, missingness, and license. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Study uncertainty intervals or a validation-only mitigation proposal with stakeholder justification and explicit error trade-offs. Do not optimize a fairness number using final labels or claim that a numerical mitigation resolves legitimacy.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 14](../14-agents/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Generated downloads/report links require the built reading artifact. Use [workspace and report access](../../setup/student-workspace.md); source notebooks are under notebooks/lessons in the repository.
