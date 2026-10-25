# Module 10 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

Format-valid and correct are different conditions. A result can be valid JSON with the wrong label or invalid despite containing the word spam. No fallback classifier is credited as LLM success. Eight balanced examples cannot establish reliability, calibration, or deployed class prevalence. The initial fixed prompt/model run produced 0 valid schemas out of 8. The service therefore rejects those outputs. The lesson preserves that failure instead of stripping prose/fences and crediting repaired outputs as model success.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Transfer cautiously

A structured support summary needs actual permitted text, a precise output contract, factual checks, and a human escalation path. Do not present message classification as an implemented summarizer.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).
