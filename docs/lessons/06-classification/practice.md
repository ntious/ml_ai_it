# Module 6: independent implementation practice

Use [concepts](concepts.md) and [guided construction](guided.md) first. Work in the existing module environment. These tasks support the same outcomes as the complete reference; your instructor's assessment requirements remain authoritative.

## Start with the clean practice notebook

If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

- [Practice notebook](https://ntious.github.io/ml_ai_it/downloads/module06/practice.ipynb "site-download:module06/practice.ipynb") — complete three function bodies and record predictions.
- In a source checkout: `notebooks/practice/module06-practice.ipynb`.
- The notebook must stay inside the complete source tree and use its installed package/kernel. It does not install dependencies for you.

Run Setup, then define a function and run its check. `not_attempted` means the placeholder remains; `needs_revision` supplies feedback; `passed` covers the visible cases. Repeating a check replaces its earlier state. When all three pass, run the supplied real-development sandbox. Partial work deliberately skips that sandbox rather than pretending it ran.

## Implement, check and explain

### Task 1: Confusion counts

Implement `confusion_counts(actual, probability, threshold)` using the declared inclusive threshold. Return integer tp/fp/fn/tn.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 1</summary><p>Trace each actual-label/decision pair; four mutually exclusive counts must sum to the record count.</p></details>

### Task 2: Cost-sensitive threshold

Implement `choose_threshold(...)` using validation labels, all declared candidates and the minimum-cost rule. Equal costs choose the smallest threshold.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 2</summary><p>Keep `(cost, threshold)` pairs so a stable ordering expresses both decisions.</p></details>

### Task 3: Training-only classifier

Implement `fit_classifier(train_x, train_y, new_x)`. Return the fitted `scaler`/`model` pipeline and one class-1 probability per new row.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 3</summary><p>Fit the scaler only on training. Locate class 1 in the fitted class ordering before selecting its probability column.</p></details>

## Transfer with less support

Consider these authored alert records, not measured operational evidence:

| Host | Day | Score | Investigation label availability |
| --- | --- | --- | --- |
| A | Monday | 0.7 | Wednesday |
| A | Tuesday | 0.8 | Thursday |
| B | Tuesday | 0.4 | Thursday |

You must decide on Tuesday. Identify labels unavailable for training that day, explain a repeated-host leakage risk and specify the additional records needed for a credible evaluation. Explain why these three rows cannot establish operational accuracy. Propose one false-alert workload question for the investigator.

After the complete reference study, trace one row through the exported shallow-tree rules. Explain each branch and why a predictive feature is not automatically causal.

## Core stability exercise: two kinds of variation

A single validation score depends on both the model's random choices and the records it was given. This exercise separates the two on development data only; the final test is never used.

Run it in the core environment from the `ml_ai_it` folder (it takes a few seconds):

```sh
python -m practical_ml_ai.stability --output runs/module06-stability
```

- **Experiment A** keeps the Module 6 training/validation split and changes only a random forest's seed (11, 23, 37, 53, 71).
- **Experiment B** keeps the seed at 17 and redraws the training/validation split five times from the same development records, grouping identical chemistry profiles as the module does.

Before running, predict which experiment will spread more. Then open `summary.txt` and `variation.csv` and answer:

1. Which experiment has the larger standard deviation of balanced accuracy, and by roughly how much?
2. How many actual positives does each validation set contain in experiment B? Why does that matter for recall?
3. Does the fixed Module 6 validation split look typical among the resplits? What does that imply about trusting one split?

A random forest is used because its result depends on the seed; logistic regression with this solver does not, so its seed spread would be zero by construction. The [capstone stability investigation](../../advanced/stability.md) runs the fuller version of both experiments.

## Applied extension: bounded tuning, including gradient boosting

Choosing settings is part of fitting, so it must stay inside the development data. This extension searches a fixed budget of 12 configurations across three model families using grouped 3-fold cross-validation on the Module 6 training records only, then scores each family's chosen configuration once on validation. Gradient boosting (scikit-learn's `HistGradientBoostingClassifier`, widely used for tabular data) is one candidate, not an assumed winner. The final test is never used.

```sh
python -m practical_ml_ai.tuning --output runs/module06-tuning
```

Before running, predict which family will score best. Then open `cv_trials.csv` and `validation_choices.csv` and answer:

1. Which configuration did each family choose, and are the differences between configurations larger than their cross-validation standard deviations?
2. Does the family with the best cross-validation score also have the best validation score? What would you do if they disagreed?
3. Why would choosing the configuration with the best validation score, and then reporting that same score, overstate performance?

All three families use balanced class weights and a 0.5 threshold, so their scores are not the Module 6 reference results, which select a threshold on validation.

## Evidence for the unchanged outcomes

| Outcome | Evidence to retain |
| --- | --- |
| M06.1 | Confusion function, total reconciliation and independently calculated precision/recall |
| M06.2 | Pipeline, fair training-prior comparison and complete-reference dummy/logistic/tree comparison |
| M06.3 | One explained path through the exported shallow tree; importance-versus-causation statement |
| M06.4 | Validation-only threshold choice, group/time rationale and final-freeze explanation |
| M06.5 | Decision memo with misses, false alarms, label meaning and a concrete limitation |

Keep your changed code, one hand-checked numerical claim, expected versus observed output, one diagnosed failure and a short decision memo. Record source/environment/command evidence when using real data. Interpretive reading alone does not replace an implementation outcome.

## Get feedback, then revisit

Open [practice solutions](solutions.md) after your first attempt. Compare the reasoning and a changed case, not only the final number. Return to your original notebook and reproduce the central operation without copying. Use [recorded-study feedback](feedback.md) after the complete reference run.

If using GenAI, keep a short disclosure of the help used and what you verified. Be able to explain and change the code independently; an equivalent no-assistant route uses the same hints and feedback. Never upload student records or credentials.

## Operational-data connection

Use the [RT-IoT completed-flow study](../../../projects/rt-iot-triage/README.md) to apply this module to captured network activity. Trace input availability, grouped evaluation, alert workload and the human review policy.

For the RT-IoT transfer, inspect the validation policy comparison and the selected policy before reading final metrics. A model can have high recall while requiring almost every flow to be reviewed. Compare assumed error cost and analyst workload separately; do not lower the threshold after inspecting final results. The project README records the protocol and its qualifications.
