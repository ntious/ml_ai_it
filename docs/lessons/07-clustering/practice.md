# Module 7: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module07/practice.ipynb "site-download:module07/practice.ipynb"). In a source checkout open `notebooks/practice/module07-practice.ipynb`. Use the [core environment and kernel](../../../QUICKSTART.md#notebook-option); the practice checks need NumPy even where the module script does not. Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `squared_distance`

Return sum of squared coordinate differences for equal-length vectors. Predict the result on `squared_distance([2, 4], [1, 2])`, implement it and call `m07_squared_distance` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for squared_distance</summary>

Square coordinate differences; do not compare signed sums.

</details>

## Construct `select_k`

Input pairs [K, validation_silhouette]; maximize score, smallest K breaks ties. Predict the result on `select_k([[2, 0.4], [3, 0.5], [4, 0.45]])`, implement it and call `m07_select_k` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for select_k</summary>

Use validation geometry and a declared tie-break, not smallest inertia.

</details>

## Construct `profile`

Return string cluster IDs mapped to count and mean of a single original-unit feature. Predict the result on `profile([2, 4, 10], [0, 0, 1])`, implement it and call `m07_profile` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for profile</summary>

Describe both support and feature level; IDs have no rank.

</details>

## Reason beyond the visible checks

Write candidate inertia and silhouette values for K = 2, 3 and 4 for which "smallest inertia" and "highest validation silhouette" select different K. Explain why inertia alone tends to favour the largest K you allow. The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Cluster service workload profiles on development data. State why a cluster alone cannot authorize throttling a service. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M07.1:** Distinguish supervised, unsupervised, and reinforcement learning by the information available.
- **M07.2:** Fit training-only scaling and k-means without quality labels.
- **M07.3:** Compare predefined cluster counts using a validation geometry criterion.
- **M07.4:** Describe clusters through counts and original-unit profiles.
- **M07.5:** Explain why internal scores and observational data do not validate actions or rewards.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Evidence activity: Interpret cluster evidence

Use test_assignments.csv to recompute each cluster size and reconcile with cluster_counts.csv. Interpret one original-unit feature mean in cluster_profiles.csv. Explain why cluster IDs can change between runs without defining new classes, and why agreement with a class label is not the objective used to choose K.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.
