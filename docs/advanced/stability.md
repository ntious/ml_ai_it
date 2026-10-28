# Advanced investigation: reproducibility and stability

Reproducing one seeded run answers “Can I obtain the same result under recorded
conditions?” Stability asks “How sensitive is the result to a justified change?”
The [capstone exemplar](../../projects/phishing-triage/README.md) keeps two sources
of variation separate.

A smaller version of both experiments runs in the core route as the [Module 6 stability exercise](../lessons/06-classification/practice.md#core-stability-exercise-two-kinds-of-variation).

## Experiment A: training randomness, fixed observations

Keep the outer split, inner folds, selected configuration, feature processing
and threshold rule fixed. Fit each substantive model for seeds 11, 23, 37, 53 and
71. Record every validation result, then select one common threshold per family
using mean validation cost across these runs. Do not pick the seed with the best
validation or final result.

The frozen evaluation reports every selected-family seed and a predeclared
probability-averaged ensemble. The ensemble is a separate serving policy, not a
sixth seed, not a best-seed selection and not a guarantee of improvement.

Inspect validation_runs.csv and validation_stability.csv. The latter provides
count, mean, sample standard deviation (ddof=1), minimum and maximum for cost,
and corresponding metric variation columns. final_seed_stability.csv reports
balanced accuracy, precision, recall, cost and Brier loss for the fixed final
seed set. The dummy runs once; its standard deviation is unavailable, not an
invented zero based on repeated observations.

Logistic regression with lbfgs is deterministic in this configuration. Identical
results across its seed labels are expected. The tree's tie-breaking and the
forest's sampling/feature choices can depend on random state. A seed only tests
the operations that actually use it.

## Experiment B: partition sensitivity, estimator seed fixed

Run the optional split-study stage. It uses only the original training partition,
resplitting profile groups for seeds 101, 202 and 303. The estimator seed stays
17. Read split_sensitivity.csv to compare scores across different development
observations rather than different random initializations.

The existing configuration was selected using these training observations in
CV. Therefore these are descriptive sensitivity checks, not untouched evaluation
sets or an unbiased estimate of the full tuning procedure. The original outer
validation and final records stay outside this investigation.

## What not to conclude

- Five seeds are five fits on largely the same evidence, not five independent populations.
- Small seed standard deviation does not establish stability to new institutions, campaigns or time periods.
- A mean plus/minus standard deviation is not a confidence interval for generalization.
- Changing the data split and training seed together obscures which change caused the variation.
- Saving only the best seed hides the instability you set out to measure.

## Independent investigation

Before reading the completed report, predict which family should vary most.
Compare the per-run table with your prediction. Calculate the mean and sample
standard deviation yourself, and explain why an unchanged logistic result is
not proof that the entire project is robust.

Next, compare the split-study spread with the training-seed spread. They answer
different questions and use different subsets, so do not subtract them as if
they were matched causal effects. Propose a group/time-aware external evaluation
that would address one limitation the seed study cannot answer.

<details><summary>Check: May I choose a different seed after seeing final performance?</summary>
That changes the evaluation protocol. Report the declared seed set; a new choice
needs development evidence and a fresh evaluation plan.
</details>

<details><summary>Check: Is k-means n_init=10 the same as this study?</summary>
No. Internal restarts choose one optimization result. A stability investigation
reports results across declared runs and, for clustering, needs appropriate
partition-comparison measures rather than classification accuracy.
</details>

Continue with [uncertainty, calibration and costs](evaluation.md).
