# Module 13 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

Historical income is not merit, need, or a justified eligibility outcome. The limited recorded categories are not complete descriptions of identity or social experience. The code reports descriptive disparities and unavailable rates, not causal discrimination or legal compliance. Individual records must not become an eligibility/targeting service.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Evidence.** Female and male recall were close (0.61 and 0.63), but selection rates differed (0.20 and 0.31). Recorded race groups differ greatly in size: the Amer-Indian-Eskimo group has 19 actual positives, and its recall is 8/19 = 0.42.

**Uncertainty changes the reading.** Approximate 95% Wilson intervals for recall are 0.57–0.64 (female), 0.61–0.64 (male), 0.23–0.64 (Amer-Indian-Eskimo), 0.41–0.77 (Other, 15/25) and 0.61–0.64 (White). Small positive-label denominators give wide intervals. Overlap of separate group intervals is not a significance test of their difference and does not establish equality. A comparison needs an interval for the difference or a suitable predeclared test, with sampling and multiple-comparison assumptions stated. These binomial intervals do not account for dependence or historical sampling bias.

**A fair diagnostic experiment.** Recompute one interval yourself with `wilson_interval(8, 19)`. Then write two sentences: one comparison the evidence supports, and one it does not. Explain why a selection-rate gap can exist even when recall is similar, using the different base rates of the historical income label.

## Transfer cautiously

IT AI governance should examine purpose, access, affected groups, proxy inputs, feedback loops, reporting channels, and authority to stop a system.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Does removing protected columns remove bias?

No. Proxies, historical labels, sampling and deployment decisions can preserve or introduce disparities.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.

## Continue the learning route

For feedback on your own functions, use [construction solutions](solutions.md). The results here describe the separate complete reference.
