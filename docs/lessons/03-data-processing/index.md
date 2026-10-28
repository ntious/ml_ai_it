# Module 3 Data processing

Read the overview and learning outcomes here, then follow the learning route. Return to this page’s run instructions for the complete study.

Turn raw event records into documented, inspectable inputs for later analysis. This module works independently: its small sample, setup, explanations, and practice are available from this page. No earlier notebook state or Canvas assignment is required.

## What you will learn

By completing the core route, you can:

1. **M03.1:** Inspect NumPy shapes/types and use a small vector or linear-system calculation.
2. **M03.2:** Read, filter, summarize, and write a pandas dataframe.
3. **M03.3:** Run a repeatable preparation script and explain rejected records.
4. **M03.4:** Identify CSV, JSON, and array representations with their fields and units.
5. **M03.5:** Write a data dictionary and justify a cleaning choice while preserving later train/test boundaries.

These are resource learning outcomes. They do not claim course credit or certified program-outcome attainment.

## Learning route

Follow [foundation](foundation.md) → [concepts and small cases](concepts.md) → [guided construction](guided.md) → [independent practice](practice.md). Use [solutions](solutions.md) after your attempt, then connect your work to the complete reference below.

## Prerequisite help

You need to run a Python command and recognize a function, list/dictionary, and file path. Use the [short foundation bridge](foundation.md) if these are new. [Setup](../../setup/index.md) explains installing dependencies and saving outputs. You may use the script route or the guided notebook.

