"""Core stability exercise: training randomness versus a changed data split.

Experiment A keeps the Module 6 training/validation split fixed and changes only
the model seed. Experiment B keeps the model seed fixed and redraws the
training/validation split from the development records. The final-test records
are never used, so this is development evidence only.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from .continuation_data import binary_metrics, wine_splits

TRAINING_SEEDS = (11, 23, 37, 53, 71)
SPLIT_SEEDS = (101, 202, 303, 404, 505)
FIXED_MODEL_SEED = 17


def _forest(seed):
    # A random forest uses its seed for bootstrap samples and feature choices; logistic regression would not vary.
    return RandomForestClassifier(n_estimators=50, max_depth=6, min_samples_leaf=5, random_state=seed, n_jobs=1)


def _score(model, training, validation, features):
    model.fit(training[features], training.label)
    predicted = (model.predict_proba(validation[features])[:, 1] >= .5).astype(int)
    return binary_metrics(validation.label, predicted)


def _spread(values):
    values = np.asarray(values, dtype=float)
    return {"runs": len(values), "mean": float(values.mean()), "sd": float(values.std(ddof=1)),
            "min": float(values.min()), "max": float(values.max())}


def compare_variation(split=None, features=None):
    """Return one row per run for both experiments, plus their spreads."""
    if split is None:
        split, features, _ = wine_splits()
    training, validation = split["train"], split["validation"]
    rows = [{"experiment": "A: training seed", "seed": seed, "training_rows": len(training), "validation_rows": len(validation),
             **_score(_forest(seed), training, validation, features)} for seed in TRAINING_SEEDS]
    development = pd.concat([training, validation])
    groups = pd.util.hash_pandas_object(development[features], index=False).astype(str)
    fraction = len(validation) / len(development)
    for seed in SPLIT_SEEDS:
        fit, check = next(GroupShuffleSplit(n_splits=1, test_size=fraction, random_state=seed).split(development, groups=groups))
        rows.append({"experiment": "B: data split", "seed": seed, "training_rows": len(fit), "validation_rows": len(check),
                     **_score(_forest(FIXED_MODEL_SEED), development.iloc[fit], development.iloc[check], features)})
    table = pd.DataFrame(rows)
    spreads = {name: {metric: _spread(part[metric]) for metric in ["balanced_accuracy", "recall"]}
               for name, part in table.groupby("experiment")}
    return table, spreads, {"final_test_rows_used": 0, "development_rows": len(development),
                            "excluded_final_test_rows": len(split["test"])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", required=True, help="A new directory for this exercise's evidence.")
    parser.add_argument("--track", help="Optional JSON-lines experiment log to append this run to.")
    args = parser.parse_args(argv)
    output = Path(args.output)
    if output.exists():
        raise SystemExit(f"Choose a new output directory: {output}")
    table, spreads, boundary = compare_variation()
    output.mkdir(parents=True)
    table.to_csv(output / "variation.csv", index=False)
    summary = {"experiments": spreads, **boundary,
               "interpretation": "Development evidence only. Seed spread measures training randomness; split spread measures sensitivity to which records are used. Neither estimates performance on future data."}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["Module 6 stability exercise (validation records only)"]
    for name, metrics in spreads.items():
        value = metrics["balanced_accuracy"]
        lines.append(f"{name}: balanced accuracy mean {value['mean']:.3f}, sd {value['sd']:.3f}, range {value['min']:.3f}-{value['max']:.3f} over {value['runs']} runs")
    lines.append(f"Final-test rows used: 0 of {boundary['excluded_final_test_rows']}.")
    (output / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if args.track:
        from .tracking import record
        record(args.track, "module06-stability", {"training_seeds": list(TRAINING_SEEDS), "split_seeds": list(SPLIT_SEEDS)},
               {name.split(":")[0] + "_balanced_accuracy_sd": metrics["balanced_accuracy"]["sd"] for name, metrics in spreads.items()})


if __name__ == "__main__":
    main()
