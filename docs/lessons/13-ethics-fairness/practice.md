# Module 13: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module13/practice.ipynb "site-download:module13/practice.ipynb"). In a source checkout open `notebooks/practice/module13-practice.ipynb`. Use the [core environment and kernel](../../../QUICKSTART.md#notebook-option); the practice checks need NumPy even where the module script does not. Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `recall_denominator`

Return the actual-positive count. Predict the result on `recall_denominator(8, 2, 11, 30)`, implement it and call `m13_recall_denominator` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for recall_denominator</summary>

Recall conditions on actual positives, not predictions.

</details>

## Construct `safe_rate`

Return numerator/denominator, or None for zero denominator. Predict the result on `safe_rate(8, 19)`, implement it and call `m13_safe_rate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for safe_rate</summary>

Unavailable is not evidence of parity.

</details>

## Construct `wilson`

Return a two-number 95% illustrative Wilson interval using learning.wilson_interval. Predict the result on `wilson(8, 10)`, implement it and call `m13_wilson` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for wilson</summary>

State the conditional independent-binomial assumption before interpreting the interval.

</details>

## Reason beyond the visible checks

Construct confusion counts for a group with no actual positives, and another group with recall 1.0. For each, give the selection rate and the result of `safe_rate` for recall, and explain why "recall unavailable" is not evidence that the groups are treated equally. The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Compare two groups with equal rates and unequal counts. Explain why this does not establish equitable outcomes or justify a group ranking. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M13.1:** Identify stakeholders, historical label limitations, and inappropriate uses.
- **M13.2:** Fit a declared training pipeline without protected audit columns.
- **M13.3:** Report group counts, confusion denominators, selection rates, TPR, and FPR.
- **M13.4:** Explain metric trade-offs, proxy effects, and uncertainty without causal/legal claims.
- **M13.5:** Write a governance recommendation, including reasons not to deploy.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.
