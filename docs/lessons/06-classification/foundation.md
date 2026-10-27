# Module 6 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

A probability estimate is not automatically calibrated confidence. A threshold converts a score into a decision. False positives and false negatives can have different costs; balanced accuracy gives equal weight to recall in each class, not to operational cost.

## Work through the evidence

If 19 higher-rated samples are correctly flagged and 30 others are incorrectly flagged, precision is 19/49. If 10 positives are missed, recall is 19/29. Read each denominator before using a percentage. The real held-out study initially produced those counts; recompute from your prediction table.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.

## Worked mental model

X is rows by chemistry inputs. y is the declared rating threshold. Fit the scaler and logistic parameters on training only. A score needs a decision threshold; changing it affects both false positives and false negatives.

Work through the [numerical construction](guided.md) before using the complete runner. Explain every new symbol using the [glossary](../../glossary.md).

## Continue at an applied pace

Use the [concept sequence](concepts.md) for the intermediate explanation before [guided construction](guided.md). Optional open readings are selected there; mathematical proofs are not an added core requirement.
