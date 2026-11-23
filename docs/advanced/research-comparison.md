# Compare research before borrowing a result

Use research to justify an experiment design, not to decorate a report with citations. Choose primary studies with accessible methods and evidence. Read beyond the abstract and record a page, section or table for each empirical claim.

## Build an evidence table

| Field | What to record |
| --- | --- |
| Question | What decision or hypothesis does the study examine? |
| Data and population | Source, period, sample size, exclusions and unit of observation |
| Target | How labels were obtained, when available and likely errors |
| Evaluation | Entity/time boundaries, validation selection and final evaluation |
| Comparison | Baselines, search budget and compute constraints |
| Result | Metric, denominator, uncertainty and exact source location |
| Validity threat | A limitation that could change the conclusion |
| Course decision | What you will adopt, change or investigate |

## Distinguish comparable evidence

A high score on randomly split historical URLs cannot be directly ranked against a score on future domains, even when both tasks are called phishing detection. Population, label, decision time and split may all differ. Describe that mismatch before discussing algorithms. If a paper does not report a detail, mark it unreported rather than infer it.

Use the [capstone exemplar](../../projects/phishing-triage/README.md) to distinguish an implementation reproduction from a new empirical claim. Its encoded benchmark cannot establish performance on newly arriving raw messages or domains.

## Worked example: variance in benchmarks versus the capstone

This completed comparison models the evidence table. The source is Bouthillier, X., Delaunay, P., Bronzi, M., et al. (2021). [*Accounting for Variance in Machine Learning Benchmarks*](https://arxiv.org/abs/2103.03098). arXiv:2103.03098 (v1, 1 March 2021; submitted to MLSys 2021). Locations refer to that version's numbered sections and figures.

| Field | Bouthillier et al. (2021) | Course capstone |
| --- | --- | --- |
| Question | Which sources of variation change benchmark conclusions, and how should comparisons account for them? (§1–§2) | Which model family and threshold should be frozen for historical phishing triage under an assumed 5:1 miss/false-alert cost? |
| Data and population | Five case studies: CIFAR10 classification with VGG11; PascalVOC segmentation with an FCN on a ResNet18 backbone; GLUE SST-2 and RTE with BERT; MHC I peptide-binding prediction with a shallow MLP (§2.2, "Cases studied"; Appendix D) | UCI Phishing Websites encoded attributes. Identical profiles are grouped across one fixed outer split; 2,107 final-test records |
| Target | Each benchmark's published labels | Source label `Result = -1` (phishing) |
| Evaluation | Each source of variance is randomized separately with 200 seeds, and 20 independent hyperparameter searches of 200 trials each are run per method (§2.2). The authors recommend multiple data splits, for example out-of-bootstrap, over one fixed test set (§1, §5; Appendix B) | One fixed outer split; 3-fold training-only CV over 10 candidate configurations; five training seeds (11, 23, 37, 53, 71); an optional resplit of the training partition with seeds 101, 202 and 303 and the estimator seed fixed; one final evaluation |
| Comparison | Variance from each source expressed as a fraction of the variance from bootstrapping the data (Figure 1) | Every seed's validation and final metrics, a probability-averaged ensemble and a training-prior baseline |
| Result and location | "Bootstrapping data stands out as the most important source of variance"; model initialization is generally less than 50% of the bootstrap variance; the three hyperparameter-search methods add on average about as much variance as weight initialization (§2.2, Figure 1) | The five seeds measure training randomness only. Logistic regression with lbfgs is deterministic, so its seed spread is zero by design ([stability investigation](stability.md)) |
| Validity threat | Deep-learning tasks with large datasets and GPU-scale searches; the variance ratios may differ for small tabular models | No repeated outer splits, so data-sampling variance in the final estimate is not measured; the profile bootstrap is conditional on the fixed split and models |
| Course decision | See below | See below |

**Evaluation differences.** The paper treats data sampling as a random source to be resampled. The capstone fixes one partition so that learners can see a single, untouched final evaluation, and runs on a laptop CPU. The capstone's five training seeds correspond to only one of the paper's sources, model initialization, which the paper finds is usually the smaller one. The optional split study is the nearest analogue to the paper's data-sampling source. It is descriptive only, because those training observations already informed cross-validation.

**Limitations of the comparison.** The paper's figures describe its five deep-learning benchmarks, not this dataset; they are not an estimate of the capstone's variance. Nothing here replicates the paper: the course implements one recommendation (reporting every seed) and documents why it does not implement another (resampled test sets).

**Course decision.** Keep the fixed outer split and single final evaluation for teaching, report all five seeds, and label their spread as training randomness, not uncertainty about future data. Do not claim that one model family is better from these results alone. Evidence that would change this decision: an adopter with the compute budget to run repeated outer splits, such as out-of-bootstrap (Appendix B), should plan that as a new evaluation design before comparing families.

## Practice a methodological comparison

Use the worked example above as a model, then complete your own evidence table for a different source. For Module 11, read [LoRA](https://arxiv.org/abs/2106.09685). Separate its parameterization idea from its task-specific empirical results. Explain why implementing adapters on the course’s small local model is not a replication of the paper’s reported performance.

## Submit a defensible conclusion

Write: “I chose ___ because source ___ provides evidence about ___. Its result is not directly comparable because ___. My experiment will check ___ using ___.” Include one credible alternative and evidence that would change your choice. An independent reviewer should be able to locate each supporting claim and identify which conclusion is yours.
