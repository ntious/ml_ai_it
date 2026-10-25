# Module 5: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before the complete [walkthrough](index.md). Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

For prediction 20 + 0.8*x, x=150 gives 140. If actual is 125, residual actual-minus-predicted is -15: overprediction. Squared training loss and absolute-error evaluation answer different optimization questions.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
import numpy as np
learning_x = np.array([100., 150.])
learning_prediction = 20 + .8 * learning_x
learning_actual = np.array([110.,125.])
learning_residual = learning_actual - learning_prediction
print("prediction", learning_prediction, "residual", learning_residual)
print("MAE", np.abs(learning_residual).mean())
assert np.abs(learning_residual).mean() == 12.5
```

## Complete with less support

Implement previous-day persistence on development records. Explain input availability at the forecast origin and compare with the provided development baseline.

Cover the worked code, implement the central step again, and explain its inputs, outputs and boundary. Keep development experiments separate from final evaluation. Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design.

## Debug a plausible misconception

Can an imputer fitted on all dates leak information? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Design a forecast in another domain and distinguish rolling daily decisions from a batch forecast.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
