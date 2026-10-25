# Module 3 practice and discussion

These original activities work for independent learning or instructor adaptation. They are not copied Canvas assignments. Complete the core work before choosing an optional extension. No external AI account is required.

## Core exercise

1. Run the sample through the preparation script. Record the accepted/rejected counts and one rejected record's explanation.
2. Make a copy of the raw CSV in a separate working folder. Add one valid event with a new key, positive whole-byte count, and missing latency. Predict how the accepted count and observed-latency count will change, then run it into a new output directory.
3. Create a second copy where one existing key has two different valid latency values. Predict the conflict policy and inspect the rejected-record reasons. Do not alter the checked-in original sample.
4. Write a five-field data dictionary in your own words. Explain the difference between missing latency and zero latency.
5. Run the small NumPy example in the lesson or notebook and verify the resource-unit solution by substitution.

Keep your modified inputs, command, report, and explanation together. Explain any AI assistance according to your instructor's policy; an independent learner can use the same disclosure/reflection habit.

## Self-check

- Can input count be reconciled with accepted plus rejected count?
- Were raw input bytes preserved?
- Does each rejected record have an understandable reason?
- Did your added missing latency remain missing?
- Did you inspect the output before describing it as clean or high quality?

## Discussion or individual reflection

An analyst proposes deleting every record with a missing value so the table looks complete. Give a reason that might support removal in one context and a reason it might distort this analysis. What additional information about the collection process would you want?

If discussing with peers, compare assumptions rather than ranking whose answer sounds more technical. A short individual reflection addresses the same concept. [Worked feedback](feedback.md) provides an example argument rather than a unique answer to memorize.

## Adaptable rubric

An instructor may adapt these criteria to local policy. No weights or passing threshold are imposed by the resource.

- Execution and traceability: identifies the input/configuration, command, and output; counts reconcile.
- Data decisions: distinguishes missingness, invalid values, exact duplicates, and conflicting keys.
- Explanation: uses fields/units correctly and supports claims with observed evidence.
- Testing and revision: predicts a change, checks the result, and explains any unexpected behavior.

## Optional extension

Allow a new source category through a documented contract change. Identify code, data dictionary, tests, and assumptions that need updating; do not merely disable validation. Or investigate whether interpreting timezone-naive timestamps as UTC is appropriate for another source.

This extension is skippable and provides no automatic extra credit. No additional library or paid service is necessary.

[Return to the module](index.md).

## Required independent construction

Inspect a rejected record and explain its policy reason. On a copy, repair one legitimate error and reconcile the changed counts.

Use the [guided construction](guided.md) for a worked example, then reconstruct its central step without copying it. Retain changed code, expected/observed evidence and an explanation. This clarifies companion practice; Canvas remains the authority for assessed submissions.
