# Advanced investigation: bounded hyperparameter tuning

A model parameter is learned during fitting; a hyperparameter defines how that
fitting works. Choosing tree depth after looking at final errors is still tuning,
even if it happens manually. The [capstone exemplar](../../projects/phishing-triage/README.md)
puts that choice inside a declared, inspectable development experiment.

A smaller version runs in the core route as the [Module 6 tuning extension](../lessons/06-classification/practice.md#applied-extension-bounded-tuning-including-gradient-boosting), which adds gradient boosting as a candidate.

## Predict, run and inspect

Before execution, name the family, parameter space, scoring rule, fold boundary,
random seed and compute budget. Predict whether increasing depth must improve
validation performance, and what happens when several configurations tie.

The default study compares:

| Family | Declared candidates | Fixed controls |
| --- | --- | --- |
| Logistic | C = 0.1, 1, 10 | One-hot categorical inputs, balanced class weights, lbfgs, 1,000-iteration maximum |
| Tree | Depth = 3, 6, 9 | One-hot inputs, minimum leaf size 5 |
| Forest | Depth = 6 or 10; leaf size = 3 or 8 | One-hot inputs, 40 trees, one CPU worker |

Ten configurations × three folds = 30 fits. The configuration rejects an
over-budget grid. In every fold, preprocessing fits only the fold's training
records. StratifiedGroupKFold attempts to preserve label proportions while
keeping identical profiles together; exact class proportions need not match.
The saved fold IDs let you verify the boundary rather than trusting the name.

Run the prepare and tune commands from the project README, or run its complete
workflow. Read search_trials.csv and tuning.json. Every fold records the actual
score, duration and fitting seed. Mean balanced accuracy at threshold 0.5 chooses
one configuration per family. Stable parameter-JSON order breaks exact ties;
there is no test-based tie-break or requirement that the complex model wins.

## What the scores mean

The winning CV score was used to choose its configuration, so it is selection-
reused and can be optimistic. It is not the final generalization estimate. The
project subsequently uses a separate validation partition for common thresholds
and family selection, freezes all choices, and evaluates the declared policy on
the final partition.

Nested CV would repeat the whole search inside each outer fold to assess the
selection procedure itself. It is a valuable extension when that is the research
question; it is not secretly performed by this example's three inner folds.

Random search, Bayesian search and successive halving are alternative search
strategies, not implemented claims here. A small explicit grid makes every fit
and decision visible to learners and keeps CPU costs bounded.

## Independent modification

Copy the configuration, change one justified search dimension within the budget,
and choose a new output directory. State the expected effect before rerunning.
Compare development scores and elapsed fitting time. Because the public final
results are already available, this is development/rehearsal; a fresh prospective
claim needs a new evaluation design.

<details><summary>Check: May I fit the encoder once before the CV loop?</summary>
No. That lets validation-fold information shape preprocessing. The pipeline fits
the encoder separately inside each fold.
</details>

<details><summary>Check: Does the best CV configuration need to beat the baseline on final data?</summary>
No. Final results test the frozen policy. A baseline win is evidence to explain,
not permission to retune the final set.
</details>

<details><summary>Check: Is a decision threshold a learned coefficient?</summary>
No. It is a declared decision-policy setting. This project chooses common
thresholds using validation error cost after fitting and tuning the models.
</details>

Read the [versioned search guide](https://scikit-learn.org/1.8/modules/grid_search.html)
and [grouped-fold documentation](https://scikit-learn.org/1.8/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html)
for the primary API references. Continue with [stability](stability.md).
