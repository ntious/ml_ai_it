"""Bounded tuning exercise: choose each model family's settings on training only.

Grouped cross-validation inside the Module 6 training records selects one
configuration per family. Each chosen configuration is then scored once on the
validation records. Gradient boosting is one candidate, not a predetermined
winner. The final-test records are never used.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from .continuation_data import binary_metrics, wine_splits

FOLDS = 3
# Twelve configurations in total; the budget is fixed before any result is seen.
GRID = {
    "logistic": [{"C": value} for value in (0.1, 1.0, 10.0)],
    "tree": [{"max_depth": value} for value in (3, 5, 8)],
    "gradient_boosting": [{"learning_rate": rate, "max_depth": depth} for rate in (0.05, 0.2) for depth in (2, 4)] + [{"learning_rate": 0.1, "max_depth": 3}, {"learning_rate": 0.1, "max_depth": None}],
}


def build(family, settings):
    if family == "logistic":
        return make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced", **settings))
    if family == "tree":
        return DecisionTreeClassifier(class_weight="balanced", min_samples_leaf=5, random_state=42, **settings)
    return HistGradientBoostingClassifier(class_weight="balanced", max_iter=150, random_state=42, **settings)


def tune(split=None, features=None):
    if split is None:
        split, features, _ = wine_splits()
    training, validation = split["train"], split["validation"]
    groups = pd.util.hash_pandas_object(training[features], index=False).astype(str)
    folds = list(GroupKFold(n_splits=FOLDS).split(training, groups=groups))
    trials = []
    for family, candidates in GRID.items():
        for settings in candidates:
            scores = []
            for fit, check in folds:
                model = build(family, settings).fit(training.iloc[fit][features], training.iloc[fit].label)
                scores.append(balanced_accuracy_score(training.iloc[check].label, model.predict(training.iloc[check][features])))
            trials.append({"family": family, "settings": json.dumps(settings, sort_keys=True),
                           "cv_mean_balanced_accuracy": float(np.mean(scores)), "cv_sd": float(np.std(scores, ddof=1))})
    table = pd.DataFrame(trials)
    chosen = []
    for family, part in table.groupby("family", sort=False):
        best = part.sort_values(["cv_mean_balanced_accuracy", "settings"], ascending=[False, True]).iloc[0]
        model = build(family, json.loads(best.settings)).fit(training[features], training.label)
        chosen.append({"family": family, "settings": best.settings, "cv_mean_balanced_accuracy": best.cv_mean_balanced_accuracy,
                       **{"validation_" + key: value for key, value in binary_metrics(validation.label, model.predict(validation[features])).items()}})
    boundary = {"cv_fits": len(trials) * FOLDS, "configurations": len(trials), "final_test_rows_used": 0}
    return table, pd.DataFrame(chosen), boundary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", required=True, help="A new directory for this exercise's evidence.")
    output = Path(parser.parse_args(argv).output)
    if output.exists():
        raise SystemExit(f"Choose a new output directory: {output}")
    trials, chosen, boundary = tune()
    output.mkdir(parents=True)
    trials.to_csv(output / "cv_trials.csv", index=False)
    chosen.to_csv(output / "validation_choices.csv", index=False)
    (output / "summary.json").write_text(json.dumps({**boundary, "selection": "highest mean grouped-CV balanced accuracy on training records; ties by settings text",
        "interpretation": "Development evidence only. Validation scores compare one chosen configuration per family; they are not a final evaluation."}, indent=2) + "\n", encoding="utf-8")
    lines = [f"Module 6 tuning exercise: {boundary['configurations']} configurations, {boundary['cv_fits']} CV fits on training records only"]
    for row in chosen.itertuples():
        lines.append(f"{row.family}: chosen {row.settings}; CV balanced accuracy {row.cv_mean_balanced_accuracy:.3f}; validation balanced accuracy {row.validation_balanced_accuracy:.3f} (recall {row.validation_recall:.3f}, precision {row.validation_precision:.3f})")
    lines.append("Final-test rows used: 0.")
    (output / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
