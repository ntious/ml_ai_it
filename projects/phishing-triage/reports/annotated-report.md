# Completed capstone: reproducible historical phishing triage

## Abstract and decision

This study investigates whether a bounded classifier could help an analyst
prioritize a review queue on a historical benchmark. Training-only group CV
compares logistic regression, a decision tree and a random forest. Validation
selects **forest**, using an illustrative false-negative:false-positive
cost ratio of 5:1, and threshold
**0.30**. The frozen ensemble's final balanced accuracy is
**0.9410**; cost is **103.94 units per
1,000 benchmark records**, versus **570.95** for the training-prior
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
42/43; actual counts are in protocol.json. Training has **6473**
rows, **2903** positives and **0**
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

| feature | min | max | difference |
| --- | --- | --- | --- |
| URL_of_Anchor | 0.0540 | 0.9906 | 0.9365 |
| SSLfinal_State | 0.1038 | 0.9875 | 0.8837 |
| Prefix_Suffix | 0.0000 | 0.5179 | 0.5179 |
| web_traffic | 0.2524 | 0.7082 | 0.4558 |
| having_Sub_Domain | 0.1943 | 0.6372 | 0.4429 |

## 3. Experiment protocol and bounded search

The protocol predeclares 3 training-only StratifiedGroupKFold
folds, CV seed 29, candidate-fit seed 17,
thresholds [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], training seeds [11, 23, 37, 53, 71] and
a maximum of 60 CV fits. This run uses **30** CV fits.
Every candidate/fold score and measured duration is in search_trials.csv.
inner_folds.json allows an independent check that profiles never cross folds.
Fold preprocessing never sees validation/final records.

| family | parameters | mean_cv_balanced_accuracy |
| --- | --- | --- |
| logistic | {"C": 1.0} | 0.9518 |
| tree | {"max_depth": 6} | 0.9400 |
| forest | {"max_depth": 10, "min_samples_leaf": 3, "n_estimators": 40} | 0.9549 |

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

| family | count | mean | std | min | max | balanced_accuracy_mean | balanced_accuracy_std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dummy | 1 | 553.3522 | unavailable | 553.3522 | 553.3522 | 0.5000 | unavailable |
| forest | 5 | 90.2738 | 2.7409 | 85.9301 | 93.4844 | 0.9531 | 0.0009 |
| logistic | 5 | 100.0944 | 0.0000 | 100.0944 | 100.0944 | 0.9465 | 0.0000 |
| tree | 5 | 130.3116 | 0.0000 | 130.3116 | 130.3116 | 0.9192 | 0.0000 |

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

Split-sensitivity experiment executed: **True**. When executed, only the
original training partition is re-split by profile for seeds [101, 202, 303];
the estimator seed stays fixed at 17. Original outer validation
and test records never enter this study. Its scores are descriptive: the
configuration already used these training observations in CV. Different split
scores are not independent samples and are not candidates for a best-seed choice.

## 5. Frozen final evaluation and uncertainty

selection.json locks family, common threshold, all seeds, ensemble rule and model
hashes before final labels are parsed. Evaluate the entire declared seed set,
its fixed ensemble and the baseline as one frozen evaluation stage. Nothing in
the stage chooses a replacement configuration.

| method | seed | tp | fp | fn | tn | balanced_accuracy | cost_per_1000 | brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| selected_seed | 11.0000 | 882 | 117 | 22 | 1086 | 0.9392 | 107.7361 | 0.0409 |
| selected_seed | 23.0000 | 881 | 103 | 23 | 1100 | 0.9445 | 103.4646 | 0.0401 |
| selected_seed | 37.0000 | 883 | 125 | 21 | 1078 | 0.9364 | 109.1599 | 0.0406 |
| selected_seed | 53.0000 | 882 | 121 | 22 | 1082 | 0.9375 | 109.6346 | 0.0400 |
| selected_seed | 71.0000 | 879 | 112 | 25 | 1091 | 0.9396 | 112.4822 | 0.0411 |
| frozen_ensemble | unavailable | 883 | 114 | 21 | 1089 | 0.9410 | 103.9393 | 0.0400 |
| training_prior | unavailable | 904 | 1203 | 0 | 0 | 0.5000 | 570.9540 | 0.2453 |

| metric | count | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| balanced_accuracy | 5 | 0.9395 | 0.0031 | 0.9364 | 0.9445 |
| precision | 5 | 0.8841 | 0.0075 | 0.8760 | 0.8953 |
| recall | 5 | 0.9750 | 0.0017 | 0.9723 | 0.9768 |
| cost_per_1000 | 5 | 108.4955 | 3.2984 | 103.4646 | 112.4822 |
| brier | 5 | 0.0405 | 0.0005 | 0.0400 | 0.0411 |

This seed summary describes training variation; the fixed ensemble is a separate
predeclared prediction policy, not another seed or an optimized best run.

| metric | low | high | repetitions |
| --- | --- | --- | --- |
| balanced_accuracy | 0.9252 | 0.9560 | 200 |
| recall | 0.9632 | 0.9880 | 200 |
| cost_per_1000 | 74.4938 | 139.9584 | 200 |

The intervals resample whole exact-profile groups 200
times with seed 907. They illustrate uncertainty conditional
on this split and trained models. They do not correct campaign dependence,
historical selection bias or hyperparameter-selection uncertainty, and do not
guarantee population coverage. Brier loss and final_calibration.csv describe
probability behavior; the model is not labelled calibrated merely because its
classifications are accurate.

## 6. Errors and practical consequences

The frozen ensemble makes **114 false positives** and **21
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
