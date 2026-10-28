# Module 10: A generated answer needs an evaluation contract

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Generation and truth are different

A language model produces likely next tokens conditioned on a prompt. Fluent text can still be unsupported. Separate the requested task, supplied evidence and response contract. For a label-only task, extra explanation may be a contract failure even when the label is plausible. A local model avoids an account requirement but still has a revision, license, memory cost and known limitations.

## Parsing is an observable boundary

For this exercise, accept exactly a JSON object with one label field containing ham or spam. Reject prose, extra keys and other labels. A parser checks structure, not whether the label is correct. Keep malformed outputs in the denominator: dropping them would reward a model for failing hard cases. Inspect representative errors before claiming a prompt improved performance.

## Compare choices without reusing the answer key

Choose prompts and decoding settings using development messages. Lock the prompt before final evaluation and compare a simpler method under the same task. Eight examples can illustrate behavior but provide weak evidence about population quality. Report valid output count, correct count and exact sample size. A deterministic decoding configuration reduces one source of variation; it does not establish stable performance across datasets or model revisions.

## Trace a small case

Predict `parse_label('{"label":"spam"}')`, `parse_label('spam')` and `parse_label('{"label":"ham","why":"x"}')` before running. Only the first meets the exact one-key contract; prose and extra keys are rejected even when the label inside them looks right. Then predict `valid_fraction(['spam', None, 'ham'])`: the malformed output stays in the denominator, giving 2/3. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/sms-llm/scripts/run.py`. `generation_evaluation.csv` records each free generation, whether it parsed and whether the parsed label was correct. `summary.json` reports validity and accuracy over all 100 final messages, not only the ones that parsed. `rate_intervals.csv` attaches uncertainty to both rates. The recorded run had free-generation validity 0.99 but accuracy 0.39: format compliance and correctness are separate measurements. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. The model replies `Label: spam`. Is that a valid output under the exact JSON contract?</summary>

No. The contract requires a one-key JSON object, so this is invalid even though the label looks plausible.

</details>

<details>
<summary>2. Of 100 messages, 90 outputs parse and 80 of those are correct. What is the end-to-end accuracy?</summary>

0.80 (80 of 100). Reporting 80/90 would reward the model for failing to answer the other 10.

</details>

<details>
<summary>3. Can you choose the prompt by comparing results on the final test messages?</summary>

No. Choose prompts and decoding settings on development messages, lock them, then evaluate once on the final set.

</details>

## Optional reading

[Hugging Face Transformers: Generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies), the greedy-search and token-limit sections, explains the decoding settings that this module holds fixed. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
