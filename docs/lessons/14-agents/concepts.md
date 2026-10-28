# Module 14: A bounded agent is a small accountable program

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Separate a suggestion from authority

A model can suggest a tool and arguments, but the program decides whether that request is allowed. Keep a small explicit allowlist, validate exact arguments and require read-only behavior in this lesson. An agent label does not grant permissions. A keyword filter can be an additional signal, but it is not a sufficient security boundary or evidence of model judgment.

## Tool results still need the right answer

If a user asks for the observation count, returning an alcohol mean is a routing failure even when both values came from valid tools. Evaluate the requested intent, selected tool, executed arguments and final response separately. Log actual tool outputs rather than reconstructing a plausible story. Handle an unknown intent with abstention instead of silently selecting a default tool.

## Budgets bound behavior, not correctness

A call budget limits repeated execution and cost. Validate it before running a tool, count attempted calls consistently and stop at the limit. An allowed tool can still return stale or misleading information. Test success, unsupported intent, denied tool, malformed arguments and exhausted budget. Compare the bounded workflow with a deterministic route for the same requests and explain what the model adds.

## Trace a small case

The first operation is **route_intent**: Return count_rows for count, mean_alcohol for alcohol; otherwise None. On authored arguments `route_intent('count')`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/bounded-assistant/scripts/run.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Further reading: agents](https://www.anthropic.com/engineering/building-effective-agents) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
