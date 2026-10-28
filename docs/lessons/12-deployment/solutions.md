# Module 12: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module12/solutions.ipynb "site-download:module12/solutions.ipynb") or open `notebooks/practice/module12-solutions.ipynb` in the complete source tree.

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

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Write a service response policy for an invalid request, a model outage and an alert without outcome labels. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
