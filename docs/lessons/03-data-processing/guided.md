# Module 3: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

Cleaning is a policy. A row can be unusable for one task and still carry evidence about measurement failure. Reconcile input = accepted + rejected before discussing averages.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
from pathlib import Path
from practical_ml_ai.data.events import prepare_file
import tempfile
learning_root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "pyproject.toml").is_file())
with tempfile.TemporaryDirectory() as learning_tmp:
    learning_cleaned = prepare_file(learning_root / "data/samples/network-events/events.csv", Path(learning_tmp) / "clean")
    print(learning_cleaned.report)
    assert learning_cleaned.report["rows_accepted"] == 6
```

## Complete with less support

Inspect a rejected record and explain its policy reason. On a copy, repair one legitimate error and reconcile the changed counts.


## Debug a plausible misconception

Should a missing latency be replaced by zero? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Write a data contract for records in another discipline, including invalid and missing values.

## Minimum mastery evidence

Keep the evidence listed in the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) and name the module outcome each item supports. The [criteria](../../study-workflow.md#how-explanations-are-judged) describe developing, meeting and extending the outcome.
