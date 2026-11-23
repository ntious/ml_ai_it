# Core bridge: which randomness changed?

After Module 6, investigate stability using the existing capstone implementation and core environment. This is a bounded development exercise: one configuration per substantive family, three training-only folds (nine search fits), three training seeds and three split seeds. The dummy baseline remains. There is no new framework or dependency. The historical phishing data downloads from its attributed, checksum-verified source; it is not the wine dataset from Module 6.

Before running, predict which model family will change with its training seed and explain what you hold fixed. From the repository root, use your core environment executable wherever `python` appears:

```sh
python projects/phishing-triage/scripts/run.py prepare --run runs/core-stability --config projects/phishing-triage/configs/core-stability.json
python projects/phishing-triage/scripts/run.py tune --run runs/core-stability
python projects/phishing-triage/scripts/run.py stability --run runs/core-stability
python projects/phishing-triage/scripts/run.py split-study --run runs/core-stability
python projects/phishing-triage/scripts/run.py stability --run runs/core-stability --resume
python projects/phishing-triage/scripts/run.py split-study --run runs/core-stability --resume
```

Use a new run directory if one already exists. Stop here: this activity does not freeze or evaluate the final test partition. The original prepare stage creates the partition files, but the tuning and sensitivity stages do not use final-test outcomes for selection. Do not inspect or tune against them.

## Calculate and explain

1. Open `validation_runs.csv` and `validation_stability.csv`. For one substantive family, calculate the mean and sample standard deviation (ddof=1) of the declared seed costs. Retain every seed and reconcile with the summary. Explain that the family’s common threshold was selected from mean validation cost, not independently optimized per seed.
2. Open `split_sensitivity.csv`. Identify the changing split seed and fixed training seed. Explain why these scores vary the observations rather than only model randomness. The configuration has already been selected using training observations, so these are descriptive sensitivity checks.
3. Compare the questions answered by the two experiments. Do not subtract their spreads as a causal estimate: they use different partitions and observations. The split study uses a fixed threshold of 0.5, while the training-seed table uses a validation-selected common threshold per family; this is another reason not to interpret their difference as a causal effect. Neither spread is a population confidence interval.
4. Give a peer the configuration and commands for a separate run. Compare deterministic counts and declared numeric tolerances, excluding timing fields. Record any discrepancy using the [worksheet](../../templates/evidence-review.md).

<details><summary>Expected reasoning after your attempt</summary>
Logistic regression with the configured lbfgs solver is deterministic here; changing its seed can leave results unchanged. Tree tie-breaking and forest sampling can respond to seeds. Identical observed scores remain possible and are valid findings. Split sensitivity changes which groups appear in development subsets. None of these observations establishes generalization to future campaigns or another institution.
</details>

For a safe integrity exercise, copy this run to another directory, change one numeric value in a copied CSV and invoke the matching completed stage with `--resume` on the copy. Expect rejection; keep the original intact. Explain which recorded evidence detected the change. The ledger detects accidental modification, not a malicious owner rewriting the ledger itself.

Continue to the [full stability investigation](stability.md) when ready for the larger protocol. Record actual runtime and learner effort separately; this smaller configuration has not been workload-tested with students.
