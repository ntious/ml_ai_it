# Complete project exemplar: historical phishing triage

This optional project shows how individual ML skills become one completed
investigation. The 14 modules and the shorter phishing case still run on their
own. No previous notebook state, GPU, paid API, cloud account or tracking server
is needed. Use the complete checkout/source archive and the existing core
environment with the regression and verification extras.

Start after Modules 3, 5 and 6. Beginners can first read the
[annotated completed report](reports/annotated-report.md); experienced learners
can run the experiment and challenge its decisions before reading the report.
The example is a reference for reasoning and deliverables, not a submission to
copy or a replacement for an adopting instructor's capstone requirements.

## What you will learn

- Frame a decision, research questions, baseline and error costs.
- Validate attributed data, establish group boundaries and audit input availability.
- Tune a bounded parameter grid using training-only group-aware CV.
- Measure training-seed stability on fixed data without cherry-picking.
- Optionally investigate different development splits with the model seed fixed.
- Freeze the protocol, evaluate once as a planned batch and explain uncertainty/errors.
- Export numeric-only inference, reject invalid inputs, rehearse monitoring and justify rollback.
- Produce a traceable report, configuration, run registry and release decision.

## Choose a route

| Route | What to do | What you can conclude |
| --- | --- | --- |
| Read and interpret | Read the report and [advanced guides](../../docs/advanced/index.md) | Explain the evidence; this does not establish implementation mastery |
| Core project | Run all stages using the default configuration | Reproduce a complete fixed-split, five-training-seed study |
| Advanced investigation | Add the separate split study; inspect trials, seed metrics and calibration | Explain the sources of variation and limits of the experiment |
| Independent transfer | Change a justified task/protocol before evaluation | Produce your own evidence and decision under your course requirements |

Planning allowance: one project session for execution/inspection, plus separate
time for interpretation and writing. These are not learner-piloted workload
estimates; use the measured seconds in each completion marker to assess your CPU.

## Run the complete project

From the repository root, `python` below means the core environment executable.
For example use `.venv/bin/python` or `.venv\Scripts\python.exe` when not activated.
First data acquisition needs internet; valid checksum-verified caches support replay.

```sh
python projects/phishing-triage/scripts/run.py all --run runs/capstone
```

For the optional split-sensitivity investigation, use a new directory:

```sh
python projects/phishing-triage/scripts/run.py all --run runs/capstone-advanced --advanced
```

Open `runs/capstone-advanced/index.html`, `report.md` or `summary.txt`. Configuration
is in `projects/phishing-triage/configs/study.json`: 10 candidate configurations ×
3 training-only folds = 30 CV fits; five predeclared training seeds; a bounded
threshold grid; illustrative FN:FP costs of 5:1. The outer split remains fixed.
Outputs belong under ignored `runs/` or outside the checkout, never inside `projects/`.

The [commented notebook](https://ntious.github.io/ml_ai_it/downloads/capstone/walkthrough.ipynb "site-download:capstone/walkthrough.ipynb")
calls these same stages. Keep it inside the complete source tree. The
[worked report](https://ntious.github.io/ml_ai_it/downloads/capstone/example/index.html "site-download:capstone/example/index.html")
is included in the complete CI reading-site artifact before public deployment.
Publication-target links work after the owner enables and completes deployment. If a download link does not open, use the [offline access route](../../docs/setup/student-workspace.md#if-a-download-link-does-not-open).

## Inspect or resume individual stages

```sh
python projects/phishing-triage/scripts/run.py prepare --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py tune --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py stability --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py split-study --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py freeze --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py evaluate --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py deliver --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py report --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py verify --run runs/capstone-stages
python projects/phishing-triage/scripts/run.py all --run runs/capstone-stages --advanced --resume
```

Completed stages are immutable. Resume verifies and skips completed stages; it
requires choosing the optional split study before freezing. To add that study to
an already frozen core run, start a new run with `--advanced`. Resume
never overwrites a partial stage. If an interrupted stage left partial outputs,
retain them for diagnosis and start a new run. Source/configuration changes also
require a new study. The ledger detects changed files; it is a teaching integrity
check, not cryptographic protection against an owner rewriting the entire ledger.

Try the saved inference contract:

```sh
python projects/phishing-triage/scripts/run.py predict --run runs/capstone-stages --input runs/capstone-stages/example_request.json
```

## Expected project deliverables

| Deliverable | Evidence |
| --- | --- |
| Proposal and literature context | Research questions, stakeholder/cost assumptions, source references in report.md |
| Data dictionary and audit | Source feature definitions, training_profile.csv, data_audit.json, protocol.json and provenance |
| Search record | config.json, inner_folds.json, search_trials.csv, tuning.json |
| Stability investigation | Every seed in validation_runs.csv; metric summaries; separate split_sensitivity.csv when run |
| Locked evaluation | selection.json, model hashes, final predictions, per-seed and ensemble metrics |
| Error/uncertainty analysis | Error IDs, illustrative profile bootstrap and reliability bins |
| Delivery demonstration | Numeric inference bundle, valid/invalid examples, offline monitoring and rollback decision |
| Reproducibility | environment.json, stage hashes/durations, commands and complete written report |

The structural dictionary lists source-coded categories, not complete semantic
definitions. Read the UCI feature documentation and investigate whether each
signal could exist at the intended decision time. A completed research project
can legitimately conclude that live deployment is not justified.

## Boundaries

The data are historical website profiles, not live traffic or independent
campaign identifiers. No URLs are visited. The project demonstrates research
orchestration, not a deployed security product. The cost ratio is illustrative;
seed variation is not population uncertainty; the bootstrap's grouping
assumptions are limited. See the [completed report](reports/annotated-report.md)
for the decision and threats to validity, and the [assessment crosswalk](../../docs/advanced/capstone-assessment.md)
for independent transfer. Original code/content and external data retain their
existing repository/source licenses.
