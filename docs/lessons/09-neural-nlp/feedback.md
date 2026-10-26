# Module 9 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

Compare the current run below with the [archived under-trained/failed baseline](../../maintenance/reviews/framework-baseline-0.7.0.md). The archive records earlier settings; it is not the current protocol. A working mechanism and a useful task model require different evidence.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Recorded evidence.** Of 128 actual positives among 1032 final records, the network finds 118 and misses 10, with 30 false alarms. Its recall is 0.922, precision 0.797 and balanced accuracy 0.944. The simpler baseline has recall 0.906, precision 0.899 and balanced accuracy 0.946.

**Explain the decision.** Validation loss selected checkpoint 7 within a 25-epoch maximum. Validation balanced accuracy selected thresholds 0.15 (neural) and 0.50 (baseline). Recall alone hides the false-alarm cost; compare both confusion tables and the threshold-free ranking metrics. Neither the baseline nor the neural model is required to win.

**Try a validation-only investigation.** Read validation_predictions.csv and validation_thresholds.csv. Explain one threshold tradeoff without changing a setting in response to final-test scores. For an imbalanced dataset, why would accuracy alone be misleading?

## Transfer cautiously

Ticket text requires genuine permitted records, careful author/customer separation, and confidentiality controls. Spam labels do not become ticket categories.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Why is adapting vocabulary on test text leakage?

It lets the final evaluation influence the learned representation, even without using its labels.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
