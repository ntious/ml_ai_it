# Module 8: Neural networks with TensorFlow

## Your route through this module

1. **Read:** start with the [foundation](foundation.md) and [concepts](concepts.md); use the [guided activity](guided.md) to work through an example.
2. **Run:** follow the complete-example commands on this page and inspect the saved output.
3. **Practice:** attempt the [practice tasks](practice.md) before opening answers.
4. **Check:** compare [practice notebook answers](solutions.md) and [interpretation feedback](feedback.md), then explain any corrections.


Train a small real neural classifier, select a checkpoint on validation, and test saved-model replay against a simpler baseline.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M08.1:** Explain input, hidden activation, output probability, loss, and gradient updates.
- **M08.2:** Fit training-only numeric preprocessing and a TensorFlow network.
- **M08.3:** Select a checkpoint using validation loss without fitting to final labels.
- **M08.4:** Compare held-out errors with a logistic baseline.
- **M08.5:** Save/reload a trained model and document compute and limitations.

## Course outcomes and evidence

<!-- OUTCOME_EVIDENCE_START -->

<details>
<summary>For instructors: course outcomes and evidence</summary>

- **Direct evidence:** CLO4 (Frameworks and evaluation), CLO8 (Communication)
- **Supporting practice:** CLO2 (Applying ML/AI to IT operations)
- **Additional direct-evidence route (complete separately):** [IT-OPS (CLO2)](../../cases/it-operations-evidence.md)
- **Data and tools:** <span class="data-label">Real public</span>
- **Evidence you produce:** Trained and reloaded TensorFlow model compared with a simpler reference. See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).
- **Boundary:** CPU-scale wine classification; IT operations transfer and production scale are not demonstrated.
- **Responsible-AI check:** Does the added complexity earn its cost in compute and explainability?

See the [outcome map](../../outcome-map.md) for all modules and the label definitions. These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.

</details>
<!-- OUTCOME_EVIDENCE_END -->



The practice sandbox uses development data and its own declared bounds. The full reference retains its model-selection, final-evaluation and artifact contract.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A dense layer combines inputs with learned weights and a bias; ReLU supplies a nonlinear hidden activation. A sigmoid output lies between zero and one. Binary cross-entropy supplies the gradient objective; a low training loss does not establish held-out performance.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. The reference study uses attributed public observations. Practice fixtures, derived task labels and authored evaluation controls are identified separately; they are not additional real-world observations. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

Training-only scaling feeds eleven numeric inputs, a 16-unit ReLU layer and one sigmoid output. An explicit minibatch GradientTape loop updates weights for at most 40 epochs, stopping after five epochs without a new minimum validation loss. The best observed checkpoint is restored. Neural and logistic thresholds are selected separately on validation balanced accuracy over 0.05–0.95 in steps of 0.05. Final labels select neither weights nor thresholds. Saved-model replay checks the trained network.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). Run framework commands in the Linux CPU reference environment; see the [support matrix](../../status.md) for platform coverage. Reading the reports needs no framework installation. Commands below start with the framework environment's Python, `.venv-ml` (Python 3.12), created in the [framework setup](../../setup/frameworks.md). **The first run downloads the public dataset or model, so it needs internet**; later runs reuse the verified cache. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

Linux, WSL or Codespaces (framework environment):

~~~sh
.venv-ml/bin/python examples/wine-neural-network/scripts/run.py --output runs/module08
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

Complete [original practice](practice.md), then compare [interpretation feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 9](../09-neural-nlp/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

## Optional project connection

The [optional stability investigation](../../advanced/stability.md) explains fixed-data training variation versus sensitivity to the partition. The worked experiment uses CPU classical models, so it requires no repeated neural training budget.

## Check before continuing

You have completed this module’s core learning route when you can:

- Save and explain this evidence: Trained and reloaded TensorFlow model compared with a simpler reference.
- Attempt the practice tasks and explain a correction or why your original answer was sound.
- Explain this limitation in your own words: CPU-scale wine classification; IT operations transfer and production scale are not demonstrated.

Use the answer pages to resolve gaps before continuing. Optional extensions are separate from this checklist.

## Connect this module to the whole study

Follow shapes through Dense, one-step LSTM, prediction, evaluation, and explanation. Use the [course-wide lifecycle map](../../connections.md#module-8-trace-the-complete-study) and the [research-case connection](../../cases/three-tier-lstm/08-integration.md). This is a short reading/reflection route; use this module's existing practice for implementation evidence.
