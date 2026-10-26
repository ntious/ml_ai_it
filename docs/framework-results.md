# Recorded Phase B framework results

Generated from actual `runs/verified/moduleNN/summary.json` files using `python scripts/update_framework_results.py`. Regenerate after changing the protocol; the site builder does not fabricate results or silently update source.

These historical benchmarks and authored controls have been inspected during development. Repeated evaluation is a teaching/reproduction exercise, not a new prospective holdout claim. The Module 10 prevalence-preserving subset and Module 11 balanced subset differ; their accuracy values are not a matched cross-module comparison.

| Module | Evaluation sample | Recorded result | Comparison / qualification |
| --- | --- | --- | --- |
| 8 | 1,599 source rows; 243 final | Neural recall 29/29 = 1.000; precision 0.244; balanced accuracy 0.790 | Lexical/logistic recall 0.897; balanced accuracy 0.829 |
| 9 | 5,159 source rows; 1,032 final | Neural recall 118/128 = 0.922; precision 0.797; balanced accuracy 0.944 | Lexical/logistic recall 0.906; balanced accuracy 0.946 |
| 10 | 100 stratified final SMS | Likelihood accuracy 0.85; free-generation validity 0.99, accuracy 0.39 | Lexical accuracy 0.97; training-majority accuracy 0.88 |
| 11 | 100 balanced final SMS | JSON validity 0.00 → 1.00; label accuracy 0.00 → 0.94 | Validation loss 1.5358 → 0.0030; selected step 200/200 |
| 14 | 26 authored final controls | Routing 22/26 = 0.846 | Correct refusals 9/10; no destructive tools available |

## Reproduce and inspect

- [Module 8 workflow](lessons/08-neural-networks/index.md) and [feedback](lessons/08-neural-networks/feedback.md).
- [Module 9 workflow](lessons/09-neural-nlp/index.md) and [feedback](lessons/09-neural-nlp/feedback.md).
- [Module 10 workflow](lessons/10-llm-workflows/index.md) and [feedback](lessons/10-llm-workflows/feedback.md).
- [Module 11 workflow](lessons/11-fine-tuning/index.md) and [feedback](lessons/11-fine-tuning/feedback.md).
- [Module 14 workflow](lessons/14-agents/index.md) and [feedback](lessons/14-agents/feedback.md).

The [historical baseline](maintenance/reviews/framework-baseline-0.7.0.md) retains the earlier failure cases. Consult each report’s rate_intervals.csv where provided. Remaining repository-wide uncertainty work belongs to Phase C.
