# Monitoring decision record

This guide supports the course outcome on deploying and monitoring AI-driven solutions. [Module 12](../lessons/12-deployment/index.md) produces monitoring artifacts from a local replay. A decision record turns those artifacts into a justified recommendation. It assesses what you observed and decided. It does not show that a system became more reliable in production, because the replay does not measure that.

Use it after Module 12, or after the optional [RT-IoT project](../../projects/rt-iot-triage/README.md). It is optional and adds no required assessment.

## Evidence to gather

From a Module 12 run, open `batch_monitoring.csv`, `prediction_log.csv`, and `service_contract.json`.

| Indicator | Where to find it | What it can and cannot tell you |
| --- | --- | --- |
| Latency | `mean_prediction_seconds` per batch | Local CPU speed for this replay, not production capacity |
| Input shift | `largest_standardized_mean_shift` per batch | A diagnostic against training data; row order is not event time, so it is not drift |
| Errors and workload | `fp`, `fn`, `selection_rate`, `recall`, `precision` per batch | Held-out behavior with known labels. Live labels usually arrive late |
| Contract failures | Requests rejected by `service_contract.json` rules | Whether invalid inputs are stopped, not whether valid inputs are good |

## Draft the evidence table

Run the helper on your batch file. It reports observed values and compares them only with thresholds you declare. It does not choose thresholds or a decision.

~~~sh
python -m practical_ml_ai.monitoring_record runs/module12/study/batch_monitoring.csv --latency-limit 0.001 --shift-limit 0.5
~~~

The numbers above are placeholders. Replace them with limits you can justify, and say where each came from. A missing standardized shift is shown as unavailable rather than zero.

## Write the record

Complete each part in a few sentences, citing numbers from your own run.

1. **Service and owner.** What does the service decide, and who is responsible when it fails?
2. **Indicators and thresholds.** Which two or three indicators would you watch, and what value triggers a response? Say where each threshold comes from. An unexplained threshold is a guess.
3. **Observed behavior.** State one batch result and one unexpected value or inconsistency.
4. **Decision.** Choose one: continue, investigate, roll back, or do not deploy. Give the evidence that would change your mind.
5. **Escalation and rollback.** Who is told, how fast, and which earlier approved version is restored?
6. **Limits.** Name at least two things this replay cannot establish.

## Check your record

- Every claim cites a named column or file from the run.
- A monitoring alert asks for investigation. It does not trigger automatic retraining.
- Malformed or unavailable inputs go to a human or a safe default, and the record says which.
- Logs are reviewed for personal or sensitive content before anyone shares them.
- The record does not claim improved reliability, availability, or performance in production.

## Optional extension

Compare two batches or two model versions, state which measure you froze before looking, and explain a case where the faster or smaller option is the wrong choice.
