# Module 4: Exploration and visual communication

Explore a service-workload table, choose useful charts, and communicate what the data support. You will run a repeatable analysis that produces figures, their actual data tables, and written descriptions. This is descriptive exploration, with no model training. No paid AI account, GPU, earlier notebook state, or Canvas assignment is required. Allow 90–120 minutes plus setup and practice; this estimate needs learner piloting.

## Learning outcomes

- **M04.1:** Justify a preprocessing choice for an exploratory question and explain what information it may remove.
- **M04.2:** Create labeled distribution, comparison, and relationship/time plots with appropriate scales and units.
- **M04.3:** Explain a pattern or anomaly with numerical evidence while distinguishing association from causation.
- **M04.4:** Write a stakeholder summary with chart descriptions, underlying values, and limitations.

You need basic functions, file paths, and dataframe selection/grouping. Use the [foundation bridge](foundation.md), [Module 2](../02-python-workflows/index.md), or [Module 3](../03-data-processing/index.md) as needed. You may enter here directly with the complete source archive and setup below.

## A question before a chart

A fictional operations lead asks: “How do request totals differ between two services, and which daily observations deserve investigation?” The unit of observation is **one service on one UTC calendar date**, not an individual request. The fixture covers January 1–12, 2027; these are invented dates and values, not measured future operations.

| Field | Meaning |
| --- | --- |
| `date` | UTC calendar date in `YYYY-MM-DD` format |
| `service` | Authentication gateway or network monitor; whitespace/case normalized to the documented names |
| `requests` | Nonnegative request count for that service-day |
| `p95_latency_ms` | An already aggregated per-service daily 95th-percentile latency, in milliseconds; blank means unavailable |

A 95th percentile is a value at or below which roughly 95% of the underlying observations fall, depending on the estimation method. Here it is supplied as a fictional daily aggregate. The mean or median of these daily service p95 values is **not an overall request-level p95**; obtaining that would require the relevant request-level distribution or an appropriate mergeable representation.

## Choose preprocessing deliberately

The raw sample contains 25 rows. Normalize the one inconsistent service label, retain the first exact duplicate, and obtain 24 distinct observations. Stop if different measurements share the same date/service key. Keep raw files unchanged.

One observation has missing latency. Retain its 130 requests for workload totals; omit it only from latency-specific views. Dropping the whole row would answer a different question with a smaller workload total. Do not replace unavailable latency with zero.

The 160 ms value is deliberately constructed as a spike, not a known recording error. A 1.5-IQR rule flags it for investigation. IQR is the upper quartile minus the lower quartile; the example uses pandas' default linear-interpolation quantiles. The fences are 10 and 58 ms. Keep the flagged observation and describe it. A statistical flag is not proof that a value is wrong.

Missing date/service rows are not inferred to mean zero traffic. Totals describe only supplied observations. The daily table reports service coverage; the time plot breaks its line across entirely absent dates. In this fixture, both services are present on all 12 dates.

## Setup and run

