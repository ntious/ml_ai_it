# Module 3 Trace data into representations

**Target:** explain the difference between source columns, the target, named features, and a model-ready array. Allow 10–15 minutes after data preparation.

**Where you are:** loading, fixed cleanup, target encoding, and partitioning. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Open only these functions

Read [src/load_data.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/load_data.py) for `load_data`; [src/preprocess.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/preprocess.py) for `drop_unnecessary`, `encode_target`, and `split_data`; then locate those calls in [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py).

## Follow the handoff

1. `load_data` reads a CSV or spreadsheet into a pandas table. Reading a file is not a complete schema or provenance check.
2. Fixed cleanup drops configured columns such as `id` and `Unnamed: 32` if present. Explain why identifiers must not accidentally become predictive measurements; preserve a separate audit identity when needed.
3. `encode_target` maps M to 1 and B to 0. Other text labels become missing values in this implementation; production-quality preparation needs explicit rejection or a justified policy.
4. `split_data` separates feature table X from target y and creates the outer training/test partitions.
5. Later selection/scaling turn the feature table into arrays. The selected feature order must stay associated with every array and saved artifact.

The configured `data/data.csv` is not tracked in the reviewed source. The README links a dataset provider, but no reviewed download/hash is supplied here. We inspect the contract rather than inventing replacement patient records or pretending we reran it.

**Carry forward:** a feature-name list, positive-label definition, input policy, and split identity. Full implementation belongs in your ordinary [Module 3 work](../../lessons/03-data-processing/index.md); the genuine [network-record bridge](../network-record-interpretation.md) supplies a different domain.

## Complete one small explanation

Describe what X and y contain. What could go wrong if an unknown label or changed feature order silently passed to the next stage? Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-3) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 5 Protect experimental integrity](05-integrity.md) · [All-module map](../../connections.md)
