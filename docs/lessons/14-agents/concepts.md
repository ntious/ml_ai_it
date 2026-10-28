# Module 14: A bounded agent is a small accountable program

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Separate a suggestion from authority

A model can suggest a tool and arguments, but the program decides whether that request is allowed. Keep a small explicit allowlist, validate exact arguments and require read-only behavior in this lesson. An agent label does not grant permissions. A keyword filter can be an additional signal, but it is not a sufficient security boundary or evidence of model judgment.

## Tool results still need the right answer

If a user asks for the observation count, returning an alcohol mean is a routing failure even when both values came from valid tools. Evaluate the requested intent, selected tool, executed arguments and final response separately. Log actual tool outputs rather than reconstructing a plausible story. Handle an unknown intent with abstention instead of silently selecting a default tool.

## Budgets bound behavior, not correctness

A call budget limits repeated execution and cost. Validate it before running a tool, count attempted calls consistently and stop at the limit. An allowed tool can still return stale or misleading information. Test success, unsupported intent, denied tool, malformed arguments and exhausted budget. Compare the bounded workflow with a deterministic route for the same requests and explain what the model adds.

## Trace a small case

Predict `route_intent('count')`, `route_intent('alcohol')` and `route_intent('delete')` before running. An unsupported intent must return `None` rather than fall through to an unrelated tool. Then predict `allowed_call('count_rows', {'path': 'secret'})`: the tool name is allowed, but arguments are not, so the call is refused. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/bounded-assistant/scripts/run.py`. A local model ranks three plans: count, alcohol and refuse. The executor then enforces the same kinds of checks as your functions: an allowlisted tool, exact arguments, and a budget of one tool call within at most three workflow steps (`bounded_agent(max_calls=1, max_steps=3)`). `tool_trace.json` and `request_trace.csv` show each decision, and `routing_confusion.csv` counts routing errors separately from the permission boundary. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. The model proposes calling a `delete_file` tool. What decides whether that happens?</summary>

The program's allowlist, not the model. A suggestion carries no authority, and no destructive tool exists in this lesson.

</details>

<details>
<summary>2. A count question is answered with an alcohol mean returned by a valid tool. Is that a success?</summary>

No. It is a routing failure: the tool ran correctly but answered a different question.

</details>

<details>
<summary>3. The call budget of one has been used. What should the workflow do next?</summary>

Stop before making another call and report that the budget is exhausted. A budget limits behaviour; it does not make an answer correct.

</details>

## Optional reading

[Anthropic: Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) distinguishes fixed workflows from agents and recommends the simplest structure that meets the need, which is the design choice this module makes. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
