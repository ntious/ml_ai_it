# Module 3 worked feedback

Try the [practice](practice.md) before reading the worked examples. Feedback is public so independent learners can check their reasoning.

## Initial run

Twelve records enter the pipeline; six are accepted and six rejected. One accepted record has missing latency. The five observed latencies total 120 milliseconds, so their mean is 24 milliseconds. Deleting the missing record would reduce the accepted dataset to five, even though other fields in that record may remain useful.

The two versions of `auth-005` conflict. Neither version is selected as truth. Both are quarantined for investigation. The exact repeated `auth-001` retains the first copy and rejects the later copy. The source field is part of the key, so identical IDs from different sources are not automatically the same event.

## Add a valid record with missing latency

With one new valid unique event, the expected counts are 13 input, 7 accepted, and 6 rejected. Accepted missing latency increases from 1 to 2. Observed latency count remains 5, and its mean/median remain 24 and 20. This is why the denominator must be named clearly.

## Make a conflicting key

If you add a different latency for an existing previously accepted key, both versions of that key are rejected. Exact counts depend on which key you changed and whether the edited row was already rejected. Inspect record identity and reasons rather than assuming every new row has the same effect.

## Discussion example

Removing a record may be justified if a required field makes it unusable for the stated task. But missing latency might occur when a source is overloaded; deleting those events could make observed latency seem better than it is. We need to inspect how the measurements are collected and why they are missing. Retaining the record is a transparent starting policy, not proof that missingness is harmless.

## What this does not establish

A passing validator confirms compliance with a specified contract. It does not establish source accuracy, representativeness, fairness, a causal relationship, or suitability for every model. Future training must still handle splits and learned preprocessing correctly.

[Return to the module](index.md).

## Construction check and misconception feedback

Question: Should a missing latency be replaced by zero?

Only under an explicit defensible measurement contract; normally missing and measured zero differ.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
