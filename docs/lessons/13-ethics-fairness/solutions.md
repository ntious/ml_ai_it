# Module 13: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module13/solutions.ipynb "site-download:module13/solutions.ipynb") or open `notebooks/practice/module13-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `recall_denominator`

Recall conditions on actual positives, not predictions. For `recall_denominator(8, 2, 11, 30)`, the expected result is `19`.

```python
def recall_denominator(tp, fp, fn, tn):
    return tp+fn
```

## `safe_rate`

Unavailable is not evidence of parity. For `safe_rate(8, 19)`, the expected result is `0.42105263157894735`.

```python
def safe_rate(numerator, denominator):
    return numerator/denominator if denominator else None
```

## `wilson`

State the conditional independent-binomial assumption before interpreting the interval. For `wilson(8, 10)`, the expected result is `[0.49016247153664183, 0.9433178485456247]`.

```python
def wilson(successes, observations):
    from practical_ml_ai.learning import wilson_interval
    return list(wilson_interval(successes,observations))
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Compare two groups with equal rates and unequal counts. Explain why this does not establish equitable outcomes or justify a group ranking. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
