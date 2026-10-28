# Module 2: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module02/solutions.ipynb "site-download:module02/solutions.ipynb") or open `notebooks/practice/module02-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `status_counts`

Initialize unseen statuses and handle an empty file. For `status_counts([{'status': 'open'}, {'status': 'closed'}, {'status': 'open'}])`, the expected result is `{'open': 2, 'closed': 1}`.

```python
def status_counts(records):
    counts = {}
    for row in records:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return counts
```

## `observed_mean`

Missing is not zero; zero is still observed. For `observed_mean([10, None, 20])`, the expected result is `15`.

```python
def observed_mean(values):
    observed = [x for x in values if x is not None]
    return sum(observed)/len(observed) if observed else None
```

## `output_path`

Join root, runs, the run name and summary.json; keep outputs separate from source files. For `output_path('course', 'trial-2')`, the expected result is `'course/runs/trial-2/summary.json'`.

```python
def output_path(root, run_name):
    from pathlib import Path
    return (Path(root)/"runs"/run_name/"summary.json").as_posix()
```

## Reasoning task feedback

The first is 0: one value was observed and it was zero. The second is `None`: nothing was observed. Printing 0 for the second would claim a measured average of zero minutes. A good report prints "no observed values" instead and keeps the count of observations beside every mean.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Summarize ticket status with an unknown status added. Explain which output changes and which source remains unchanged. A defensible response shows the unknown status appearing as its own key with count 1, all other counts unchanged and `tickets.csv` untouched. The new summary goes to a new run folder, so the original result stays comparable.
