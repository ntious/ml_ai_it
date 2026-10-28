# Module 1: From a task to an accountable decision

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## A prediction is not the whole decision

A help desk predicts whether a ticket needs escalation. The prediction is an estimate; the action also depends on staff capacity, error costs and the option to ask a person. Start by naming the unit (one ticket at arrival), target (eventual escalation) and decision time. A field written after escalation cannot be an input at arrival. A rule is a useful baseline because you can trace every branch; machine learning estimates a rule from examples, but still needs a human-defined target.

## Trace before you train

For an authored rule that escalates priority at least 3, priorities 2, 3 and 4 produce False, True and True. The boundary matters. Against labels False, False, True, the middle case is a false alert. Correct execution of the rule does not establish that its threshold is useful. Change the threshold and predict which cases change before running code.

## Separate development from the final question

This is a preview: [Module 5](../05-regression/index.md) builds these split roles with a real dataset. Training fits parameters; validation supports choices; a final test estimates the locked procedure on held-out examples. Once you use the final answer to select a threshold, that answer has become development evidence. A new random seed does not erase that reuse. Save the original question, the decision and the evidence needed to contradict it.

## Trace a small case

Predict `route(2)`, `route(3)` and `route(4, threshold=5)` before running. The first two sit on either side of the inclusive boundary; the third checks that your function uses its `threshold` argument rather than a fixed 3. Then predict `error_counts([False, False, True], [True, True, True])`: the two actual negatives were flagged, so there are two false alerts and no misses. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/first-run/scripts/first_run.py`, whose storage rule is strict (`storage_percent > 80`). The practice priority rule is inclusive (`priority >= 3`). They are deliberately different rules on different inputs, so do not look for the priority rule inside the storage script. Run the script with `--storage-percent 80` and `81`, open each saved `first-run.txt`, and explain which comparison operator produces each decision. Success on an authored fixture does not establish performance on a real service.

## Optional reading

[Google's Introduction to Machine Learning: supervised learning](https://developers.google.com/machine-learning/intro-to-ml/supervised) defines features, labels, training and inference: the terms this module uses to separate a written rule from a learned model. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
