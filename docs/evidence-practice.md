# Reproduce a result and justify its use

Use this activity after your module's complete reference run. Keep the current lesson order and environment. Start with your own output; a published worked report is a reading alternative when execution is blocked, and must be labelled as such. Early modules use authored teaching data, not external observations.

**Reproducibility** asks whether another person can reconstruct the recorded experiment. **Stability** asks how a justified change affects the result. **Trustworthiness** asks whether the evidence supports a particular use, including its consequences for people. A reproducible mistake is still a mistake.

## Four steps for every module

1. **Predict:** choose the module task below before opening its worked feedback. State what you expect and what observation would contradict your expectation.
2. **Recompute:** use the output of the module's reference script or notebook. Recalculate one claim from its underlying records, not by copying the displayed summary. Save your calculation and the exact artifact path.
3. **Reproduce:** restart your session and repeat with the same inputs and configuration in a new output directory. Compare counts exactly. Before comparing floating-point results, declare a tolerance appropriate to the quantity; explain any disagreement. Timestamps and timing measurements need not match. Do not assume that fixed seeds guarantee identical results on different hardware.
4. **Decide:** state one supported conclusion, one unsupported conclusion and what additional evidence would change your decision. Use the [evidence worksheet](../templates/evidence-review.md).

For machine-learning studies, preserve the original test boundary. Recalculating a fixed test metric is an audit; choosing a new model or threshold from that result is a new selection decision. Use development data for changes and predeclare the next evaluation.

## Module tasks

Follow the matching module's practice page for a specific task. The progression is deliberate: trace records in Modules 1–4, audit selection and stability in Modules 5–9, then assess contracts, harms and operational limits in Modules 10–14. The task uses existing artifacts rather than adding a second full training run unless reproduction is selected for that session.

For long framework runs, exchange the source revision, configuration, saved predictions and logs for a calculation audit first. Schedule a full rerun separately. Record these as different levels of verification; a calculation audit does not demonstrate that training reproduces.

## Peer reproduction

Give a peer the source revision, public data acquisition instructions, environment recipe, exact command, expected artifact and comparison rule. Do not supply your live environment or private data. Have them record whether they needed clarification and whether the result matched. A solo learner can repeat from a fresh session and label the activity self-review. The [instructor rubric](instructor/evidence-assessment.md) explains what counts as adequate evidence.

## Check your reasoning

<details><summary>Two runs match exactly. Does that show the model is fair?</summary>
No. It establishes agreement under those recorded conditions. Fairness needs a justified use, affected-group evidence, relevant uncertainty and consideration of alternatives and contestability.
</details>

<details><summary>One of five seeds is much better. Should I report only that seed?</summary>
No. Retain every declared run. Selecting the best seed hides variation and changes the selection procedure. A seed standard deviation is not a confidence interval for performance in a new population.
</details>

<details><summary>The report is correct but a peer cannot rebuild it. What should change?</summary>
Keep the numerical result and record the reproduction failure. Repair missing instructions, source identity or environment details, then ask for another attempt. Do not relabel an unexecuted reconstruction as successful.
</details>
