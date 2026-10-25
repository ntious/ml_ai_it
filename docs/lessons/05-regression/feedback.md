# Module 5 worked feedback

Compare reasoning and artifacts after [practice](practice.md). Your generated report supplies fitted values and scores; retain its source/version record when comparing runs.

## Forecast timing and split

Today's finalized count and the same weekday's count last week are observed at the end-of-day origin. Tomorrow's actual weather, casual/registered rental components, and total are unavailable. Future calendar features may be known, but they are not the same as future observations.

The real file has 731 days. Seven warm-up days leave 724 examples: 504 training targets, 110 validation, and 110 final test. Dates do not overlap. A previous holdout day's count can become a legitimate feature at a later origin under this rolling one-day-ahead protocol; it would not be available if every forecast were issued before the holdout began.

## Fitting and selection

Training fits the dummy mean and linear pipelines. Persistence applies observed lags. Each training CV fold fits its own imputer and regression using earlier rows. Validation alone selects among predefined methods.

A persistence winner is acceptable. Choosing another method after inspecting final test would turn that test into development data. Report the frozen method and obtain appropriate new evaluation data for changes. The core implementation does not silently refit on train plus validation.

A pipeline prevents inconsistent application of learned preprocessing, but does not prevent every type of leakage. The candidate artifact records only valid feature names. The intentionally invalid identity example remains outside the selection workflow.

## A verified real-data result

The initial Windows/Linux run selected **previous-day persistence** on validation. On 110 final dates, its MAE was about **926.57 rentals/day**, compared with **2,330.68** for the training mean and **1,382.10** for weekly persistence. Its mean residual was about **-46.74 rentals**, indicating a small net overprediction despite much larger individual errors.

This is a useful finding: fitting a linear model did not automatically make it the right choice under the declared selection rule. The losing linear candidates remain in the validation table; final testing does not reopen that choice. Reproduce using the recorded source digest and constraints; do not generalize these historical numbers to current demand.

The original synthetic fixture instead selected the weekly linear model, with final MAE about 17.44 synthetic count units. That different result illustrates why synthetic behavior checks and real-data evidence are reported separately.

## Check errors by hand

Actual 110 minus prediction 100 gives residual +10 and absolute error 10. Actual 125 minus prediction 140 gives -15 and absolute error 15. MAE is 12.5. Positive residual means underprediction under this repository's convention.

MAE is an average, not a maximum or guarantee. Mean residual can hide cancellation. Use date-ordered values to support a claim about runs, changing direction, or isolated errors. Do not invent a pattern because an assignment asks you to investigate one.

The future row has inputs and a target date but no actual outcome. It cannot produce an error score. A plausible-looking forecast is not evidence of accuracy.

## Why the near-perfect leakage score fails

A linear model supplied with the target itself learns an identity mapping. It can obtain almost-zero validation error, but tomorrow's actual target is unavailable when the forecast is needed. Target-day casual and registered components also arrive too late and reconstruct the total. Good-looking error numbers cannot repair invalid feature timing.

## Stakeholder memo scaffold

“We forecast tomorrow's rentals after today's count is complete. We used chronological training/validation/final-test splits and fixed-parameter rolling one-day-ahead evaluation. Validation selected [method] using MAE. The frozen method's final MAE was [value] rentals/day, compared with [baseline/value]. On [date], actual [value] versus predicted [value] gave residual [value].”

Then add a supported limitation and next action: historical coverage, changing conditions, delayed observations, unequal error costs, or dependence. Fill values from actual artifacts, not imagined favorable results. A new prospective monitoring period with agreed cost criteria could be a next step; this historical study does not establish readiness for automated operations.

## Reviewing AI suggestions

Reject a random shuffle that defeats the forecast-time question, full-dataset median fitting that includes holdouts, or a final-test-based change to the frozen choice. Check actual code and artifacts rather than confidence of wording.

Return to [Module 5](index.md) or the [instructor notes](instructor.md).

## Construction check and misconception feedback

Question: Can an imputer fitted on all dates leak information?

Yes. Its learned value can incorporate future observations. Fit preprocessing inside training boundaries.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
