# Module 11: What changes when a model is fine-tuned?

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Parameters, data and objective

Fine-tuning changes selected weights using task examples. A prompt changes the input without updating weights. Low-rank adapters train a smaller parameterization while retaining frozen base weights; smaller does not automatically mean safer or better. Record the actual trainable parameter count and changed tensors. If the trainable count is zero, a decreasing printed loss may not demonstrate the intended update.

## Mask the objective you mean to teach

In a completion task, prompt tokens and padded positions may need to be ignored by the loss. A label value of -100 is the common ignore marker used by this exercise. For IDs [5,6,7,0] with a two-token prompt and mask [1,1,1,0], labels become [-100,-100,7,-100]. The target token remains supervised; padding never becomes a desired answer. A causal language model also shifts prediction alignment internally, so do not apply an unexplained second shift.

## Lower training loss is a mechanism check

A model can memorize the adaptation set and still fail the output contract on held-out messages. Compare before and after under the same fixed evaluation settings, keep invalid responses in the denominator and retain the untuned baseline. Use development behavior to choose an update budget, then report the locked comparison. A small or adverse change is a result to explain, not a reason to keep tuning on final examples.

## Trace a small case

The first operation is **trainable_count**: Input [size, trainable] pairs; return number of trainable scalar values. On authored arguments `[[[100, False], [8, True], [2, True]]]`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/sms-fine-tuning/scripts/run.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Primary explanation](https://arxiv.org/abs/2106.09685) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
