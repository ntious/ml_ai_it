# Module 6: practice solutions and diagnostic feedback

Try the [practice](practice.md), then compare the [worked solution notebook](https://ntious.github.io/ml_ai_it/downloads/module06/solutions.ipynb "site-download:module06/solutions.ipynb"). Use the notebook to inspect a completed approach; assess your understanding with changed inputs and an independent explanation. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Confusion counts: trace a boundary case

For labels `[0,1,0,1]`, scores `[.2,.4,.5,.8]` and threshold `.5`, the rule is `score >= threshold`. Counts are TP=1, FP=1, FN=1, TN=1. The score exactly .5 belongs to the positive decisions. Using `>` moves that negative record into TN and changes the contract.

Precision is TP/(TP+FP); recall is TP/(TP+FN). Both are .5 in this example. Adding three easy negatives increases TN to 4 and accuracy from 2/4 to 5/7; recall remains 1/2. The extra correct negatives did not recover the missed positive. When a denominator is zero, a rate is unavailable rather than automatically zero.

## Threshold selection: recompute under the declared costs

The authored thresholds `.3,.5,.7` produce costs `[1,4,3]` under miss cost 3 and false-alarm cost 1. Choose .3. Under miss cost 1 and false-alarm cost 5, costs are `[5,6,1]`; choose .7. No weights were fitted again. Ties use the smallest threshold even if candidates arrive in a different order.

If a function always returns .5, it ignores the question. If it maximizes accuracy while the contract asks for cost, it optimizes a different decision. If it chooses from final-test results, its number may be correct arithmetic but the evaluation design is invalid.

## Pipeline: preserve the class and preprocessing contracts

Fit the scaler and logistic regression on training only. Training inputs `[0,2,4,6]` have mean 3; a later input of 100 must not change it. Find the class-1 column in `model.classes_` when extracting `predict_proba`. Return one score per new observation rather than two columns or hard labels.

The real Wine Quality sandbox uses grouped training/validation partitions, not final labels. Both logistic and training-prior methods receive validation-selected thresholds under the same candidate set and cost assumption. That makes their cost comparison interpretable. It does not make the illustrative wine costs operational incident costs.

## Debugging and transfer feedback

| Symptom | What to inspect | Why it matters |
| --- | --- | --- |
| Confusion total differs from row count | Boolean conditions and row alignment | Each record belongs to exactly one cell |
| A score at the threshold is counted negative | `>=` versus `>` | Boundary conventions change decisions |
| Cost change never affects the choice | Cost formula, candidate loop and tie rule | A fixed default does not implement selection |
| Scaler mean includes the new extreme | Fitting after combining rows | New observations must not influence training quantities |

For the authored IT alert scenario, repeated host rows can share behavior and labels may arrive after investigation. A strong transfer response states the intended future population, grouping/time boundary and label delay before proposing a split. With only the supplied few rows, no credible operational model comparison is possible; identify the additional records needed instead of inventing an accuracy claim.

## Core stability exercise feedback

The recorded run (October 28, 2026) gave a balanced-accuracy standard deviation of 0.009 for experiment A (seed only; range 0.561–0.586) and 0.017 for experiment B (split only; range 0.624–0.664). Changing which records are used moved the result about twice as much as changing the seed.

Experiment B's validation sets contain between 27 and 42 actual positives, so recall rests on a different denominator in each run, and one record changes it by 2–4 percentage points. Every resplit (lowest 0.624) scored higher than any seed on the fixed split (highest 0.586), which suggests the fixed validation set is a harder sample than most; a single split can be unrepresentative without anything being wrong.

A good answer separates the two sources: seed spread describes training randomness, while split spread describes sensitivity to the particular records. Neither is an estimate of performance on future data, and neither justifies looking at the final test to pick a seed. The threshold here is fixed at 0.5, so recall is low; tuning it would be a separate, validation-only decision.

## Compare the quality of explanations

**Developing:** “Recall is higher, so deploy.” The false-alert workload and label meaning are unexplained.

**Meets:** “Under the declared validation cost rule, [threshold] gives [FN] misses and [FP] false alarms on [n] records. Changing costs changes the preferred decision. I traced one tree path in the complete reference and explained its prediction without treating importance as causation.” Attach the actual tables and changed code.

**Extends:** Predeclare a development-only sensitivity analysis and discuss capacity, sampling and label uncertainty. A larger model or a final-test-driven threshold change does not establish stronger reasoning.

Return to [practice](practice.md), then the [complete reference study](index.md) and [recorded feedback](feedback.md).
