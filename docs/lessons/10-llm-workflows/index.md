# Module 10: LLMs and evaluated generative workflows

Run an actual small local language model and evaluate structured outputs without repairing failures into apparent success.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M10.1:** Explain token generation and distinguish instructions from untrusted message data.
- **M10.2:** Run a recorded public model revision with bounded greedy decoding.
- **M10.3:** Validate an exact JSON schema and count failures.
- **M10.4:** Compare task fit, latency, and limitations with simpler NLP.
- **M10.5:** Write a source-grounded model-use note with privacy and cost constraints.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A language model predicts token continuations, not guaranteed facts or valid JSON. Temperature/sampling change generation behavior; this core uses greedy decoding and a token cap. Format compliance, label correctness, and latency are separate measurements.

## Real data and its limits

UCI SMS Spam Collection; real human-labeled messages. Public messages may contain personal content; processing stays local and reports use hashes/contact masking. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

Eight actual held-out SMS records (four per class) are sent to a CPU-local 135M instruct model. The prompt requests exactly one label field. Contact-string masking is an explicit transformation, not a privacy guarantee. Invalid JSON, extra keys, and unknown labels count as failures. The class-balanced tiny sample is an engineering check, not a population benchmark.

## Run and inspect

Download the [complete source](../../setup/student-workspace.md#reading-reports-from-github "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). The tested framework route is Linux CPU; Windows/macOS framework execution remains unverified. Reading the reports needs no framework installation. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/sms-llm/scripts/run.py --output runs/module10
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module10/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](../../setup/student-workspace.md#reading-reports-from-github "site-download:module10/example/index.html") without installing an execution interface.

Key artifacts:

- generation_evaluation.csv
- split_manifest.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](../../setup/student-workspace.md#reading-reports-from-github "site-download:module10/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. Operating a notebook/app interface is a separate skill; manual screen-reader, keyboard, zoom/reflow, and interface usability remain pending.

## Read selectively

- **Core concept/reference:** [Transformers generation strategies](https://huggingface.co/docs/transformers/v4.46.3/en/generation_strategies) — greedy decoding, token limits, and inference. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Declare a prompt/template or decoding comparison on validation examples. Freeze it before a new final evaluation. Larger models or hosted providers are optional and need separate rights, privacy, compute, and evaluation decisions.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 11](../11-fine-tuning/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Generated downloads/report links require the built reading artifact. Use [workspace and report access](../../setup/student-workspace.md); source notebooks are under notebooks/lessons in the repository.
