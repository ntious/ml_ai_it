# Module 14: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module14/practice.ipynb "site-download:module14/practice.ipynb"). In a source checkout open `notebooks/practice/module14-practice.ipynb`. Use the [framework environment and kernel](../../setup/frameworks.md). Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `route_intent`

Return count_rows for count, mean_alcohol for alcohol; otherwise None. Predict the result on `route_intent('count')`, implement it and call `m14_route_intent` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for route_intent</summary>

An unsupported intent must not fall through to an unrelated answer.

</details>

## Construct `allowed_call`

Allow only count_rows with no arguments, or mean_alcohol with no arguments. Predict the result on `allowed_call('count_rows', {})`, implement it and call `m14_allowed_call` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for allowed_call</summary>

Validate tool and argument contract, not just words in a prompt.

</details>

## Construct `can_call`

Return True for nonnegative whole-number used/budget and used < budget; reject bool. Predict the result on `can_call(0, 1)`, implement it and call `m14_can_call` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for can_call</summary>

Stop before exceeding the budget and reject malformed limits.

</details>

## Work with the complete study's results

Open `routing_confusion.csv` from the complete study. Compute routing accuracy over the 26 test requests and the share of refusal requests that were refused. Which kind of mistake is most common, and which control limits its consequences? Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

For each request, name the control that stops it and the function call that shows it: "delete the dataset", "count the rows in /etc/passwd", and a second tool call after the first has been used with a budget of 1. The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Trace an unsupported destructive request and a valid count question. Identify which control enforces each boundary. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Evidence and feedback

- **M14.1:** Distinguish a fixed workflow, constrained LLM routing, and autonomous planning.
- **M14.2:** Define tool/argument schemas and a bounded execution budget.
- **M14.3:** Run actual model-based plan ranking against real dataset tools.
- **M14.4:** Inspect traces for intent match, refusals, and source-grounded answers.
- **M14.5:** Test unsupported/destructive requests and explain remaining limitations.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.
