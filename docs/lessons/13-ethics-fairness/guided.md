# Module 13: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

In an illustrative group with 20 positives and 15 true positives, TPR is .75. If a second group has 4 positives and 3 true positives, its TPR is also .75 but based on much less evidence. A metric cannot establish that predicting historical income is a legitimate decision.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
from practical_ml_ai.learning import wilson_interval
for learning_successes,learning_n in [(15,20),(3,4)]:
    print("rate",learning_successes/learning_n,"illustrative interval",wilson_interval(learning_successes,learning_n))
assert wilson_interval(3,4)[1]-wilson_interval(3,4)[0] > wilson_interval(15,20)[1]-wilson_interval(15,20)[0]
```

## Complete with less support

Reconcile two real group rates and denominators. Explain the historical label and an intersectional limitation. Demonstrate uncertainty arithmetic while stating dependence and sampling assumptions.


## Debug a plausible misconception

Does removing protected columns remove bias? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Write a stakeholder recommendation that includes a reason not to deploy; distinguish a normative judgment from an observed rate.

## Minimum mastery evidence

Keep the evidence listed in the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) and name the module outcome each item supports. The [criteria](../../study-workflow.md#how-explanations-are-judged) describe developing, meeting and extending the outcome.
