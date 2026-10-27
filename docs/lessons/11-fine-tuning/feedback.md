# Module 11 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

The core checks actual gradients and numeric replay; it does not replace training with a mocked response. Tiny balanced samples and a short step budget cannot validate generalization. An unchanged/worse final loss is a result to report. Repeatedly changing steps after viewing final loss would invalidate its holdout role.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Recorded evidence.** The selected all-layer adapter has 460,800 trainable parameters. Validation completion loss moves from 1.5358 to 0.0030; validation loss selects step 200 within the 200-step maximum. On 100 balanced final messages, JSON validity changes from 0% to 100%, and label accuracy from 0% to 94%.

**Explain the improvement.** This study updates rank-8 adapters in every query/value layer, rather than eight updates to a single rank-2 projection. More training capacity and examples can change completion behavior. The checkpoint uses validation loss only; the final comparison cannot choose steps. The rank-2 hand construction remains useful for understanding the matrix operation.

**Check what each output establishes.** validation_generation.csv provides development format/label checks; generation_comparison.csv provides the frozen final comparison. Safetensors replay checks serialization, not quality. Valid JSON can still be wrong, the balanced sample changes prevalence, and the interval does not correct historical sampling bias. If the last checkpoint wins, later training behavior is unknown.

## Transfer cautiously

A real organization needs consent/rights, a data-retention policy, versioned adapters, regression evaluation, and rollback. This tiny adaptation is not a production support model.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Does a nonzero adapter update establish better labels?

No. It establishes changed parameters. Lower completion loss also does not establish better generated decisions.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.

## Continue the learning route

For feedback on your own functions, use [construction solutions](solutions.md). The results here describe the separate complete reference.
