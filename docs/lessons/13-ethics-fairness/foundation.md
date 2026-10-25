# Module 13 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

Fairness is a contextual normative question, not one scalar score. Excluding a protected column cannot remove proxy effects or historical label bias. Group rate differences require denominators, sample context, and uncertainty; they do not prove a causal mechanism or legal conclusion.

## Work through the evidence

TPR divides true positives by actual positives; FPR divides false positives by actual negatives. A selection rate uses all group records. Different denominators answer different questions. A zero denominator means unavailable, not a rate of zero.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.
