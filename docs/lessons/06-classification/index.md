# Module 6: Classification and decision trees

Read the overview and learning outcomes here, then follow the learning route. Return to this page’s run instructions for the complete study.

Classify a declared human-rating threshold from real chemistry measurements, then explain the mistakes and decision threshold.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 90–150 minutes plus practice. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M06.1:** Define the positive class and explain confusion counts, precision, recall, and balanced accuracy.
- **M06.2:** Fit and compare a dummy classifier, logistic model, and depth-limited trees using validation only.
- **M06.3:** Explain a tree path and distinguish predictive importance from causation.
- **M06.4:** Justify group boundaries and a decision threshold before final evaluation.
- **M06.5:** Communicate error trade-offs and limits of the chosen label.

## Learning sequence for this module

Follow [foundation](foundation.md) → [applied concepts](concepts.md) → [guided construction](guided.md) → [independent practice](practice.md) → [practice feedback](solutions.md) → the complete reference workflow below. If experienced, attempt practice first and use feedback to locate gaps.

The practice sandbox uses development data and its own declared bounds. The full reference retains its model-selection, final-evaluation and artifact contract. Human learner piloting of this prototype is pending.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A probability estimate is not automatically calibrated confidence. A threshold converts a score into a decision. False positives and false negatives can have different costs; balanced accuracy gives equal weight to recall in each class, not to operational cost.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The target is quality score at least seven, a classroom choice. Identical chemistry profiles are kept within one seeded group split. A dummy, logistic regression, and depth-2/4/8 trees are fitted on training; validation chooses a model and threshold from 0.3, 0.5, 0.7. Final labels never choose them. A shallow tree is exported as readable rules even when another method wins.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the [core environment instructions](../../../QUICKSTART.md) and install the regression extra. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/wine-classification/scripts/run.py --output runs/module06
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module06/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module06/example/index.html "site-download:module06/example/index.html") without installing an execution interface.

Key artifacts:

- validation_scores.csv
- test_scores.csv
- test_predictions.csv
- tree_importance.csv
- tree_rules.txt

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module06/walkthrough.ipynb "site-download:module06/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [scikit-learn decision trees](https://scikit-learn.org/stable/modules/tree.html) — classification, tree structure, and overfitting controls. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Declare a class-weight or tree-depth alternative before final evaluation. Use training-only cross-validation, then the same validation rule. Additional tuning is optional and needs fresh evaluation planning once the public final data have been viewed.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 7](../07-clustering/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).

## Optional project connection

Extend model comparison with the [optional grouped tuning investigation](../../advanced/tuning.md) and [complete capstone exemplar](../../../projects/phishing-triage/README.md). These are separate experiments; this module remains independently runnable.
