# Module 14: Bounded agents and AI workflows

Connect a real local LLM router to narrowly allowed read-only tools, with exact evidence and enforceable limits.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M14.1:** Distinguish a fixed workflow, constrained LLM routing, and autonomous planning.
- **M14.2:** Define tool/argument schemas and a bounded execution budget.
- **M14.3:** Run actual model-based plan ranking against real dataset tools.
- **M14.4:** Inspect traces for intent match, refusals, and source-grounded answers.
- **M14.5:** Test unsupported/destructive requests and explain remaining limitations.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A valid tool call is not necessarily the right action for the user's intent. This core deliberately constrains routing to three enumerated plans and one read-only call. Mean completion log-probability ranks plans; it is not calibrated confidence. Hard policy checks live outside the model.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The actual small LLM ranks summary, alcohol-feature summary, or refusal plans. Exact schemas and allowed feature names are enforced before execution. Returned evidence comes from actual wine records. Destructive control requests are refused; no shell, upload, credential, or write tool exists. The final response displays tool values rather than inventing unsupported generated facts.

## Run and inspect

Download the [complete source](../../setup/student-workspace.md#reading-reports-from-github "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). The tested framework route is Linux CPU; Windows/macOS framework execution remains unverified. Reading the reports needs no framework installation. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/bounded-assistant/scripts/run.py --output runs/module14
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module14/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](../../setup/student-workspace.md#reading-reports-from-github "site-download:module14/example/index.html") without installing an execution interface.

Key artifacts:

- request_trace.csv
- tool_trace.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](../../setup/student-workspace.md#reading-reports-from-github "site-download:module14/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. Operating a notebook/app interface is a separate skill; manual screen-reader, keyboard, zoom/reflow, and interface usability remain pending.

## Read selectively

- **Core concept/reference:** [Transformers generation/inference reference](https://huggingface.co/docs/transformers/v4.46.3/en/main_classes/text_generation) — model outputs and bounded inference; compare with the actual constrained router. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Add one reviewed read-only tool with a new schema, evidence contract, and failure tests. Broader planning or external write actions require a separate authorization and evaluation design; they are not necessary for the core.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

This completes the 14-module sequence. Revisit the evaluation, deployment, and governance evidence together before proposing a real system.

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Generated downloads/report links require the built reading artifact. Use [workspace and report access](../../setup/student-workspace.md); source notebooks are under notebooks/lessons in the repository.
