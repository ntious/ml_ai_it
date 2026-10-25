# Module 4 practice: three figures and an operations memo

This is independently authored companion practice, not an official Canvas assignment. Complete the [walkthrough](index.md) first. Allow 45–75 minutes. Use synthetic copies and a new directory under `runs/module04-practice/` to preserve the raw sample and earlier results.

## Core task P04

1. State the operations question and observation unit. Explain the duplicate, missing-latency, and outlier policies before interpreting a chart.
2. Run the supplied analysis. Select three figures: one distribution, one comparison, and one time or relationship view. For each, justify the chart type, name axes/units and scales, supply its underlying table, and write a short alternative plus a detailed description. Use the shared plotting code as a starting point. Make and explain at least one purposeful chart change, such as a horizontal comparison; the notebook supplies a runnable variation. Preserve or update its matching table/description. Keep your code and regenerated artifact.
3. Identify one pattern or anomaly using at least two exact values. Name one limitation and a next investigation question. Distinguish descriptive association from a causal explanation.
4. Create a copy of the raw CSV. Remove only the row with unavailable latency, retaining the other raw rows. Predict which totals/counts will change, run using a new output directory, and explain why the reduced workload total answers a different question.
5. In a separate sensitivity analysis, use the normalized observations and exclude the flagged 160 ms observation. Recompute the latency mean and median. Label this as an analytical comparison, not a justified cleaning decision. Explain what information removal loses.
6. Write a 150–250-word memo for the fictional operations lead. Include the question, numerical finding, preprocessing rationale, limitation, and next action. A figure with its table or an equivalent text/table account may support the memo. Do not require a sight-dependent screenshot as evidence.

You can reuse this notebook pattern for the sensitivity analysis:

```python
observed = frame.dropna(subset=["p95_latency_ms"])
sensitivity = observed.loc[observed["p95_latency_ms"] != 160, "p95_latency_ms"]
print("Sensitivity mean (ms):", sensitivity.mean())
print("Sensitivity median (ms):", sensitivity.median())
```

For this known fixture, 160 identifies the single flagged observation. For other datasets, identify the actual date/service key and investigate it; do not turn “remove 160” into a general cleaning rule.

If your workflow evaluates chart-authoring skill, retain the code and generated figure artifacts. Blind learners can author those figures through code and verify them through labels, tables, and descriptions; the interpretation task uses the same numerical evidence. Where you cannot run an interface, use the generated worked example and explain that your evidence demonstrates interpretation rather than program execution.

## Discussion or solo reflection

A stakeholder requests “a chart proving that traffic caused the spike.” Explain why the scatter plot cannot provide that proof and propose evidence that could help investigate. In class, compare explanations; independently, write and critique one alternative explanation. Also compare the zero-baseline and cropped-baseline bars: what changed, and what did not?

## Work with GenAI

Optional prompt: “Critique this memo against the supplied table. Flag any causal claim, missing denominator, unsupported extrapolation, or confusion between daily p95 and overall p95.” Verify each suggestion yourself. Keep a short record of the suggestion, evidence checked, and your final decision. Without an assistant, apply those same four checks using the supplied feedback. Do not upload real service records to an unapproved service.

## Optional extension

Change the histogram bin width or create a two-panel service comparison without changing observations. Explain which impressions change and which statistics remain fixed. Alternatively, frame an agriculture or education-support question and identify the analogous observation unit and coverage risk; new data collection is not required. These are skippable extensions, not implied extra credit.

## Self-check and adaptable criteria

| Criterion | Evidence of a satisfactory result |
| --- | --- |
| Preprocessing, M04.1 | Explicit policies, changed-row accounting, and a justified distinction between a flag and an error |
| Chart authoring, M04.2 | Three appropriate plots, reproducible code, labels/units/scales, and matching tables |
| Interpretation, M04.3 | An exact evidence-based finding, limitation, and no unsupported causal claim |
| Communication, M04.4 | A concise stakeholder memo, useful descriptions, underlying values, and a next question |

Adopting instructors choose local grading weights and submission rules. Public [worked feedback](feedback.md) is available for self-study.

## Required independent construction

Construct one labeled plot from development data and supply its numeric table and a noncausal interpretation. Choose and defend its missing-value policy.

Use the [guided construction](guided.md) for a worked example, then reconstruct its central step without copying it. Retain changed code, expected/observed evidence and an explanation. This clarifies companion practice; Canvas remains the authority for assessed submissions.
