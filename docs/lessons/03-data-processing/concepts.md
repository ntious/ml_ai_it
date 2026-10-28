# Module 3: Turn records into trustworthy inputs

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Validation precedes modeling

An event record has a grain: one event, not one user or one day. Choose a key before counting records. Repeated exports can contain the same event twice; deduplicating by every column may fail if an annotation changed. Declare which version wins and retain a reconciliation ledger: input rows equal accepted rows plus rejected rows plus duplicates removed.

## Preserve the meaning of absence

A blank latency does not mean a fast request. Parse blank or None as missing and preserve a measured zero. Negative latency violates this exercise contract and should raise an error. Do not silently coerce invalid strings into zero. Reject a malformed value or quarantine it with a reason so the resulting model population is visible.

## The preparation boundary is part of evaluation

Schema checks describe what is allowed; learned transformations estimate properties of training data. A fixed nonnegative check can apply to every partition, but a median or vocabulary must be fitted on training. A preparation step can leak even when the target column is absent: computing a median across final-test records reveals their distribution.

## Trace a small case

Predict `parse_latency('')`, `parse_latency('0')` and `parse_latency('12.5')` before running: missing, measured zero and a measured value are three different results. Then predict `reconcile(10, 7, 2, 1)` and `reconcile(10, 8, 2, 1)`: only the first accounts for every source row exactly once. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/network-events/scripts/prepare.py`. Its `quality_report.json` and `summary.txt` reconcile 12 input rows into 6 accepted and 6 rejected, and keep one accepted record with missing latency. The script's duplicate policy is stricter than the practice `deduplicate`. An exact repeat is rejected as `exact_duplicate` and the first copy kept. Two rows with the same `event_id` but different values are both rejected as `conflicting_event_key`, because neither can be trusted. Find both cases in `rejected_events.csv`. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. One record has latency `''` and another has `'0'`. Should both be stored as 0?</summary>

No. A blank is missing (unavailable); 0 is a measured value. Treating missing as 0 would invent fast requests.

</details>

<details>
<summary>2. An export repeats an event with a changed annotation. Why can deduplicating by every column fail?</summary>

The two rows differ, so whole-row deduplication keeps both. Deduplicate by the event's key and declare which version wins.

</details>

<details>
<summary>3. Why should a median used to fill missing values be computed from training records only?</summary>

Computing it across all records lets final-test values shape the preparation, which leaks information even though the target column is absent.

</details>

## Optional reading

[scikit-learn: Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html), sections on inconsistent preprocessing and data leakage, explains why cleaning rules must be fixed before they meet evaluation data. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
