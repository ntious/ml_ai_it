# Module 14: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module14/solutions.ipynb "site-download:module14/solutions.ipynb") or open `notebooks/practice/module14-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `route_intent`

An unsupported intent must not fall through to an unrelated answer. For `route_intent('count')`, the expected result is `'count_rows'`.

```python
def route_intent(intent):
    return {"count":"count_rows","alcohol":"mean_alcohol"}.get(intent)
```

## `allowed_call`

Validate tool and argument contract, not just words in a prompt. For `allowed_call('count_rows', {})`, the expected result is `True`.

```python
def allowed_call(tool, arguments):
    return tool in {"count_rows","mean_alcohol"} and arguments == {}
```

## `can_call`

Stop before exceeding the budget and reject malformed limits. For `can_call(0, 1)`, the expected result is `True`.

```python
def can_call(used, budget):
    return type(used) is int and type(budget) is int and 0 <= used < budget
```

## Reasoning task feedback

"Delete the dataset" has no supported intent: `route_intent('delete')` is `None`, and no destructive tool exists to call. The path request uses an allowed tool with a forbidden argument: `allowed_call('count_rows', {'path': '/etc/passwd'})` is False. The second call exceeds the budget: `can_call(1, 1)` is False. Each boundary is enforced by code outside the model.

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Trace an unsupported destructive request and a valid count question. Identify which control enforces each boundary. A defensible response shows the destructive request refused because no such tool exists and its intent route returns `None`, and the count question passing the argument allowlist and budget. It names which control enforced each boundary. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
