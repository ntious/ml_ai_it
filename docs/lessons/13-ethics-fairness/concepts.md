# Module 13: Group evidence, uncertainty and a legitimate task

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## A rate answers one particular question

Selection rate divides positive predictions by all records. Recall divides true positives by actual positives. False-positive rate divides false positives by actual negatives. A group with no actual positives has undefined recall, even if its selection rate is zero. Report the numerator and denominator before comparing groups; otherwise a small denominator can disappear behind a precise-looking percentage.

## Equal point estimates can hide unequal information

Eight successes in ten trials and eighty in one hundred both give 80%, but a binomial interval is wider for the first. Wilson intervals avoid a zero-width interval at zero successes. They still assume a suitable independent sampling model. The Adult extract does not establish that model or independent people, so its interval columns are conditional illustrations, not population confidence claims. Sampling bias and label error are not repaired by a formula.

## The target may be the problem

Historical income labels reflect past social conditions; predicting them accurately does not justify allocating opportunities. Excluding recorded sex or race does not remove proxies. Ask who is affected, what action is proposed, how a person can contest it and whether automation is legitimate at all. Neither a single fairness metric nor overlapping intervals settles that decision. Compare the task definition, uncertainty and nonautomated alternative before recommending a next step.

## Trace a small case

Predict `recall_denominator(8, 2, 11, 30)` before running: recall conditions on actual positives, TP + FN = 19, not on predictions. Then predict `safe_rate(0, 0)` and `safe_rate(0, 10)`: no actual positives means the rate is unavailable (`None`), while 0 of 10 is a measured 0. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/income-fairness/scripts/run.py`. `group_audit.csv` lists, for each recorded group, the numerator and denominator behind recall, false-positive rate and selection rate. It also lists their illustrative Wilson intervals and a small-denominator flag. For example, female recall is 357 of 590 actual positives. Recompute one row's recall with `safe_rate` and its interval with `wilson`, and check that the flag follows the recall denominator, not the group size. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. A group has no actual positives and a selection rate of 0. What is its recall?</summary>

Undefined (unavailable), because its denominator is zero. That is not evidence that the group is treated equally.

</details>

<details>
<summary>2. Recall is 8/10 in one group and 80/100 in another. Is the evidence equally certain?</summary>

No. The rates match, but the 95% Wilson intervals are about 0.49–0.94 and 0.71–0.87. Report counts and intervals with each rate.

</details>

<details>
<summary>3. Does removing recorded sex and race from the inputs make the model fair?</summary>

No. Other features can act as proxies, historical labels reflect past conditions, and fairness depends on the decision and the people affected.

</details>

## Optional reading

[Fairlearn user guide: Assessment](https://fairlearn.org/main/user_guide/assessment/index.html) explains disaggregated metrics by group and why a single fairness number cannot settle whether a system is appropriate. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
