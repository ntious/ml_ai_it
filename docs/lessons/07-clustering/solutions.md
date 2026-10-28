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

## Reasoning task feedback

Inertia sums squared distances to the nearest centre. Adding centres can only shorten those distances for an optimal solution, so inertia generally falls as K grows and "smallest inertia" picks the largest candidate. The validation silhouette can peak at a small K, as in the recorded study, where K = 2 scored 0.206. Choose K by a declared criterion, not by inertia.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Cluster service workload profiles on development data. State why a cluster alone cannot authorize throttling a service. A defensible response describes each cluster by size and original-unit profile, and notes that a cluster ID has no rank. Throttling a service needs an owner, a defined outcome and evidence about consequences; cluster membership alone is not that evidence.
