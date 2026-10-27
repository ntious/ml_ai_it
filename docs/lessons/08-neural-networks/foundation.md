# Module 8 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

A dense layer combines inputs with learned weights and a bias; ReLU supplies a nonlinear hidden activation. A sigmoid output lies between zero and one. Binary cross-entropy supplies the gradient objective; a low training loss does not establish held-out performance.

## Work through the evidence

Separate the feature matrix from the target vector. Eleven chemistry measurements enter a row; the target rating threshold is not an input. The loss is differentiated with respect to trainable weights. Validation can select the checkpoint, but its values never become gradient targets.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.

## Worked mental model

For x=[1,2], w=[.5,-1] and bias .5, the weighted sum is -1 and ReLU returns 0. A sigmoid maps a number into 0–1. A batch of 32 wine observations has shape (32,11), hidden values (32,16), and output (32,1). The network has 11*16+16+16+1=209 parameters. An epoch visits training examples; a batch drives one update.

Work through the [numerical construction](guided.md) before using the complete runner. Explain every new symbol using the [glossary](../../glossary.md).

## Continue at an applied pace

Use the [concept sequence](concepts.md) for the intermediate explanation before [guided construction](guided.md). Optional open readings are selected there; mathematical proofs are not an added core requirement.
