# From Python Foundation to ML workflows

First complete the relevant [Python Foundation](https://ntious.github.io/python_foundation/) lessons. This bridge adds skills the introductory course intentionally does not require. Allow additional guided practice; completing the introductory course alone does not establish dataframe or file-I/O mastery.

## Records and collections

```python
record = {"category": "network", "minutes": 15}
records = [record, {"category": "software", "minutes": 20}]
print(record["minutes"])
print(sum(item["minutes"] for item in records))
```

Predict 15 and 35 before running. A dictionary describes one record; the list contains two records. The generator supplies each duration to sum. Rewrite it as the explicit loop you learned in Foundation. Then add a third record and predict the new total.

## Imports, folders and files

Use [workspace setup](student-workspace.md) first. Run from the folder containing this repository's README, pyproject.toml and data folder.

```python
from pathlib import Path
import csv
import json
root = Path.cwd()
print("Working folder:", root)
path = root / "data/samples/service-files/tickets.csv"
with path.open(newline="", encoding="utf-8") as stream:
    tickets = list(csv.DictReader(stream))
minutes = [int(row["minutes"]) for row in tickets]
print(len(tickets), sum(minutes))
output = root / "runs/bridge"
output.mkdir(parents=True, exist_ok=True)
(output / "summary.json").write_text(json.dumps({"minutes": sum(minutes)}), encoding="utf-8")
```

Expect four rows and 60 minutes. CSV fields arrive as text; int converts them before arithmetic. A with block closes the file even if processing fails. pathlib and csv are standard-library modules; pandas is installed separately. FileNotFoundError suggests inspecting the working folder first, not reinstalling Python.

## Dataframes and packages

After the core installation in [first run](../../QUICKSTART.md):

```python
import pandas as pd
frame = pd.read_csv(path)
print(frame[["category", "minutes"]].head())
print(frame.groupby("category")["minutes"].sum())
```

A dataframe is a table; selecting a column returns a series. Grouping collects rows by a key before aggregation. Compare the grand total with your standard-library result. A table library reduces repeated code, but does not choose the right unit or missing-value policy for you.

## Independent completion check

On a copy, add a valid ticket and reconcile the total in both implementations. Replace one duration with unknown; explain the conversion error and choose a visible validation policy. Do not silently substitute zero. Save your modified code, input copy, expected total, observed total and one error explanation. You are ready for Module 2 when you can repeat this with changed records and explain the imports and paths without the completed example.