The core reading and demonstration are designed as a bounded introduction, with a provisional 45–75 minutes for practice plus setup. These times require learner piloting. [Optional extensions](practice.md#transfer-to-an-it-decision) can be skipped.

## Operational problem

An IT team receives event exports from two fictional sources. The authentication gateway reports sign-in service activity; the network monitor reports transfer observations. Before analyzing latency or fitting a later model, the team must know which records are valid and which assumptions were applied.

The 12-row sample is hand-authored synthetic data. Its irregularities are deliberate. It contains no real users, credentials, or network measurements. Small fictional data can demonstrate a workflow; it cannot validate an operational prediction or represent a production population.

## Data dictionary

- `event_id`: nonempty identifier scoped to its source. The pair `source` and `event_id` is the event key.
- `timestamp`: ISO 8601 timestamp, normalized to UTC. This sample includes explicit time zones. Naive timestamps are interpreted as UTC by this implementation; confirm that assumption before applying it to other data.
- `source`: either `authentication_gateway` or `network_monitor`.
- `latency_ms`: finite nonnegative milliseconds; a missing value is retained.
- `bytes_sent`: a whole number of bytes from zero through the signed 64-bit integer maximum; missing, fractional, and out-of-range values are rejected. Exact parsing prevents silent rounding/overflow.

CSV stores rows and columns as text. pandas parses them into a dataframe. The generated JSON report stores named metrics and decisions. NumPy represents numeric values as arrays for calculations. None of these formats establishes that the measurements are meaningful or unbiased.

## Predict before running

Consider an accepted record with missing latency. Should it become zero, be deleted, or remain missing? Write a reason before running the example. Then consider two different measurements sharing the same event key. Is choosing the first one defensible without further evidence?

Our documented policy retains missing latency and reports it. It keeps the first exact duplicate, but rejects every conflicting version of an event key. Other policies may be justified in other systems; an undocumented arbitrary choice is difficult to defend.

## Run the workflow

After [setup](../../setup/index.md), run from the repository root:

```sh
python examples/network-events/scripts/prepare.py --input data/samples/network-events/events.csv --output runs/module03
```

`python` should refer to the project environment; the setup page provides explicit Windows and Unix executable paths. The script imports `prepare_file` from `src/practical_ml_ai/data/events.py`. The notebook imports that same function. Neither contains a separate copy of the cleaning algorithm.

Download the [sample CSV](https://ntious.github.io/ml_ai_it/downloads/events.csv "site-download:events.csv"), [data contract](https://ntious.github.io/ml_ai_it/downloads/network-events.schema.json "site-download:network-events.schema.json"), [guided notebook](https://ntious.github.io/ml_ai_it/downloads/complete_walkthrough.ipynb "site-download:complete_walkthrough.ipynb"), or [complete source archive](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip"). The archive includes setup, data, package, scripts, and tests. Downloading a notebook alone does not install its dependencies or provide the package. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Inspect the result

The initial sample produces the following text evidence:

```text
Input records: 12
Accepted records: 6
Rejected records: 6
Accepted records with missing latency: 1
Observed accepted latency values: 5
Mean observed latency: 24 milliseconds
Median observed latency: 20 milliseconds
```

The six rejected rows consist of one exact duplicate, one invalid timestamp, one negative latency, one negative byte count, and two conflicting versions of the same event. A different dataset can have more than one rejection reason per row, so reason counts need not sum to rejected-row counts.

The report is meaningful without a chart. The five observed accepted latencies are 12, 18, 25, 45, and 20 milliseconds. Their sum is 120; dividing by 5 gives 24. The median after sorting is 20. The missing sixth value is not evidence of zero latency.

Inspect four generated files:

1. `cleaned_events.csv`: accepted records with normalized timestamps and numeric values.
2. `rejected_events.csv`: original field values, source row numbers, and rejection reasons.
3. `quality_report.json`: counts, numeric evidence, and policy notes.
4. `summary.txt`: a short text summary suitable for reading or comparing runs.

## Small NumPy calculation

An array has a shape and data type; these help explain what a calculation means. This example counts requests for two fictional services:

```python
import numpy as np
requests = np.array([12, 18, 20])
print("Shape:", requests.shape)
print("Total requests:", requests.sum())
print("Mean requests:", requests.mean())
```

The shape is a one-dimensional array of three values, total 50, and mean about 16.67. These counts are separate from the latency fixture above; do not mix their units.

A tiny linear-system illustration asks: two units of service A and one of B require eight resource units, while one of A and two of B require seven. Solve the simultaneous equations as an illustration, not a fitted ML model:

```python
coefficients = np.array([[2, 1], [1, 2]])
requirements = np.array([8, 7])
solution = np.linalg.solve(coefficients, requirements)
print("Resource units for A and B:", solution)
```

The solution is A = 3 and B = 2. Substituting them gives 2 times 3 plus 2 = 8, and 3 plus 2 times 2 = 7. Full linear-algebra derivations are optional.

## Preparation is not model fitting

This workflow validates field values and applies a fixed policy. It does not estimate replacement means, fit a scaler, choose features, or train a model. When those learned steps are introduced, fit them using training data and the appropriate cross-validation folds. Do not fit transformations on the complete dataset and then claim the held-out test data was untouched.

## Practice and continuation

Complete the [original practice, discussion, and self-checks](practice.md). Then inspect [worked feedback](feedback.md). Instructors can select individual sections and adapt the rubric; no automatic submission or grading rule applies.

## Selected readings

- Concept/reference: [NumPy beginner guide](https://numpy.org/doc/stable/user/absolute_beginners.html), focusing on shape and basic calculations.
- Reference while practicing: [pandas introductory tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html), focusing on read/write, filtering, and summary operations.
- Optional next concept: [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), focusing on preprocessing and leakage.

Read the named selections rather than assigning an entire documentation site. [Accessibility routes and limitations](../../accessibility/index.md) explain the verification status of the reading and execution interfaces.

## Earlier modules

For the complete beginner sequence, start with [Module 1: ML and AI foundations](../01-foundations/index.md), then [Module 2: Python workflows](../02-python-workflows/index.md). You may also use this data-processing module directly with its foundation support.

## Next module

Continue to [Module 4: Exploration and visual communication](../04-exploration/index.md) to investigate workload patterns with plots, underlying tables, and descriptions.

## Instructor adaptation

See [instructor guidance](instructor.md) for evidence selection, accessible routes, and local adoption.

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).
