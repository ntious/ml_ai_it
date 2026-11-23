# Module 2 Connect functions and configuration

**Optional. Target:** distinguish orchestration, reusable behavior, settings, and dependencies. Allow 8–10 minutes after functions and file handling.

**Where you are:** Python organization across the whole workflow. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Open only the structural pieces

- [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py): imports and calls, without studying TensorFlow arguments.
- [config.yaml](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/config.yaml): input/output paths, a split seed, and training settings.
- [requirements.txt](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/requirements.txt): one pip environment specification.
- [tests/test_research_pipeline.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/tests/test_research_pipeline.py): small checks, not proof of full model reproduction.

## Follow one function call

The controller imports `load_data`, reads settings, and passes the configured path to the function. Changing a function's implementation differs from changing a setting. The shared return value becomes another function's input, so a function signature is a handoff contract.

A dependency file describes software; it does not supply the dataset. The Conda and pip files also specify different scikit-learn versions in this revision. Compare and record an environment rather than assuming the two routes are identical. Do not install the upstream dependencies into the course framework environment; this optional source-reading activity needs neither.

## Complete one small explanation

Which file decides the operation order, and which file supplies the split setting? Explain why mixing those responsibilities makes a study harder to inspect. Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-2) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 3 Trace data into representations](03-data.md) · [All-module map](../../connections.md)
