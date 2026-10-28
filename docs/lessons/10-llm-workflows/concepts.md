# Module 10: A generated answer needs an evaluation contract

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Generation and truth are different

A language model produces likely next tokens conditioned on a prompt. Fluent text can still be unsupported. Separate the requested task, supplied evidence and response contract. For a label-only task, extra explanation may be a contract failure even when the label is plausible. A local model avoids an account requirement but still has a revision, license, memory cost and known limitations.

## Parsing is an observable boundary

For this exercise, accept exactly a JSON object with one label field containing ham or spam. Reject prose, extra keys and other labels. A parser checks structure, not whether the label is correct. Keep malformed outputs in the denominator: dropping them would reward a model for failing hard cases. Inspect representative errors before claiming a prompt improved performance.

## Compare choices without reusing the answer key

Choose prompts and decoding settings using development messages. Lock the prompt before final evaluation and compare a simpler method under the same task. Eight examples can illustrate behavior but provide weak evidence about population quality. Report valid output count, correct count and exact sample size. A deterministic decoding configuration reduces one source of variation; it does not establish stable performance across datasets or model revisions.

## Trace a small case

The first operation is **parse_label**: Return ham/spam only for an exact one-key JSON object; otherwise return None. On authored arguments `parse_label('{"label":"spam"}')`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/sms-llm/scripts/run.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Further reading: llm workflows](https://huggingface.co/docs/transformers/main/en/generation_strategies) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
