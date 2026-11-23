# Module 4 Ask what a figure establishes

**Optional. Target:** match a performance figure to its underlying evidence and explain a limitation. Allow 8–10 minutes.

**Where you are:** evaluation and communication. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Open the evidence before the picture

Read [the committed numeric report](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/outputs/reports/metrics_numeric.json) and [the committed classification report](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/outputs/reports/classification_report.txt). Optionally inspect [the source confusion matrix](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/outputs/figures/confusion_matrix.png). The following table supplies the matrix's full numeric content: rows are source labels, columns are predicted labels.

| Actual label | Predicted benign 0 | Predicted malignant 1 |
| --- | --- | --- |
| Benign 0 | 71 | 1 |
| Malignant 1 | 3 | 39 |

In words: 71 benign cases were predicted benign and 1 was predicted malignant; 3 malignant cases were predicted benign and 39 were predicted malignant. There are 72 actual benign cases and 42 actual malignant cases, totaling 114. The predictions total 74 benign and 40 malignant.

These are committed upstream results at the reviewed revision, not a new run or independently verified cohort. They allow a reading exercise without requiring image interpretation.

## Ask the question the figure can answer

The confusion matrix shows error counts at one threshold. The ROC curve compares score discrimination across thresholds; it does not select a deployment threshold or establish calibration. Training curves describe the supplied optimization/validation data; their interpretation depends on how those partitions were constructed.

The source feature-importance plotting path can pair already-sorted feature names with an unsorted importance array. The [source notes](source-notes.md) locate the mismatch. Do not infer a trustworthy feature ranking from that chart before checking the name/value alignment. An attractive plot can communicate incorrect labels.

## Complete one small explanation

Use the table to explain one error count in words. State one additional fact that a stakeholder would need before judging whether that error rate is acceptable. Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-4) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 5 Protect experimental integrity](05-integrity.md) · [All-module map](../../connections.md)
