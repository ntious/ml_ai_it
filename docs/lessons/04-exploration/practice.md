# Module 4: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module04/practice.ipynb "site-download:module04/practice.ipynb"). In a source checkout open `notebooks/practice/module04-practice.ipynb`. Use the [core environment and kernel](../../../QUICKSTART.md#notebook-option); the practice checks need NumPy even where the module script does not. Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `error_rate`

Return errors/requests; None when requests is zero. Predict the result on `error_rate(3, 10)`, implement it and call `m04_error_rate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for error_rate</summary>

A zero denominator is unavailable, not zero percent.

</details>

## Construct `median`

Return the median of a nonempty numerical list, without changing the input. Predict the result on `median([1, 2, 3, 100])`, implement it and call `m04_median` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for median</summary>

Average the two middle observations for an even count.

</details>

## Construct `weighted_rate`

Input pairs [errors, requests]. Return total errors / total requests, or None. Predict the result on `weighted_rate([[1, 2], [1, 8]])`, implement it and call `m04_weighted_rate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for weighted_rate</summary>

Do not average daily percentages with unequal denominators.

</details>

## Work with the complete study's results

Run the Module 4 exploration and open `request_latency.csv`. Apply your `median` to the observed `p95_latency_ms` values, leaving out the unavailable one. Compare your result with "Median daily service p95" in `summary.txt`, and explain why the mean in the same file is higher. Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

Choose daily counts `[errors, requests]` for two days so that the average of the daily error rates differs from `weighted_rate`. Explain which number answers "what fraction of all requests failed?" The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Compare request counts and error rates for two services with unequal volume. Write a caption that prevents a misleading ranking. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Evidence and feedback

- **M04.1:** Justify a preprocessing choice for an exploratory question and explain what information it may remove.
- **M04.2:** Create labeled distribution, comparison, and relationship/time plots with appropriate scales and units.
- **M04.3:** Explain a pattern or anomaly with numerical evidence while distinguishing association from causation.
- **M04.4:** Write a stakeholder summary with chart descriptions, underlying values, and limitations.

You need basic functions, file paths, and dataframe selection/grouping. Use the [foundation bridge](foundation.md), [Module 2](../02-python-workflows/index.md), or [Module 3](../03-data-processing/index.md) as needed. You may enter here directly with the complete source archive and setup below.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.
