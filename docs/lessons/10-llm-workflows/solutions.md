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

## Complete-study results feedback

In the verified CI run 40697234797 (October 28, 2026), 99 of 100 outputs are schema-valid and 39 are correct: validity 0.99 and end-to-end accuracy 0.39. Dropping the invalid output gives 39/99, about 0.394; here the difference is small, but the rule matters whenever many outputs fail. High validity with low accuracy shows that format compliance and correctness are separate.

## Reasoning task feedback

The parsed labels are `spam`, `None` and `ham`, so `valid_fraction` is 2/3. End-to-end accuracy is 1/3: only the first is correct, and `None` counts as wrong. Dropping the malformed output gives 1/2, which rewards the model for failing to answer.

## Advanced extension feedback: retrieval

In the recorded run (October 28, 2026), validation chose single-word TF-IDF with sublinear term frequency and an abstention threshold of 0.15. On the 12 answerable test questions, recall@3 and MRR were both 1.0: the right runbook ranked first every time. Overall, 14 of 16 test decisions were correct.

Two of the four unanswerable test questions were not refused. "What is the budget approval process for new furniture?" and "How do I train a new machine learning model for sales?" both retrieved the new-employee laptop runbook at similarity 0.247, mainly through the shared word "new". A generator grounded in that passage would give a confident, irrelevant answer. The threshold was chosen on only four unanswerable validation questions, so it is weak evidence about unfamiliar questions. Changing it now would be tuning on the test; a new set of validation questions, including near-miss wording, is the honest next step.

## Judge the explanation

Compare your explanation with the [criteria in the study workflow](../../study-workflow.md#how-explanations-are-judged): passing the visible checks alone is *developing*; a changed case that you predict, implement and explain *meets* the task.

## Transfer feedback

Evaluate three changed message outputs including one malformed response. Explain why structural validity alone cannot justify automation. A defensible response counts the malformed response in the denominator for both validity and accuracy. It explains that a structurally valid label can still be wrong, so automation also needs accuracy, error costs and a fallback for unparseable output.
