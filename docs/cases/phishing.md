# Authentic IT case: historical website phishing

A security analyst wants a review queue for potentially phishing websites. We use real recorded URL/host/content attributes from [UCI Phishing Websites](https://archive.ics.uci.edu/dataset/327/phishing+websites), not synthetic incidents. Citation: Mohammad, R. & McCluskey, L. (2012), DOI 10.24432/C51W2X. UCI lists CC BY 4.0. The reviewed archive SHA-256 is 514f582cb44cba17251baf1d59f64cddff16efa2b644d091ce8d2a1e8d492940. Original archived files remain unchanged in the runtime cache.

## Task and observation

One row is a recorded website feature profile, with 30 encoded attributes and the source's Result label. The selected Training Dataset.arff contains 11,055 records. Original Result=-1 is phishing and +1 is legitimate; our positive label is phishing. Inputs include URL patterns, domain/host attributes and content-derived indicators. Values -1, 0 and 1 encode source-defined categories, not a physical continuous scale. Retain the source feature descriptions when interpreting them.

A false positive wastes investigation and may disrupt access; a false negative misses an attack. This example ranks/classifies historical profiles for review. It does not justify automatic blocking or teach a live URL crawler. No websites are visited and no credentials or real customer records are required.

## Run separate pipeline stages

Use the [core environment](../../QUICKSTART.md), including the regression extra, from the project root. Python below means that environment's executable. First download needs internet; later runs reuse checksum-verified cache files.

```sh
python scripts/phishing_study.py prepare --output runs/phishing
python scripts/phishing_study.py train --output runs/phishing
python scripts/phishing_study.py validate --output runs/phishing
python scripts/phishing_study.py evaluate --output runs/phishing
python scripts/phishing_study.py report --output runs/phishing
```

Alternatively run all stages with `python scripts/phishing_study.py all --output runs/phishing-new`. Use a new directory for each study. Open its index.html, protocol.json, validation_scores.csv and test_scores.csv. The [combined notebook](https://github.com/ntious/ml_ai_it/blob/main/notebooks/cases/phishing.ipynb) calls those same stages from a complete checkout.

## Boundaries and interpretation

Preparation groups identical feature profiles and excludes profiles with conflicting labels. Grouped seeded splits approximate 60/20/20; actual row counts are reported. There are no usable domain/campaign identifiers or event-time contract in this implementation, so independence across those units and prospective performance remain unknown.

Training fits a dummy, logistic model, depth-limited tree and bounded forest on training only. Inference on held-out inputs is precomputed with frozen parameters; test labels do not enter fitting. Validation selects by balanced accuracy at the predeclared 0.5 threshold. Evaluation reports the frozen choice and dummy; report generation cannot choose a replacement. No model pickle is loaded. Stage guards demonstrate protocol and do not hide the public test file.

## Construct, critique and transfer

Before execution, state why each feature could be available at the review decision. Investigate whether a source indicator could depend on later blacklist knowledge. After execution, explain exclusions, compare the three substantive models with the dummy on validation, reconcile final confusion counts and state why historical performance does not establish present-day attack detection.

For a development extension, one-hot encode the categorical indicators and compare with treating them numerically. Declare the change before selection, explain resource tradeoffs, and preserve final boundaries. Reusing public final results is rehearsal, not fresh evidence.

Transfer the same contract to a service desk, healthcare support system, educational platform or another approved domain. Do not relabel phishing records as those domains. A genuine transfer needs real observation definitions, source rights, entity/time grouping, labels, costs and a nondeployment option.
