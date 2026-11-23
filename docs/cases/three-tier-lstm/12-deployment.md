# Module 12 Identify the deployment gap

**Optional. Target:** separate a training study from repeatable inference and monitoring. Allow 10–12 minutes after the deployment module.

**Where you are:** the boundary after evaluation and outputs. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Inspect the boundary

Read [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py) for writes to disk and [config.yaml](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/config.yaml) for output paths. The controller creates a model directory but does not call a model-saving method or serialize the fitted scaler and feature contract. Existing reports and figures are not a complete inference bundle.

## Define what would need to travel together

A usable inference artifact needs the fitted model, transformations, selected feature names/order, input/output schema, threshold, source/version identity, and a replay check. A service also needs validated new inputs, clear failure behavior, access/privacy controls, an owner, monitoring, and a fallback appropriate to its intended use.

Those are proposed extensions to this research case. No API, Streamlit app, monitoring stream, or production service is claimed in its source. One command that trains a model does not establish a deployed system.

For actual course implementation, use [Module 12](../../lessons/12-deployment/index.md) and the [completed phishing-triage project](../../../projects/phishing-triage/README.md). Their local checks and replays have their own limits; source-order replay is not measured temporal drift.

## Complete one small explanation

Name two fitted artifacts that must accompany the model at inference. What evidence would you request to check that an application transforms inputs consistently? Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-12) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 13 Scrutinize errors and explanations](13-responsibility.md) · [All-module map](../../connections.md)
