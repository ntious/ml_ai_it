# Module 8: Neural networks with TensorFlow

Read the overview and learning outcomes here, then follow the learning route. Return to this page’s run instructions for the complete study.

Train a small real neural classifier, select a checkpoint on validation, and test saved-model replay against a simpler baseline.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M08.1:** Explain input, hidden activation, output probability, loss, and gradient updates.
- **M08.2:** Fit training-only numeric preprocessing and a TensorFlow network.
- **M08.3:** Select a checkpoint using validation loss without fitting to final labels.
- **M08.4:** Compare held-out errors with a logistic baseline.
- **M08.5:** Save/reload a trained model and document compute and limitations.

## Learning sequence for this module

Follow [foundation](foundation.md) → [applied concepts](concepts.md) → [guided construction](guided.md) → [independent practice](practice.md) → [practice feedback](solutions.md) → the complete reference workflow below. If experienced, attempt practice first and use feedback to locate gaps.

The practice sandbox uses development data and its own declared bounds. The full reference retains its model-selection, final-evaluation and artifact contract. Human learner piloting of this prototype is pending.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A dense layer combines inputs with learned weights and a bias; ReLU supplies a nonlinear hidden activation. A sigmoid output lies between zero and one. Binary cross-entropy supplies the gradient objective; a low training loss does not establish held-out performance.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

Training-only scaling feeds eleven numeric inputs, a 16-unit ReLU layer and one sigmoid output. An explicit minibatch GradientTape loop updates weights for at most 40 epochs, stopping after five epochs without a new minimum validation loss. The best observed checkpoint is restored. Neural and logistic thresholds are selected separately on validation balanced accuracy over 0.05–0.95 in steps of 0.05. Final labels select neither weights nor thresholds. Saved-model replay checks the trained network.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). Run framework commands in the Linux CPU reference environment; see the [support matrix](../../status.md) for platform coverage. Reading the reports needs no framework installation. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/wine-neural-network/scripts/run.py --output runs/module08
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module08/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module08/example/index.html "site-download:module08/example/index.html") without installing an execution interface.

Key artifacts:

- learning_history.csv
- comparison.csv
- test_predictions.csv
- numeric_preprocessing.json
- model.keras

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module08/walkthrough.ipynb "site-download:module08/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [TensorFlow Sequential models](https://www.tensorflow.org/guide/keras/sequential_model) — layer construction, input shape, and training state. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Declare another width, epoch budget, or class-weight policy as a development experiment. Explain parameter count and resource effects; do not require a GPU or treat the extension as necessary for core completion.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 9](../09-neural-nlp/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).

## Optional project connection

The [optional stability investigation](../../advanced/stability.md) explains fixed-data training variation versus sensitivity to the partition. The worked experiment uses CPU classical models, so it requires no repeated neural training budget.
