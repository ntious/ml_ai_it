# Module 10 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

Format-valid and correct are different conditions. A result can be valid JSON with the wrong label or invalid despite containing the word spam. No fallback classifier is credited as LLM success. Eight balanced examples cannot establish reliability, calibration, or deployed class prevalence. The initial fixed prompt/model run produced 0 valid schemas out of 8. The service therefore rejects those outputs. The lesson preserves that failure instead of stripping prose/fences and crediting repaired outputs as model success.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Evidence.** None of the 8 responses matched the required schema: seven repeated the message back inside its `<sms>` wrapper, and one answered an unrelated grammar question. The TF-IDF/logistic baseline was correct on 5 of the same 8 messages. With only 8 examples, a 95% Wilson interval for 0/8 runs from 0 to 0.32, and for 5/8 from 0.31 to 0.86, so this run cannot rank the methods precisely.

**Likely causes.**

1. **A 135-million-parameter model follows instructions weakly.** It continues the pattern it sees, including the tags, instead of obeying the system message.
2. **Free generation is the hardest way to classify.** The strict parser correctly rejects near misses, so every format slip counts as an error.

**A fair diagnostic experiment.** Keep the strict parser, and separately score the two legal answers. Compute the model's log-likelihood of `{"label":"ham"}` and of `{"label":"spam"}` for each message and choose the higher; Module 14 already uses this method to rank plans. Run it on validation messages first. Report schema validity for free generation and accuracy for scoring as separate results, never as one combined success rate. Use more than 8 messages before comparing methods.

## Transfer cautiously

A structured support summary needs actual permitted text, a precise output contract, factual checks, and a human escalation path. Do not present message classification as an implemented summarizer.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Can 100 percent valid JSON establish a useful classifier?

No. Labels may all be wrong; schema validity, correctness, cost and latency are separate evidence.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
