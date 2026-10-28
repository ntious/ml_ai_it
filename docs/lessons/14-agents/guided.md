# Module 14: guided construction and mastery

Use this after the [foundation bridge](foundation.md) and before attempting independent practice; return to the [module run instructions](index.md) afterward. Read, predict, run, change, and explain. The shared runner remains the complete reference; these small steps expose its ideas.

## Worked concept

The model ranks three permitted plans. The policy and exact schema are enforced by code; the model does not grant itself permissions. A request may still be routed to the wrong legal operation. This bounded router has no general planning or memory implementation.

## Predict and construct

Predict the printed values, shape or rejection before running. Use the documented environment. The notebook contains this same runnable construction cell.

```python
from practical_ml_ai.continuation_data import wine_splits
from practical_ml_ai.language import execute_tool
learning_split,learning_features,_ = wine_splits()
print(execute_tool({"tool":"summary","arguments":{}},learning_split["train"],learning_features))
try:
    execute_tool({"tool":"shell","arguments":{}},learning_split["train"],learning_features)
except ValueError as learning_error:
    print("Expected rejection:",learning_error)
else:
    raise AssertionError("Unknown tool must be rejected")
```

## Complete with less support

Trace legitimate, unsupported and adversarial requests. Verify returned values and separately score intent match, schema validity, policy validity and evidence correctness.


## Debug a plausible misconception

Does a legal JSON plan prove correct understanding? Write a prediction before opening [feedback](feedback.md). Include a counterexample or calculation, not only a definition.

## Independent transfer

Compare this router with an agent framework model/tool loop: identify where state, planning, tool execution, observations and stopping live. Do not claim this example implements every framework feature.

## Minimum mastery evidence

Submit or retain your changed executable code, one independently checked numerical claim, expected versus observed output, one diagnosed failure and a short decision/limitation explanation. Name the module outcomes each artifact supports. Interpretation-only work can demonstrate reasoning, but implementation outcomes require an executed and explained modification. A screenshot or copied report alone is insufficient.

Developing: expected report reproduced but the central operation cannot be explained or changed. Meets: an independently explained change, reconciled evidence and preserved evaluation boundary. Extends: a predeclared experiment or transfer with measured tradeoffs; extra complexity alone is insufficient.
