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

## Evidence activity: Audit a classification decision

Use test_predictions.csv and the recorded selected threshold. Recompute TP, FP, FN, TN and recall, checking that the counts sum to the number of records. Compare with test_scores.csv. Explain how choosing a new threshold after this audit would reuse test evidence. Then complete the small stability bridge linked below when assigned.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.

Continue with the [small core stability experiment](../../advanced/core-stability.md), which uses the core environment and keeps the final test untouched.
