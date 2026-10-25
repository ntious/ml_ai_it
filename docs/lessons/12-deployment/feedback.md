# Module 12 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

The replay uses real measurements and measured durations, not invented telemetry. It explicitly labels the offline batch order. AppTest interactions and HTTP health cover software behavior; the [accessibility guide](../../accessibility/index.md) records human interface-review scope. Operational suitability needs task-specific evidence. An uncalibrated probability is not guaranteed confidence.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Evidence.** Across four batches of about 61 held-out records, recall ranged from 0.40 to 0.73, and batch 3 had a selection rate of 0.41 compared with 0.10–0.16 for the others. The largest standardized input-mean shift was 0.69 standard deviations, also in batch 3.

**Likely causes.**

1. **Different numbers of positives per batch.** From the confusion counts, the batches contain about 5, 6, 15 and 3 higher-rated wines. With 3–6 positives, one record changes recall by 0.17–0.33.
2. **Record order is not time.** Batches follow the source file's order, which can group similar wines. The shift is real for these batches, but it is not evidence of drift over time.

**A fair diagnostic experiment.** Before setting an alert, compute a 95% Wilson interval for each batch's recall (`practical_ml_ai.learning.wilson_interval`). Write an alert rule that needs a minimum number of labeled positives. Then explain which of the four batches would trigger it and why.

## Transfer cautiously

Before real IT deployment, add suitable access controls, data governance, observability, failure recovery, and prospectively measured service objectives.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Does an input mean shift prove concept drift?

No. It signals distribution differences; changing outcome relationships requires additional evidence.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
