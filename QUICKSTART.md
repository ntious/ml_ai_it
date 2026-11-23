# First run

**Before setup:** use [readiness and Python Foundation](docs/start-here.md), [workspace acquisition](docs/setup/student-workspace.md) and [environment choices](docs/setup/hosted.md). Python Foundation is preparation, not a formal admission prerequisite. Our [Python-to-ML bridge](docs/setup/python-bridge.md) adds file and table skills.

Obtain a checkout or extract the complete source archive, then open a terminal in its `ml_ai_it` folder. Use Python 3.11, 3.12 or 3.13; CI checks the core modules on 3.12 (Windows and Linux) and 3.13 (Windows). If Python is missing, use the [official download page](https://www.python.org/downloads/) and your platform's installer instructions. Check your version before proceeding.

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

Expect storage used 85 percent, threshold 80 percent, and `Review storage`. Open the saved text file. This is a human-written rule; no model is trained. Continue with [Module 1](docs/lessons/01-foundations/index.md). The Module 1 script needs nothing extra, but its practice notebook does: if you want the notebook, do the Module 3 environment steps and the [notebook option](#notebook-option) first (about 10 minutes).

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

From here on, the course uses a **virtual environment**: a private copy of Python, stored in a folder named `.venv` inside `ml_ai_it`, that holds the course's packages without changing the rest of your computer.

- You create it **once**, with the first command below.
- After that, start every course command with the environment's own Python: `.venv/bin/python` on macOS/Linux, or `.\.venv\Scripts\python.exe` on Windows. That is how the command finds the packages you installed.
- You do not need to "activate" the environment. Activation is an optional shortcut that lets you type plain `python`; if you have not activated it, plain `python` runs a different Python that does not have the course packages.
- If something goes badly wrong, you can delete the `.venv` folder and create it again.

The install commands download third-party packages, so internet access is needed. The constraints file pins the NumPy/pandas versions the course was tested with.

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e . -c environments/constraints-tested.txt
.\.venv\Scripts\python.exe examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e . -c environments/constraints-tested.txt
.venv/bin/python examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

`py -m venv` uses your default Python; run `py --list` if you have several versions, and record the version when reporting an issue. Expect 12 input records, 6 accepted, 6 rejected, and 1 accepted record retaining missing latency. Observed latency mean/median are 24/20 milliseconds. See [Module 3](docs/lessons/03-data-processing/index.md).

## Module 4: add plotting libraries

After creating `.venv`, install the visualization extra and run exploration. In Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[visualization]" -c environments/constraints-tested.txt
.\.venv\Scripts\python.exe examples/service-workload/scripts/explore.py --input data/samples/service-workload/daily.csv --output runs/module04
```

On macOS/Linux:

```sh
.venv/bin/python -m pip install -e ".[visualization]" -c environments/constraints-tested.txt
.venv/bin/python examples/service-workload/scripts/explore.py --input data/samples/service-workload/daily.csv --output runs/module04
```

Expect 24 distinct observations, 4,180 requests, 23 observed latencies and one unavailable latency. Open `runs/module04/index.html` for the five figures with actual tables/descriptions, or use its plain-text/CSV evidence. See [Module 4](docs/lessons/04-exploration/index.md) for preprocessing and interpretation. No display server is required for generating figures.

## Module 5: regression and real public data

After creating the environment, add the regression/visualization extras, download the attributed UCI data, and run a fresh study. Windows PowerShell:

~~~powershell
.\.venv\Scripts\python.exe -m pip install -e ".[regression,visualization]" -c environments/constraints-tested.txt
.\.venv\Scripts\python.exe examples/bike-demand/scripts/study.py download --run runs/datasets/bike-sharing
.\.venv\Scripts\python.exe examples/bike-demand/scripts/study.py all --input runs/datasets/bike-sharing/day.csv --run runs/module05 --holdout-days 110 --plots --dataset-label "UCI Bike Sharing daily counts, CC BY 4.0"
~~~

macOS/Linux:

~~~sh
.venv/bin/python -m pip install -e ".[regression,visualization]" -c environments/constraints-tested.txt
.venv/bin/python examples/bike-demand/scripts/study.py download --run runs/datasets/bike-sharing
.venv/bin/python examples/bike-demand/scripts/study.py all --input runs/datasets/bike-sharing/day.csv --run runs/module05 --holdout-days 110 --plots --dataset-label "UCI Bike Sharing daily counts, CC BY 4.0"
~~~

Expect 504 training, 110 validation, and 110 final-test examples after seven warm-up days. Open runs/module05/index.html or its text/CSV evidence. Use a new study directory for a replay. [Module 5](docs/lessons/05-regression/index.md) explains separate stages, the forecast origin, source/license, and the clearly synthetic offline alternative. The first real-data download needs internet, while later runs reuse a checksum-verified cache.

## Notebook option

Notebooks are optional execution companions. Every course notebook, including the Module 1 and 2 practice notebooks, needs the core environment: the practice checks use NumPy even though the Module 1 and 2 scripts do not. Do these steps once, from the `ml_ai_it` folder.

1. Create `.venv` and install the package with the Module 3 commands above.
2. Install a notebook interface into that environment and register it as the course kernel.
3. Launch the interface from the same folder.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install notebook ipykernel
.\.venv\Scripts\python.exe -m ipykernel install --user --name ml-ai-core --display-name "Python (course core)"
.\.venv\Scripts\python.exe -m notebook
```

macOS or Linux:

```sh
.venv/bin/python -m pip install notebook ipykernel
.venv/bin/python -m ipykernel install --user --name ml-ai-core --display-name "Python (course core)"
.venv/bin/python -m notebook
```

Course notebooks request the kernel named **Python (course core)**. If the interface asks you to choose a kernel, or reports that `ml-ai-core` is missing, choose **Python (course core)** (Kernel → Change kernel), or rerun the registration command. Framework notebooks (Modules 8–12 and 14) request **Python (course frameworks)**, registered by the [framework setup](docs/setup/frameworks.md).

From the opened interface, open the module's notebook under `notebooks/lessons/`, or its practice notebook under `notebooks/practice/`. Select and run code cells in order. Save with the interface's File → Save command, restart the kernel, and run all cells. The notebook imports shared source from the complete repository folder; downloading a notebook alone is insufficient. Use the documented script/text route when it better fits your interface needs; the accessibility guide records interface testing scope. See [setup and accessibility status](docs/setup/index.md).

## Save and troubleshoot

Use different output names/directories for experiments. Overwriting rules differ by module: **Modules 1–4 replace** generated files at the same paths when you rerun, while **Modules 5–14 refuse** to overwrite an existing run, so give each rerun a new `--output` or `--run` folder (for example `runs/module06-try2`). Keep raw samples unchanged. A failed run may leave an older report from a previous successful run, so retain commands and error text with your experiment.

- Command unavailable: check the installed Python command and version.
- File not found: check the working folder and the exact input path.
- Missing columns or invalid value: inspect the CSV header and named field; use a synthetic copy for repair practice.
- Missing NumPy/pandas (`ModuleNotFoundError`): you probably ran plain `python` or `python3`. Run the command again starting with `.venv/bin/python` (macOS/Linux) or `.\.venv\Scripts\python.exe` (Windows).
- `urlopen error`, `Max retries` or a proxy message: a dataset or model download failed. Check that you are online and that your network allows archive.ics.uci.edu and huggingface.co, then rerun.

For help, retain the command, Python/platform version, error text, and small synthetic input. Screenshots are not required. Keep credentials and personal information out of public issues.

## Modules 6–14

Choose a module from the [curriculum map](docs/modules.md). Modules 6, 7, and 13 use the core environment; Modules 8–12 and 14 use the [isolated CPU framework setup](docs/setup/frameworks.md), which needs Python 3.12 and has its own environment folder, `.venv-ml`.

Lesson pages write commands with the environment's Python in front. If a command you copy starts with plain `python`, replace that word as follows:

| Modules | macOS/Linux | Windows PowerShell |
| --- | --- | --- |
| 1–7 and 13 | `.venv/bin/python` | `.\.venv\Scripts\python.exe` |
| 8–12 and 14 | `.venv-ml/bin/python` | Use WSL (see the framework setup), then `.venv-ml/bin/python` |

The first run of Modules 5–14 downloads a public dataset (from the UCI repository) or a small language model (from Hugging Face), so it needs internet. Later runs reuse the verified cache. Each entry supplies its script, commented notebook, actual source, and evidence requirements. Use fresh output directories and retain verified data/model caches for replay.

## Maintainer verification

To execute the curated notebooks programmatically, install the verification extra in the relevant environment, register its Jupyter kernel, and follow [development verification](DEVELOPMENT.md). A notebook frontend alone is not the complete automated-check setup. The [framework guide](docs/setup/frameworks.md) uses its own environment and kernel. Clean source notebooks and saved executed build copies have different purposes.
