"""Completed, annotated capstone report rendered from frozen run evidence."""
from pathlib import Path
import json
import pandas as pd

from .continuation_data import publish_report


def markdown_table(frame):
    def cell(value):
        if pd.isna(value):
            return "unavailable"
        if isinstance(value, float):
            return f"{value:.4f}"
        return str(value).replace("|", "/")
    return "| " + " | ".join(frame.columns) + " |\n| " + " | ".join("---" for _ in frame.columns) + " |\n" + "\n".join("| " + " | ".join(cell(value) for value in row) + " |" for row in frame.itertuples(index=False, name=None))


def write_report(run):
    run = Path(run)
    load = lambda name: json.loads((run / name).read_text(encoding="utf-8"))
    evaluation, selection, config, audit = (load(name) for name in ["evaluation.json", "selection.json", "config.json", "data_audit.json"])
    current, baseline = evaluation["ensemble"], evaluation["baseline"]
    tuning = load("tuning.json")
    choices = pd.DataFrame([{"family": family, "parameters": json.dumps(row["parameters"], sort_keys=True),
                             "mean_cv_balanced_accuracy": row["mean_cv_balanced_accuracy"]} for family, row in tuning["selected"].items()])
    development = pd.read_csv(run / "validation_stability.csv")
    final = pd.read_csv(run / "final_scores.csv")
    intervals = pd.read_csv(run / "profile_bootstrap.csv")
    monitoring = pd.read_csv(run / "monitoring_rehearsal.csv")
    profile = pd.read_csv(run / "training_profile.csv")
    association = profile.loc[profile.observations >= 30].groupby("feature").observed_positive_rate.agg(["min", "max"]).reset_index()
    association["difference"] = association["max"] - association["min"]
    association = association.sort_values(["difference", "feature"], ascending=[False, True]).head(5)
    seed_stability = pd.read_csv(run / "final_seed_stability.csv")
    tables = {"cv_choices": choices, "development_stability": development, "heldout_metrics": final, "training_seed_variation": seed_stability,
              "training_associations": association,
              "illustrative_intervals": intervals, "offline_monitoring": monitoring,
              "reliability_bins": pd.read_csv(run / "final_calibration.csv")}
    split_run = (run / "split-study.done.json").is_file()
    if split_run:
        tables["development_split_sensitivity"] = pd.read_csv(run / "split_sensitivity.csv")
    names = ["report.md", "summary.json", "summary.txt", "index.html", *[name + ".csv" for name in tables]]
    if any((run / name).exists() for name in names):
        raise ValueError("Partial report outputs exist; do not overwrite them. Start a new run.")
    notes = [
        "Historical UCI Phishing Websites, DOI:10.24432/C51W2X, CC BY 4.0. No live URLs, customer records or credentials are used.",
        "Hyperparameters use group CV inside training. Threshold/family choices use mean validation cost across the predeclared training seeds. Final labels select neither configuration nor seed.",
        "Every stochastic run is reported; no best-seed cherry-picking. Seed standard deviation is conditional on fixed data and is not a confidence interval for generalization.",
        "The profile bootstrap is illustrative and conditional on the split and frozen models; exact-profile grouping cannot establish domain/campaign/time independence.",
        "Source-order monitoring is an offline rehearsal. The release decision rejects live deployment pending prospective evidence, feature-availability review and operational approval.",
    ]
    summary = {"project": "phishing-triage", "selected_family": selection["family"], "threshold": selection["threshold"],
               "training_seeds": config["training_seeds"], "inner_cv_fits": tuning["fits"],
               "evaluation": evaluation, "split_sensitivity_run": split_run, "live_deployment_approved": False}
    publish_report(run, "Complete capstone exemplar: historical phishing triage", summary, tables, notes)
    report = f'''# Completed capstone: reproducible historical phishing triage

## Abstract and decision

This study investigates whether a bounded classifier could help an analyst
prioritize a review queue on a historical benchmark. Training-only group CV
compares logistic regression, a decision tree and a random forest. Validation
selects **{selection['family']}**, using an illustrative false-negative:false-positive
cost ratio of {config['false_negative_cost']}:{config['false_positive_cost']}, and threshold
**{selection['threshold']:.2f}**. The frozen ensemble's final balanced accuracy is
**{current['balanced_accuracy']:.4f}**; cost is **{current['cost_per_1000']:.2f} units per
1,000 benchmark records**, versus **{baseline['cost_per_1000']:.2f}** for the training-prior
baseline at its validation-selected threshold. These units are a teaching
assumption, not measured financial losses.

**Decision: do not deploy for live blocking.** Complete a permitted prospective
data and feature-availability assessment before considering a monitored triage pilot.

> Annotation: lead with the question, evidence and decision. A high benchmark
> score is neither a business case nor permission to deploy.

## 1. Questions and source context

RQ1: Which declared model family best meets the development error-cost criterion?
RQ2: How much do predictions and metrics change across training seeds on fixed data?
RQ3: Separately, how sensitive are development results to the choice of data partition?

The [UCI source](https://archive.ics.uci.edu/dataset/327/phishing+websites) provides
11,055 historical website profiles and 30 encoded attributes. Its introductory
paper is Mohammad, Thabtah and McCluskey (2012), *An assessment of features related
to phishing websites using an automated technique*. This example uses its data
context; it does not replicate that paper's reported experiment or assert current
attack performance. The runtime provenance records the original archive hash,
retrieval information and CC BY 4.0 attribution.

## 2. Data preparation and decision-time constraints

The positive class is original Result=-1. Exclude the target from all inputs,
remove profiles with conflicting labels and keep identical encoded profiles
together. The outer 60/20/20 approximate grouped split is fixed using seeds
42/43; actual counts are in protocol.json. Training has **{audit['training_rows']}**
rows, **{audit['training_positives']}** positives and **{audit['training_missing_cells']}**
missing cells. training_profile.csv provides every feature's observed category counts.

All 30 inputs are source-coded categories in -1/0/+1. One-hot encoding is fitted
inside each training fold and ignores unknown encoded categories during model
comparison. The delivery contract is deliberately stricter and rejects values
outside the declared source domain. Feature names alone do not establish when
the underlying signals would be available; blacklist/reputation-derived fields
need a prospective audit. No domain/campaign/time identifiers establish independence.

> Annotation: a structural dictionary and correct encoding do not replace the
> source's semantic feature documentation or a decision-time availability audit.

### Training-only exploratory associations

The table shows the five largest differences in observed positive-label rates
between source categories with at least 30 training records. It is descriptive
training exploration, not causal attribution, held-out evidence or a new
feature-selection rule. All declared features remain in the experiment.

{markdown_table(association)}

## 3. Experiment protocol and bounded search

The protocol predeclares {config['cv_folds']} training-only StratifiedGroupKFold
folds, CV seed {config['cv_seed']}, candidate-fit seed {config['search_seed']},
thresholds {config['thresholds']}, training seeds {config['training_seeds']} and
a maximum of {config['max_cv_fits']} CV fits. This run uses **{tuning['fits']}** CV fits.
Every candidate/fold score and measured duration is in search_trials.csv.
inner_folds.json allows an independent check that profiles never cross folds.
Fold preprocessing never sees validation/final records.

{markdown_table(choices)}

The best mean training-CV balanced accuracy selects one configuration per family;
stable parameter-JSON order breaks exact ties. These winning CV scores are
selection-reused, not unbiased generalization estimates. We retain a separate
outer validation set and final evaluation; nested CV is an optional investigation,
not claimed by this run.

## 4. Validation, thresholds and seed stability

Fit each selected configuration on the same training partition for every declared
training seed. For each family, choose one common threshold by minimum mean
validation cost across seeds, then higher mean balanced accuracy, then threshold
order. Choose the family by that same mean-cost criterion. The dummy is eligible
to win. Logistic lbfgs is deterministic for this setup; repeated identical
results are expected and do not establish generalization certainty.

{markdown_table(development[['family','count','mean','std','min','max','balanced_accuracy_mean','balanced_accuracy_std']])}

The mean/std/min/max columns refer to validation cost per 1,000 records; the
balanced_accuracy columns report that metric separately. The complete CSV also
contains recall and precision variation.

Do not report only the best seed. Standard deviation/range describe sensitivity
to training randomness on these fixed observations. They do not measure sampling
uncertainty or future data shift. The serving policy is predeclared probability
averaging over all selected-family seeds, not a test-selected representative run.
The threshold is selected for mean individual-seed validation cost; ensemble
averaging is fixed in advance, not separately optimized against test outcomes.

### Separate development split investigation

Split-sensitivity experiment executed: **{split_run}**. When executed, only the
original training partition is re-split by profile for seeds {config['split_seeds']};
the estimator seed stays fixed at {config['search_seed']}. Original outer validation
and test records never enter this study. Its scores are descriptive: the
configuration already used these training observations in CV. Different split
scores are not independent samples and are not candidates for a best-seed choice.

## 5. Frozen final evaluation and uncertainty

selection.json locks family, common threshold, all seeds, ensemble rule and model
hashes before final labels are parsed. Evaluate the entire declared seed set,
its fixed ensemble and the baseline as one frozen evaluation stage. Nothing in
the stage chooses a replacement configuration.

{markdown_table(final[['method','seed','tp','fp','fn','tn','balanced_accuracy','cost_per_1000','brier']])}

{markdown_table(seed_stability)}

This seed summary describes training variation; the fixed ensemble is a separate
predeclared prediction policy, not another seed or an optimized best run.

{markdown_table(intervals)}

The intervals resample whole exact-profile groups {config['bootstrap_repetitions']}
times with seed {config['bootstrap_seed']}. They illustrate uncertainty conditional
on this split and trained models. They do not correct campaign dependence,
historical selection bias or hyperparameter-selection uncertainty, and do not
guarantee population coverage. Brier loss and final_calibration.csv describe
probability behavior; the model is not labelled calibrated merely because its
classifications are accurate.

## 6. Errors and practical consequences

The frozen ensemble makes **{current['fp']} false positives** and **{current['fn']}
false negatives**. Inspect every error in error_analysis.csv, joined to source
attributes by record_id when needed. These are encoded profiles, not browsable
URLs or real incidents to investigate. A queue-capacity or cost claim needs
actual operational evidence and a predeclared sensitivity analysis.

> Annotation: discuss what the mistakes mean and what additional evidence could
> change the decision. Do not invent a causal explanation from a row identifier.

## 7. Inference, monitoring and rollback

inference_bundle.json contains only numeric model parameters and categories,
without executable pickle. Exported probabilities are checked against fitted
estimators; bundle replay matches the frozen prediction table. example_request.json
and example_response.json demonstrate the exact schema. Missing features, target
leakage fields, booleans and unknown categories are rejected in service_checks.json.

monitoring_rehearsal.csv reports four source-order batches, category-frequency
changes and retrospectively known outcome metrics. The order is not time and
cannot establish production drift or latency objectives. The measured example
prediction duration is one local call, not an HTTP service-level guarantee.

The service owner and security/data-governance reviewers must approve permitted
inputs, human oversight, queue capacity, delayed-label collection and measurable
objectives before live use. On schema or model failure, route to manual review.
Rollback stops automated flags, retains version/hash and the incident record,
and returns to the manual queue. release_decision.json records that live
deployment is **not approved**.

## 8. Reproduction and threats to validity

Run the project CLI's all stage in a new directory. Each stage completion marker
hashes outputs and parent markers; environment.json records runtime versions and
source hashes. verify checks the complete ledger. all --resume skips only verified
completed stages; partial stages are not overwritten and require a new run.
The original modules and shorter phishing case remain independently runnable.

These are public historical teaching data. Repeated experimentation after seeing
their results is development/rehearsal, not a new blinded study. Grouping exact
profiles does not identify sites or campaigns. The declared illustrative cost policy,
small seed set, bounded search, encoded features and missing prospective
validation limit the conclusions. Human learner/accessibility testing and actual
service deployment are outside this executed experiment.

## 9. References and artifact guide

- UCI Phishing Websites, DOI:10.24432/C51W2X; original archive/provenance retained.
- [scikit-learn grouped CV](https://scikit-learn.org/1.8/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html).
- [scikit-learn hyperparameter search](https://scikit-learn.org/1.8/modules/grid_search.html).
- config.json, environment.json, data_audit.json: declared protocol and source identity.
- search_trials.csv, inner_folds.json, tuning.json: full bounded search record.
- validation_runs.csv, validation_stability.csv, validation_thresholds.csv: development decisions.
- selection.json, final_predictions.csv, final_scores.csv: frozen final evaluation.
- profile_bootstrap.csv, error_analysis.csv, final_calibration.csv: uncertainty and diagnosis.
- inference_bundle.json, service_checks.json, release_decision.json: delivery contract and decision.

> Annotation: this is a completed worked example, not a submission to copy.
> A student's transfer must justify its own task, rights, boundaries, experiments
> and recommendation, following the adopting course's assessment requirements.
'''
    (run / "report.md").write_text(report, encoding="utf-8")
    return names
