# Module 8: guided construction and mastery

Start with the [foundation bridge](foundation.md) and [applied concept sequence](concepts.md). This is the worked stage; the next stage removes implementation support. Use the existing environment for this module.

## Predict before running

The actual label is 1. Predict whether this small update raises or lowers its probability and loss. Write what each array dimension represents. This demonstrates one logistic-output update; the hidden-layer derivatives are computed by the framework.

## Follow a small worked implementation

```python
import numpy as np
x = np.array([[1., 2.]])
w = np.array([[.5], [-1.]])
bias = .5
before = 1 / (1 + np.exp(-(x @ w + bias)))
gradient = (before - 1) * x   # one positive label; illustrative output-layer gradient
updated = w - .1 * gradient.T
after = 1 / (1 + np.exp(-(x @ updated + bias)))
print("Probability before/after:", before.item(), after.item())
print("Positive-label loss before/after:", -np.log(before.item()), -np.log(after.item()))
```

## Change one thing and explain

Use a negative label instead: replace the target 1 by 0 in the gradient, then compare the negative-label loss `-log(1-p)` before and after. Reset before independent practice. Explain why a very large step might behave differently.

Record the prediction, actual output and explanation. If they differ, identify the line or assumption responsible instead of simply replacing your answer.

## Reconstruct with less support

Open [independent practice](practice.md). Implement the three functions in its starter notebook. Visible checks give actionable feedback; solutions are separate. Preserve your attempted code and reasoning before inspecting a solution.

## Connect to the complete study

After practice, use the [complete reference walkthrough](index.md). Its real-data protocol, baseline comparison, final evaluation and artifacts remain the module reference. The small sandbox is development practice and does not replace that evidence.

Use [practice solutions](solutions.md) for misconception-specific feedback and [recorded-study feedback](feedback.md) to interpret the complete study. The [pilot guide](../../instructor/teaching-prototype-pilot.md) distinguishes technical verification from observed learner mastery.
