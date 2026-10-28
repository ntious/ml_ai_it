# Module 11: construction feedback

Try [practice](practice.md) before reading the worked notebook. [Download solutions](https://ntious.github.io/ml_ai_it/downloads/module11/solutions.ipynb "site-download:module11/solutions.ipynb") or open `notebooks/practice/module11-solutions.ipynb` in the complete source tree.

## `trainable_count`

Count scalars in trainable tensors, not the number of tensors. For `trainable_count([[100, False], [8, True], [2, True]])`, the expected result is `10`.

```python
def trainable_count(parameters):
    return sum(size for size,trainable in parameters if trainable)
```

## `completion_labels`

Mask both prompt and padding, while retaining completion tokens. For `completion_labels([5, 6, 7, 0], 2, [1, 1, 1, 0])`, the expected result is `[-100, -100, 7, -100]`.

```python
def completion_labels(ids, prompt_length, attention_mask):
    return [token if i>=prompt_length and attention_mask[i] else -100 for i,token in enumerate(ids)]
```

## `changed_tensors`

Demonstrate an actual parameter change; a new loss string is insufficient. For `changed_tensors([[1, 2], [3]], [[1, 2], [4]])`, the expected result is `[1]`.

```python
def changed_tensors(before, after):
    return [i for i,(a,b) in enumerate(zip(before,after)) if a != b]
```

## Judge the explanation

**Developing:** the visible case passes, but the explanation does not identify its denominator, boundary or contract. **Meets the task:** a changed case is predicted correctly, implemented and linked to a specific module artifact. **Extends:** the learner identifies where the operation is insufficient for the IT transfer case and proposes an investigation using development evidence.

## Transfer feedback

Explain a run where adapter weights change but held-out validity does not. Propose a development-only investigation. A defensible response names a decision time, affected stakeholder, evidence source and human fallback. A changed narrative alone is insufficient: retain changed inputs/code and observed outputs. Follow the [research comparison guide](../../advanced/research-comparison.md) when making a claim from published work.
