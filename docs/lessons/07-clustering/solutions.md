# Module 7: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module07/solutions.ipynb "site-download:module07/solutions.ipynb") or open `notebooks/practice/module07-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `squared_distance`

Square coordinate differences; do not compare signed sums. For `squared_distance([2, 4], [1, 2])`, the expected result is `5`.

```python
def squared_distance(point, center):
    return sum((a-b)**2 for a,b in zip(point,center))
```

## `select_k`

Use validation geometry and a declared tie-break, not smallest inertia. For `select_k([[2, 0.4], [3, 0.5], [4, 0.45]])`, the expected result is `3`.

```python
def select_k(candidates):
    return min(candidates, key=lambda row:(-row[1],row[0]))[0]
```

## `profile`

Describe both support and feature level; IDs have no rank. For `profile([2, 4, 10], [0, 0, 1])`, the expected result is `{'0': {'count': 2, 'mean': 3}, '1': {'count': 1, 'mean': 10}}`.

```python
def profile(values, labels):
    result = {}
    for label in sorted(set(labels)):
        subset = [v for v,k in zip(values,labels) if k == label]
        result[str(label)] = {"count":len(subset),"mean":sum(subset)/len(subset)}
    return result
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Cluster service workload profiles on development data. State why a cluster alone cannot authorize throttling a service. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
