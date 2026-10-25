# Module 5: Regression and reliable evaluation

Train a first ML model and ask whether it improves on a simple baseline. The real-data case forecasts tomorrow's bike rentals for a digitally operated sharing service. Its historical counts are not network traffic; an optional transfer question connects the workflow to IT demand.

No earlier notebook state, Canvas assignment, paid account, or GPU is needed. Allow 2–3 hours plus practice; this estimate needs piloting. Use the [foundation bridge](foundation.md), [Module 3](../03-data-processing/index.md), and [Module 4](../04-exploration/index.md) as needed.

## Learning outcomes

- **M05.1:** Explain a linear prediction, residual, and training loss numerically.
- **M05.2:** Fit a scikit-learn regression pipeline and compare it with a dummy baseline.
- **M05.3:** Choose features available at prediction time and identify leakage.
- **M05.4:** Justify train/validation/test boundaries and interpret MAE and residuals.
- **M05.5:** Report an operational interpretation, limitations, and reproducibility evidence.

## Define the forecast

At the end of a fully observed day, predict the following day's total rentals. The unit is one calendar day. We assume today's finalized count is available at issue time; a real system must establish its count-finalization time and time zone.

| Field | Role and timing |
| --- | --- |
| UCI dteday / cnt | Historical date / total daily rentals |
| prior_day_requests | Count one day before target; known at origin |
| prior_week_requests | Count seven days before target; known before origin |
| target_requests | Actual target-day count, unavailable at origin |

The implementation uses generic "requests" field names; here their unit is bike rentals. Tomorrow's measured weather, casual/registered rental components, and actual total arrive too late to be observed forecast inputs. A separately issued weather forecast could be considered under a different, documented contract.

## Data and license

[UCI Bike Sharing](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) supplies historical Capital Bikeshare counts from 2011–2012. We use its daily file. UCI lists CC BY 4.0.

