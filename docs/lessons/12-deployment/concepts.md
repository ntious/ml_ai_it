# Module 12: Delivery includes rejection and recovery

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## An inference request is a contract

A trained model expects a particular feature order, type and unit. A service must reject missing, extra, nonnumeric or nonfinite inputs instead of silently coercing them. A successful response demonstrates the local inference path, not safe deployment. Keep the schema alongside the model and compare a saved-model response to the original fitted estimator on permitted fixtures.

## Monitoring needs a denominator and an owner

A change in mean input is one signal, not a diagnosis. Standardize by a fixed training reference scale and state what happens if that scale is zero. Predictions can drift because inputs, collection or behavior changed. Accuracy monitoring additionally needs delayed outcomes; until labels arrive, input monitoring cannot tell you whether the model is still correct. Assign an owner to investigate rather than automatically retraining from any alert.

## Evaluate the whole service path

Measure latency with its percentile definition, sample count and environment. A single fast request is weak evidence. Validate rejection behavior and a human fallback when inference is unavailable. Keep old and new model versions with the same request contract, an explicit rollback trigger and a record of the affected period. Do not collect unnecessary personal data merely to make monitoring easier.

## Trace a small case

Predict `valid_request({'x': 2}, ['x'])`, `valid_request({'x': True}, ['x'])` and `valid_request({'extra': 1, 'x': 2}, ['x'])` before running. Only the first meets the contract: a boolean is not a measurement, and extra fields are rejected rather than ignored. Then predict `shift_score(12, 10, 2)`: an absolute standardized difference of 1. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/model-service/scripts/run.py`. `service_contract.json` records the expected features and numeric bounds that `valid_request` enforces in miniature. `batch_monitoring.csv` reports each batch's largest standardized mean shift, using the training standard deviation as a fixed scale, as `shift_score` does. It also reports the mean prediction time, not a percentile. Apply your `nearest_rank` to the per-request `prediction_seconds` in `prediction_log.csv` to compare the two summaries. One difference to notice: for a feature with zero training variance, your function returns `None`, while the complete script reports a shift of 0 (`src/practical_ml_ai/deployment.py`). No wine feature has zero variance, so the recorded results are unaffected, but the two policies differ. Success on an authored fixture does not establish performance on a real service.

## Optional reading

[Google: Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml), the rules on monitoring and on training–serving skew, explains why a deployed model needs checked inputs and an owner for alerts. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
