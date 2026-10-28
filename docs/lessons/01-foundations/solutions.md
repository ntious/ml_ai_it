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

## Complete-study results feedback

80 gives `Within the chosen threshold` (80 > 80 is false); 81 and 100 give `Review storage`; 100.5 is rejected with "storage_percent must be a finite number from 0 through 100". The rule decides only valid inputs; the input check runs first and stops impossible percentages. These values come from running the script during the October 28, 2026 review.

## Reasoning task feedback

For example, `[False, False, False]` gives `[0, 1]` (one miss) and `[True, True, False]` gives `[1, 0]` (one false alert); both are 2/3 accurate. The preferred list depends on which error costs more. A missed storage problem can cause an outage, while a false alert costs a review. Accuracy alone cannot express that choice.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Frame an escalation aid with a human fallback. Explain one field unavailable at ticket arrival. A defensible response names the decision time (ticket arrival), the affected stakeholder, the evidence source and the human fallback. It also names a field that only exists after escalation, such as the resolver group.
