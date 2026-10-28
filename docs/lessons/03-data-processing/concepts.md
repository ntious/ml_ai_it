# Module 3: Turn records into trustworthy inputs

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Validation precedes modeling

An event record has a grain: one event, not one user or one day. Choose a key before counting records. Repeated exports can contain the same event twice; deduplicating by every column may fail if an annotation changed. Declare which version wins and retain a reconciliation ledger: input rows equal accepted rows plus rejected rows plus duplicates removed.

## Preserve the meaning of absence

A blank latency does not mean a fast request. Parse blank or None as missing and preserve a measured zero. Negative latency violates this exercise contract and should raise an error. Do not silently coerce invalid strings into zero. Reject a malformed value or quarantine it with a reason so the resulting model population is visible.

## The preparation boundary is part of evaluation

Schema checks describe what is allowed; learned transformations estimate properties of training data. A fixed nonnegative check can apply to every partition, but a median or vocabulary must be fitted on training. A preparation step can leak even when the target column is absent: computing a median across final-test records reveals their distribution.

## Trace a small case

The first operation is **parse_latency**: Parse blank/None as None; otherwise return a nonnegative float, raising ValueError for negatives. On authored arguments `['']`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/network-events/scripts/prepare.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Primary explanation](https://scikit-learn.org/stable/common_pitfalls.html) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
