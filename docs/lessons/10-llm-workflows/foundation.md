# Module 10 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

A language model predicts token continuations, not guaranteed facts or valid JSON. Temperature/sampling change generation behavior; this core uses greedy decoding and a token cap. Format compliance, label correctness, and latency are separate measurements.

## Work through the evidence

The prompt and output have token lengths, and generation is bounded by new tokens. A fluent explanation is not a valid response when the contract requires strict JSON. The parser returns unavailable on invalid output; it never guesses the intended label.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.

## Worked mental model

A token model chooses continuations. Greedy decoding chooses a highest-scoring next token at each step; it does not guarantee a globally best answer. Valid JSON and correct classification are separate events. On 100 records, one changed outcome moves the observed rate by one percentage point; uncertainty still depends on the sample and its design.

Work through the [numerical construction](guided.md) before using the complete runner. Explain every new symbol using the [glossary](../../glossary.md).

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
