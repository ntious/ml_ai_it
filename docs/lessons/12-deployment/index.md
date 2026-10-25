# Module 12: Deployment and monitoring

Expose shared model inference through a checked local app and rehearse monitoring with actual held-out records.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M12.1:** Define an input/output contract and reject invalid requests.
- **M12.2:** Serve the same trained classifier and a bounded local LLM workflow through Streamlit.
- **M12.3:** Replay actual held-out records and measure prediction duration/outcomes.
- **M12.4:** Distinguish batch diagnostics from genuine time drift and production service guarantees.
- **M12.5:** Propose ownership, escalation, monitoring, and rollback criteria.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

Training and serving must use the same feature order, transformation, and threshold. Schema validation protects the contract, but does not guarantee in-distribution inputs. Monitoring combines input quality, score/outcome behavior, resource cost, and operational responsibilities.

## Real data and its limits

UCI Wine Quality and SMS Spam Collection; actual records supply app defaults, inference, and replay. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The app's default numeric values come from one actual held-out wine record. Checked inference rejects missing/extra fields, booleans, nonfinite values, and a documented technical range; it flags departures from observed training ranges. A separate form performs local LLM triage with strict rejection. Four actual-record batches measure durations and a training-referenced mean-shift diagnostic; source row order is not event time.

## Run and inspect

Download the [complete source](../../setup/student-workspace.md#reading-reports-from-github "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). The tested framework route is Linux CPU; Windows/macOS framework execution remains unverified. Reading the reports needs no framework installation. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/model-service/scripts/run.py --output runs/module12
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module12/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](../../setup/student-workspace.md#reading-reports-from-github "site-download:module12/example/index.html") without installing an execution interface.

Key artifacts:

- batch_monitoring.csv
- prediction_log.csv
- service_contract.json

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](../../setup/student-workspace.md#reading-reports-from-github "site-download:module12/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. Operating a notebook/app interface is a separate skill; manual screen-reader, keyboard, zoom/reflow, and interface usability remain pending.

To launch the local interface after installing the deployment/framework extras:

~~~sh
python -m streamlit run apps/wine_quality.py --server.address 127.0.0.1
~~~

The app has classifier and local-LLM forms. The CLI/text report remains a usable route when an interface is a barrier.

## Read selectively

- **Core concept/reference:** [Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest) — form interaction, exceptions, and test limitations. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Package a local container or add an authenticated service only under an explicit deployment plan. Do not expose the teaching app publicly by default. An extra platform is optional, with its own validation burden.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 13](../13-ethics-fairness/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Generated downloads/report links require the built reading artifact. Use [workspace and report access](../../setup/student-workspace.md); source notebooks are under notebooks/lessons in the repository.
