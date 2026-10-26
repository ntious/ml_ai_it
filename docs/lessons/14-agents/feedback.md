# Module 14 worked feedback

Compare this with your [practice](practice.md) after attempting it. Exact current results are in the generated report; retain the source hash and versions when comparing runs.

## A reasoned interpretation

The planner really uses a language model, but it is a constrained router rather than free-form autonomous planning. A refusal can be safe yet unhelpful. A legal summary plan can still be semantically wrong. Tests verify hard bounds and actual source evidence rather than manufacturing a perfect success rate.

## What a good explanation contains

State the purpose, observed unit, allowed input, and fitting/selection boundary. Name an actual value or record from the output table, explain its denominator or scale, and state what it cannot establish. Distinguish code correctness, statistical evidence, operational usefulness, and responsible use.

A useful recommendation has this structure: “For [declared task], the recorded workflow produced [actual evidence]. Compared with [relevant alternative], this suggests [limited interpretation]. The unresolved limitation is [specific issue]. Before use, we would [test or decision with an owner].” Fill the brackets from your run; do not invent a favorable score or causal story.

## Diagnose the verified run

**Recorded evidence.** Routing is correct for 22 of 26 authored final requests (84.6%). The model correctly refuses 9 of 10 unsupported requests. The validation-selected scoring rule is `validation_offsets`.

**Inspect actual mistakes.** request_trace.csv includes expected_tool, chosen_tool and correct; routing_confusion.csv exposes which intents are confused. Read a wrong refusal and a wrong permitted operation if present. A one-call limit does not make an irrelevant answer correct.

**Separate control from understanding.** The workflow plans, observes one allowlisted tool result and answers using that evidence. The model cannot add a write/shell/export capability. This permission boundary is enforced independently of whether a destructive request is correctly refused; there is no keyword denylist credited as model intelligence. Test the smaller max_steps budgets and explain why an incomplete workflow must not claim an evidence-backed answer. The authored controls and six validation examples are small; their interval does not estimate real-user reliability.

## Transfer cautiously

A real support assistant needs permitted knowledge sources, explicit authority boundaries, trace retention/privacy, escalation, and independent evaluation of task success.

If GenAI calls a result “accurate,” “fair,” or “safe,” ask for the actual metric, population, decision rule, and supporting evidence. Reject claims not supported by this study. Return to the [lesson](index.md) or [adaptation notes](instructor.md).

## Construction check and misconception feedback

Question: Does a legal JSON plan prove correct understanding?

No. The selected legal tool can be irrelevant to the request. Test semantics separately from permission.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
