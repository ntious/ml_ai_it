# Module 1: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module01/practice.ipynb "site-download:module01/practice.ipynb"). In a source checkout open `notebooks/practice/module01-practice.ipynb`. Use the [core environment and kernel](../../../QUICKSTART.md#notebook-option); the practice checks need NumPy even where the module script does not. Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `route`

Return a bool: priority >= threshold. Predict the result on `route(2)`, implement it and call `m01_route` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for route</summary>

Use an inclusive boundary; do not return the priority itself.

</details>

## Construct `partition_role`

Return fit, choose or evaluate for train, validation or test. Predict the result on `partition_role('train')`, implement it and call `m01_partition_role` through the notebook check. Then add a changed case and explain which assumption it tests.

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

## Transfer to an IT decision

Frame an escalation aid with a human fallback. Explain one field unavailable at ticket arrival. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M01.1:** Distinguish AI, ML, deep learning, and generative AI using an IT example.
- **M01.2:** Identify a problem's stakeholder, input, output, and reason for choosing a rule or learned model.
- **M01.3:** Execute and save a supplied Python example; in the notebook route, launch the interface, run a cell, and save the notebook. Explain the installation route.
- **M01.4:** Change an input, predict the result, and explain what happened.

The script route supplies the same programming evidence when a notebook interface is a barrier. It does not demonstrate notebook-interface operation. An instructor assessing that particular skill should arrange an accessible interface and support with the learner.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Before opening the notebook

Follow the notebook setup in [QUICKSTART](../../../QUICKSTART.md). The standard-library-only claim applies to the first script; notebook practice requires the core environment and a Jupyter kernel. The practice rule intentionally uses `>=`, unlike the first storage example’s strict `>`. At the threshold, these rules make different decisions.
