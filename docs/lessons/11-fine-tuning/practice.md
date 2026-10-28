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

## Transfer to an IT decision

Explain a run where adapter weights change but held-out validity does not. Propose a development-only investigation. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M11.1:** Distinguish prompting, inference, supervised fine-tuning, and LoRA.
- **M11.2:** Prepare completion labels with prompt-token loss masking.
- **M11.3:** Update a small adapter on training-only real annotations.
- **M11.4:** Compare predeclared base/adapted held-out completion losses without promising improvement.
- **M11.5:** Save/reload adapter arrays with the exact model revision and disclose limits.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.
