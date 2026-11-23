# Foundation bridge for Module 3

You can use this support during the lesson. It is not an entrance requirement.

## Files and folders

The input file is raw evidence; generated outputs belong in `runs/`. A relative path starts from the folder where your command runs. A file-not-found error often means the working folder or filename differs from the instruction.

## Dataframes and types

A dataframe is a table with named columns. Numeric-looking text still needs interpretation: the string `"12"` can be converted to a number, while `"unknown"` cannot. A missing measurement and a measured zero carry different meanings.

```python
import pandas as pd
events = pd.read_csv("data/samples/network-events/events.csv")
print("Column names:", list(events.columns))
print("Number of records:", len(events))
print(events[["event_id", "source"]].head(3).to_string(index=False))
```

This code is an exploration example. The shared preparation function initially reads fields as strings so its conversion and validation policy is explicit.

## Functions and results

```python
from practical_ml_ai.data.events import prepare_file
result = prepare_file("data/samples/network-events/events.csv", "runs/my-first-run")
print(result.report["rows_accepted"])
```

`prepare_file` is a function with input and output paths. It returns a result with cleaned records, rejected records, and a report. The report is a dictionary: square brackets select a named value.

## Where to ask for help

Use the help channel chosen by your instructor, or a project issue for a nonsensitive reproducible problem. Include the command, expected result, actual result/error, and one attempted fix. A plain-text error is more useful than a screenshot alone. Keep sensitive files and credentials private.

[Return to Module 3](index.md).

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
