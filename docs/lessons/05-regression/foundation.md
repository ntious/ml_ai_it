# Module 5 foundation bridge: prediction, residual, and loss

Use this before the [main lesson](index.md). Arithmetic and basic function calls are sufficient; calculus is not required.

## A simple linear prediction

Suppose an illustrative model predicts 20 plus 0.8 times yesterday's count. At 100 yesterday it predicts 100 tomorrow; at 150 it predicts 140. The intercept is 20, and the coefficient is 0.8 predicted-count units per input-count unit. These are hand examples, not fitted UCI parameters.

Regression predicts a numerical quantity. Classification predicts a class or class-related score and is introduced next. Fitting estimates parameters; inference applies fixed parameters. A coefficient is a fitted association, not proof of causation.

## Errors and loss

For actual counts [110, 125] and predictions [100, 140], residuals using actual minus predicted are [10, -15]. The first prediction is 10 too low; the second is 15 too high.

Mean residual is -2.5 because signed errors partly cancel. MAE is (10 + 15) / 2 = 12.5 count units. Mean squared error is (100 + 225) / 2 = 162.5 squared count units. Squaring gives larger errors greater weight. Ordinary least squares minimizes squared training residuals; the module evaluates with held-out MAE.

A MAE of 12.5 does not guarantee every prediction is within 12.5. It summarizes the observed errors in that split.

## Why compare a baseline?

A mean baseline always predicts the training average. Persistence copies a recent observation; weekly persistence uses last week's same weekday. The latter can be a stronger reference when demand is seasonal. A trained method's usefulness depends on relevant alternatives and the costs of its errors.

Training fits. Validation selects. Final testing evaluates the frozen choice. Inference predicts without requiring the unknown target. These roles remain distinct when one script runs the stages in sequence.

## What a pipeline protects

A pipeline keeps learned preprocessing and the estimator together. Training learns the imputer's median and the regression's parameters. Prediction applies the same learned transformation.

A pipeline cannot repair an unavailable feature or a badly designed time split. You still need a forecast origin, a feature-availability audit, and a split rationale.

Return to [Module 5](index.md), or review [Python structures and paths](../02-python-workflows/foundation.md).
