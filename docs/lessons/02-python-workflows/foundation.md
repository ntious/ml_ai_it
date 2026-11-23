# Module 2 foundation bridge: from values to files

Use this short bridge before the [complete workflow](index.md). You can read every example as text or execute it in the supplied notebook. Predict each result first.

## Values and containers

```python
minutes = 15                 # integer
category = "network"         # string
needs_review = minutes > 10  # Boolean: True
record = {"category": category, "minutes": minutes}  # dictionary
records = [record, {"category": "software", "minutes": 20}]  # list
```

A list keeps a sequence of items. A dictionary associates a key with a value. `record["minutes"]` retrieves 15. The string `"15"` and integer `15` are different types; file input often needs conversion before arithmetic.

## A loop, condition, and function

```python
def total_minutes(records):
    total = 0
    for record in records:
        if record["minutes"] >= 0:
            total += record["minutes"]
    return total

print(total_minutes(records))  # 35
```

Indentation defines the function, loop, and conditional bodies. `return` supplies a value to the caller; `print` displays text. This small example skips negative values. The complete workflow instead rejects invalid records with an error so that missing work is visible. Validation policy is part of the program's meaning.

## Imports and paths

```python
from pathlib import Path
input_path = Path("data") / "samples" / "service-files" / "tickets.csv"
print(input_path.exists())
```

`pathlib` is a standard-library module. `/` joins path components here; it is not division when used between a `Path` and text. A relative path starts at the current working folder, not necessarily the folder containing a script. Run the lesson command from the repository root, where `README.md` and `data` are visible. A result of `False` means inspect your working folder and path before assuming the file disappeared.

## Errors are evidence

`int("unknown")` raises `ValueError`: that text cannot be converted to an integer. A direct Python call usually displays a traceback showing the call chain, ending with the exception type and message. Read the last line first, then locate the relevant line in your own code. The lesson CLI catches common errors and prints a shorter message, for example `Ticket CSV line 2: minutes must be a nonnegative whole number.` A short CLI error is not a full traceback.

Do not paste an unfamiliar command into a terminal merely because an assistant suggests it. For this lesson, inspect file paths, the CSV header, and the failing value. A small synthetic copy of the input makes a safer debugging example than a real service record.

Return to the [workflow](index.md). The notebook includes a runnable version of the values/function example above.

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