Credit: Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. [DOI: 10.24432/C5W894](https://doi.org/10.24432/C5W894). The cached ZIP, day.csv, and README are unchanged; preparation selects date/count, constructs lags, and separates splits.

The downloader saves attribution, license, retrieval time, and actual archive/CSV SHA-256 digests. It checks the cached CSV before reuse. New archives must match the SHA-256 verified in the initial real-data CI run. If upstream bytes change, the downloader stops for source review rather than silently changing the teaching dataset. Retain that cache and provenance for exact replay.

The site also provides a [complete attributed data-cache ZIP](../../setup/student-workspace.md#reading-reports-from-github "site-download:module05/bike-sharing-cache.zip"). Extract its contents into runs/datasets/bike-sharing for a no-network replay; retain [attribution](../../setup/student-workspace.md#reading-reports-from-github "site-download:module05/ATTRIBUTION.txt"). The original-source ZIP keeps external downloaded data separate.

A separately labeled original synthetic fixture supports offline practice/tests. Its deliberately patterned values are not evidence of real operational performance.

## Install and download

Obtain a checkout or the [complete source archive](../../setup/student-workspace.md#reading-reports-from-github "site-download:ml_ai_it-source.zip"). Work in its ml_ai_it folder. Create the environment using [first run](../../../QUICKSTART.md), then install the extra dependencies.

Windows PowerShell:

~~~powershell
.\.venv\Scripts\python.exe -m pip install -e ".[regression,visualization]" -c environments/constraints-tested.txt
.\.venv\Scripts\python.exe examples/bike-demand/scripts/study.py download --run runs/datasets/bike-sharing
~~~

macOS/Linux:

~~~sh
.venv/bin/python -m pip install -e ".[regression,visualization]" -c environments/constraints-tested.txt
.venv/bin/python examples/bike-demand/scripts/study.py download --run runs/datasets/bike-sharing
~~~

First download and normally installation require internet access, with no account/key. Keep day.csv, original.zip, Readme.txt, provenance.json, and ATTRIBUTION.txt unchanged. An altered/incomplete cache produces an error; investigate or choose a new cache directory.

## Run distinct stages

Below, **python means your environment executable**: the Windows or Unix path above if not activated.

~~~sh
python examples/bike-demand/scripts/study.py prepare --input runs/datasets/bike-sharing/day.csv --run runs/module05 --holdout-days 110
python examples/bike-demand/scripts/study.py train --run runs/module05
python examples/bike-demand/scripts/study.py validate --run runs/module05
python examples/bike-demand/scripts/study.py evaluate --run runs/module05
python examples/bike-demand/scripts/study.py predict --run runs/module05
python examples/bike-demand/scripts/study.py report --run runs/module05 --plots --dataset-label "UCI Bike Sharing daily counts, CC BY 4.0"
~~~

Preparation requires a **new directory**. Training, selection, and final evaluation each refuse accidental repetition. These are protocol guards, not access control: the entire historical dataset is public. Repeated classroom runs are an evaluation rehearsal, not an independent blind benchmark.

One command can reproduce the complete demonstration:

~~~sh
python examples/bike-demand/scripts/study.py all --input runs/datasets/bike-sharing/day.csv --run runs/module05-complete --holdout-days 110 --plots --dataset-label "UCI Bike Sharing daily counts, CC BY 4.0"
~~~

For an explicitly synthetic offline route after installing dependencies:

~~~sh
python examples/bike-demand/scripts/study.py all --input data/samples/forecast-demand/daily.csv --run runs/module05-smoke --dataset-label "Original synthetic smoke fixture"
~~~

Without the plots flag, the same study still produces text, HTML tables, and CSV evidence; Matplotlib is then unnecessary.

## Preserve evaluation boundaries

Seven warm-up days supply lag history. The 731 real daily records yield 724 examples:

| Split | Target dates | Rows | Use |
| --- | --- | --- | --- |
| Training | January 8, 2011–May 25, 2012 | 504 | Fit parameters/preprocessing; training-only CV |
| Validation | May 26–September 12, 2012 | 110 | Compare predefined candidates and freeze a choice |
| Final test | September 13–December 31, 2012 | 110 | Evaluate frozen choice and predefined baselines |

No shuffling or overlapping targets is used. Chronology rehearses forecasting, but does not eliminate seasonality, dependence, growth, or distribution shift.

This is **rolling one-day-ahead prediction with fixed parameters**. At a later origin, an earlier holdout day's now-observed count may legitimately become a lag feature. These are not 110 forecasts issued together before the holdout began. No holdout targets fit parameters. The core lesson also does not silently refit on train plus validation after selection.

## Fit, compare, and freeze

A simple linear model predicts intercept plus coefficient times a feature. Ordinary least squares fits coefficients to minimize squared training residuals; this study compares held-out **MAE**, average absolute error in rentals/day.

Five candidates are predefined: a scikit-learn training-mean DummyRegressor, previous-day persistence, previous-week persistence, and two simple linear pipelines using either the prior-day or prior-week count. The lowest validation MAE wins, with alphabetical tie breaking. **A baseline may win.**

Each linear pipeline contains a training-fitted median imputer followed by LinearRegression. The daily dataset has no missing count targets; the imputer demonstrates the correct fitting boundary. It does not justify missing labels or absent calendar days. Expanding-window CV fits its own pipeline inside each training fold.

Saved numeric JSON exposes features, fill values, coefficients, and intercepts. Inference applies those numbers without fitting or executing an opaque model file. This exporter supports only the lesson's narrow model kinds.

## Interpret the evidence

Open runs/module05/index.html, or read summary.txt and the CSV/JSON files. The [generated worked report](../../setup/student-workspace.md#reading-reports-from-github "site-download:module05/example/index.html") supports reading without installation.

Residuals are **actual minus predicted**: positive means underprediction. MAE loses direction; inspect mean residual, largest errors, and date-ordered values too. Isolated errors and persistent underprediction may warrant different investigations. MAE also does not express unequal operational costs.

Optional actual/predicted and residual figures include alternatives, numerical descriptions, and a table of every selected prediction. Line style distinguishes the two series. Manual screen-reader, keyboard, zoom/reflow, and rendered-figure review remain pending for this increment.

Forecast.csv predicts the next day after the last observed day, without an actual target. It is historical inference practice, not an evaluated prediction or current demand forecast. Negative/fractional predictions are reported without hidden clipping/rounding; applications need explicit policies.

## Read selectively and continue

- **Core:** [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html): consistent preprocessing and leakage.
- **Core/reference:** [ordinary least squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares): equation and fit/predict.
- **Reference:** [MAE](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html): units and aggregation.
- **Optional:** [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html): expanding windows.

Read named sections; current docs may describe newer versions than the tested constraints. Use the [commented notebook](../../setup/student-workspace.md#reading-reports-from-github "site-download:module05/regression.ipynb") inside the complete source folder, complete [practice](practice.md), then compare [worked feedback](feedback.md). [Instructor adaptation notes](instructor.md) explain alignment and alternatives. [Module 6](../06-classification/index.md) introduces classification and decision trees.

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Generated downloads/report links require the built reading artifact. Use [workspace and report access](../../setup/student-workspace.md); source notebooks are under notebooks/lessons in the repository.
