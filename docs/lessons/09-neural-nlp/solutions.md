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

## Reasoning task feedback

Tokens are `offer, free, prize, now`, giving IDs `[4, 2, 1, 3]`. Keeping the first three gives `[4, 2, 1]`: `prize` becomes unknown (1) and `now` is truncated. At length 2 the result is `[4, 2]`, and even the marker that an unseen word appeared is gone. The complete study's length of 96 makes truncation rare but not impossible.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Add a message with unseen words and a suspicious suffix beyond the length limit. Explain what the model can and cannot inspect. A defensible response shows unseen words mapping to the unknown ID and the suffix beyond the length limit being truncated, so the model never sees it. It proposes a length or vocabulary-coverage check on validation data, not on the final test.
