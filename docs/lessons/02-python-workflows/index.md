# Module 2: Python for reproducible ML workflows

Build a small service-file processing program before adding ML libraries. You will read CSV tickets and JSON events, use functions to summarize them, and save labeled results. This is descriptive processing, not model training. No paid account, third-party package, or earlier notebook state is needed. Estimated effort: 90–120 minutes plus practice; pilot this estimate with learners.

## Learning outcomes

- **M02.1:** Use lists, dictionaries, conditionals, and loops to summarize records.
- **M02.2:** Call a function with explicit inputs and outputs and import a reusable module.
- **M02.3:** Read CSV and JSON and write a correctly labeled summary.
- **M02.4:** Diagnose a path, type, or input error using its message, traceback where available, and a small check.
- **M02.5:** Run the same processing function from a script and notebook and explain why the results agree.

Start with the [Python foundation bridge](foundation.md) if variables, loops, functions, or paths are unfamiliar. [Module 1](../01-foundations/index.md) supplies the first-run route. You may enter here directly by obtaining the complete source and following the commands below.

## The service-file problem

A fictional service lead asks how much handling time the sample tickets represent and how the sample events are labeled. Answer only about these supplied records. A four-ticket fixture cannot justify staffing forecasts or real-world incident-rate claims.

| File and field | Meaning and accepted value |
| --- | --- |
| `tickets.csv`: `ticket_id` | Nonempty unique identifier |
| `tickets.csv`: `category` | Nonempty category text; the sample uses network, software, billing |
| `tickets.csv`: `minutes` | Nonnegative whole-number handling minutes |
| `events.json`: `event_id` | Nonempty unique identifier |
| `events.json`: `source` | Nonempty source text; fictional authentication gateway or network monitor in the sample |
| `events.json`: `severity` | Exactly `info`, `warning`, or `critical` |

CSV stores rows and columns as text; the reader converts `minutes` to an integer. JSON can represent lists and objects: here the outer list contains event objects. The program selects the documented fields; extra fields are ignored. Validation stops on the first invalid record, rather than quietly dropping it. Module 3 introduces a different policy with accepted and rejected record reports.

The checked-in fixtures are original synthetic data, licensed CC BY 4.0, with checksums in `data/manifests/service-files.json`. They contain no actual tickets or system logs.

## Run the complete example

Download and extract the [source archive](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Run from its `ml_ai_it` folder. Python 3.11 or newer is sufficient; Modules 1 and 2 need no `pip install` step.

Windows PowerShell:

```powershell
py examples/service-files/scripts/summarize.py --tickets data/samples/service-files/tickets.csv --events data/samples/service-files/events.json --output runs/module02
```

macOS or Linux:

```sh
python3 examples/service-files/scripts/summarize.py --tickets data/samples/service-files/tickets.csv --events data/samples/service-files/events.json --output runs/module02
```

Expected named results:

| Measure | Value |
| --- | --- |
| Tickets | 4 |
| Total handling minutes | 60 |
| Average handling minutes | 15 |
| Network category | 2 tickets; 25 minutes |
| Software category | 1 ticket; 20 minutes |
| Billing category | 1 ticket; 15 minutes |
| Events | 3 |
| Severity counts | info: 2; warning: 1; critical: 0 |

Open `runs/module02/summary.txt` for a text explanation, `report.json` for structured results, and `category_summary.csv` for a table. Keep raw inputs separate from generated files. Rerunning replaces those three output files; choose another directory to preserve an experiment. Inputs remain unchanged.

## Trace the program

The thin entry script imports `main` from `src/practical_ml_ai/python_workflow.py`. Read that shared file in this order:

1. `read_tickets` reads one CSV record at a time, validates it, converts minutes, and returns a list of dictionaries.
2. `summarize_tickets` loops over that list and adds counts and minutes to a dictionary keyed by category. A conditional creates a category entry the first time it appears.
3. `read_events` uses the standard-library `json` module to load a list, then validates each object. `summarize_events` counts source and severity values.
4. `run_workflow` calls these functions and writes outputs with `pathlib`, `csv`, and `json`. The returned report is also usable by a notebook.

A module is an importable Python file; a package organizes modules. Standard-library modules ship with Python. NumPy and pandas are third-party packages introduced in Module 3. Installing a package and importing it are separate actions.

For no tickets, the total is zero but the average is `None` in Python and `null` in JSON. An average of an empty set is unavailable, not zero. The text output says `not available (no tickets)`.

## Notebook and downloads

The [workflow notebook](https://ntious.github.io/ml_ai_it/downloads/module02/workflow.ipynb "site-download:module02/workflow.ipynb") imports the same shared functions. Use [notebook setup](../../../QUICKSTART.md#notebook-option), keep the source structure, and run cells in order. Compare its returned report with the script's JSON output: both should give the values above. Restart and run all cells before saving. Notebook UI and screen-reader compatibility still need verification; the script/text route covers the same file-processing behavior.

Individual files are available as [ticket CSV](https://ntious.github.io/ml_ai_it/downloads/module02/tickets.csv "site-download:module02/tickets.csv") and [event JSON](https://ntious.github.io/ml_ai_it/downloads/module02/events.json "site-download:module02/events.json"). Downloading only a notebook or data file does not supply the shared code; use the complete source archive for execution.

## Read selectively

- **Core concepts:** [Python data structures](https://docs.python.org/3/tutorial/datastructures.html): lists and dictionaries; skip the advanced comprehensions on the first pass.
- **Core concepts:** [Python control flow](https://docs.python.org/3/tutorial/controlflow.html): `if`, `for`, and defining functions.
- **Implementation reference:** [Python input and output](https://docs.python.org/3/tutorial/inputoutput.html): reading/writing files and saving JSON.
- **Troubleshooting reference:** [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html): reading an exception message and a traceback.

Read the named sections as needed; entire documentation sites are not assignments. Current documentation may show features beyond the Python version used here.

Complete [practice](practice.md), then compare [worked feedback](feedback.md). Continue to [Module 3: Data processing](../03-data-processing/index.md).

## Instructor adaptation

See [instructor guidance](instructor.md) for evidence selection, accessible routes, and local adoption.

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).
