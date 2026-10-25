# Module 11: Fine-tuning language models responsibly

Perform real parameter-efficient gradient updates on annotated messages, preserve the base model, and audit held-out loss and replay.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M11.1:** Distinguish prompting, inference, supervised fine-tuning, and LoRA.
- **M11.2:** Prepare completion labels with prompt-token loss masking.
- **M11.3:** Update a small adapter on training-only real annotations.
- **M11.4:** Compare predeclared base/adapted held-out completion losses without promising improvement.
- **M11.5:** Save/reload adapter arrays with the exact model revision and disclose limits.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

LoRA adds a low-rank update to a frozen linear projection. Here a rank-2 pair targets one query projection; this is a deliberately small adaptation, not full-model retraining. Masking prompt labels with -100 prevents the objective from training on every instruction token.

## Real data and its limits

UCI SMS Spam Collection; real human-labeled messages. Public messages may contain personal content; processing stays local and reports use hashes/contact masking. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The default uses eight actual gradient steps, alternating real ham/spam training records. Validation and final subsets are disjoint text IDs. Only adapter parameters are optimized; base weights stay frozen. Base/adapted final completion loss comparisons are predefined. Numeric adapter arrays and configuration are saved and reloaded, with a replay check. No synthetic labels/messages are generated for training.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). Run framework commands in the Linux CPU reference environment; see the [support matrix](../../status.md) for platform coverage. Reading the reports needs no framework installation. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/sms-fine-tuning/scripts/run.py --output runs/module11
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module11/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module11/example/index.html "site-download:module11/example/index.html") without installing an execution interface.

Key artifacts:

- training_history.csv
- adapter.npz
- adapter_config.json
- split_manifest.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module11/walkthrough.ipynb "site-download:module11/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [LoRA primary paper](https://arxiv.org/abs/2106.09685) — low-rank update idea, frozen weights, and evaluation distinctions. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Use a predeclared validation plan for another rank, step budget, or target projection. More complete supervised training and a credible prospective evaluation require additional real data, compute, and review; they are optional depth.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 12](../12-deployment/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).
