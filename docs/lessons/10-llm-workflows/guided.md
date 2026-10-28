# Module 10: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

A token model chooses continuations. Greedy decoding chooses a highest-scoring next token at each step; it does not guarantee a globally best answer. Valid JSON and correct classification are separate events. On 100 records, one changed outcome moves the observed rate by one percentage point; uncertainty still depends on the sample and its design.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
from practical_ml_ai.language import parse_label
learning_outputs = ['{"label":"ham"}', '{"label":"spam","extra":1}', 'spam']
learning_parsed = [parse_label(value) for value in learning_outputs]
print(learning_parsed)
assert learning_parsed == [0,None,None]
```

## Complete with less support

Inspect matched_comparison.csv after the real run. Reconcile per-record baseline and LLM outcomes and explain preprocessing, prevalence and sample-size limits. Declare any prompt experiment on validation first.


## Debug a plausible misconception

Can 100 percent valid JSON establish a useful classifier? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Compare zero-shot instructions, an explicit example and a structured schema prompt on validation with a fixed budget. Record literature sources and unresolved claims.

## Minimum mastery evidence

Keep the evidence listed in the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) and name the module outcome each item supports. The [criteria](../../study-workflow.md#how-explanations-are-judged) describe developing, meeting and extending the outcome.
