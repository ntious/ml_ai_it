# Module 2: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module02/practice.ipynb "site-download:module02/practice.ipynb"). In a source checkout open `notebooks/practice/module02-practice.ipynb`. Use the module’s existing environment. Three unfinished functions report **not_attempted**, not a pass.

## Construct `status_counts`

Return a dictionary counting the status string in each record. Predict the result on `[[{'status': 'open'}, {'status': 'closed'}, {'status': 'open'}]]`, implement it and call `m02_status_counts` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for status_counts</summary>

Initialize unseen statuses and handle an empty file.

</details>

## Construct `observed_mean`

Return the mean excluding None; return None if no values are observed. Predict the result on `[[10, None, 20]]`, implement it and call `m02_observed_mean` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for observed_mean</summary>

Missing is not zero; zero is still observed.

</details>

## Construct `output_path`

Return the string path root/runs/run_name/summary.json using pathlib. Predict the result on `['course', 'trial-2']`, implement it and call `m02_output_path` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for output_path</summary>

Keep run names separate from the source file.

</details>

## Transfer to an IT decision

Summarize ticket status with an unknown status added. Explain which output changes and which source remains unchanged. Retain an input, predicted output, actual result and a brief explanation of a failure or limitation. Run the complete module study and verify one claim against its actual artifacts. If you use the published report, identify your evidence as interpretation.

## Evidence and feedback

- **M02.1:** Use lists, dictionaries, conditionals, and loops to summarize records.
- **M02.2:** Call a function with explicit inputs and outputs and import a reusable module.
- **M02.3:** Read CSV and JSON and write a correctly labeled summary.
- **M02.4:** Diagnose a path, type, or input error using its message, traceback where available, and a small check.
- **M02.5:** Run the same processing function from a script and notebook and explain why the results agree.

Start with the [Python foundation bridge](foundation.md) if variables, loops, functions, or paths are unfamiliar. [Module 1](../01-foundations/index.md) supplies the first-run route. You may enter here directly by obtaining the complete source and following the commands below.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

Windows paths normally use backslashes; Linux paths use forward slashes. The path check accepts either representation. `Path(...).as_posix()` explicitly produces forward slashes when a portable display string is desired.
