# Module 6: guided construction and mastery

Start with the [foundation bridge](foundation.md) and [applied concept sequence](concepts.md). This is the worked stage; the next stage removes implementation support. Use the existing environment for this module.

## Predict before running

Trace the record scored exactly .5. Which candidate has the smallest cost if a miss costs three units? Write the row decisions before running.

## Follow a small worked implementation

```python
import numpy as np
labels = np.array([0, 1, 0, 1])
scores = np.array([.2, .4, .5, .8])
for threshold in [.3, .5, .7]:
    decisions = scores >= threshold
    misses = int(((labels == 1) & ~decisions).sum())
    alarms = int(((labels == 0) & decisions).sum())
    print(threshold, "misses", misses, "false alarms", alarms, "cost", 3*misses+alarms)
```

## Change one thing and explain

Change only the miss/false-alarm costs from 3:1 to 1:5. Recompute the preferred threshold without retraining or changing the score array. Explain the new decision in words.

Record the prediction, actual output and explanation. If they differ, identify the line or assumption responsible instead of simply replacing your answer.

## Reconstruct with less support

Open [independent practice](practice.md). Implement the three functions in its starter notebook. Visible checks give actionable feedback; solutions are separate. Preserve your attempted code and reasoning before inspecting a solution.

## Connect to the complete study

After practice, use the [complete reference walkthrough](index.md). Its real-data protocol, baseline comparison, final evaluation and artifacts remain the module reference. The small sandbox is development practice and does not replace that evidence.

Use [practice solutions](solutions.md) for misconception-specific feedback and [recorded-study feedback](feedback.md) to interpret the complete study. The [pilot guide](../../instructor/teaching-prototype-pilot.md) distinguishes technical verification from observed learner mastery.
