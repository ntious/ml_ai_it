# Module 11 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

The core checks actual gradients and numeric replay; it does not replace training with a mocked response. Tiny balanced samples and a short step budget cannot validate generalization. An unchanged/worse final loss is a result to report. Repeatedly changing steps after viewing final loss would invalidate its holdout role.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Evidence.** The adapter has 2,304 trainable parameters and took 8 single-example steps. Validation completion loss moved from 1.9836 to 1.9809, a 0.14% change. Generated accuracy stayed at 0 of 8 for both the base and adapted model, because neither produced the required JSON.

**Likely causes.**

1. **The budget is far too small to change behavior.** Eight steps show only 8 of the 24 training messages, once each, and update one projection in one layer.
2. **Accuracy cannot move until the format does.** The base model fails the schema on every example (as in Module 10), so a tiny loss improvement cannot appear as correct labels.

**A fair diagnostic experiment.** Treat the step budget as the declared variable: run `--steps 48` (the allowed maximum) in a new output directory and compare **validation** completion loss and validation schema validity, not final scores. Predict what a larger adapter on more layers would change. Explain why format compliance is often the first measurable gain from fine-tuning.

## Transfer cautiously

A real organization needs consent/rights, a data-retention policy, versioned adapters, regression evaluation, and rollback. This tiny adaptation is not a production support model.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Does a nonzero adapter update establish better labels?

No. It establishes changed parameters. Lower completion loss also does not establish better generated decisions.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
