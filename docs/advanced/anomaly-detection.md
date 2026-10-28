# Optional extension: unusual days and review workload

After Module 7 or 12, use the core environment to flag unusual observations in the UCI Bike Sharing daily data. This is a dated service-demand analogue, not IT incident telemetry. The data has no verified incident labels. A flag means “investigate this observation,” not “an incident occurred.” Learning outcomes and the required module sequence remain unchanged.

## Declare the decision before running

The decision happens after the day ends, when its rental count and temperature are available. This is not an advance warning or a forecast. Fit on 2011, set thresholds on January–June 2012 and inspect July–December 2012 once. Seven initial days supply past-week features. A previous-week observation from the test period is available for a later day's end-of-day calculation; the model is never refitted on test observations.

Two methods use the same dates: Isolation Forest on log count, change from seven days earlier and temperature; and a baseline measuring absolute deviation of weekly log-count change from its training median, scaled by training median absolute deviation. The baseline makes a simple alternative visible. The model settings are fixed before evaluation. For each method, the threshold is the validation score's 95th percentile; only strictly greater scores are flagged. Ties can reduce the validation flag fraction. This is a declared review-budget rule, not an estimate of the true anomaly prevalence.

## Execute and audit

From the repository root, with `python` meaning the installed core environment executable:

```sh
python -m practical_ml_ai.anomaly --output runs/anomaly-days
```

The command downloads the existing checksum-pinned source into `runs/datasets/bike-sharing` or validates a prior cache. It refuses an existing output directory. It saves:

| File | What to check |
| --- | --- |
| `protocol.json` | Calendar boundaries, features, model settings, thresholds and source hashes |
| `scores.csv` | Each dated score, method, partition and flag |
| `workload.csv` | Flagged days and denominator for each method/partition |
| `monthly_context.csv` | Test-month mean counts and their difference from the training mean in training standard-deviation units |

Before reading the output, predict whether growth and seasonality could increase flags. Then recompute one test flag fraction from `scores.csv` and reconcile it with `workload.csv`. Compare how many days each method asks a person to review. A lower flag count alone does not make a method better.

Inspect three flagged dates and three unflagged dates. Identify what would be needed to confirm an incident, and which observations could reflect expected weather, seasonal demand or growth. Do not label an unflagged date “normal” merely because the detector omitted it. If you propose calendar-adjusted features, define a new development experiment and preserve the original final results.

## Distribution change is not a diagnosis

The monthly table describes a change in the distribution of observed demand. It does not distinguish seasonality, trend, measurement changes or an incident. It is not a statistical significance test, and it cannot establish concept drift (a change in a predictive relationship) without an appropriate target and evaluation design. External validation would require operational data with context and a justified response process.

<details><summary>Feedback: can I choose the threshold that catches a famous disruption?</summary>
Not after inspecting the held-out period. That would use the event to select the rule. Retain the declared threshold, report its observed behavior and specify a fresh evaluation if you change the rule. Even matching a historical disruption does not validate all the other flags.
</details>

<details><summary>Feedback: how do I measure precision without incident labels?</summary>
You cannot infer incident precision from these flags. Report workload, agreement between methods and contextual investigations. A future evaluation needs a defined incident outcome and a reviewed sample that includes both flagged and unflagged periods.
</details>

Read the [Isolation Forest API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) for score direction and parameter meanings. The implementation uses negative `score_samples`, so larger values are more unusual, and applies its own validation threshold. See [uncertainty and costs](evaluation.md) for the distinction between measurement and operational justification.

## Recorded reference run

On the pinned daily archive, the local core run produced 358 training, 182 validation and 184 final days after the initial seven-day lag. Each method flagged 10 validation days; Isolation Forest flagged 14 final days (7.61%) and the weekly-change baseline flagged 16 (8.70%). These are review-workload observations, not true-positive counts or a model ranking. The final period did not choose either threshold.
