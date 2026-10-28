# Learning paths

Every module can be entered on its own, but a path gives you an order and a reason for it. Each path keeps the course's core habit: decide what evidence a result needs before you trust it. Time estimates on each module page are the author's estimates; measured learner times will replace them after piloting.

## Practical foundations: new to programming or machine learning

1. Take the [readiness check](start-here.md); use [Python Foundation](https://ntious.github.io/python_foundation/) and the [Python-to-ML bridge](setup/python-bridge.md) where it suggests.
2. Work through Modules [1](lessons/01-foundations/index.md) to [4](lessons/04-exploration/index.md): rules versus models, files and functions, cleaning, exploring.
3. Continue to [Module 5](lessons/05-regression/index.md) (your first trained model and baseline) and [Module 6](lessons/06-classification/index.md) (classification and thresholds).
4. Finish Module 6 with the [stability exercise](lessons/06-classification/practice.md#core-stability-exercise-two-kinds-of-variation).

At every module, answer the "Check yourself" questions on the concepts page before practice, and use the [study workflow](study-workflow.md) for what to keep.

## IT operations analyst: applying ML to operational data

1. Modules [2](lessons/02-python-workflows/index.md), [3](lessons/03-data-processing/index.md) and [4](lessons/04-exploration/index.md): tickets, network events and service workload.
2. [Module 6](lessons/06-classification/index.md), then the [historical phishing case](cases/phishing.md) and the [RT-IoT intrusion triage transfer](../projects/rt-iot-triage/README.md).
3. [Module 12](lessons/12-deployment/index.md): monitoring, then the JSON API extension.
4. [Module 10](lessons/10-llm-workflows/index.md)'s retrieval extension and [Module 14](lessons/14-agents/index.md): grounding answers and bounding tools.

## Evaluation-focused practitioner: you already build models

1. Skim the [readiness check](start-here.md), then [Module 5](lessons/05-regression/index.md) for the evaluation protocol the course uses.
2. In [Module 6](lessons/06-classification/practice.md), run the stability, tuning and encoding extensions (the encoding one is in [Module 3](lessons/03-data-processing/practice.md)).
3. The [complete capstone](../projects/phishing-triage/README.md), the [advanced investigations](advanced/index.md) and the [research comparison guide](advanced/research-comparison.md).
4. Modules [8](lessons/08-neural-networks/index.md) to [11](lessons/11-fine-tuning/index.md) for neural, language-model and fine-tuning evaluation.

## The recurring IT case thread

IT examples recur through the course alongside other datasets. Each has limits, and stating them is part of using it well.

| Where | IT case | Data | What it can and cannot show |
| --- | --- | --- | --- |
| Module 1 | Storage review rule | Original fixture | A written rule, not a learned model |
| Module 2 | Help-desk tickets and events | Original fixture | Counting, missing values and file contracts; no real workload |
| Module 3 | Network event quality | Original fixture | Validation, duplicates and reconciliation |
| Module 4 | Service workload and latency | Original fixture | Rates with denominators; descriptive only |
| Module 5 | Ticket forecasting (design transfer) | Real bike-sharing counts | The forecasting protocol; not real ticket data |
| Phishing case and capstone | Website phishing triage | Real historical UCI attributes | A historical benchmark, not a live detector |
| Module 3 extension | Encoding the phishing attributes | Real historical UCI attributes | Representation choices on validation data |
| RT-IoT transfer | Completed-flow intrusion triage | Real captured flows | No device, session or time identifiers, so no claim about new devices or drift |
| Module 10 extension | Runbook retrieval | Original fictional runbooks | The retrieval and abstention method; a small corpus |
| Module 12 | Model service, monitoring and API | Real wine records as stand-in inputs | Contracts and monitoring mechanics; not IT telemetry |
| Module 14 | Bounded tool workflow | Authored requests over real data | Permission boundaries; not real user intent |
