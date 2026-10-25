# Module 6: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before the complete [walkthrough](index.md). Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

X is rows by chemistry inputs. y is the declared rating threshold. Fit the scaler and logistic parameters on training only. A score needs a decision threshold; changing it affects both false positives and false negatives.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from practical_ml_ai.continuation_data import wine_splits, binary_metrics
learning_split, learning_features, _ = wine_splits()
learning_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
learning_model.fit(learning_split["train"][learning_features], learning_split["train"].label)
learning_scores = learning_model.predict_proba(learning_split["validation"][learning_features])[:,1]
for learning_threshold in [.3,.5,.7]:
    print(learning_threshold, binary_metrics(learning_split["validation"].label, learning_scores >= learning_threshold))
assert len(learning_scores) == len(learning_split["validation"])
```

## Complete with less support

Reconstruct the confusion counts and explain a threshold choice using validation. Implement one predefined alternative on development data; freeze before a planned final evaluation.

Cover the worked code, implement the central step again, and explain its inputs, outputs and boundary. Keep development experiments separate from final evaluation. Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design.

## Debug a plausible misconception

If TP=19, FP=30 and FN=10, what are precision and recall? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Design an incident-triage task with entity grouping, decision-time inputs and investigation costs.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.

## Calibration and sample-size investigation

Inspect validation_calibration.csv. For each occupied probability bin, compare mean predicted probability with the observed positive fraction and its count. Empty bins are absent, not zero-rate bins. A high ranking score does not establish calibrated probabilities. Do not select a calibrator from final-test outcomes.

In development, use learning.wilson_interval on the hand counts 15/20 and 3/4 to see how the same rate has different uncertainty. That binomial calculation assumes appropriate independent trials; duplicated chemistry profiles and selection mean it must not be advertised as a rigorous interval for this grouped benchmark. An advanced experiment can use group-resampling on development data with explicit assumptions and no final-test tuning.
