# Module 4: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

For values 2, 3 and 10, the mean is 5 and median is 3. One large value moves the mean more strongly. The numerical table is evidence a chart should preserve.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
import numpy as np
learning_values = np.array([2., 3., 10.])
print("mean", learning_values.mean(), "median", np.median(learning_values))
assert learning_values.mean() == 5 and np.median(learning_values) == 3
print("after changing the largest value", np.mean([2,3,100]), np.median([2,3,100]))
```

## Complete with less support

Construct one labeled plot from development data and supply its numeric table and a noncausal interpretation. Choose and defend its missing-value policy.


## Debug a plausible misconception

Does a rising scatter pattern establish causation? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Explain a chart to a stakeholder outside IT using units, denominators and one alternative explanation.

## Minimum mastery evidence

Keep the evidence listed in the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) and name the module outcome each item supports. The [criteria](../../study-workflow.md#how-explanations-are-judged) describe developing, meeting and extending the outcome.
