# Module 11 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

LoRA adds a low-rank update to a frozen linear projection. The rank-2 hand construction illustrates one projection; the full study uses rank-8 PEFT adapters in every query/value projection. Masking prompt labels with -100 prevents the objective from training on every instruction token.

## Work through the evidence

A frozen base still performs the forward computation. Gradients flow to the low-rank matrices. Starting one matrix at zero preserves the original output initially; an optimizer step can then change the adapter. A nonzero update proves mechanics, not improved language quality.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.

## Worked mental model

If W has output-by-input shape (6,4), it has 24 parameters. A rank-2 A has shape (2,4), B has shape (6,2), and BA has shape (6,4). Their 20 parameters are fewer here; savings become much larger for wide projections. Starting B at zero makes the initial update zero. A frozen base participates in forward computation without optimizer updates. Labels -100 exclude prompt positions from the completion-loss objective; they are a library masking convention.

Work through the [numerical construction](guided.md) before using the complete runner. Explain every new symbol using the [glossary](../../glossary.md).

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
