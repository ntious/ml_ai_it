# Module 1: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module01/solutions.ipynb "site-download:module01/solutions.ipynb") or open `notebooks/practice/module01-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `route`

Use an inclusive boundary; do not return the priority itself. For `route(2)`, the expected result is `False`.

```python
def route(priority, threshold=3):
    return priority >= threshold
```

## `partition_role`

The final test must not choose a model. For `partition_role('train')`, the expected result is `'fit'`.

```python
def partition_role(name):
    return {"train":"fit","validation":"choose","test":"evaluate"}[name]
```

## `error_counts`

Count errors by their consequences, not only total accuracy. For `error_counts([False, True, True], [True, False, True])`, the expected result is `[1, 1]`.

```python
def error_counts(actual, predicted):
    return [sum((not a) and p for a,p in zip(actual,predicted)), sum(a and not p for a,p in zip(actual,predicted))]
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Frame an escalation aid with a human fallback. Explain one field unavailable at ticket arrival. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
