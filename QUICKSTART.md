# First run

Obtain a checkout or extract the complete source archive, then open a terminal in its `ml_ai_it` folder. Use Python 3.11 or newer; development checks use Python 3.12. If Python is missing, use the [official download page](https://www.python.org/downloads/) and your platform's installer instructions. Check your version before proceeding.

Commands below are selectable text. `py` is the usual Windows Python launcher; if it is unavailable but `python --version` reports the intended interpreter, use `python` instead. On macOS/Linux, use `python3`. Report an unavailable command rather than entering unrelated installation commands suggested by an unverified source.

## Module 1: no package installation needed

Windows PowerShell:

```powershell
py --version
py examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

macOS or Linux:

```sh
python3 --version
python3 examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

Expect storage used 85 percent, threshold 80 percent, and `Review storage`. Open the saved text file. This is a human-written rule; no model is trained. Continue with [Module 1](docs/lessons/01-foundations/index.md).

## Module 2: read CSV and JSON

Windows PowerShell:

```powershell
py examples/service-files/scripts/summarize.py --tickets data/samples/service-files/tickets.csv --events data/samples/service-files/events.json --output runs/module02
```

macOS or Linux:

```sh
python3 examples/service-files/scripts/summarize.py --tickets data/samples/service-files/tickets.csv --events data/samples/service-files/events.json --output runs/module02
```

Expect 4 tickets, 60 total minutes, average 15 minutes, and 3 events. Inspect `summary.txt`, `report.json`, and `category_summary.csv` under `runs/module02/`. See [Module 2](docs/lessons/02-python-workflows/index.md) for interpretation and input-error practice.

## Module 3: add the data libraries

Create an isolated environment and install the local package. Calling the environment's Python directly avoids a script-activation requirement. These commands install third-party dependencies; internet access is normally needed. The constraints record the NumPy/pandas versions used in development.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e . -c environments/constraints-tested.txt
.\.venv\Scripts\python.exe examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e . -c environments/constraints-tested.txt
.venv/bin/python examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

If Python 3.12 is unavailable, use a supported installed version and record it when reporting an issue. Expect 12 input records, 6 accepted, 6 rejected, and 1 accepted record retaining missing latency. Observed latency mean/median are 24/20 milliseconds. See [Module 3](docs/lessons/03-data-processing/index.md).

## Notebook option

Notebooks are optional execution companions. To operate one locally, create a project environment as above and install an interface into that environment:

```sh
python -m pip install notebook
python -m notebook
```

Here `python` means the environment executable: `.\.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux if you have not activated it. The interface is an additional dependency even though Modules 1 and 2 themselves need only the standard library. Module 3 also needs the local package and its dependencies installed.

From the opened interface, open the module's notebook under `notebooks/lessons/`. Select and run code cells in order. Save with the interface's File → Save command, restart the kernel, and run all cells. The notebook imports shared source from the complete repository folder; downloading a notebook alone is insufficient. Notebook UI and assistive-technology compatibility remain unverified. See [setup and accessibility status](docs/setup/index.md).

## Save and troubleshoot

Use different output names/directories for experiments; rerunning replaces generated files at the same paths. Keep raw samples unchanged. A failed run may leave an older report from a previous successful run, so retain commands and error text with your experiment.

- Command unavailable: check the installed Python command and version.
- File not found: check the working folder and the exact input path.
- Missing columns or invalid value: inspect the CSV header and named field; use a synthetic copy for repair practice.
- Missing NumPy/pandas: install with the same environment executable used to run Module 3.

For help, retain the command, Python/platform version, error text, and small synthetic input. Screenshots are not required. Keep credentials and personal information out of public issues.
