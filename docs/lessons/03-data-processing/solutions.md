# Module 3: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module03/solutions.ipynb "site-download:module03/solutions.ipynb") or open `notebooks/practice/module03-solutions.ipynb` in the complete source tree.

## `parse_latency`

Preserve measured zero and missingness separately. For `parse_latency('')`, the expected result is `None`.

```python
def parse_latency(value):
    if value is None or value == "":
        return None
    number = float(value)
    if number < 0:
        raise ValueError("negative latency")
    return number
```

## `deduplicate`

Deduplicate by identity, not the entire row. For `deduplicate([{'event_id': 'a', 'v': 1}, {'event_id': 'a', 'v': 2}, {'event_id': 'b', 'v': 3}])`, the expected result is `[{'event_id': 'a', 'v': 1}, {'event_id': 'b', 'v': 3}]`.

```python
def deduplicate(records):
    seen = set()
    kept = []
    for row in records:
        if row["event_id"] not in seen:
            kept.append(row)
            seen.add(row["event_id"])
    return kept
```

## `reconcile`

Every source row needs one accounted-for outcome. For `reconcile(10, 7, 2, 1)`, the expected result is `True`.

```python
def reconcile(input_rows, accepted, rejected, duplicates):
    return all(x >= 0 for x in [input_rows,accepted,rejected,duplicates]) and input_rows == accepted+rejected+duplicates
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Add a repeated event with a changed annotation and a missing latency. Explain the retained record and reconciliation. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
