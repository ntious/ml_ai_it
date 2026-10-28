# Module 12: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module12/solutions.ipynb "site-download:module12/solutions.ipynb") or open `notebooks/practice/module12-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `valid_request`

Booleans are not numerical measurements in this contract; reject extras. For `valid_request({'x': 2}, ['x'])`, the expected result is `True`.

```python
def valid_request(record, expected):
    import math
    return set(record)==set(expected) and all(type(record[k]) in [int,float] and math.isfinite(record[k]) for k in expected)
```

## `shift_score`

Use the fixed training scale, not a scale fitted on new requests. For `shift_score(12, 10, 2)`, the expected result is `1`.

```python
def shift_score(current_mean, training_mean, training_scale):
    return abs(current_mean-training_mean)/training_scale if training_scale>0 else None
```

## `nearest_rank`

Name the percentile convention and retain the tail request. For `nearest_rank([1, 2, 3, 100], 0.95)`, the expected result is `100`.

```python
def nearest_rank(values, percentile):
    import math
    return sorted(values)[math.ceil(percentile*len(values))-1]
```

## Reasoning task feedback

The 95th percentile is the value at position ceil(0.95 × 4) = 4, which is 0.250 s, while the mean is about 0.071 s and hides the slow request. Below 20 requests, ceil(0.95 × n) equals n, so the 95th percentile is the maximum. With 20 requests it is the second largest. Report the sample count with any percentile.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Write a service response policy for an invalid request, a model outage and an alert without outcome labels. A defensible response rejects the invalid request with a reason, routes outages to the human fallback, and treats an input-shift alert as an investigation until delayed labels arrive. It names the owner and the rollback trigger.
