# Module 10: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before the complete [walkthrough](index.md). Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

A token model chooses continuations. Greedy decoding chooses a highest-scoring next token at each step; it does not guarantee a globally best answer. Valid JSON and correct classification are separate events. On eight records, one changed outcome moves the observed rate by 12.5 percentage points.

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

Cover the worked code, implement the central step again, and explain its inputs, outputs and boundary. Keep development experiments separate from final evaluation. Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design.

## Debug a plausible misconception

Can 100 percent valid JSON establish a useful classifier? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Compare zero-shot instructions, an explicit example and a structured schema prompt on validation with a fixed budget. Record literature sources and unresolved claims.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
