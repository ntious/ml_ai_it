# Module 11: What changes when a model is fine-tuned?

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Parameters, data and objective

Fine-tuning changes selected weights using task examples. A prompt changes the input without updating weights. Low-rank adapters train a smaller parameterization while retaining frozen base weights; smaller does not automatically mean safer or better. Record the actual trainable parameter count and changed tensors. If the trainable count is zero, a decreasing printed loss may not demonstrate the intended update.

## Mask the objective you mean to teach

In a completion task, prompt tokens and padded positions may need to be ignored by the loss. A label value of -100 is the common ignore marker used by this exercise. For IDs [5,6,7,0] with a two-token prompt and mask [1,1,1,0], labels become [-100,-100,7,-100]. The target token remains supervised; padding never becomes a desired answer. A causal language model also shifts prediction alignment internally, so do not apply an unexplained second shift.

## Lower training loss is a mechanism check

A model can memorize the adaptation set and still fail the output contract on held-out messages. Compare before and after under the same fixed evaluation settings, keep invalid responses in the denominator and retain the untuned baseline. Use development behavior to choose an update budget, then report the locked comparison. A small or adverse change is a result to explain, not a reason to keep tuning on final examples.

## Trace a small case

Predict `trainable_count([[100, False], [8, True], [2, True]])` before running: only trainable tensors count, and you count their scalar values, giving 10. Then predict `completion_labels([5, 6, 7, 0], 2, [1, 1, 1, 0])`: the two prompt positions and the padding position become -100, giving `[-100, -100, 7, -100]`. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/sms-fine-tuning/scripts/run.py`. It trains rank-8 LoRA adapters on every `q_proj` and `v_proj` of SmolLM2-135M with prompt and padding labels masked to -100, which is your `completion_labels` at scale. `summary.json` reports `trainable_parameters` (460,800 in the recorded run) and an adapter update norm, which check that parameters actually changed. `generation_comparison.csv` then measures whether held-out answers improved: a separate question. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. What is the difference between changing a prompt and fine-tuning?</summary>

A prompt changes the input and updates no weights. Fine-tuning changes selected weights using task examples; adapters train a small set while the base weights stay frozen.

</details>

<details>
<summary>2. For IDs `[5, 6, 7, 0]`, a two-token prompt and mask `[1, 1, 1, 0]`, what are the training labels?</summary>

`[-100, -100, 7, -100]`: prompt and padding positions are ignored and only the completion token is supervised.

</details>

<details>
<summary>3. Training loss dropped sharply but held-out output validity did not improve. Was fine-tuning successful?</summary>

Not by that evidence. Lower training loss checks the mechanism; the model may have memorized the adaptation set. The held-out comparison is the result.

</details>

## Optional reading

[LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)](https://arxiv.org/abs/2106.09685), Section 4 (the method), explains why a low-rank update to a frozen weight needs few trainable values. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
