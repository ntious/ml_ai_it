# Module 7: Distances, groups and useful descriptions

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Geometry determines what is nearby

K-means assigns a point to its nearest center using squared Euclidean distance. For x=[2,4] and centers [1,2] and [4,4], squared distances are 5 and 4, so the second center wins. If the first feature is multiplied by 100, the decision may change. Scaling therefore changes the question, not just numerical convenience. Fit scaling on training and retain original units for explanation.

## Choose K without smuggling in classes

Training inertia generally decreases as K increases, even for unhelpful subdivisions. Validation silhouette contrasts within-cluster cohesion and between-cluster separation, so a predeclared candidate set is preferable to endlessly searching for an attractive picture. This score favors particular geometry. It cannot tell you whether groups deserve different actions or whether a historical quality label is legitimate.

## Describe before naming

A cluster ID is an arbitrary identifier. Swapping 0 and 1 preserves the partition. Report counts and original-unit profiles before assigning names. A group with high average acidity is not automatically bad wine, a risk group or a causal explanation. Reinforcement learning adds actions and feedback over time; a table of observational clusters supplies neither rewards nor evidence for an action policy.

## Trace a small case

Predict `squared_distance([2, 4], [1, 2])` before running: (2−1)² + (4−2)² = 5. Signed differences would sum to 3 and could cancel. Then predict `select_k([[4, 0.5], [2, 0.5]])`: the scores tie, so the declared rule chooses the smaller K, 2. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/wine-clustering/scripts/run.py`. `k_comparison.csv` lists the validation silhouette for each K (0.206 for K = 2, 0.184 for K = 3, 0.162 for K = 4), and selecting K from it is the job of `select_k`. `cluster_profiles.csv` and `cluster_counts.csv` describe clusters by size and original-unit features, which is what `profile` produces. Wine quality is never used to fit or select clusters, so a cluster number is not a quality grade. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. For point `[2, 4]` and centres `[1, 2]` and `[4, 4]`, which centre does k-means choose?</summary>

The second: squared distances are 5 and 4.

</details>

<details>
<summary>2. Training inertia keeps falling as K increases. Should you choose the largest K?</summary>

No. Inertia generally falls with more clusters even when the extra subdivisions are unhelpful. Choose among predeclared candidates using validation silhouette.

</details>

<details>
<summary>3. Cluster 1 has high average acidity. Can you call it the "bad wine" cluster?</summary>

No. Cluster IDs are arbitrary and quality was not used. Describe each cluster's size and original-unit profile before naming anything.

</details>

## Optional reading

[scikit-learn user guide: Clustering](https://scikit-learn.org/stable/modules/clustering.html), the K-means and silhouette sections, explains the inertia objective and why the number of clusters must be chosen by a separate criterion. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
