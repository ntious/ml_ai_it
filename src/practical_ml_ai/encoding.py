"""Categorical encoding exercise on the historical phishing attributes.

The UCI attributes are coded -1, 0 and 1. These are categories, not measured
quantities. This exercise compares three representations on validation records
only: the codes treated as numbers, one-hot categories, and one-hot categories
plus one engineered count. Every transformation is fitted on training records;
the final test is never used.
"""
import argparse
import json
from pathlib import Path
import tempfile
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from .continuation_data import binary_metrics
from .phishing import prepare


def minus_one_count(frame):
    """Engineered feature: how many attributes take the code -1 in each record."""
    return (frame == -1).sum(axis=1).to_frame("minus_one_count")


def representations(features):
    one_hot = OneHotEncoder(handle_unknown="ignore")
    return {
        "codes_as_numbers": make_pipeline(StandardScaler()),
        "one_hot": make_pipeline(one_hot),
        "one_hot_plus_count": ColumnTransformer([
            ("categories", OneHotEncoder(handle_unknown="ignore"), features),
            ("count", make_pipeline(FunctionTransformer(minus_one_count), StandardScaler()), features)]),
    }


def compare(training, validation, features):
    rows = []
    for name, transform in representations(features).items():
        model = make_pipeline(transform, LogisticRegression(max_iter=2000, random_state=42))
        model.fit(training[features], training.label)
        columns = model[:-1].transform(training[features].head(1)).shape[1]
        rows.append({"representation": name, "model_input_columns": int(columns),
                     **binary_metrics(validation.label, model.predict(validation[features]))})
    phishing_rate = {code: [training.loc[training[name] == code, "label"].mean() for name in features] for code in (-1, 1)}
    direction = sum(low > high for low, high in zip(phishing_rate[-1], phishing_rate[1]) if pd.notna(low) and pd.notna(high))
    unseen = {name: sorted(set(validation[name]) - set(training[name])) for name in features}
    evidence = {"features": len(features), "features_where_minus_one_has_higher_training_phishing_rate": int(direction),
                "validation_codes_unseen_in_training": {name: codes for name, codes in unseen.items() if codes},
                "final_test_rows_used": 0}
    return pd.DataFrame(rows), evidence


def load():
    with tempfile.TemporaryDirectory() as folder:
        directory = prepare(Path(folder) / "study")
        protocol = json.loads((directory / "protocol.json").read_text(encoding="utf-8"))
        return pd.read_csv(directory / "train.csv"), pd.read_csv(directory / "validation.csv"), protocol["features"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", required=True, help="A new directory for this exercise's evidence.")
    parser.add_argument("--track", help="Optional JSON-lines experiment log to append this run to.")
    args = parser.parse_args(argv)
    output = Path(args.output)
    if output.exists():
        raise SystemExit(f"Choose a new output directory: {output}")
    training, validation, features = load()
    table, evidence = compare(training, validation, features)
    output.mkdir(parents=True)
    table.to_csv(output / "representations.csv", index=False)
    (output / "summary.json").write_text(json.dumps({**evidence, "training_rows": len(training), "validation_rows": len(validation)}, indent=2) + "\n", encoding="utf-8")
    lines = [f"Categorical encoding exercise: {len(features)} encoded phishing attributes, validation records only"]
    for row in table.itertuples():
        lines.append(f"{row.representation}: {row.model_input_columns} model inputs; validation balanced accuracy {row.balanced_accuracy:.3f}, recall {row.recall:.3f}, false-positive rate {row.fpr:.3f}")
    lines.append(f"Attributes where -1 has the higher training phishing rate than +1: {evidence['features_where_minus_one_has_higher_training_phishing_rate']} of {len(features)}")
    lines.append(f"Validation codes unseen in training: {evidence['validation_codes_unseen_in_training'] or 'none'}")
    lines.append("Final-test rows used: 0.")
    (output / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if args.track:
        from .tracking import record
        record(args.track, "module03-encoding", {"representations": table.representation.tolist()},
               {row.representation + "_validation_balanced_accuracy": float(row.balanced_accuracy) for row in table.itertuples()})


if __name__ == "__main__":
    main()
