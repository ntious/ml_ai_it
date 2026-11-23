# Module 5 Protect experimental integrity

**Target:** distinguish protecting an outer test set from protecting every validation boundary. Allow 12–15 minutes after fitting, splitting, and leakage concepts.

**Where you are:** splitting, learned feature selection, scaling, and optional balancing. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Open the actual order

In [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py), locate `split_data`, `feature_selection_dt`, `scale_features`, `apply_smote`, and `model.fit`. Use [src/preprocess.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/preprocess.py) only to check where fitting occurs.

The controller protects the **outer test partition** from feature-selector/scaler fitting and SMOTE. However, its later `validation_split` is applied inside `model.fit` **after** those operations on the outer training partition. The resulting validation subset is not independent of learned preparation and resampling.

## Explain why the inner boundary matters

A training example can inform feature selection or scaling before it later appears in the internal validation slice. Resampling can also generate related points before that slice exists. Keras selects the validation tail before training shuffle; SMOTE's row ordering can therefore affect its label mix. The exact validation composition needs examination in a reproduced run; we do not claim a measured contamination count here.

This is a useful audit case, not an instruction to repeat that ordering. See the primary [Keras fit contract](https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit), [resampling pitfalls](https://imbalanced-learn.org/stable/common_pitfalls.html), and [training-only preprocessing guidance](https://scikit-learn.org/stable/common_pitfalls.html).

## Design the clearer alternative

1. Reserve real training, validation, and final-test partitions before learned preparation, using appropriate entity/time boundaries.
2. Fit feature selection and scaling on training data only. Transform validation/test with those fitted objects and the same feature order.
3. If balancing is justified, apply it only to training data. SMOTE creates synthetic training points; it is an optional method to critique, not new observed patients or a course-required dataset.
4. Train with explicit untouched validation data, select on development evidence, and freeze the choice before final evaluation.
5. If you redesign after reading public final results, use a new defensible evaluation plan; a public benchmark does not become unseen through code guards.

This is a proposed redesign, not an alteration or rerun of the upstream repository. Use the existing [course evaluation workflow](../../lessons/05-regression/index.md) for your runnable practice.

## Complete one small explanation

Why can “SMOTE is limited to training data” be true while the later validation estimate still has a problem? Name where you would create validation in the redesigned order. Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-5) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 6 Separate selection prediction and evaluation](06-classification.md) · [All-module map](../../connections.md)
