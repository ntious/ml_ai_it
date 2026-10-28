# Completed-flow IoT intrusion triage

This optional IT transfer activity connects Modules 3, 6 and 12 without changing their outcomes. A network analyst reviews completed flows flagged as potentially hostile. The action is human review, not automated blocking.

## Run

Use the core environment with the regression extra, from the repository root:

```sh
python projects/rt-iot-triage/scripts/run.py --output runs/rt-iot-triage
```

The first run downloads a checksum-pinned archive; later runs reuse the verified cache. Choose a fresh output directory for a changed experiment. Inspect summary.json, label_counts.csv, validation.csv, evaluation.csv and predictions.csv.

## Source and data dictionary

S., B. & Nagapadma, R. (2023). RT-IoT2022 [Dataset]. UCI Machine Learning Repository. [DOI](https://doi.org/10.24432/C5P338). [Source and CC BY 4.0 license](https://archive.ics.uci.edu/dataset/942/rt-iot2022).

The archive contains 123,117 flow records from an IoT infrastructure with normal activity and staged attacks. It is a captured experimental environment, not a representative production fleet. We retain original source bytes in the cache; modeling selects five fields and derives a binary target. The unnamed index is excluded.

| Field | Role and availability |
| --- | --- |
| proto | Recorded transport protocol; categorical |
| service | Recorded service; categorical, despite inconsistent repository metadata |
| flow_duration | Recorded duration; available after observing the flow; confirm source units before operational use |
| fwd_pkts_tot | Forward packet count over the observed flow |
| bwd_pkts_tot | Backward packet count over the observed flow |
| Attack_type | Source-assigned scenario label, used only as the evaluation target |

MQTT_Publish, Thing_Speak and Wipro_bulb are the normal labels in the inspected file. The other nine labels are attacks. The webpage's descriptive label list differs from the archive; use the generated counts and original bytes as the reproducible evidence.

## Evaluation and decisions

Identical selected-feature profiles stay in one partition. A fixed split targeting 60/20/20 of unique input groups (row proportions differ when group sizes differ) supplies training, validation and final evaluation. Preprocessing is fitted on training only. Validation selects among four thresholds under an explicitly assumed 5:1 missed-attack/false-alert cost. Final evaluation compares logistic regression with always-review and never-review policies and reports the alert workload.

The file supplies no explicit capture-session, device identity or timestamp suitable for independent grouping. Profile grouping prevents identical-input overlap but cannot remove shared-capture dependence. Results describe this retrospective partition; they cannot establish future-device or future-attack performance. Full-flow features are unavailable at connection start. Source scenario labels are not analyst-confirmed future incident outcomes.

## Independent transfer task

Trace one source row through the five inputs, probability, threshold and review decision. Compare false-alert workload with available analyst capacity. Explain how a missing feature or unknown service should be handled. Propose a future evaluation using separate captures and delayed analyst labels before considering deployment.

For monitoring, retain aggregate volume, missing-input counts, unknown-service frequency and review workload. With delayed verified outcomes, inspect misses and false alerts by capture period. Route unavailable or malformed inputs to human review; a monitoring alert requests investigation, not automatic retraining. Preserve an earlier approved policy for rollback and record the reason for a change.

Use the [research comparison guide](../../docs/advanced/research-comparison.md) and [capstone checkpoints](../../docs/advanced/capstone-assessment.md) to document evidence and revisions.

## Download with the UCI Python client

The repository contains scripts, not this dataset. Downloads and generated results belong under the Git-ignored `runs/` directory.

For the UCI-provided Python interface:

```sh
python -m pip install ucimlrepo
python projects/rt-iot-triage/scripts/download.py
```

This calls `fetch_ucirepo(id=942)` and saves features, targets, variable information, metadata and a provenance record locally. Use a fresh `--output` directory to retain another retrieval. The client export is useful for exploration; its recorded checksums describe that retrieval and do not prove it is the same version as the course archive.

The complete study command above already downloads directly from UCI automatically. It uses the reviewed archive checksum so the tested experiment has a stable input. It does not silently substitute a newer client export.

Additional UCI datasets can follow this pattern after checking each dataset's license, citation, fields, label meaning and evaluation boundaries. Availability through the same client does not make their schemas or appropriate split strategies interchangeable.
