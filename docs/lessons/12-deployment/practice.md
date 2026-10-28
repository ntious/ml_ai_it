# Module 12: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module12/practice.ipynb "site-download:module12/practice.ipynb"). In a source checkout open `notebooks/practice/module12-practice.ipynb`. Use the [framework environment and kernel](../../setup/frameworks.md). Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `valid_request`

Return True for exactly the expected keys, finite int/float values; reject bool. Predict the result on `valid_request({'x': 2}, ['x'])`, implement it and call `m12_valid_request` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for valid_request</summary>

Booleans are not numerical measurements in this contract; reject extras.

</details>

## Construct `shift_score`

Return absolute standardized difference, or None for a nonpositive training scale. Predict the result on `shift_score(12, 10, 2)`, implement it and call `m12_shift_score` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for shift_score</summary>

Use the fixed training scale, not a scale fitted on new requests.

</details>

## Construct `nearest_rank`

Return sorted values at ceil(percentile*n)-1 for 0 < percentile <= 1. Predict the result on `nearest_rank([1, 2, 3, 100], 0.95)`, implement it and call `m12_nearest_rank` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for nearest_rank</summary>

Name the percentile convention and retain the tail request.

</details>

## Reason beyond the visible checks

Compute `nearest_rank([0.010, 0.011, 0.012, 0.250], 0.95)` and the mean of the same four durations. Which summary would alert an owner to the slow request? How many requests do you need before the 95th percentile is no longer simply the maximum? The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Write a service response policy for an invalid request, a model outage and an alert without outcome labels. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M12.1:** Define an input/output contract and reject invalid requests.
- **M12.2:** Serve the same trained classifier and a bounded local LLM workflow through Streamlit.
- **M12.3:** Replay actual held-out records and measure prediction duration/outcomes.
- **M12.4:** Distinguish batch diagnostics from genuine time drift and production service guarantees.
- **M12.5:** Propose ownership, escalation, monitoring, and rollback criteria.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Operational-data connection

Use the [RT-IoT completed-flow study](../../../projects/rt-iot-triage/README.md) to apply this module to captured network activity. Trace input availability, grouped evaluation, alert workload and the human review policy.

For the RT-IoT transfer, inspect the validation policy comparison and the selected policy before reading final metrics. A model can have high recall while requiring almost every flow to be reviewed. Compare assumed error cost and analyst workload separately; do not lower the threshold after inspecting final results. The project README records the protocol and its qualifications.

## Evidence activity: Distinguish replay from monitoring

Use the saved batch predictions and batch summary. Recompute one batch’s error rate and identify its denominator. Explain why source-order batches do not demonstrate temporal drift; specify what timestamp and delayed-label evidence a live monitor would require.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.
