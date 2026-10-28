# Module 3: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module03/solutions.ipynb "site-download:module03/solutions.ipynb") or open `notebooks/practice/module03-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

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

## Complete-study results feedback

12 input rows reconcile as 6 accepted plus 6 rejected. The accepted latencies are 12, 18, 25, 45 and 20 ms, plus one missing value, which must be left out rather than counted as 0. The mean of the five observed values is 24 ms and the median is 20 ms, matching the report. These values come from the fixture run during the October 28, 2026 review.

## Reasoning task feedback

For example, `{'event_id': 'a', 'v': 1}` and `{'event_id': 'a', 'v': 2}`: the rows differ, so whole-row deduplication keeps both, but there is one identity. With one accepted and one duplicate, `reconcile(2, 1, 0, 1)` is True. The complete script treats this pair as conflicting and rejects both, because it cannot tell which value is correct. State which policy you chose and why.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Add a repeated event with a changed annotation and a missing latency. Explain the retained record and reconciliation. A defensible response keeps the first record for the repeated `event_id` under the practice policy, or explains the complete script's conflict rejection. It keeps the missing latency as missing rather than zero, and shows input rows = accepted + rejected + duplicates.
