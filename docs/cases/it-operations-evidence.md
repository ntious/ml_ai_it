# IT operations transfer: completed-flow review

This optional application supplies **additional evidence for CLO2**, the working summary “applying ML/AI to IT operations.” Complete the [RT-IoT study](../../projects/rt-iot-triage/README.md) and this decision record. A wine, bike or SMS result alone is not the evidence for this activity.

Use the documented core environment with the regression extra. Start after Module 6; if you first encounter this link in Module 5, return after learning classification. Modules 8, 9 and 14 can reuse the same completed record. **Complete the shared study once**, cite its run directory and extend your explanation as needed; do not count repeated references as independent assessments.

## Run and inspect

From the repository root:

```sh
python projects/rt-iot-triage/scripts/run.py --output runs/it-operations-evidence
```

The script downloads and checks the original UCI archive; no dataset is committed to this repository. Use a fresh output directory for a new experiment. Inspect `summary.json`, `validation.csv`, `evaluation.csv` and `predictions.csv`. The README explains source labels, grouping and decision-time feature availability.

## Produce an operations decision record

1. **Define the task:** which completed flows should a network analyst review? State why these features do not justify a connection-start decision or automated blocking.
2. **Explain the frozen choice:** identify the policy selected on validation and its threshold, if applicable. Compare it with always-review and never-review. Test results describe the frozen policies; they must not change the selection.
3. **Recompute the evidence:** from `evaluation.csv`, verify one policy's assumed cost as `5 * fn + fp`, then its cost per 1,000 flows using `summary.json`'s test-row count. Reconcile `alerts_per_1000` with `tp + fp`. The 5:1 costs are an illustrative assumption, not measured organizational costs.
4. **Make an operational decision:** propose analyst capacity and explain whether the selected policy's workload fits it. Label capacity as your scenario assumption. Decide investigate, supervised trial, or do not deploy; identify the evidence needed to change that decision.
5. **Account for uncertainty:** explain why within-capture results do not demonstrate generalization across devices, sessions, future traffic or a production fleet. Name an owner for escalation and a fallback policy.

Submit the run path, your independent calculations and a short decision memo. Use the [evidence worksheet](../../templates/evidence-review.md).

## Connect it to your module

| Module | Additional explanation | Boundary |
| --- | --- | --- |
| 5 | Explain how baseline-first evaluation transfers from demand forecasting to analyst workload | This is classification evidence for IT application, not a network forecasting or regression result |
| 6 | Explain the validation threshold, false alerts and missed attacks | Never choose the threshold from the final test |
| 8 | Compare the simpler model's evidence with the evidence you would demand before considering a neural replacement | This activity does not train a neural model on network flows; neural training evidence remains in Module 8 |
| 9 | Contrast completed-flow features with SMS text and explain the different privacy and availability constraints | This is network triage evidence, not an NLP model on network records |
| 14 | Specify a bounded read-only tool that would report these saved metrics; list permitted inputs, outputs, approvals and stopping conditions | A design is not an implemented or deployed agent |

## Success criteria

The record identifies the correct frozen selection, reconciles the cost and workload calculations, separates source facts from scenario assumptions, and makes a defensible human-review decision. A recommendation not to deploy can meet these criteria. A passing calculation alone does not demonstrate the full course outcome; the adopting instructor judges the submitted reasoning against the authoritative outcome.

For actual serving and monitoring evidence, complete [Module 12](../lessons/12-deployment/index.md) and the [monitoring decision record](../advanced/monitoring-decision-record.md). Those are a separate executed activity, not something established by a Module 14 agent trace.
