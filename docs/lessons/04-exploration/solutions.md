# Module 4: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module04/solutions.ipynb "site-download:module04/solutions.ipynb") or open `notebooks/practice/module04-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `error_rate`

A zero denominator is unavailable, not zero percent. For `error_rate(3, 10)`, the expected result is `0.3`.

```python
def error_rate(errors, requests):
    return errors/requests if requests else None
```

## `median`

Average the two middle observations for an even count. For `median([1, 2, 3, 100])`, the expected result is `2.5`.

```python
def median(values):
    ordered = sorted(values)
    n = len(ordered)
    return ordered[n//2] if n%2 else (ordered[n//2-1]+ordered[n//2])/2
```

## `weighted_rate`

Do not average daily percentages with unequal denominators. For `weighted_rate([[1, 2], [1, 8]])`, the expected result is `0.2`.

```python
def weighted_rate(counts):
    denominator = sum(row[1] for row in counts)
    return sum(row[0] for row in counts)/denominator if denominator else None
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Compare request counts and error rates for two services with unequal volume. Write a caption that prevents a misleading ranking. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
