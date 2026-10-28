# Module 11: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

If W has output-by-input shape (6,4), it has 24 parameters. A rank-2 A has shape (2,4), B has shape (6,2), and BA has shape (6,4). Their 20 parameters are fewer here; savings become much larger for wide projections. Starting B at zero makes the initial update zero. A frozen base participates in forward computation without optimizer updates. Labels -100 exclude prompt positions from the completion-loss objective; they are a library masking convention.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
import numpy as np
learning_w = np.ones((6,4))
learning_a = np.ones((2,4)) * .02
learning_b = np.zeros((6,2))
print("base",learning_w.shape,"A",learning_a.shape,"B",learning_b.shape)
assert (learning_b @ learning_a).shape == learning_w.shape
assert np.allclose(learning_w + learning_b @ learning_a,learning_w)
print("base parameters",learning_w.size,"adapter parameters",learning_a.size+learning_b.size)
```

## Complete with less support

Inspect one packed training example and identify prompt/completion masks. Explain a saved adapter shape. Compare base/adapted held-out generation as well as loss; do not select training settings from those final comparisons.


## Debug a plausible misconception

Does a nonzero adapter update establish better labels? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Before changing rank or steps, justify whether prompting or a simpler classifier already meets the task. Declare a validation experiment and resource budget.

## Minimum mastery evidence

Keep the evidence listed in the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) and name the module outcome each item supports. The [criteria](../../study-workflow.md#how-explanations-are-judged) describe developing, meeting and extending the outcome.
