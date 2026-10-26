# Module 8 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

The code checks that weights changed and that saved/reloaded predictions match. Neither check proves useful accuracy. A small imbalanced dataset can yield a neural model that misses most positives; report that honestly. Training/validation loss differences invite investigation, not automatic test-based retuning.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Evidence.** The [verified run](../../status.md#verified-results) found 7 of 29 higher-rated wines (recall 0.24, balanced accuracy 0.593). Logistic regression on the same rows at the same 0.5 threshold found 9 of 29 (balanced accuracy 0.629). The best validation epoch was 8, the last allowed: validation loss was still falling (0.3111 at epoch 6, 0.3021 at epoch 8).

**Likely causes.**

1. **The threshold, not only the model.** Only about 12% of wines are positive, so most predicted probabilities sit below 0.5. Module 6 chose 0.3 on validation for the same label and reached balanced accuracy 0.757. Comparing a 0.5 network with a 0.3 logistic model would mix up two separate decisions.
2. **The search ended at its boundary.** Validation loss selected epoch 8 from the eight observed checkpoints. Because the best checkpoint is also the final epoch, a larger budget might find a better checkpoint, but this run cannot establish what happens later. Longer training need not produce a visible rise in validation loss.

**A fair diagnostic experiment.** On validation only, list the predicted probabilities for actual positives and choose a threshold with the rule Module 6 uses. Separately, declare a larger epoch budget (for example `--epochs 30`) in a new output directory and find the epoch where validation loss is lowest. Change one factor at a time, and record both results before you look at final-test counts again. The public final results are already known, so treat any rerun as rehearsal.

## Transfer cautiously

For IT telemetry, preserve host/time boundaries and final-test discipline before replacing numeric inputs. More layers do not replace data-quality or availability checks.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Can the lowest training-loss epoch be the wrong checkpoint?

Yes. Training fit can improve while validation degrades. Selection uses validation under the declared rule.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
