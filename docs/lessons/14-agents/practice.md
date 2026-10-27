# Module 14: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module14/practice.ipynb "site-download:module14/practice.ipynb"). In a source checkout open `notebooks/practice/module14-practice.ipynb`. Use the module’s existing environment. Three unfinished functions report **not_attempted**, not a pass.

## Construct `route_intent`

Return count_rows for count, mean_alcohol for alcohol; otherwise None. Predict the result on `['count']`, implement it and call `m14_route_intent` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for route_intent</summary>

An unsupported intent must not fall through to an unrelated answer.

</details>

## Construct `allowed_call`

Allow only count_rows with no arguments, or mean_alcohol with no arguments. Predict the result on `['count_rows', {}]`, implement it and call `m14_allowed_call` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for allowed_call</summary>

Validate tool and argument contract, not just words in a prompt.

</details>

## Construct `can_call`

Return True for nonnegative whole-number used/budget and used < budget; reject bool. Predict the result on `[0, 1]`, implement it and call `m14_can_call` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for can_call</summary>

Stop before exceeding the budget and reject malformed limits.

</details>

## Transfer to an IT decision

Trace an unsupported destructive request and a valid count question. Identify which control enforces each boundary. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M14.1:** Distinguish a fixed workflow, constrained LLM routing, and autonomous planning.
- **M14.2:** Define tool/argument schemas and a bounded execution budget.
- **M14.3:** Run actual model-based plan ranking against real dataset tools.
- **M14.4:** Inspect traces for intent match, refusals, and source-grounded answers.
- **M14.5:** Test unsupported/destructive requests and explain remaining limitations.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.
