# Module 2: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before the complete [walkthrough](index.md). Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

A function can return a computed value for reuse. File fields may be strings even when they look numeric. Validate before aggregation; an absent duration is not a measured zero.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
from pathlib import Path
import csv
learning_root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "pyproject.toml").is_file())
with (learning_root / "data/samples/service-files/tickets.csv").open(newline="", encoding="utf-8") as stream:
    learning_rows = list(csv.DictReader(stream))
def measured_total(rows):
    values = [int(row["minutes"]) for row in rows]
    if any(value < 0 for value in values):
        raise ValueError("Negative duration")
    return sum(values)
print(measured_total(learning_rows))
assert measured_total(learning_rows) == 60
```

## Complete with less support

Write an explicit loop version independently. Add one record on a copy and reconcile both totals. Demonstrate one rejected value.

Cover the worked code, implement the central step again, and explain its inputs, outputs and boundary. Keep development experiments separate from final evaluation. Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design.

## Debug a plausible misconception

Why does replacing unknown with zero change the question? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Summarize a different small CSV with named units and a documented validation policy.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
