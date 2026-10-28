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

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
