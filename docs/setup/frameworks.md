# Isolated CPU framework environment

Modules 8–12 and 14 use this environment; Modules 6, 7, and 13 use core dependencies. CI verifies **Linux CPU, Python 3.12**. Keep 3.12 here even if your core environment uses 3.13: the pinned TensorFlow 2.19 release does not support Python 3.13. Use this reference environment for framework execution; additional platform and interface coverage is documented in the [support matrix](../status.md).

## Install separately

Windows PowerShell installation recipe (the execution reference below is Linux CPU):

~~~powershell
py -3.12 -m venv .venv-ml
.\.venv-ml\Scripts\python.exe -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
.\.venv-ml\Scripts\python.exe -m pip install -e ".[regression,visualization,neural,language,deployment,verification]" -c environments/constraints-neural.txt
~~~

Linux:

~~~sh
python3.12 -m venv .venv-ml
.venv-ml/bin/python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
.venv-ml/bin/python -m pip install -e ".[regression,visualization,neural,language,deployment,verification]" -c environments/constraints-neural.txt
~~~

Do not combine this constraint file with the core one. It isolates NumPy 2.1.3/TensorFlow 2.19.1 from core NumPy 2.3.5. Constraints record exercised choices, not the newest release or a full transitive lockfile.

Allow several GB of disk and sufficient memory; 8 GB RAM is a starting allowance, not a guarantee. No paid API or GPU is required. First package/data/model downloads need connectivity; later valid caches support replay.

## Run and save

Here python means your environment executable above if not activated.

~~~sh
python examples/wine-neural-network/scripts/run.py --output runs/module08
python -m ipykernel install --user --name ml-ai-frameworks
python scripts/check_notebook.py --group frameworks --kernel ml-ai-frameworks
~~~

An optional local notebook interface can be installed with python -m pip install notebook and launched with python -m notebook. Keep notebooks inside the complete source tree, run in order, save, restart, and run all. The script/text route shares implementation but does not demonstrate notebook-interface operation.

USE_TF=0 is a Transformers backend setting for the PyTorch language model, not a switch disabling the separate TensorFlow examples.

## Reproduce the complete site

Execute both notebook groups in their corresponding environments while retaining runs/verified. Install the verification extra in each and run only that profile's commands from that environment; the block below lists the overall sequence, not one combined environment:

~~~sh
python -m ipykernel install --user --name ml-ai-core
python scripts/check_notebook.py --group core --kernel ml-ai-core
python -m ipykernel install --user --name ml-ai-frameworks
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

## Phase B study controls

Module 9 defaults to the full deduplicated corpus and a 25-epoch maximum; `--epochs 3 --sample-limit 1200` provides a deliberately smaller diagnostic variant. It is not byte-identical to the archived run because tokenization and threshold selection were corrected. Module 10 accepts `--examples N` (20 through the final-partition size; default 100). Module 11 accepts `--steps N` (1–300; default 200). Smaller budgets exercise the software interface without promising the default study quality. Keep outputs in new directories and declare settings before inspecting final results.
