# Module 2: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module02/solutions.ipynb "site-download:module02/solutions.ipynb") or open `notebooks/practice/module02-solutions.ipynb` in the complete source tree.

## `status_counts`

Initialize unseen statuses and handle an empty file. For `[[{'status': 'open'}, {'status': 'closed'}, {'status': 'open'}]]`, the expected result is `{'open': 2, 'closed': 1}`.

```python
def status_counts(records):
    counts = {}
    for row in records:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return counts
```

## `observed_mean`

Missing is not zero; zero is still observed. For `[[10, None, 20]]`, the expected result is `15`.

```python
def observed_mean(values):
    observed = [x for x in values if x is not None]
    return sum(observed)/len(observed) if observed else None
```

## `output_path`

Keep run names separate from the source file. For `['course', 'trial-2']`, the expected result is `'course/runs/trial-2/summary.json'`.

```python
def output_path(root, run_name):
    from pathlib import Path
    return (Path(root)/"runs"/run_name/"summary.json").as_posix()
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Summarize ticket status with an unknown status added. Explain which output changes and which source remains unchanged. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
