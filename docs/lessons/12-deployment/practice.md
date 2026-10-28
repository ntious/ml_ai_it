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

## Work with the complete study's results

Open `prediction_log.csv` from your run. For each batch, compute the nearest-rank 95th percentile of `prediction_seconds` with your `nearest_rank` and compare it with that batch's `mean_prediction_seconds` in `batch_monitoring.csv`. Your times depend on your hardware; compare the two summaries, not the absolute values. Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

Compute `nearest_rank([0.010, 0.011, 0.012, 0.250], 0.95)` and the mean of the same four durations. Which summary would alert an owner to the slow request? How many requests do you need before the 95th percentile is no longer simply the maximum? The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Write a service response policy for an invalid request, a model outage and an alert without outcome labels. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Advanced extension: serve the model as a JSON API

A web form is one interface; services usually call a model through an API. This extension serves the Module 6 model, the same one the replay monitors, with the same checked input contract, using only Python's standard library. It needs the core environment with the regression extra.

```sh
python -m practical_ml_ai.api --port 8000
```

In a second terminal, send a request, for example with `curl -s localhost:8000/health`, or from Python with `urllib.request`. Then try each case and record the status code and message:

1. A complete record of the eleven chemistry features.
2. The same record with an extra `quality` field.
3. A record where `alcohol` is `true`.
4. A body that is not valid JSON.

Explain why the service rejects cases 2–4 instead of guessing, which status code each receives, and what is still missing before this could be exposed beyond your own computer (authentication, rate limits, logging policy, monitoring and an owner). Frameworks such as FastAPI provide request schemas and documentation; the contract is the part to keep.

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
