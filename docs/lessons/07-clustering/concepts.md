# Module 7: Distances, groups and useful descriptions

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Geometry determines what is nearby

K-means assigns a point to its nearest center using squared Euclidean distance. For x=[2,4] and centers [1,2] and [4,4], squared distances are 5 and 4, so the second center wins. If the first feature is multiplied by 100, the decision may change. Scaling therefore changes the question, not just numerical convenience. Fit scaling on training and retain original units for explanation.

## Choose K without smuggling in classes

Training inertia generally decreases as K increases, even for unhelpful subdivisions. Validation silhouette contrasts within-cluster cohesion and between-cluster separation, so a predeclared candidate set is preferable to endlessly searching for an attractive picture. This score favors particular geometry. It cannot tell you whether groups deserve different actions or whether a historical quality label is legitimate.

## Describe before naming

A cluster ID is an arbitrary identifier. Swapping 0 and 1 preserves the partition. Report counts and original-unit profiles before assigning names. A group with high average acidity is not automatically bad wine, a risk group or a causal explanation. Reinforcement learning adds actions and feedback over time; a table of observational clusters supplies neither rewards nor evidence for an action policy.

## Trace a small case

The first operation is **squared_distance**: Return sum of squared coordinate differences for equal-length vectors. On authored arguments `squared_distance([2, 4], [1, 2])`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/wine-clustering/scripts/run.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Further reading: clustering](https://scikit-learn.org/stable/modules/clustering.html) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
