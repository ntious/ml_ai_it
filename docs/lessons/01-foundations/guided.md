# Module 1: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

At 80 percent storage, a rule using >80 says no review. At 81 it says review. Editing a threshold changes a human rule; fitting parameters requires examples and a learning objective.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
def needs_review(used, threshold=80):
    return used > threshold
learning_boundary = {n: needs_review(n) for n in [79, 80, 81]}
print(learning_boundary)
assert learning_boundary == {79: False, 80: False, 81: True}
```

## Complete with less support

Change the threshold to 90. Predict 90 and 91 before running. Explain what data a learned alternative would need.


## Debug a plausible misconception

Why is changing 80 to 90 not training? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Recommend a rule versus ML for a familiar non-IT task. Identify a stakeholder and one error cost.

## Minimum mastery evidence

Keep the evidence listed in the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) and name the module outcome each item supports. The [criteria](../../study-workflow.md#how-explanations-are-judged) describe developing, meeting and extending the outcome.
