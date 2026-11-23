# Isolated CPU framework environment

Modules 8–12 and 14 use this environment; Modules 6, 7, and 13 use core dependencies. CI verifies **Linux CPU, Python 3.12**. Keep 3.12 here even if your core environment uses 3.13: the pinned TensorFlow 2.19 release does not support Python 3.13. Use this reference environment for framework execution; additional platform and interface coverage is documented in the [support matrix](../status.md).

**Which route should I use?**

| Your computer | Route |
| --- | --- |
| Linux with Python 3.12 | [Linux](#linux) below |
| Linux without Python 3.12 | Install Python 3.12 first (see [Install Python 3.12](#install-python-3-12)), or use Codespaces |
| Windows | [WSL with Ubuntu 24.04](#windows-use-wsl-with-ubuntu-24-04) below |
| macOS | GitHub Codespaces (see [environment choices](hosted.md#codespaces)); native macOS framework installs are not verified |

The framework environment lives in its own folder, `.venv-ml`, separate from the core `.venv`. Commands for Modules 8–12 and 14 start with `.venv-ml/bin/python`.

## Install separately

### Linux

First check that Python 3.12 is installed. This must print `Python 3.12.x`:

~~~sh
python3.12 --version
~~~

If the command is not found, see [Install Python 3.12](#install-python-3-12). Then create the environment:

~~~sh
python3.12 -m venv .venv-ml
.venv-ml/bin/python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
.venv-ml/bin/python -m pip install -e ".[regression,visualization,neural,language,deployment,verification]" -c environments/constraints-neural.txt
.venv-ml/bin/python -m ipykernel install --user --name ml-ai-frameworks --display-name "Python (course frameworks)"
~~~

Or run `python3.12 scripts/bootstrap.py --profile frameworks`, which performs the same steps, registers the kernel and runs the preflight check. Start it with `python3.12`, not `python3`: the script builds `.venv-ml` from whichever Python runs it, and stops with an explanation if that is not 3.12.

#### Install Python 3.12

- Ubuntu 24.04 and WSL Ubuntu 24.04 already include it; install the venv module with `sudo apt install -y python3.12-venv`.
- Other Linux distributions: install a 3.12 package from your distribution, or download it from the [official Python downloads page](https://www.python.org/downloads/). Newer distributions (for example Ubuntu 25.04 and Fedora 41) default to Python 3.13, which TensorFlow 2.19 does not support.
- If you cannot install 3.12, use GitHub Codespaces, whose course container already uses Python 3.12.

### Windows: use WSL with Ubuntu 24.04

Native Windows framework installs are not verified, and `scripts/bootstrap.py` refuses them. On Windows, run the Linux route inside the Windows Subsystem for Linux (WSL). Ubuntu 24.04 provides Python 3.12 by default.

**Prerequisites**

- Windows 11, or Windows 10 version 22H2. Administrator rights are needed once, to install WSL.
- Hardware virtualization enabled in the firmware settings. `wsl --install` reports it if it is disabled.
- Internet access for the first installation and for model and data downloads.
- Resources: see [Resource requirements](#resource-requirements) below. Close large applications during training.

**Steps**

1. In PowerShell opened as administrator, run `wsl --install -d Ubuntu-24.04`. Restart Windows if prompted, then open **Ubuntu 24.04** from the Start menu and create a Linux user name and password.
2. In the Ubuntu terminal, install the system packages:

   ~~~sh
   sudo apt update && sudo apt install -y python3.12-venv unzip
   python3 --version
   ~~~

   The version check should report Python 3.12.
3. Copy the course source into your Linux home folder. Working under `/mnt/c` is slow and can break file permissions. Replace `YOUR-WINDOWS-NAME` with your Windows user folder name:

   ~~~sh
   mkdir -p ~/courses && cd ~/courses
   cp /mnt/c/Users/YOUR-WINDOWS-NAME/Downloads/ml_ai_it-source.zip .
   unzip ml_ai_it-source.zip && cd ml_ai_it
   ~~~

4. Create the framework environment, register its kernel and run the preflight check:

   ~~~sh
   python3.12 scripts/bootstrap.py --profile frameworks
   ~~~

5. Run a module script, for example `.venv-ml/bin/python examples/wine-neural-network/scripts/run.py --output runs/module08`.
6. For notebooks, run `.venv-ml/bin/python -m pip install notebook` and then `.venv-ml/bin/python -m notebook --no-browser`. Open the printed `http://localhost:8888/...` address in your Windows browser and choose the kernel **Python (course frameworks)**.

Windows File Explorer shows your results at `\\wsl$\Ubuntu-24.04\home\<linux-user>\courses\ml_ai_it\runs`. Copy anything you need to keep to a Windows folder before removing the distribution.

Verification scope: steps 4–6 are the commands the Linux CPU CI job runs. The WSL installation itself (steps 1–3) has not been tested by the maintainers; report problems with the exact command and message.

### Resource requirements

Allow at least 10 GB of free disk and 8 GB of RAM. On the reference CI machine (2 CPU cores, 7.9 GB RAM), the installed framework packages take 3.0 GB, the pip download cache 0.7 GB and the data and model caches about 0.3 GB. Installing PyTorch without the CPU index line above pulls GPU libraries and roughly doubles the size. For maintainers only: the automated framework tests take about 70 minutes and executing every framework notebook about 50; students do not need to run these. Peak memory has not been measured, so close large applications during training. No paid API or GPU is required. First package/data/model downloads need connectivity; later valid caches support replay.

Do not combine this constraint file with the core one. It isolates NumPy 2.1.3/TensorFlow 2.19.1 from core NumPy 2.3.5. Constraints record exercised choices, not the newest release or a full transitive lockfile.

## Run and save

Run a module script with the framework environment's Python, giving a new output folder each time:

~~~sh
.venv-ml/bin/python examples/wine-neural-network/scripts/run.py --output runs/module08
~~~

The first run downloads the dataset or model, so it needs internet; later runs reuse the cache. For notebooks, install an interface once with `.venv-ml/bin/python -m pip install notebook`, launch it with `.venv-ml/bin/python -m notebook`, and choose the kernel **Python (course frameworks)**. The kernel was registered during installation; rerun the `ipykernel install` line above only if the interface says it is missing. Keep notebooks inside the complete source tree, run in order, save, restart, and run all. The script/text route shares implementation but does not demonstrate notebook-interface operation.

USE_TF=0 is a Transformers backend setting for the PyTorch language model, not a switch disabling the separate TensorFlow examples.

## Reproduce the complete site

This section is for maintainers. Execute both notebook groups in their corresponding environments while retaining runs/verified. Install the verification extra in each and run only that profile's commands from that environment; the block below lists the overall sequence, not one combined environment:

~~~sh
python -m ipykernel install --user --name ml-ai-core --display-name "Python (course core)"
python scripts/check_notebook.py --group core --kernel ml-ai-core
python -m ipykernel install --user --name ml-ai-frameworks --display-name "Python (course frameworks)"
python scripts/check_notebook.py --group frameworks --kernel ml-ai-frameworks
npm install --ignore-scripts
npm run build
npm run check
python scripts/check_downloads.py
~~~

The builder requires actual verified reports and fails rather than inventing missing evidence. CI assembles complete-reading-site automatically. The resulting site artifact can be read locally or served by the chosen host.

## Troubleshoot and interpret

Retain exact commands, versions, and error text. A changed-source hash requires review. Use the [source register](../data-sources.md) for attribution, cache layout, and privacy limits. Do not disclose credentials in issues.

The short neural NLP model can miss positives, and free-text LLM output can fail its schema. Module 11 now trains all-layer rank-8 PEFT LoRA for up to 200 steps, with batches of 8 and validation-only checkpoint selection; allow additional CPU time (roughly 15–30 minutes on the reference-sized setup, hardware dependent). The rank-2 hand example remains a construction aid. Successful execution is separate from useful/safe model behavior. See the [accessibility evidence](../accessibility/review-log.md) for interface test scope.

## Study controls

Module 9 defaults to the full deduplicated corpus and a 25-epoch maximum; `--epochs 3 --sample-limit 1200` provides a deliberately smaller diagnostic variant. It is not byte-identical to the archived run because tokenization and threshold selection were corrected. Module 10 accepts `--examples N` (20 through the final-partition size; default 100). Module 11 accepts `--steps N` (1–300; default 200). Smaller budgets exercise the software interface without promising the default study quality. Keep outputs in new directories and declare settings before inspecting final results.

## Runtime and cached replay

The learning-time estimates on module pages include reading and practice; they are not script runtime benchmarks. Apart from the qualified Module 11 estimate, per-module CPU timings have not yet been measured consistently. Keep the terminal open while a study runs and record elapsed time and hardware when reporting a slow run.

Complete, valid dataset caches are reused without downloading again. Model loading may still check Hugging Face even when weights are cached. Do not assume that one successful download guarantees every later task will run offline: additional files or a different model revision may be needed. Keep the original error and use the worked report while resolving network access.
