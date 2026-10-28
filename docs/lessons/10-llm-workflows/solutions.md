# Module 10: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module10/solutions.ipynb "site-download:module10/solutions.ipynb") or open `notebooks/practice/module10-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `parse_label`

Reject prose and extra keys; parsing is separate from correctness. For `parse_label('{"label":"spam"}')`, the expected result is `'spam'`.

```python
def parse_label(text):
    import json
    try:
        value = json.loads(text)
    except (ValueError,TypeError):
        return None
    return value["label"] if isinstance(value,dict) and set(value)=={"label"} and value["label"] in ["ham","spam"] else None
```

## `valid_fraction`

Count malformed outputs in the denominator. For `valid_fraction(['spam', None, 'ham'])`, the expected result is `0.6666666666666666`.

```python
def valid_fraction(labels):
    return sum(x in ["ham","spam"] for x in labels)/len(labels) if labels else None
```

## `end_to_end_accuracy`

Do not condition accuracy on the outputs the parser accepted. For `end_to_end_accuracy(['spam', 'ham'], ['spam', None])`, the expected result is `0.5`.

```python
def end_to_end_accuracy(actual, parsed):
    return sum(a==p for a,p in zip(actual,parsed))/len(actual) if actual else None
```

## Reasoning task feedback

The parsed labels are `spam`, `None` and `ham`, so `valid_fraction` is 2/3. End-to-end accuracy is 1/3: only the first is correct, and `None` counts as wrong. Dropping the malformed output gives 1/2, which rewards the model for failing to answer.

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Evaluate three changed message outputs including one malformed response. Explain why structural validity alone cannot justify automation. A defensible response counts the malformed response in the denominator for both validity and accuracy. It explains that a structurally valid label can still be wrong, so automation also needs accuracy, error costs and a fallback for unparseable output. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
