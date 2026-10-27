# Module 12: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module12/practice.ipynb "site-download:module12/practice.ipynb"). In a source checkout open `notebooks/practice/module12-practice.ipynb`. Use the module’s existing environment. Three unfinished functions report **not_attempted**, not a pass.

## Construct `valid_request`

Return True for exactly the expected keys, finite int/float values; reject bool. Predict the result on `[{'x': 2}, ['x']]`, implement it and call `m12_valid_request` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for valid_request</summary>

Booleans are not numerical measurements in this contract; reject extras.

</details>

## Construct `shift_score`

Return absolute standardized difference, or None for a nonpositive training scale. Predict the result on `[12, 10, 2]`, implement it and call `m12_shift_score` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for shift_score</summary>

Use the fixed training scale, not a scale fitted on new requests.

</details>

## Construct `nearest_rank`

Return sorted values at ceil(percentile*n)-1 for 0 < percentile <= 1. Predict the result on `[[1, 2, 3, 100], 0.95]`, implement it and call `m12_nearest_rank` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for nearest_rank</summary>

Name the percentile convention and retain the tail request.

</details>

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
