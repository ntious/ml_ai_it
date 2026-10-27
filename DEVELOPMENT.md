# Maintainer setup and verification

Use this guide to reproduce edition 0.7.0 and validate changes. Learners should begin with [first run](QUICKSTART.md). Independent reviewers can use the [review guide](docs/review-guide.md). The [workflow](https://github.com/ntious/ml_ai_it/blob/main/.github/workflows/checks.yml) is the executable reference; [support scope](docs/status.md) explains what its evidence establishes.

## Keep two environments

The applied teaching prototype adds separate practice/solution notebooks for Modules 5, 6 and 8. Run `python scripts/check_practice.py --group core --kernel ml-ai-core` in the core environment and `python scripts/check_practice.py --group frameworks --kernel ml-ai-frameworks` in the framework environment before building the reading site. The checker preserves clean source, verifies unchanged outcome hashes and records unfinished starter feedback separately from completed solution/sandbox execution. The site build rejects stale practice source identities. Regenerate the original explanatory SVGs with `python scripts/build_teaching_figures.py`; exact-value tables remain in the lessons.

Use the [pilot protocol](docs/instructor/teaching-prototype-pilot.md) for human observation and the [prototype review handoff](docs/maintenance/reviews/applied-teaching-prototype-handoff.md) for implementation review. These are verification procedures, not claims that a human pilot has occurred.

Use Python 3.12 for the reference profiles. From the complete checkout, scripts/bootstrap.py installs either core or frameworks. Framework execution uses Linux CPU. Do not combine the core and framework constraint files: they exercise different NumPy/TensorFlow combinations. The Windows core job in the workflow provides its exact Windows commands.

```sh
python3 scripts/bootstrap.py --profile core
python3 scripts/bootstrap.py --profile frameworks
```

Each bootstrap creates its own .venv or .venv-ml environment and registers ml-ai-core or ml-ai-frameworks. The commands below are the Linux reference; use that profile's Python explicitly. First installation and source/model downloads need connectivity. Preserve source hashes, attribution and model revisions for replay.

## Core behavior and notebooks

```sh
.venv/bin/python scripts/preflight.py --profile core
.venv/bin/python scripts/check_repository.py
ML_AI_REAL_DATA=1 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/check_notebook.py --group core --kernel ml-ai-core
```

Core discovery reports framework tests as skips. Those checks run in the separate framework job; skipped tests are not passes. Core notebook verification also executes the independent phishing case. Clean source notebooks retain no outputs; executed copies and real reports are saved under runs/verified.

## Framework behavior and notebooks

```sh
.venv-ml/bin/python scripts/preflight.py --profile frameworks
ML_AI_HEAVY=1 USE_TF=0 HF_HUB_DISABLE_XET=1 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 .venv-ml/bin/python -m unittest discover -s tests -p test_continuation_heavy.py -v
USE_TF=0 HF_HUB_DISABLE_XET=1 .venv-ml/bin/python scripts/check_notebook.py --group frameworks --kernel ml-ai-frameworks
```

These checks train actual models, evaluate generation, update/reload adapters, exercise public CLIs and test both app forms and HTTP health. Observed poor model results remain evidence, not failures to conceal. A successful software test is distinct from a useful model.

## Build and inspect the reading site

The separate optional capstone has its own core-profile notebook check. Before building the complete reading site, run `python scripts/check_capstone.py --kernel ml-ai-core`. After intentionally updating its protocol, use `python scripts/refresh_capstone_report.py` to refresh the source report from verified execution and inspect the change. Existing module notebook checks remain separate. CI executes the project on the core Windows/Linux matrix and publishes its verified artifacts with the core results.

Execute both notebook groups first so runs/verified contains their reports. Install the pinned Node dependencies with npm ci. Activate the core environment for Python subprocesses used by the builder, or set PYTHON to its executable.

```sh
npm ci --ignore-scripts
PYTHON=.venv/bin/python npm run build
.venv/bin/python scripts/check_source_links.py
.venv/bin/python scripts/check_site.py
.venv/bin/python scripts/check_http_routes.py
.venv/bin/python scripts/check_downloads.py
npx playwright install --with-deps chromium
node scripts/check_browser.mjs
.venv/bin/python -m pip wheel . --no-deps --wheel-dir dist
.venv/bin/python scripts/check_wheel.py
```

The archive check requires a Git checkout and compares source membership and bytes against tracked files. Stage new authored files before checking a local source archive. The builder recognizes Markdown link titles beginning site-download:; source links use the published https://ntious.github.io/ml_ai_it/downloads/ URL, while generated HTML links to the local download. check_source_links.py enforces that form. Validate both representations. Do not commit site, runs, installed environments or source/model caches.

Browser checks serve the built site on an automatically assigned loopback port and save evidence under runs/browser-review. They cover selected core, capstone and advanced reading pages, selected axe rules, skip-link focus and 320px reflow; the readiness page also has a dark-mode scan. Use the [accessibility evidence log](docs/accessibility/review-log.md) for human task-based review.

## Runtime and source maintenance

Checkout dataset/model caches default to runs. Installed packages use a user cache; ML_AI_RUNS_DIR overrides the Module 6–14 runtime directory when set before import. Output directories remain explicit. Source acquisition stops on changed reviewed hashes. Investigate upstream changes rather than disabling checks.

Update curriculum/modules.json when paths/profiles change. Each module has six teaching pages, a clean notebook and a public script. Change shared code, teaching explanations, feedback, tests and provenance together. The staged phishing CLI separates prepare, train, validate, evaluate and report; its combined notebook calls those same functions.

The [release/adoption checklist](docs/release-checklist.md) records evidence and owner decisions for a tested commit. CI produces reviewable artifacts. After the owner approves publication, select GitHub Actions as the Pages source and set the repository Actions variable `PUBLISH_READING_SITE` to `true`. The deploy-pages job then publishes complete-reading-site only from main after every check passes. Without that variable, deployment stays skipped. Earlier implementation details are retained in the [historical notes](docs/maintenance/reviews/implementation-history.md).
