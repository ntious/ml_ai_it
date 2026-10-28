# Module 4: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module04/practice.ipynb "site-download:module04/practice.ipynb"). In a source checkout open `notebooks/practice/module04-practice.ipynb`. Use the module’s existing environment. Three unfinished functions report **not_attempted**, not a pass.

## Construct `error_rate`

Return errors/requests; None when requests is zero. Predict the result on `[3, 10]`, implement it and call `m04_error_rate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for error_rate</summary>

A zero denominator is unavailable, not zero percent.

</details>

## Construct `median`

Return the median of a nonempty numerical list, without changing the input. Predict the result on `[[1, 2, 3, 100]]`, implement it and call `m04_median` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for median</summary>

Average the two middle observations for an even count.

</details>

## Construct `weighted_rate`

Input pairs [errors, requests]. Return total errors / total requests, or None. Predict the result on `[[[1, 2], [1, 8]]]`, implement it and call `m04_weighted_rate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for weighted_rate</summary>

Do not average daily percentages with unequal denominators.

</details>

## Transfer to an IT decision

Compare request counts and error rates for two services with unequal volume. Write a caption that prevents a misleading ranking. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M04.1:** Justify a preprocessing choice for an exploratory question and explain what information it may remove.
- **M04.2:** Create labeled distribution, comparison, and relationship/time plots with appropriate scales and units.
- **M04.3:** Explain a pattern or anomaly with numerical evidence while distinguishing association from causation.
- **M04.4:** Write a stakeholder summary with chart descriptions, underlying values, and limitations.

You need basic functions, file paths, and dataframe selection/grouping. Use the [foundation bridge](foundation.md), [Module 2](../02-python-workflows/index.md), or [Module 3](../03-data-processing/index.md) as needed. You may enter here directly with the complete source archive and setup below.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.
