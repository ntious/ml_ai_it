# A repeatable study workflow

Start with the module foundation when its vocabulary is unfamiliar. Read the concept example, predict its result, then attempt the starter notebook before opening solutions. Keep the complete reference for connecting your small operation to the full experiment.

## Save evidence that explains your work

Keep changed code, the input, your expected result, the actual output, one diagnosed failure or limitation and a short explanation, and name the module outcome each item supports. Include source attribution and environment versions for a full experiment. An executed reference demonstrates reproduction; a changed case and its explanation provide evidence of your understanding.

## Recover from an expected failure

Edit the practice function or your own configuration. Inspect the visible check and the named report. Keep source data, provenance and completed run artifacts intact. If a completed study rejects changed inputs or code, retain that study and start a new named output directory using the module command. Compare the two reports rather than altering the old manifest. Restart the notebook kernel and run all cells if a value depends on earlier hidden state.

## How explanations are judged

These criteria apply to every module's practice, transfer task and mastery check.

- **Developing:** the visible checks pass or the expected report is reproduced, but you cannot yet explain or change the central operation, or name its denominator, boundary or contract.
- **Meets the task:** you predict a changed case correctly, implement it, reconcile it with a specific module artifact and keep the evaluation boundary.
- **Extends:** you show where the operation is insufficient for the transfer case, or run a predeclared experiment and report its measured tradeoffs. Extra complexity alone does not extend the task.

A satisfactory response includes the calculation or a concrete counterexample, the fitting or decision boundary, your changed code and one limitation. A changed narrative alone is insufficient: keep the changed inputs or code and the observed outputs. Interpretation-only work can show reasoning, but implementation outcomes need an executed and explained modification; a screenshot or copied report is not enough. If you rely on a published report rather than your own run, label that evidence as interpretation. When a claim comes from published work, follow the [research comparison guide](advanced/research-comparison.md).

## Use feedback deliberately

A failed check identifies a case to investigate. Trace the input by hand, change one operation and rerun. A passing check covers its visible cases; add a boundary or changed case before claiming the function is generally correct. Use the separate solution to explain a discrepancy, then reconstruct the operation without copying.

## Optional AI assistance

Ask for a critique of your reasoning or a hint about a failing case. Verify suggestions against actual artifacts. Record material assistance and what you accepted or rejected according to your instructor’s policy. Keep personal records and secrets out of prompts. A solo alternative is to write the strongest counterargument to your own interpretation.

## Track your experiments (optional)

When you compare runs, record each one the same way. The stability, tuning, encoding and retrieval exercises accept `--track runs/experiments.jsonl`, which appends one JSON line with the settings, metrics, Python and package versions and the input files' SHA-256 hashes. List the runs with `python -m practical_ml_ai.tracking runs/experiments.jsonl`. Experiment trackers such as MLflow add a server and a user interface on top of the same idea.

## Prepare for review

Explain one design choice, one observed limitation and one development-only next investigation. Keep final-test evidence out of model selection. Official deadlines, submission formats and grading weights belong to the adopting instructor.
