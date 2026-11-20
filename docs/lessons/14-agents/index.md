# Module 14: Bounded agents and AI workflows

## Your route through this module

1. **Read:** start with the [foundation](foundation.md) and [concepts](concepts.md); use the [guided activity](guided.md) to work through an example.
2. **Run:** follow the complete-example commands on this page and inspect the saved output.
3. **Practice:** attempt the [practice tasks](practice.md) before opening answers.
4. **Check:** compare [practice notebook answers](solutions.md) and [interpretation feedback](feedback.md), then explain any corrections.


Connect a real local LLM router to narrowly allowed read-only tools, with exact evidence and enforceable limits.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M14.1:** Distinguish a fixed workflow, constrained LLM routing, and autonomous planning.
- **M14.2:** Define tool/argument schemas and a bounded execution budget.
- **M14.3:** Run actual model-based plan ranking against real dataset tools.
- **M14.4:** Inspect traces for intent match, refusals, and source-grounded answers.
- **M14.5:** Test unsupported/destructive requests and explain remaining limitations.

## Course outcomes and evidence

<!-- OUTCOME_EVIDENCE_START -->

<details>
<summary>For instructors: course outcomes and evidence</summary>

- **Direct evidence:** CLO4 (Frameworks and evaluation), CLO5 (GenAI and LLM integration), CLO8 (Communication)
- **Supporting practice:** CLO2 (Applying ML/AI to IT operations), CLO6 (Deployment and monitoring)
- **Additional direct-evidence route (complete separately):** [IT-OPS (CLO2)](../../cases/it-operations-evidence.md); [MONITOR (CLO6)](../../advanced/monitoring-decision-record.md)
- **Data and tools:** <span class="data-label">Real public</span> <span class="data-label">Local model</span> <span class="data-label">Offline fixture</span>
- **Evidence you produce:** Bounded router and tool-loop comparison with a recorded trace and failure cases. See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).
- **Boundary:** No full agent-framework implementation is claimed; tools are local and read-only.
- **Responsible-AI check:** What actions may the agent take, who approves them, and how is a trace audited?

See the [outcome map](../../outcome-map.md) for all modules and the label definitions. These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.

</details>
<!-- OUTCOME_EVIDENCE_END -->



## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

A valid tool call is not necessarily the right action for the user's intent. This core deliberately constrains routing to three enumerated plans and one read-only call. Mean completion log-probability ranks plans; it is not calibrated confidence. Hard policy checks live outside the model.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. The reference study uses attributed public observations. Practice fixtures, derived task labels and authored evaluation controls are identified separately; they are not additional real-world observations. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The authored request file separates six demonstrations, six validation controls and 26 labelled test requests. A real local LLM scores count/alcohol/refuse labels; these map to summary/feature/refuse plans. Class-score offsets are chosen using validation controls only. The executor supplies an exact allowlisted argument schema. A bounded plan → observe → answer workflow uses at most three steps and one read-only call. The answer displays returned source values. Measure routing accuracy, missed refusals and the confusion table separately from the permission boundary: no destructive, shell, upload or credential tool exists.

The request controls are authored examples, not a representative sample of real users. A model can choose an irrelevant read tool for an unsafe request; that counts as a routing error even though no unsafe operation can execute.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). Run framework commands in the Linux CPU reference environment; see the [support matrix](../../status.md) for platform coverage. Reading the reports needs no framework installation. Commands below start with the framework environment's Python, `.venv-ml` (Python 3.12), created in the [framework setup](../../setup/frameworks.md). **The first run downloads the public dataset or model, so it needs internet**; later runs reuse the verified cache. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

Linux, WSL or Codespaces (framework environment):

~~~sh
.venv-ml/bin/python examples/bounded-assistant/scripts/run.py --output runs/module14
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module14/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module14/example/index.html "site-download:module14/example/index.html") without installing an execution interface.

Key artifacts:

- request_trace.csv
- tool_trace.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module14/walkthrough.ipynb "site-download:module14/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [Transformers generation/inference reference](https://huggingface.co/docs/transformers/v4.46.3/en/main_classes/text_generation) — model outputs and bounded inference; compare with the actual constrained router. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Add one reviewed read-only tool with a new schema, evidence contract, and failure tests. Broader planning or external write actions require a separate authorization and evaluation design; they are not necessary for the core.

## Practice and continue

Complete [original practice](practice.md), then compare [interpretation feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

This completes the 14-module sequence. Revisit the evaluation, deployment, and governance evidence together before proposing a real system.

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

## Check before continuing

You have completed this module’s core learning route when you can:

- Save and explain this evidence: Bounded router and tool-loop comparison with a recorded trace and failure cases.
- Attempt the practice tasks and explain a correction or why your original answer was sound.
- Explain this limitation in your own words: No full agent-framework implementation is claimed; tools are local and read-only.

Use the answer pages to resolve gaps before continuing. Optional extensions are separate from this checklist.
