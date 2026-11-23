# Applied teaching prototype: owner and independent-review handoff

This change addresses the explanation/practice/feedback gap in Modules 5, 6 and 8. It preserves their outcome text, 14-module order, original modeling code, complete reference commands and distinction between optional depth and core evidence. It does not claim superiority to another institution or completed human piloting.

## Review the learner route

Start with each module's index and follow foundation → concepts → guided construction → practice → practice solutions → complete reference and recorded feedback:

- [Module 5](../../lessons/05-regression/index.md): origin/lag timing, residual versus MAE, training-only preprocessing and validation baseline comparison.
- [Module 6](../../lessons/06-classification/index.md): labels, inclusive thresholds, denominators, cost sensitivity, preprocessing and the complete reference's shallow-tree explanation.
- [Module 8](../../lessons/08-neural-networks/index.md): activations/shapes, a concrete output update, validation checkpoint restoration, model construction and saved replay.

Six clean notebooks under `notebooks/practice/` separate learner functions from worked solutions. A visible `not_attempted` result is deliberately not a pass. Checks call the learner's functions; completing the reference solution does not establish independent mastery. The unchanged outcomes are checked against recorded hashes in `curriculum/practice.json`.

## Check the evidence boundaries

1. The figures use original, explicitly authored hand examples and matching tables. The neural illustrative loss history is not presented as an observed course result.
2. Module 5's sandbox uses the first 81 source dates: seven warm-up days, 60 training targets and 14 validation targets. It answers a rolling daily-origin question, not an all-days-ahead batch forecast. Its result must not be substituted for the complete reference's 110-date final evaluation.
3. Module 6 uses the existing grouped development partitions. Logistic and training-prior probabilities receive thresholds from the same validation cost rule. The assumed costs are not measured operating costs. The complete reference's original selection criterion remains intact.
4. Module 8's sandbox uses bounded training/validation slices, eight epochs, an explicit gradient loop, checkpoint weights and numeric saved-model replay. The complete reference retains its larger protocol, logistic comparison and final evaluation. Sandbox selection never uses final labels.
5. Local feedback covers visible cases and plausible mistakes. Review explanations, changed cases and transfer artifacts separately. Check that incorrect signed MAE, target-day persistence, exclusive threshold comparison, cost-insensitive selection, training-loss selection and leaked imputation are rejected.

## Reproduce technical checks

Use the existing separate environments and registered kernels:

```sh
python scripts/check_repository.py
ML_AI_REAL_DATA=1 python -m unittest discover -s tests
python scripts/check_practice.py --group core --kernel ml-ai-core
```

In the framework environment:

```sh
python scripts/check_practice.py --group frameworks --kernel ml-ai-frameworks
```

The checker executes each starter and solution in a fresh kernel. Starters must report three unfinished tasks and skip the real sandbox. Solutions must pass three checks and execute it. Generated evidence includes source/check hashes, environment versions and executed notebook copies under `runs/verified/practice/`. The site build rejects stale practice identities. CI runs both profiles and includes these outputs in the existing verification artifacts.

The existing full-site build also needs the usual verified module/case/capstone outputs. Then run:

```sh
npm run build
python scripts/check_site.py
python scripts/check_http_routes.py
python scripts/check_downloads.py
node scripts/check_browser.mjs
npm run check:browser
```

Windows users should set `ML_AI_REAL_DATA` using their shell's environment-variable syntax. Notebook and browser execution records are technical evidence, not a human accessibility claim.

## Applied depth and external sources

The new explanations, tasks, figures and solutions are original. The reviewed university materials informed the teaching pattern; their assignments and prose were not imported. Optional links point to open D2L textbook explanations, official scikit-learn/TensorFlow documentation and a named UBC alternative explanation. The core does not add proofs, a new framework requirement or mandatory advanced topics.

## Owner review and pilot decision

Use the [pilot protocol](../../instructor/teaching-prototype-pilot.md) and [observation template](../../../templates/learner-pilot.md). **Human pilot: NOT RUN.** Review whether a new learner can locate the route, recover using a hint, implement and explain a changed case, preserve boundaries and save usable evidence. Record actual workload and access barriers. Ask the independent reviewer to assess clarity, task difficulty, check quality, solution separation and outcome coverage before extending this pattern beyond the three prototypes.
