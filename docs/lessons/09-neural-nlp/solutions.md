# Module 9: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module09/solutions.ipynb "site-download:module09/solutions.ipynb") or open `notebooks/practice/module09-solutions.ipynb` in the complete source tree. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## `vocabulary`

Fit only training text and reserve unknown/padding separately. For `vocabulary(['FREE offer', 'offer now'])`, the expected result is `{'free': 2, 'now': 3, 'offer': 4}`.

```python
def vocabulary(training_texts):
    tokens = sorted({token for text in training_texts for token in text.lower().split()})
    return {word:i+2 for i,word in enumerate(tokens)}
```

## `encode`

Unknown is not padding; declare truncation direction. For `encode('NEW offer', {'offer': 2}, 4)`, the expected result is `[1, 2, 0, 0]`.

```python
def encode(text, vocabulary, length):
    ids = [vocabulary.get(token,1) for token in text.lower().split()][:length]
    return ids + [0]*(length-len(ids))
```

## `recall`

Use actual positives, not total messages or predicted positives. For `recall(0, 10)`, the expected result is `0`.

```python
def recall(tp, fn):
    return tp/(tp+fn) if tp+fn else None
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Add a message with unseen words and a suspicious suffix beyond the length limit. Explain what the model can and cannot inspect. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
