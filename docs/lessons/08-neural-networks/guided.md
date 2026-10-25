# Module 8: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before the complete [walkthrough](index.md). Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

For x=[1,2], w=[.5,-1] and bias .5, the weighted sum is -1 and ReLU returns 0. A sigmoid maps a number into 0–1. A batch of 32 wine observations has shape (32,11), hidden values (32,16), and output (32,1). The network has 11*16+16+16+1=209 parameters. An epoch visits training examples; a batch drives one update.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
import numpy as np
learning_x = np.array([[1.,2.]])
learning_w = np.array([[.5],[-1.]])
learning_z = learning_x @ learning_w + .5
print("weighted sum", learning_z, "ReLU", np.maximum(0,learning_z))
learning_p = 1/(1+np.exp(-learning_z))
print("sigmoid", learning_p)
assert learning_z.shape == (1,1) and learning_z.item() == -1
learning_gradient = (learning_p - 1) * learning_x
learning_updated = learning_w - .1 * learning_gradient.T
print("weights after one illustrative logistic-loss update", learning_updated)
```

## Complete with less support

In a separate development cell construct the 11-input/16-hidden/1-output TensorFlow model. Print and explain every shape and parameter count; make one declared width change before final evaluation.

Cover the worked code, implement the central step again, and explain its inputs, outputs and boundary. Keep development experiments separate from final evaluation. Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design.

## Debug a plausible misconception

Can the lowest training-loss epoch be the wrong checkpoint? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Explain when a simple linear model is preferable to a larger network despite its smaller capacity.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
