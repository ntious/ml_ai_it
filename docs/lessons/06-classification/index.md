# Module 6: Classification and decision trees

## Your route through this module

1. **Read:** start with the [foundation](foundation.md) and [concepts](concepts.md); use the [guided activity](guided.md) to work through an example.
2. **Run:** follow the complete-example commands on this page and inspect the saved output.
3. **Practice:** attempt the [practice tasks](practice.md) before opening answers.
4. **Check:** compare [practice notebook answers](solutions.md) and [interpretation feedback](feedback.md), then explain any corrections.


Classify a declared human-rating threshold from real chemistry measurements, then explain the mistakes and decision threshold.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 90–150 minutes plus practice. Small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M06.1:** Define the positive class and explain confusion counts, precision, recall, and balanced accuracy.
- **M06.2:** Fit and compare a dummy classifier, logistic model, and depth-limited trees using validation only.
- **M06.3:** Explain a tree path and distinguish predictive importance from causation.
- **M06.4:** Justify group boundaries and a decision threshold before final evaluation.
- **M06.5:** Communicate error trade-offs and limits of the chosen label.

## Course outcomes and evidence

<!-- OUTCOME_EVIDENCE_START -->

<details>
<summary>For instructors: course outcomes and evidence</summary>

- **Direct evidence:** CLO4 (Frameworks and evaluation), CLO8 (Communication)
- **Supporting practice:** CLO1 (Learning paradigms), CLO2 (Applying ML/AI to IT operations)
- **Additional direct-evidence route (complete separately):** [IT-OPS (CLO2)](../../cases/it-operations-evidence.md)
- **Data and tools:** <span class="data-label">Real public</span>
- **Evidence you produce:** Classifier comparison chosen on validation data, with a confusion-matrix explanation. See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).
- **Boundary:** Wine chemistry builds technique; genuine flow classification is in the RT-IoT extension.
- **Responsible-AI check:** What do a false positive and a false negative cost, and who bears each?

See the [outcome map](../../outcome-map.md) for all modules and the label definitions. These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.

</details>
<!-- OUTCOME_EVIDENCE_END -->



The practice sandbox uses development data and its own declared bounds. The full reference retains its model-selection, final-evaluation and artifact contract.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A probability estimate is not automatically calibrated confidence. A threshold converts a score into a decision. False positives and false negatives can have different costs; balanced accuracy gives equal weight to recall in each class, not to operational cost.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. The reference study uses attributed public observations. Practice fixtures, derived task labels and authored evaluation controls are identified separately; they are not additional real-world observations. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The target is quality score at least seven, a classroom choice. Identical chemistry profiles are kept within one seeded group split. A dummy, logistic regression, and depth-2/4/8 trees are fitted on training; validation chooses a model and threshold from 0.3, 0.5, 0.7. Final labels never choose them. A shallow tree is exported as readable rules even when another method wins.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the [core environment instructions](../../../QUICKSTART.md) and install the regression extra. Commands below start with the core environment's Python, `.venv`, which you created in [first run](../../../QUICKSTART.md#module-3-add-the-data-libraries). **The first run downloads the public dataset or model, so it needs internet**; later runs reuse the verified cache. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

macOS/Linux:

~~~sh
.venv/bin/python examples/wine-classification/scripts/run.py --output runs/module06
~~~

Windows PowerShell:

~~~powershell
.\.venv\Scripts\python.exe examples/wine-classification/scripts/run.py --output runs/module06
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

Complete [original practice](practice.md), then compare [interpretation feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 7](../07-clustering/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

## Optional project connection

Extend model comparison with the [optional grouped tuning investigation](../../advanced/tuning.md) and [complete capstone exemplar](../../../projects/phishing-triage/README.md). These are separate experiments; this module remains independently runnable.

## Check before continuing

You have completed this module’s core learning route when you can:

- Save and explain this evidence: Classifier comparison chosen on validation data, with a confusion-matrix explanation.
- Attempt the practice tasks and explain a correction or why your original answer was sound.
- Explain this limitation in your own words: Wine chemistry builds technique; genuine flow classification is in the RT-IoT extension.

Use the answer pages to resolve gaps before continuing. Optional extensions are separate from this checklist.

## Connect this module to the whole study

Distinguish feature selection from prediction; check a confusion matrix. Use the [course-wide lifecycle map](../../connections.md#module-6-compare-decisions-and-errors) and the [research-case connection](../../cases/three-tier-lstm/06-classification.md). This is a short reading/reflection route; use this module's existing practice for implementation evidence.
