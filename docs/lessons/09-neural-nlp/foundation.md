# Module 9 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

Tokens are discrete representations; embeddings are learned numeric vectors. Padding supports fixed-length batches and should not become a real word signal. Global average pooling summarizes token vectors. Unknown words and truncated messages limit what the model can use.

## Work through the evidence

Vocabulary adaptation is fitting. Including final-test words in that step would let the holdout influence the representation. The label is a human spam/ham annotation, not a property inferred from a phone number alone. Class imbalance can make accuracy look good while recall is poor.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.
