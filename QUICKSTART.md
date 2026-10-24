# First run

Use Python 3.11 or newer. The recorded development verification used Python 3.12; other versions/platforms require testing. Run these commands from the `ml_ai_it` repository folder. Commands are available as selectable text; no screenshot interpretation is needed.

## Windows PowerShell

Create a project environment and install the local package. Calling the environment's Python directly avoids a script-activation requirement.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

If Python 3.12 is not installed, use a supported installed Python version and record it when reporting a problem. Windows execution has not yet been verified in this development environment.

## macOS or Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

## What to expect

The text result identifies 12 input records, 6 accepted, 6 rejected, and 1 accepted record with missing latency. The observed latency mean is 24 milliseconds and median is 20 milliseconds, computed from 5 observed accepted values. Missing latency is excluded from those calculations, not changed to zero.

Inspect `runs/module03/summary.txt`, `quality_report.json`, `cleaned_events.csv`, and `rejected_events.csv`. The rejected CSV includes the source row and reasons. The raw sample remains unchanged. Rerunning replaces only those generated output files; use a new output directory to retain an experiment.

## Notebook option

Install a notebook interface inside the same environment, then open `notebooks/lessons/03-data-processing/complete_walkthrough.ipynb`:

```sh
python -m pip install notebook
python -m notebook
```

Here `python` means the Python executable from your project environment; use its full path if you have not activated it. Notebook-interface accessibility varies. The script and HTML reading path cover the same example and produce the same results. See [setup/accessibility status](docs/setup/index.md).

## If something goes wrong

- `No module named pandas` or `numpy`: install the package using the Python executable that will run it.
- File not found: check the working folder and the input path. The script prints a text error and exits without a successful result.
- Missing columns: compare the CSV header with the module's data dictionary.
- An empty accepted dataset is a result to inspect, not a successful model-training dataset.

When requesting help, include the command, Python/platform version, error text, and a small synthetic input. Keep credentials and personal data out of public issues.
