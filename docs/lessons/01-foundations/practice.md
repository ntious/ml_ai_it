# Module 1: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module01/practice.ipynb "site-download:module01/practice.ipynb"). In a source checkout open `notebooks/practice/module01-practice.ipynb`. Use the [core environment and kernel](../../../QUICKSTART.md#notebook-option); the practice checks need NumPy even where the module script does not. Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `route`

Return a bool: priority >= threshold. Predict the result on `route(2)`, implement it and call `m01_route` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for route</summary>

Use an inclusive boundary; do not return the priority itself.

</details>

## Construct `partition_role`

This task previews the split roles that [Module 5](../05-regression/index.md) develops with real data; it supports reasoning about evidence rather than a separate Module 1 outcome. Return fit, choose or evaluate for train, validation or test. Predict the result on `partition_role('train')`, implement it and call `m01_partition_role` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for partition_role</summary>

The final test must not choose a model.

</details>

## Construct `error_counts`

Return [false_alerts, misses] for equally sized boolean lists. Predict the result on `error_counts([False, True, True], [True, False, True])`, implement it and call `m01_error_counts` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for error_counts</summary>

Count errors by their consequences, not only total accuracy.

</details>

## Work with the complete study's results

Run the first-run script with `--storage-percent` values 80, 81, 100 and 100.5, each to its own output file. Predict each decision first. Which inputs give `Review storage`, which give `Within the chosen threshold`, and which is rejected? Relate each result to `storage_percent > 80` and to the script's input check. Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

Construct two prediction lists for the actual labels `[True, False, False]` that both have accuracy 2/3 but different error counts. Use `error_counts` to show the difference, then say which list you would prefer for a storage alert and why. The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Frame an escalation aid with a human fallback. Explain one field unavailable at ticket arrival. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Evidence and feedback

- **M01.1:** Distinguish AI, ML, deep learning, and generative AI using an IT example.
- **M01.2:** Identify a problem's stakeholder, input, output, and reason for choosing a rule or learned model.
- **M01.3:** Execute and save a supplied Python example; in the notebook route, launch the interface, run a cell, and save the notebook. Explain the installation route.
- **M01.4:** Change an input, predict the result, and explain what happened.

The script route supplies the same programming evidence when a notebook interface is a barrier. It does not demonstrate notebook-interface operation. An instructor assessing that particular skill should arrange an accessible interface and support with the learner.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Before opening the notebook

Follow the notebook setup in [QUICKSTART](../../../QUICKSTART.md). The standard-library-only claim applies to the first script; notebook practice requires the core environment and a Jupyter kernel. The practice rule intentionally uses `>=`, unlike the first storage example’s strict `>`. At the threshold, these rules make different decisions.

## Evidence activity: Trace one decision

Use your first-run output and its input records. Recompute one rule decision, including the exact threshold boundary. Identify what a wrong decision would mean and explain why agreement with the rule is not measured predictive accuracy.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.
