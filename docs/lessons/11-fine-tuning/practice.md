# Module 11: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module11/practice.ipynb "site-download:module11/practice.ipynb"). In a source checkout open `notebooks/practice/module11-practice.ipynb`. Use the [framework environment and kernel](../../setup/frameworks.md). Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `trainable_count`

Input [size, trainable] pairs; return number of trainable scalar values. Predict the result on `trainable_count([[100, False], [8, True], [2, True]])`, implement it and call `m11_trainable_count` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for trainable_count</summary>

Count scalars in trainable tensors, not the number of tensors.

</details>

## Construct `completion_labels`

Return ids with prompt and padding positions replaced by -100. Predict the result on `completion_labels([5, 6, 7, 0], 2, [1, 1, 1, 0])`, implement it and call `m11_completion_labels` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for completion_labels</summary>

Mask both prompt and padding, while retaining completion tokens.

</details>

## Construct `changed_tensors`

Input equally sized lists of scalar lists. Return indices of tensors with any changed value. Predict the result on `changed_tensors([[1, 2], [3]], [[1, 2], [4]])`, implement it and call `m11_changed_tensors` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for changed_tensors</summary>

Demonstrate an actual parameter change; a new loss string is insufficient.

</details>

## Work with the complete study's results

Open `generation_comparison.csv` and `summary.json` from the complete study. Count schema-valid and correct answers for the base and adapted models, and check `trainable_parameters` against the LoRA formula: rank 8 on every `q_proj` (576 → 576) and `v_proj` (576 → 192) in 30 layers. Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

A rank-2 adapter on a 4 × 4 projection has matrices of shape 2 × 4 and 4 × 2. Use `trainable_count([[16, False], [8, True], [8, True]])` and compare the result with the frozen matrix. Explain when LoRA actually saves parameters, and why `changed_tensors` returning `[1]` does not show that fine-tuning helped. The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Explain a run where adapter weights change but held-out validity does not. Propose a development-only investigation. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Evidence and feedback

- **M11.1:** Distinguish prompting, inference, supervised fine-tuning, and LoRA.
- **M11.2:** Prepare completion labels with prompt-token loss masking.
- **M11.3:** Update a small adapter on training-only real annotations.
- **M11.4:** Compare predeclared base/adapted held-out completion losses without promising improvement.
- **M11.5:** Save/reload adapter arrays with the exact model revision and disclose limits.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Evidence activity: Check the adaptation claim

Use the saved base/adapted outputs and evaluation results. Recompute the change in one task metric on the same held-out examples and compare it with the reported training loss change. Explain why decreasing loss alone does not establish improved task performance.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.
