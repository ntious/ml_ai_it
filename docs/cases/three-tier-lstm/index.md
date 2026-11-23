# Follow one research pipeline

Use the public **3-Tier-LSTM** project to see how selected ML topics meet inside a single research workflow. Start with the question and data; return to the same controller as each stage becomes familiar. You do not need to understand every file at the beginning.

This is an original reading companion to the [upstream repository](https://github.com/ntious/3-Tier-LSTM/tree/a6ca70ada14ce6b98f8ffccc71164d549c733dbb). Links use reviewed revision `a6ca70ada14ce6b98f8ffccc71164d549c733dbb` so a changed upstream main branch does not silently change the lesson. Author/source attribution and review limits are in the [source notes](source-notes.md).

## Start here without installing anything

1. Read the [study overview](01-study.md) for 8–10 minutes.
2. Complete your module's normal lesson and guided practice.
3. Open only the files named by the relevant connection below.
4. At Module 8, use the [integration checkpoint](08-integration.md) to trace the complete controller.
5. Apply the workflow discipline to your own task with the [transfer activity](transfer.md).

Times are planning estimates. Reading completion requires a brief explanation, not code execution or screenshots. These are companion activities; Canvas controls any actual grading or submission requirement. An optional live prompt also has an asynchronous solo route.

## Keep the whole sequence visible

Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

**Architecture:** the three tiers are Dense feature extraction, an LSTM layer, and a Dense prediction head. They are not three difficulty levels or three stacked LSTM layers. The reviewed input has **one timestep of numeric measurements**, not a sequence of visits or text tokens.

## Revisit these connections

| When | Connection | Suggested status |
| --- | --- | --- |
| Module 1 | [Recognize a complete study](01-study.md) | Recommended |
| Module 2 | [Connect functions and configuration](02-structure.md) | Optional |
| Module 3 | [Trace data and representations](03-data.md) | Recommended |
| Module 4 | [Ask what a figure establishes](04-figures.md) | Optional |
| Module 5 | [Protect experimental integrity](05-integrity.md) | Recommended |
| Module 6 | [Separate selection, prediction, and evaluation](06-classification.md) | Recommended |
| Module 7 | [Compare learning paradigms](07-paradigms.md) | Brief contrast |
| Module 8 | [Bring the pieces together](08-integration.md) | Integration checkpoint |
| Module 12 | [Identify the deployment gap](12-deployment.md) | Optional |
| Module 13 | [Scrutinize errors and explanations](13-responsibility.md) | Responsibility checkpoint |
| Project or independent study | [Transfer the design discipline](transfer.md) | Recommended |

## Connect the remaining topics honestly

The upstream case does not implement clustering, reinforcement learning, text classification, LLM prompting/fine-tuning, an inference service, or an LLM agent. The [all-module map](../../connections.md) and [extension bridge](extensions.md) show how those topics share the lifecycle while introducing different inputs, outputs, and evaluation requirements. The existing course examples remain their hands-on route.

## What the case does and does not establish

The source separates loading, preprocessing, model construction, evaluation, and explanation. It also contains issues worth investigating: validation is created after learned preparation and resampling; feature-importance names and scores can become misaligned; input data are not bundled; and model/scaler serialization is absent from the reviewed controller. Use the [integrity connection](05-integrity.md) and [source notes](source-notes.md) before treating it as a reproduction recipe.

We inspected source and committed outputs; we did not rerun upstream training or certify its published results. This historical research example does not authorize diagnosis, patient-care decisions, or production deployment. For a runnable teaching exemplar with explicit saved inference artifacts, use the [course capstone](../../../projects/phishing-triage/README.md).

[Public feedback](feedback.md) · [Instructor placement and facilitation](../../instructor/connected-research-case.md) · [Return to the course-wide map](../../connections.md)
