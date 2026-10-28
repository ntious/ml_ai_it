# Module 5: independent implementation practice

Use [concepts](concepts.md) and [guided construction](guided.md) first. Work in the existing module environment. These tasks support the same outcomes as the complete reference; your instructor's assessment requirements remain authoritative.

## Start with the clean practice notebook

- [Practice notebook](https://ntious.github.io/ml_ai_it/downloads/module05/practice.ipynb "site-download:module05/practice.ipynb") — complete three function bodies and record predictions.
- In a source checkout: `notebooks/practice/module05-practice.ipynb`.
- The notebook must stay inside the complete source tree and use its installed package/kernel. It does not install dependencies for you.

Run Setup, then define a function and run its check. `not_attempted` means the placeholder remains; `needs_revision` supplies feedback; `passed` covers the visible cases. Repeating a check replaces its earlier state. When all three pass, run the supplied real-development sandbox. Partial work deliberately skips that sandbox rather than pretending it ran.

## Implement, check and explain

### Task 1: Residual summary

Implement `residual_summary(actual, predicted)` with residuals, MAE and mean residual. Explain why averaging signed errors before taking the absolute value fails.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 1</summary><p>Subtract corresponding elements first; magnitude and direction require separate summaries.</p></details>

### Task 2: Previous-day persistence

Implement `previous_day(counts)`. Preserve a missing first lag and a real count of zero. Trace each prediction to its issue time.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 2</summary><p>Shift the observations toward the later target rows; do not copy the same row or look forward.</p></details>

### Task 3: Training-only pipeline

Implement `fit_regression(train_x, train_y, new_x)`. Return the fitted pipeline and predictions, using named `imputer` and `model` steps.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 3</summary><p>Fit once on training. Inspect the imputer median before and after prediction on the new extreme.</p></details>

## Transfer with less support

A support team supplies authored daily ticket counts `[12,15,0,18]`. They are not real operational records. Construct previous-day predictions, explain how you would score only rows with a supplied lag, then describe what changes if the zero is actually an incomplete export. State the issue time, one forbidden future input and a fallback when counts are delayed.

For the real Bike Sharing sandbox, reconcile one prediction/residual and compare all three validation MAEs with units. Do not replace its label with "tickets" and claim operational IT performance.

## Evidence for the unchanged outcomes

| Outcome | Evidence to retain |
| --- | --- |
| M05.1 | Changed residual function and a hand-reconciled example with units |
| M05.2 | Fitted training-only pipeline plus dummy/persistence development comparison |
| M05.3 | Lag construction, issue-time explanation and a diagnosed target-day leak |
| M05.4 | Split roles, rolling-versus-batch explanation and observed validation errors |
| M05.5 | A short decision memo, limitations, commands and source/version evidence |

Keep your changed code, one hand-checked numerical claim, expected versus observed output, one diagnosed failure and a short decision memo. Record source/environment/command evidence when using real data. Interpretive reading alone does not replace an implementation outcome.

## Get feedback, then revisit

Open [practice solutions](solutions.md) after your first attempt. Compare the reasoning and a changed case, not only the final number. Return to your original notebook and reproduce the central operation without copying. Use [recorded-study feedback](feedback.md) after the complete reference run.

If using GenAI, keep a short disclosure of the help used and what you verified. Be able to explain and change the code independently; an equivalent no-assistant route uses the same hints and feedback. Never upload student records or credentials.
