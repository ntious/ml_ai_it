# Module 10 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

Compare the current run below with the [archived under-trained/failed baseline](../../maintenance/reviews/framework-baseline-0.7.0.md). The archive records earlier settings; it is not the current protocol. A working mechanism and a useful task model require different evidence.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Recorded evidence.** On 100 matched final messages, free generation produces valid JSON 99% of the time but correct labels only 39% of the time. Candidate likelihood with a validation-selected threshold of 0.85 has accuracy 85%. The lexical baseline reaches 97%, while always predicting the training-majority label reaches 88%.

**Explain the difference.** Few-shot examples can improve output format without fixing semantic classification. Candidate scoring returns a legal label by construction; that is not evidence of learned JSON compliance. Read confusion_counts.csv before declaring an accuracy improvement useful: a classifier can recover spam while scoring below majority accuracy. The selected relative likelihood score is not calibrated confidence.

**Check uncertainty.** Read the successes, observations and Wilson intervals in rate_intervals.csv. These are intervals for individual rates, not a paired significance test of method differences. Use llm_validation_predictions.csv to investigate errors; do not choose a prompt from final-test outcomes.

## Transfer cautiously

A structured support summary needs actual permitted text, a precise output contract, factual checks, and a human escalation path. Do not present message classification as an implemented summarizer.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Can 100 percent valid JSON establish a useful classifier?

No. Labels may all be wrong; schema validity, correctness, cost and latency are separate evidence.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.

## Continue the learning route

For feedback on your own functions, use [construction solutions](solutions.md). The results here describe the separate complete reference.
