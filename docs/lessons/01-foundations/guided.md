# Module 1: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before the complete [walkthrough](index.md). Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

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

Cover the worked code, implement the central step again, and explain its inputs, outputs and boundary. Keep development experiments separate from final evaluation. Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design.

## Debug a plausible misconception

Why is changing 80 to 90 not training? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Recommend a rule versus ML for a familiar non-IT task. Identify a stakeholder and one error cost.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
