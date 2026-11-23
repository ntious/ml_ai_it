# Module 11: Fine-tuning language models responsibly

## Your route through this module

1. **Read:** start with the [foundation](foundation.md) and [concepts](concepts.md); use the [guided activity](guided.md) to work through an example.
2. **Run:** follow the complete-example commands on this page and inspect the saved output.
3. **Practice:** attempt the [practice tasks](practice.md) before opening answers.
4. **Check:** compare [practice notebook answers](solutions.md) and [interpretation feedback](feedback.md), then explain any corrections.


Perform real parameter-efficient gradient updates on annotated messages, preserve the base model, and audit held-out loss and replay.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads; the default CPU training study can take 15–30 minutes depending on hardware. Small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M11.1:** Distinguish prompting, inference, supervised fine-tuning, and LoRA.
- **M11.2:** Prepare completion labels with prompt-token loss masking.
- **M11.3:** Update a small adapter on training-only real annotations.
- **M11.4:** Compare predeclared base/adapted held-out completion losses without promising improvement.
- **M11.5:** Save/reload adapter arrays with the exact model revision and disclose limits.

## Course outcomes and evidence

<!-- OUTCOME_EVIDENCE_START -->

<details>
<summary>For instructors: course outcomes and evidence</summary>

- **Direct evidence:** CLO4 (Frameworks and evaluation), CLO5 (GenAI and LLM integration), CLO8 (Communication)
- **Supporting practice:** none
- **Data and tools:** <span class="data-label">Real public</span> <span class="data-label">Local model</span>
- **Evidence you produce:** Saved configuration, logs and adapters from a real tiny fine-tuning run, with an evaluation. See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).
- **Boundary:** Tiny balanced subset; scale and generalization are limited.
- **Responsible-AI check:** Could the tuned model reproduce private text, and do the data and model licenses allow this use?

See the [outcome map](../../outcome-map.md) for all modules and the label definitions. These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.

</details>
<!-- OUTCOME_EVIDENCE_END -->



## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

LoRA adds a low-rank update to a frozen linear projection. The guided rank-2 construction exposes the operation; the complete study uses rank 8 in query and value projections across all layers, while base weights remain frozen. Masking prompt labels with -100 prevents the objective from training on every instruction token.

## Real data and its limits

UCI SMS Spam Collection; real human-labeled messages. Public messages may contain personal content; processing stays local and reports use hashes/contact masking. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. The reference study uses attributed public observations. Practice fixtures, derived task labels and authored evaluation controls are identified separately; they are not additional real-world observations. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

Train rank-8 PEFT LoRA on every q_proj and v_proj, using 256 real training messages, batch size 8 and a predeclared 200-step maximum. Prompt and padding labels are masked with -100. Every 25 steps, measure completion loss on 40 disjoint validation messages; retain the lowest-loss checkpoint, including the zero-step adapter if training never improves it. The selected checkpoint is reloaded before validation generation and the predefined base/adapted comparison on 100 disjoint balanced final messages. Compare JSON validity, label correctness and completion loss separately. Save adapter safetensors, configuration and the exact base revision; verify reloaded logits. No invented training messages or labels are used.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). Run framework commands in the Linux CPU reference environment; see the [support matrix](../../status.md) for platform coverage. Reading the reports needs no framework installation. Commands below start with the framework environment's Python, `.venv-ml` (Python 3.12), created in the [framework setup](../../setup/frameworks.md). **The first run downloads the public dataset or model, so it needs internet**; later runs reuse the verified cache. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

Linux, WSL or Codespaces (framework environment):

~~~sh
.venv-ml/bin/python examples/sms-fine-tuning/scripts/run.py --output runs/module11
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module11/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module11/example/index.html "site-download:module11/example/index.html") without installing an execution interface.

Key artifacts:

- training_history.csv
- adapter/adapter_model.safetensors
- adapter/adapter_config.json
- study_config.json
- validation_generation.csv
- generation_comparison.csv
- rate_intervals.csv
- split_manifest.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module11/walkthrough.ipynb "site-download:module11/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [LoRA primary paper](https://arxiv.org/abs/2106.09685) — low-rank update idea, frozen weights, and evaluation distinctions. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Use a predeclared validation plan for another rank, step budget, or target projection. More complete supervised training and a credible prospective evaluation require additional real data, compute, and review; they are optional depth.

## Practice and continue

Complete [original practice](practice.md), then compare [interpretation feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 12](../12-deployment/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

## Check before continuing

You have completed this module’s core learning route when you can:

- Save and explain this evidence: Saved configuration, logs and adapters from a real tiny fine-tuning run, with an evaluation.
- Attempt the practice tasks and explain a correction or why your original answer was sound.
- Explain this limitation in your own words: Tiny balanced subset; scale and generalization are limited.

Use the answer pages to resolve gaps before continuing. Optional extensions are separate from this checklist.

## Connect this module to the whole study

Fine-tune a language model only with a separate justified objective, dataset, and evaluation. Use the [course-wide lifecycle map](../../connections.md#module-11-decide-whether-adaptation-is-justified) and the [research-case connection](../../cases/three-tier-lstm/extensions.md). This is a short reading/reflection route; use this module's existing practice for implementation evidence.
