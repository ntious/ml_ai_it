# Module 7 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

K-means minimizes squared distances to centers, so units and scaling affect the result. Silhouette contrasts within-cluster closeness with separation from other clusters. It is not classification accuracy. Cluster IDs can be permuted without changing the partition.

## Work through the evidence

Two columns measured on very different scales can dominate Euclidean distance differently. Centering and scaling use training means/standard deviations. Compare original-unit profile means after fitting; do not interpret the standardized number as a physical measurement.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.

## Worked mental model

Without scaling, a feature measured in thousands can dominate a feature measured in fractions. K-means minimizes squared distance to centers. Its IDs have no inherent order or meaning.

Work through the [numerical construction](guided.md) before using the complete runner. Explain every new symbol using the [glossary](../../glossary.md).

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
