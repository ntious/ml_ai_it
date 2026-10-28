# Module 9: implement, explain and transfer

Read [concepts](concepts.md), then attempt [the starter notebook](https://ntious.github.io/ml_ai_it/downloads/module09/practice.ipynb "site-download:module09/practice.ipynb"). In a source checkout open `notebooks/practice/module09-practice.ipynb`. Use the [framework environment and kernel](../../setup/frameworks.md). Three unfinished functions report **not_attempted**, not a pass. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Construct `vocabulary`

Return alphabetical lowercase whitespace tokens with IDs starting at 2; 0=padding,1=unknown. Predict the result on `vocabulary(['FREE offer', 'offer now'])`, implement it and call `m09_vocabulary` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for vocabulary</summary>

Fit only training text and reserve unknown/padding separately.

</details>

## Construct `encode`

Lowercase/split, map unknown to 1, keep first length tokens and pad with 0. Predict the result on `encode('NEW offer', {'offer': 2}, 4)`, implement it and call `m09_encode` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for encode</summary>

Unknown is not padding; declare truncation direction.

</details>

## Construct `recall`

Return TP/(TP+FN); None when there are no actual positives. Predict the result on `recall(0, 10)`, implement it and call `m09_recall` through the notebook check. Then add a changed case and explain which assumption it tests.

<details>
<summary>Hint for recall</summary>

Use actual positives, not total messages or predicted positives.

</details>

## Work with the complete study's results

Open `comparison.csv` from the complete study. Recompute recall and precision for the neural model and the lexical baseline from their TP, FN and FP counts. Which finds more spam, and what does it cost in false alarms? Compare with the [construction feedback](solutions.md#complete-study-results-feedback) afterwards.

## Reason beyond the visible checks

With `vocab = vocabulary(['FREE offer', 'offer now'])`, predict `encode('Offer FREE prize now', vocab, 3)`. Which word is lost, which becomes unknown, and what would a length of 2 also lose? The checks cannot mark this; compare your reasoning with the [construction feedback](solutions.md#reasoning-task-feedback).

## Transfer to an IT decision

Add a message with unseen words and a suspicious suffix beyond the length limit. Explain what the model can and cannot inspect. Run the complete module study and verify one claim against its actual artifacts; keep the evidence the [study workflow](../../study-workflow.md#save-evidence-that-explains-your-work) lists.

## Evidence and feedback

- **M09.1:** Explain tokenization, vocabulary, padding, embeddings, and pooling.
- **M09.2:** Deduplicate real texts before a declared sample/split.
- **M09.3:** Adapt text preprocessing only on training and train a TensorFlow text model.
- **M09.4:** Compare neural errors with TF-IDF/logistic regression.
- **M09.5:** Document privacy, prevalence, vocabulary limits, and reproducibility.

Use [construction feedback](solutions.md) after an attempt and [recorded experiment feedback](feedback.md) for the full workflow. Follow [the shared study workflow](../../study-workflow.md) for evidence, recovery and optional AI disclosure. Official assessment weights remain with your instructor.

## Evidence activity: Compare on the same messages

Use saved neural and lexical-baseline results. Recompute recall from confusion counts and compare their evaluation denominators before interpreting a difference. Trace one false negative when present; distinguish an observed error from a claim about all future spam.

Follow the four steps in [reproduce a result and justify its use](../../evidence-practice.md). Submit your artifact path, independent calculation, discrepancy or agreement, and bounded use decision in the [evidence worksheet](../../../templates/evidence-review.md). Use your complete reference run; this activity complements the small function checks.
