# Module 3: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module03/practice.ipynb "site-download:module03/practice.ipynb"). In a source checkout open `notebooks/practice/module03-practice.ipynb`. Use the module’s existing environment. Three unfinished functions report **not_attempted**, not a pass.

## Construct `parse_latency`

Parse blank/None as None; otherwise return a nonnegative float, raising ValueError for negatives. Predict the result on `['']`, implement it and call `m03_parse_latency` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for parse_latency</summary>

Preserve measured zero and missingness separately.

</details>

## Construct `deduplicate`

Keep the first record for each event_id, preserving input order. Predict the result on `[[{'event_id': 'a', 'v': 1}, {'event_id': 'a', 'v': 2}, {'event_id': 'b', 'v': 3}]]`, implement it and call `m03_deduplicate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for deduplicate</summary>

Deduplicate by identity, not the entire row.

</details>

## Construct `reconcile`

Return True exactly when nonnegative counts reconcile. Predict the result on `[10, 7, 2, 1]`, implement it and call `m03_reconcile` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for reconcile</summary>

Every source row needs one accounted-for outcome.

</details>

## Transfer to an IT decision

Add a repeated event with a changed annotation and a missing latency. Explain the retained record and reconciliation. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

By completing the core route, you can:

1. **M03.1:** Inspect NumPy shapes/types and use a small vector or linear-system calculation.
2. **M03.2:** Read, filter, summarize, and write a pandas dataframe.
3. **M03.3:** Run a repeatable preparation script and explain rejected records.
4. **M03.4:** Identify CSV, JSON, and array representations with their fields and units.
5. **M03.5:** Write a data dictionary and justify a cleaning choice while preserving later train/test boundaries.

These are resource learning outcomes. They do not claim course credit or certified program-outcome attainment.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Operational-data connection

Use the [RT-IoT completed-flow study](../../../projects/rt-iot-triage/README.md) to apply this module to captured network activity. Trace input availability, grouped evaluation, alert workload and the human review policy.
