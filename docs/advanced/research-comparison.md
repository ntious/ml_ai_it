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

## Practice a methodological comparison

Compare the capstone’s bounded hyperparameter search and all-seed reporting with the questions raised by [Accounting for Variance in Machine Learning Benchmarks](https://arxiv.org/abs/2103.03098). Identify which sources of variation your experiment measures and which remain fixed. Extract one actual result from the paper with its location; do not treat the paper’s benchmark results as estimates for your dataset.

For Module 11, read [LoRA](https://arxiv.org/abs/2106.09685). Separate its parameterization idea from its task-specific empirical results. Explain why implementing adapters on the course’s small local model is not a replication of the paper’s reported performance.

## Submit a defensible conclusion

Write: “I chose ___ because source ___ provides evidence about ___. Its result is not directly comparable because ___. My experiment will check ___ using ___.” Include one credible alternative and evidence that would change your choice. An independent reviewer should be able to locate each supporting claim and identify which conclusion is yours.
