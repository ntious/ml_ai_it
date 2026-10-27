# Module 5: guided construction and mastery

Start with the [foundation bridge](foundation.md) and [applied concept sequence](concepts.md). This is the worked stage; the next stage removes implementation support. Use the existing environment for this module.

## Predict before running

Which training rows determine the missing-value fill? Predict whether adding 100 as a new input should change it. Explain why predicting a missing input is different from knowing its unknown target.

## Follow a small worked implementation

```python
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
import numpy as np
train_x = np.array([[1.], [3.], [np.nan], [5.]])
train_y = np.array([2., 6., 6., 10.])
model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
model.fit(train_x, train_y)
print("Training median:", model[0].statistics_)
print("Predictions:", model.predict([[np.nan], [100.]]))
```

## Change one thing and explain

Change one training input, refit on training only, and explain whether its median or fitted predictions change. Restore the example before starting your independent implementation.

Record the prediction, actual output and explanation. If they differ, identify the line or assumption responsible instead of simply replacing your answer.

## Reconstruct with less support

Open [independent practice](practice.md). Implement the three functions in its starter notebook. Visible checks give actionable feedback; solutions are separate. Preserve your attempted code and reasoning before inspecting a solution.

## Connect to the complete study

After practice, use the [complete reference walkthrough](index.md). Its real-data protocol, baseline comparison, final evaluation and artifacts remain the module reference. The small sandbox is development practice and does not replace that evidence.

Use [practice solutions](solutions.md) for misconception-specific feedback and [recorded-study feedback](feedback.md) to interpret the complete study. The [pilot guide](../../instructor/teaching-prototype-pilot.md) distinguishes technical verification from observed learner mastery.
