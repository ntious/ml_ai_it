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

## Complete-study results feedback

There are 23 observed values and their median is 34.0 ms, matching `summary.txt`. The mean (38.7 ms) is higher because a few high-latency days pull it up, while the median depends only on the middle value. These values come from the fixture run during the October 28, 2026 review.

## Reasoning task feedback

For example, `[[1, 2], [1, 8]]` gives daily rates 0.5 and 0.125, whose average is 0.3125, but `weighted_rate` is 2/10 = 0.2. The weighted rate answers the question about all requests. The plain average gives a two-request day the same weight as an eight-request day.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Compare request counts and error rates for two services with unequal volume. Write a caption that prevents a misleading ranking. A defensible response reports counts beside rates, uses the weighted rate for each service, and captions the chart so a high rate on a low-volume service is not read as a ranking.
