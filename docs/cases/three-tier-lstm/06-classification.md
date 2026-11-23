# Module 6 Separate selection prediction and evaluation

**Target:** explain the jobs of the feature-selection tree, final classifier, and metrics. Allow 12–15 minutes after comparing classifiers.

**Where you are:** selection, prediction, and evaluation. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Open only the handoffs

Read `feature_selection_dt` in [src/preprocess.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/preprocess.py), the selection/model calls in [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py), and `evaluate_scores` in [src/evaluate.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/evaluate.py).

The tree ranks candidate inputs for the next model; it is not the final predictor in this controller. The Dense/LSTM/Dense model produces a score. Evaluation compares the resulting decision with known labels. To claim a benefit from using the tree or the hybrid model, an investigator would need fair comparisons with simpler alternatives under the same evaluation design.

## Check one metric yourself

Use the [accessible error-count table](04-figures.md). Label 1 is positive. There are 39 true positives, three false negatives, one false positive, and 71 true negatives.

- Accuracy: 110 correct predictions / 114 observations, approximately 0.9649.
- Recall for label 1: 39 / 42, approximately 0.9286.
- Precision for label 1: 39 / 40, equal to 0.975.

The denominators answer different questions. None of these stored benchmark values establishes outcomes for a different population. Error costs require a defined use case and accountable domain judgment, not a generic instruction to optimize accuracy.

## Complete one small explanation

Explain why a tree-based feature selector and a final classifier are different roles. Which denominator would you use to check missed positive labels? Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-6) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 7 Compare learning paradigms](07-paradigms.md) · [All-module map](../../connections.md)
