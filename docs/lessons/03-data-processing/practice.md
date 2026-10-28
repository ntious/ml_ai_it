# Module 3: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module03/practice.ipynb "site-download:module03/practice.ipynb"). In a source checkout open `notebooks/practice/module03-practice.ipynb`. Use the [core environment and kernel](../../../QUICKSTART.md#notebook-option); the practice checks need NumPy even where the module script does not. Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `parse_latency`

Parse blank/None as None; otherwise return a nonnegative float, raising ValueError for negatives. Predict the result on `parse_latency('')`, implement it and call `m03_parse_latency` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for parse_latency</summary>

Preserve measured zero and missingness separately.

</details>

## Construct `deduplicate`

Keep the first record for each event_id, preserving input order. Predict the result on `deduplicate([{'event_id': 'a', 'v': 1}, {'event_id': 'a', 'v': 2}, {'event_id': 'b', 'v': 3}])`, implement it and call `m03_deduplicate` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for deduplicate</summary>

Deduplicate by identity, not the entire row.

</details>

## Construct `reconcile`

Return True exactly when nonnegative counts reconcile. Predict the result on `reconcile(10, 7, 2, 1)`, implement it and call `m03_reconcile` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for reconcile</summary>

Every source row needs one accounted-for outcome.

</details>

## Work with the complete study's results

Run the Module 3 preparation and open `cleaned_events.csv` and `quality_report.json`. Check that input rows equal accepted plus rejected rows, then recompute the mean and median latency from the accepted records yourself. Which accepted record must you leave out, and why? Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

Construct two records where deduplicating by the whole row keeps both but deduplicating by `event_id` keeps one. Then write the `reconcile` call that accounts for them, and explain what the complete script would do with the same pair. The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Add a repeated event with a changed annotation and a missing latency. Explain the retained record and reconciliation. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Applied extension: represent categories

The historical phishing attributes are coded -1, 0 and 1. These codes are categories, not measurements, so treating them as numbers assumes an order and equal spacing that may not exist. This extension compares three representations of the same records, fitting every transformation on training records and scoring on validation only. It needs the regression extra (`pip install -e ".[regression]"`) and downloads the attributed UCI data on first use.

```sh
python -m practical_ml_ai.encoding --output runs/module03-encoding
```

- **codes_as_numbers:** the 30 codes, scaled, as numeric inputs.
- **one_hot:** one indicator column per observed code of each attribute. Codes not seen in training are ignored, and the script reports any it meets.
- **one_hot_plus_count:** one-hot columns plus an engineered feature counting how many attributes are -1.

Predict which representation scores best and whether the count helps. Then answer from `summary.txt`:

1. How many model inputs does one-hot encoding create, and why that number rather than 90?
2. Does the engineered count improve validation performance? Use the reported direction check to explain why or why not.
3. Which choice would you carry forward, and what evidence would you need before using it on the final test?

## Evidence and feedback

By completing the core route, you can:

1. **M03.1:** Inspect NumPy shapes/types and use a small vector or linear-system calculation.
2. **M03.2:** Read, filter, summarize, and write a pandas dataframe.
3. **M03.3:** Run a repeatable preparation script and explain rejected records.
4. **M03.4:** Identify CSV, JSON, and array representations with their fields and units.
5. **M03.5:** Write a data dictionary and justify a cleaning choice while preserving later train/test boundaries.

These are resource learning outcomes. They do not claim course credit or certified program-outcome attainment.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Operational-data connection

Use the [RT-IoT completed-flow study](../../../projects/rt-iot-triage/README.md) to apply this module to captured network activity. Trace input availability, grouped evaluation, alert workload and the human review policy.

The reconciliation exercise uses three disjoint categories: accepted, rejected for other reasons, and duplicates. The complete preparation script includes duplicates within its rejected count. Subtract duplicate rejections before translating its report into this exercise; never count the same row twice.

For the RT-IoT transfer, inspect the validation policy comparison and the selected policy before reading final metrics. A model can have high recall while requiring almost every flow to be reviewed. Compare assumed error cost and analyst workload separately; do not lower the threshold after inspecting final results. The project README records the protocol and its qualifications.

## Evidence activity: Audit row accounting

Use your processing report and source events. Trace an accepted record, a rejected record and a duplicate where present. Reconcile the reported input/output counts under the script’s actual processing order; explain how duplicate identity differs from identical rows. If a category is absent, record zero rather than inventing an example.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.