Obtain a checkout or extract the [complete source archive](../../setup/student-workspace.md#reading-reports-from-github "site-download:ml_ai_it-source.zip"). Open a terminal in `ml_ai_it`. Follow the [environment instructions](../../../QUICKSTART.md#module-3-add-the-data-libraries) if you do not yet have `.venv`. Install the additional plotting libraries into that same environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[visualization]" -c environments/constraints-tested.txt
.\.venv\Scripts\python.exe examples/service-workload/scripts/explore.py --input data/samples/service-workload/daily.csv --output runs/module04
```

macOS or Linux:

```sh
.venv/bin/python -m pip install -e ".[visualization]" -c environments/constraints-tested.txt
.venv/bin/python examples/service-workload/scripts/explore.py --input data/samples/service-workload/daily.csv --output runs/module04
```

The visualization extra adds Matplotlib and Seaborn; NumPy/pandas remain the shared data dependencies. Internet access is normally needed for installation. No dataset download occurs at runtime. Open `runs/module04/index.html` in a browser, or read `summary.txt`, `chart_descriptions.md`, and the paired CSV tables using your preferred editor. Rerunning replaces these generated outputs; use another directory to retain an experiment.

You can also [read the generated worked example](../../setup/student-workspace.md#reading-reports-from-github "site-download:module04/example/index.html") without installing Python. It contains five figures, short alternatives, detailed descriptions, and labeled HTML tables. This is a teaching demonstration, not a restricted assessment answer.

## Match the chart to the question

| Question | Example and implementation | Evidence beyond the image |
| --- | --- | --- |
| How are observed latencies distributed? | Matplotlib histogram with stated bin boundaries | Bin-count table, observed/missing counts, mean and median |
| Which service has more supplied requests? | pandas bar plot, zero baseline | Exact service totals and observation coverage |
| How do totals change over the supplied dates? | Matplotlib time line with markers | Daily totals and services observed; date gaps remain gaps |
| Do requests and daily service p95 vary together? | Seaborn scatter plot with color and marker shape | All complete date/service pairs; note overlapping points |
| How can a scale exaggerate differences? | The same bars on zero and cropped baselines | Unchanged totals; clearly labeled misleading example |

The four analytical figures share the same cleaned observations, but use the rows relevant to their question. The fifth is an axis-design demonstration. A bar's length encodes magnitude, so cropping its baseline distorts that comparison. Not every line or scatter plot must start at zero; choose and explain a scale appropriate to its question.

## Inspect named results

| Measure | Expected value |
| --- | --- |
| Input rows / distinct observations | 25 / 24 |
| Exact duplicate removed / labels normalized | 1 / 1 |
| Total requests | 4,180 |
| Gateway / monitor requests | 1,860 / 2,320 |
| Observed / unavailable daily service p95 values | 23 / 1 |
| Mean / median of observed daily service p95 | About 38.70 ms / 34 ms |
| Highest daily combined requests | 560 on January 7 |
| Retained IQR flag | Network monitor, January 7, 160 ms |

The histogram bins are `[0,40)`: 16 observations, `[40,80)`: 6, `[80,120)`: 0, `[120,160)`: 0, and `[160,200]`: 1. The scatter contains 23 observations, some at identical coordinates. Its table preserves every pair even when marks overlap.

A defensible summary says that the fictional January 7 monitor observation combines 400 requests and 160 ms daily p95. It does not say traffic caused latency or that these 12 constructed days predict production reliability. Before investigating a real anomaly, ask about instrumentation, coverage, changes, and operational context.

## Shared code and notebook

The script imports `src/practical_ml_ai/exploration.py`. `read_workload` documents validation/normalization, `summarize_workload` produces numerical evidence and plot tables, and `render_charts` creates labeled figures. `run_exploration` writes the report and returns the summary. The [guided notebook](../../setup/student-workspace.md#reading-reports-from-github "site-download:module04/exploration.ipynb") calls these same functions; keep it within the complete source folder and follow [notebook setup](../../../QUICKSTART.md#notebook-option).

Saved outputs include normalized observations, `summary.json`, named text values, per-chart CSVs/PNGs, descriptions, and an HTML report. HTML tables have captions and column headers. Charts use labels and, where grouping matters, marker shapes as well as colors. These provisions need manual task-based testing; [interface test coverage and effective routes](../../accessibility/index.md).

## Read selectively

- **Core concepts:** [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html): a Figure and Axes, plotting, labels, and legends.
- **Core/reference:** [pandas descriptive statistics](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html): count, mean, and percentiles; check which values are missing.
- **Implementation reference:** [Seaborn statistical relationships](https://seaborn.pydata.org/tutorial/relational.html): scatter plots and using style alongside hue. Our example reads local synthetic data, rather than the tutorial's internet-loaded dataset.
- **Accessibility reference:** [WAI complex images](https://www.w3.org/WAI/tutorials/images/complex/): short alternatives plus detailed descriptions and data.

Read only the named sections. Current documentation may describe newer versions than the tested environment; the repository records its exercised versions.

Complete [practice and the operations memo](practice.md), then consult [worked feedback](feedback.md). [Module 5](../05-regression/index.md) introduces regression and held-out evaluation. When exploration informs model choices, use training/development data and preserve final test data for its planned evaluation; no predictive evaluation is performed here.

## Instructor adaptation

See [instructor guidance](instructor.md) for evidence selection, accessible routes, and local adoption.

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Generated downloads/report links require the built reading artifact. Use [workspace and report access](../../setup/student-workspace.md); source notebooks are under notebooks/lessons in the repository.
