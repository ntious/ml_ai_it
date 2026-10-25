# Module 9 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

A vocabulary file and nonzero weight updates confirm actual training, but do not guarantee usefulness. The same final rows support both methods. Public SMS may contain personal details; public access and a license do not remove the need for restraint. Report a baseline win rather than assuming neural NLP must be superior. In the first default run, the neural model predicted no spam: TP 0, FN 30, TN 210, FP 0. Its 87.5% accuracy would conceal zero positive recall and balanced accuracy 0.5. The lexical baseline recovered 6 of 30 positives. This is an explicit failure case for diagnosis, not a deployable filter.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Evidence.** The neural model flagged no spam (TP 0, FN 30 among 240 test messages). Validation loss fell at every epoch (0.428, 0.338, 0.286), and the best epoch was 3, the last allowed. The TF-IDF/logistic baseline flagged 6 messages, all correct (precision 1.00, recall 0.20).

**Likely causes.**

1. **The scores rank, but the threshold hides it.** A model that always predicts the 12.5% spam rate has a cross-entropy of about 0.377. A validation loss of 0.286 is lower, so the network does separate the classes somewhat; its spam probabilities simply stay below 0.5.
2. **Too few updates.** 720 training messages and 3 epochs give about 70 gradient steps. Loss was still falling steeply when training stopped.
3. **The baseline has the same threshold problem.** Perfect precision with low recall means the logistic scores are cautious, not that lexical features are weak.

**A fair diagnostic experiment.** Using validation messages only, compare the probability distributions for spam and ham, then choose one threshold rule for both methods. As a separate declared experiment, run `--epochs 20` in a new output directory. Report recall and precision with their denominators; accuracy (87.5% for predicting nothing) would hide the failure.

## Transfer cautiously

Ticket text requires genuine permitted records, careful author/customer separation, and confidentiality controls. Spam labels do not become ticket categories.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Why is adapting vocabulary on test text leakage?

It lets the final evaluation influence the learned representation, even without using its labels.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
