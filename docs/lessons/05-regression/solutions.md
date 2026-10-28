# Module 5: practice solutions and diagnostic feedback

Attempt the [practice](practice.md) before opening the [worked solution notebook](https://ntious.github.io/ml_ai_it/downloads/module05/solutions.ipynb "site-download:module05/solutions.ipynb"). The notebook executes the three functions and a real-data development comparison. Reading it is useful feedback, not evidence of independent implementation. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Residuals: direction and magnitude answer different questions

For actual `[110,125]` and predicted `[100,140]`, actual-minus-predicted gives `[10,-15]`. MAE averages the absolute errors: 12.5. Mean residual averages the signed values: -2.5. Taking the absolute value after averaging gives 2.5 and loses error magnitude through cancellation.

For the changed example `[1,4,10]` versus `[3,4,4]`, residuals are `[-2,0,6]`; MAE is 8/3 and mean residual is 4/3. A function returning a remembered 12.5 fails this case. An error-message about shape means the function must return one residual per observation rather than a single batch total.

## Persistence: a missing lag is not zero

Counts `[10,13,9]` become predictions `[None,10,13]`. The first preceding count was not supplied. For `[4,0,7,2]`, predictions are `[None,4,0,7]`: the observed zero remains a valid value. Copying the target-day count yields a perfect-looking but invalid forecast.

Explain the origin: when forecasting a later day in a rolling protocol, a previously evaluated day's finalized count may now be available. It would not be available in a single batch issued before all target days. Naming the split without naming that protocol leaves the leakage question incomplete.

## Pipeline: check what was fitted, not only the final prediction

The median imputer learns 3 from training `[1,3,missing,5]`. It must still report 3 after predicting on `[missing,100]`. The fitted illustrative linear relationship gives predictions `[6,200]`. If the median changes, inspect where `.fit` is called: use training features and labels; use `.predict` for later rows.

The real-data sandbox compares linear regression, previous-day persistence and a training-mean baseline on the same 14 validation targets. Read your actual values; the lesson does not require a trained model to win. This short development slice differs from the complete reference study, so its ranking or MAE must not be quoted as that study's final result.

## Debugging and transfer feedback

| Observed problem | Likely explanation to investigate | Useful next check |
| --- | --- | --- |
| MAE near zero despite large opposing errors | Signed errors averaged before taking magnitude | Compute absolute error for each row |
| Persistence exactly equals each target | Target-day values copied into features | Trace three issue times and preceding dates |
| Fitted median changes on prediction | Preprocessing fitted again or fitted on combined rows | Inspect imputer statistics before and after prediction |
| Sandbox skipped | One or more functions remain unfinished or failed | Rerun the edited function and its check; the result replaces its earlier state |

For the support-ticket transfer, distinguish an observed zero-ticket day from a missing export. A sound answer identifies the date boundary, available lag, delayed count risk and a manual fallback. An excellent explanation states what would change under a batch forecast and what evidence would validate the count-finalization assumption.

## Compare the quality of explanations

**Developing:** “The linear model has an MAE, so it works.” No baseline, units, origin or supporting count.

**Meets:** “At each daily origin we use the preceding finalized count. On the development interval, [method] has MAE [value] rentals/day versus [baseline/value]. I checked [date]'s residual by hand. This does not establish current staffing performance.” Attach the changed function and actual table.

**Extends:** Predeclare a cost or feature-availability sensitivity question using development data, reconcile the changed result, and justify whether more complexity helps the decision. Extra code alone does not strengthen the evidence.

Return to [practice](practice.md), then the [complete reference workflow](index.md#run-distinct-stages) and its [recorded feedback](feedback.md).
