"""One-day-ahead forecasting: prepare, train, validate, evaluate, and infer.

The selected model is frozen before final evaluation. Models are stored as
transparent numeric JSON, not executable pickle files. These small exporters
support only this lesson's named linear and baseline models.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
import io
import json
from pathlib import Path
import platform
import urllib.request
import zipfile

import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline

FEATURES = ["prior_day_requests", "prior_week_requests"]
TARGET = "target_requests"
MODEL_FEATURES = {"linear_day": ["prior_day_requests"], "linear_week": ["prior_week_requests"]}
BASELINES = ["training_mean", "previous_day", "previous_week"]
UCI_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"
UCI_PAGE = "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset"
# Verified in the initial Windows/Linux real-data CI run; review upstream changes.
UCI_ARCHIVE_SHA256 = "b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value, exclusive=False):
    """Exclusive writes stop accidental repetition of a frozen study stage."""
    with Path(path).open("x" if exclusive else "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def download_bike_data(output_dir):
    """Fetch the official CC BY 4.0 archive once, retaining attribution/hashes.

    Reuse checks the cached CSV's recorded digest. New retrievals must match the archive digest verified in this lesson's
    initial real-data integration run; upstream changes require review.
    """
    output_dir = Path(output_dir)
    daily, provenance = output_dir / "day.csv", output_dir / "provenance.json"
    if daily.exists() or provenance.exists():
        if not daily.exists() or not provenance.exists():
            raise ValueError("Incomplete data cache; use a new directory or restore its original files.")
        metadata = read_json(provenance)
        if metadata.get("archive_sha256") != UCI_ARCHIVE_SHA256:
            raise ValueError("Cached archive provenance differs from the reviewed source version.")
        if digest(daily) != metadata["day_csv_sha256"]:
            raise ValueError("Cached day.csv checksum changed; keep raw data unchanged.")
        return daily
    with urllib.request.urlopen(UCI_URL, timeout=45) as response:
        archive_bytes = response.read(2_000_001)
    if len(archive_bytes) > 2_000_000:
        raise ValueError("Unexpectedly large archive; inspect the upstream source.")
    if hashlib.sha256(archive_bytes).hexdigest() != UCI_ARCHIVE_SHA256:
        raise ValueError("Upstream archive checksum changed; review the new source before using it.")
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        daily_bytes = archive.read("day.csv")
        readme_bytes = archive.read("Readme.txt")
    # Validate actual content before creating a cache. No arbitrary ZIP extraction.
    candidate = pd.read_csv(io.BytesIO(daily_bytes))
    if not {"dteday", "cnt"}.issubset(candidate.columns):
        raise ValueError("The downloaded daily file does not match the documented UCI fields.")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "original.zip").write_bytes(archive_bytes)
    daily.write_bytes(daily_bytes)
    (output_dir / "Readme.txt").write_bytes(readme_bytes)
    metadata = {
        "source": UCI_PAGE, "download_url": UCI_URL,
        "citation": "Fanaee-T, H. (2013). Bike Sharing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894.",
        "license": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        "day_csv_sha256": digest(daily),
        "changes": "None to archived day.csv. Later preparation selects dteday/cnt and derives past-only lag features.",
    }
    write_json(provenance, metadata)
    (output_dir / "ATTRIBUTION.txt").write_text(metadata["citation"] + "\nLicense: CC BY 4.0\nSource: " + UCI_PAGE + "\nOriginal CSV unchanged; derived examples select fields and construct lag features.\n", encoding="utf-8")
    return daily


def read_daily(path):
    """Accept UCI dteday/cnt or the explicitly synthetic date/requests fixture."""
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if {"dteday", "cnt"}.issubset(frame.columns):
        frame = frame[["dteday", "cnt"]].rename(columns={"dteday": "date", "cnt": "requests"})
    elif {"date", "requests"}.issubset(frame.columns):
        frame = frame[["date", "requests"]].copy()
    else:
        raise ValueError("Daily CSV needs dteday/cnt (UCI) or date/requests (synthetic).")
    if not frame["date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
        raise ValueError("Dates must use YYYY-MM-DD.")
    frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="raise")
    if len(frame) < 42:
        raise ValueError("At least 42 consecutive days are needed for this teaching split.")
    if not frame["date"].diff().iloc[1:].eq(pd.Timedelta(days=1)).all():
        raise ValueError("Dates must be unique, ascending, and consecutive; do not treat absent days as zero.")
    if not frame["requests"].str.fullmatch(r"[0-9]+").all():
        raise ValueError("Requests must be nonnegative whole-number text, with no missing targets.")
    counts = frame["requests"].map(int)
    if any(value > 1_000_000_000 for value in counts):
        raise ValueError("Counts exceed this teaching contract's upper bound of one billion.")
    frame["requests"] = counts.astype("int64")
    return frame


def build_examples(daily):
    """Target day d uses only d-1 and d-7 counts, known at origin d-1 end-of-day."""
    examples = pd.DataFrame({
        "origin_date": daily["date"] - pd.Timedelta(days=1),
        "target_date": daily["date"],
        "prior_day_requests": daily["requests"].shift(1),
        "prior_week_requests": daily["requests"].shift(7),
        TARGET: daily["requests"],
    }).iloc[7:].reset_index(drop=True)
    # The next forecast has no target column: tomorrow has not been observed.
    last = daily.iloc[-1]
    future = pd.DataFrame([{
        "origin_date": last["date"],
        "target_date": last["date"] + pd.Timedelta(days=1),
        "prior_day_requests": int(last["requests"]),
        "prior_week_requests": int(daily.iloc[-7]["requests"]),
    }])
    return examples, future


def prepare_study(input_path, run_dir, holdout_days=14):
    """Create a fresh run directory with chronological train/validation/test files."""
    input_path, run_dir = Path(input_path), Path(run_dir)
    if run_dir.exists():
        raise ValueError("Use a new run directory; preparation does not overwrite an existing study.")
    if isinstance(holdout_days, bool) or not isinstance(holdout_days, int) or holdout_days < 7:
        raise ValueError("Each holdout must contain at least seven days.")
    daily = read_daily(input_path)
    examples, future = build_examples(daily)
    training_count = len(examples) - 2 * holdout_days
    if training_count < 7:
        raise ValueError("Not enough training rows after the two holdouts.")
    splits = {
        "train": examples.iloc[:training_count],
        "validation": examples.iloc[training_count:training_count + holdout_days],
        "final_test": examples.iloc[training_count + holdout_days:],
    }
    run_dir.mkdir(parents=True)
    manifest = {
        "source_sha256": digest(input_path), "raw_days": len(daily),
        "features": FEATURES, "target": TARGET,
        "protocol": "Fixed parameters; rolling one-day-ahead origins. Later origins may use earlier observed holdout counts. No refitting during holdouts.",
        "selection": "Lowest validation MAE, tie broken alphabetically; final test never selects the model.",
        "splits": {},
    }
    for name, frame in splits.items():
        path = run_dir / (name + ".csv")
        frame.to_csv(path, index=False, date_format="%Y-%m-%d")
        manifest["splits"][name] = {
            "rows": len(frame), "first_target": frame["target_date"].iloc[0].strftime("%Y-%m-%d"),
            "last_target": frame["target_date"].iloc[-1].strftime("%Y-%m-%d"), "sha256": digest(path),
        }
    future.to_csv(run_dir / "future_features.csv", index=False, date_format="%Y-%m-%d")
    write_json(run_dir / "split_manifest.json", manifest, exclusive=True)
    return manifest


def load_split(run_dir, name):
    """Read only the requested split and verify that its prepared bytes match."""
    run_dir = Path(run_dir)
    manifest = read_json(run_dir / "split_manifest.json")
    if name not in {"train", "validation", "final_test"}:
        raise ValueError("Unknown split.")
    path = run_dir / (name + ".csv")
    if digest(path) != manifest["splits"][name]["sha256"]:
        raise ValueError("Prepared split changed; start a new study instead of altering frozen inputs.")
    return pd.read_csv(path)


def feature_values(frame, features):
    if not features or not set(features).issubset(FEATURES):
        raise ValueError("Only declared past-only features are allowed; target-time information is not a feature.")
    values = frame[features].apply(pd.to_numeric, errors="raise").to_numpy(dtype=float)
    if np.isinf(values).any():
        raise ValueError("Feature values must be finite or explicitly missing.")
    return values


def fit_linear(training, features):
    """Imputer fitting belongs to training, including within each CV fold."""
    values = feature_values(training, features)
    if np.isnan(values).all(axis=0).any():
        raise ValueError("A feature has no observed training values; do not fill it from a holdout.")
    pipeline = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
    pipeline.fit(values, training[TARGET].to_numpy(dtype=float))
    artifact = {
        "kind": "linear", "features": list(features),
        "fill_values": pipeline[0].statistics_.tolist(),
        "coefficients": np.atleast_1d(pipeline[1].coef_).tolist(),
        "intercept": float(pipeline[1].intercept_),
    }
    return pipeline, artifact


def predict_artifact(artifact, frame):
    """Apply this lesson's numeric JSON without refitting or deserializing code."""
    kind = artifact["kind"]
    if kind == "mean":
        result = np.full(len(frame), float(artifact["constant"]))
    else:
        values = feature_values(frame, artifact["features"])
        if kind == "copy":
            if np.isnan(values).any():
                raise ValueError("A persistence baseline needs its observed lag value.")
            result = values[:, 0]
        elif kind == "linear":
            fills = np.asarray(artifact["fill_values"], dtype=float)
            coefficients = np.asarray(artifact["coefficients"], dtype=float)
            if len(fills) != values.shape[1] or len(coefficients) != values.shape[1]:
                raise ValueError("Model feature dimensions do not match.")
            values = np.where(np.isnan(values), fills, values)
            result = values @ coefficients + float(artifact["intercept"])
        else:
            raise ValueError("Unsupported model kind.")
    if not np.isfinite(result).all():
        raise ValueError("Prediction must be finite.")
    return result


def training_cv(training):
    """Three expanding-window folds inside training only; not random shuffling."""
    rows = []
    for fold, (fit_ids, check_ids) in enumerate(TimeSeriesSplit(n_splits=3).split(training), start=1):
        fit_rows, check_rows = training.iloc[fit_ids], training.iloc[check_ids]
        _, artifact = fit_linear(fit_rows, MODEL_FEATURES["linear_week"])
        rows.append({
            "fold": fold, "fit_rows": len(fit_rows), "check_rows": len(check_rows),
            "last_fit_target": fit_rows["target_date"].iloc[-1],
            "first_check_target": check_rows["target_date"].iloc[0],
            "mae": float(mean_absolute_error(check_rows[TARGET], predict_artifact(artifact, check_rows))),
        })
    return pd.DataFrame(rows)


def train_study(run_dir):
    """Fit on training only. No validation/final-test CSV is opened."""
    run_dir = Path(run_dir)
    if (run_dir / "candidates.json").exists() or (run_dir / "selection.json").exists():
        raise ValueError("Training is already recorded; use a new study for another experiment.")
    training = load_split(run_dir, "train")
    dummy = DummyRegressor(strategy="mean").fit(training[FEATURES], training[TARGET])
    models = {
        "training_mean": {"kind": "mean", "constant": float(dummy.constant_[0, 0])},
        "previous_day": {"kind": "copy", "features": ["prior_day_requests"]},
        "previous_week": {"kind": "copy", "features": ["prior_week_requests"]},
    }
    for name, features in MODEL_FEATURES.items():
        _, models[name] = fit_linear(training, features)
    training_cv(training).to_csv(run_dir / "training_cv.csv", index=False)
    result = {
        "manifest_sha256": digest(run_dir / "split_manifest.json"), "models": models,
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scikit_learn": sklearn.__version__},
        "training_rows": len(training), "fit_boundary": "train only; no final refit on train+validation in this lesson",
    }
    write_json(run_dir / "candidates.json", result, exclusive=True)
    return result


def validated_candidates(run_dir):
    run_dir = Path(run_dir)
    candidates = read_json(run_dir / "candidates.json")
    if candidates["manifest_sha256"] != digest(run_dir / "split_manifest.json"):
        raise ValueError("Candidate artifact belongs to a different split manifest.")
    return candidates


def validate_study(run_dir):
    """Choose among baselines and linear models using validation MAE only."""
    run_dir = Path(run_dir)
    if (run_dir / "selection.json").exists():
        raise ValueError("Selection is frozen; use a new study for a new protocol.")
    candidates = validated_candidates(run_dir)
    validation = load_split(run_dir, "validation")
    scores = [
        {"model": name, "mae": float(mean_absolute_error(validation[TARGET], predict_artifact(model, validation)))}
        for name, model in candidates["models"].items()
    ]
    scores.sort(key=lambda row: (row["mae"], row["model"]))
    pd.DataFrame(scores).to_csv(run_dir / "validation_scores.csv", index=False)
    selection = {
        "selected": scores[0]["model"], "validation_mae": scores[0]["mae"],
        "candidate_sha256": digest(run_dir / "candidates.json"),
        "rule": "minimum validation MAE, alphabetical tie break; baselines are eligible to win",
    }
    write_json(run_dir / "selection.json", selection, exclusive=True)
    return selection


def locked_models(run_dir):
    run_dir = Path(run_dir)
    candidates = validated_candidates(run_dir)
    selection = read_json(run_dir / "selection.json")
    if selection["candidate_sha256"] != digest(run_dir / "candidates.json"):
        raise ValueError("Candidates changed after selection.")
    if selection["selected"] not in candidates["models"]:
        raise ValueError("Selected model is absent from its candidate artifact.")
    return selection, candidates


def evaluate_study(run_dir):
    """Evaluate the frozen selection and predefined baselines; never fit/select."""
    run_dir = Path(run_dir)
    if (run_dir / "final_evaluation.json").exists():
        raise ValueError("Final evaluation is already recorded. Do not tune against its results.")
    selection, candidates = locked_models(run_dir)
    test = load_split(run_dir, "final_test")
    names = list(dict.fromkeys([selection["selected"], *BASELINES]))
    predictions, scores = [], []
    for name in names:
        predicted = predict_artifact(candidates["models"][name], test)
        residual = test[TARGET].to_numpy(dtype=float) - predicted
        scores.append({"model": name, "mae": float(np.abs(residual).mean()), "mean_residual": float(residual.mean()), "negative_predictions": int((predicted < 0).sum())})
        for date, actual, estimate, error in zip(test["target_date"], test[TARGET], predicted, residual):
            predictions.append({"target_date": date, "model": name, "actual_requests": int(actual), "predicted_requests": float(estimate), "residual": float(error)})
    result = {"selected": selection["selected"], "test_rows": len(test), "scores": scores, "residual_definition": "actual minus predicted; positive means underprediction", "protocol": "Frozen model, rolling one-day-ahead features; no parameter updates."}
    pd.DataFrame(predictions).to_csv(run_dir / "final_predictions.csv", index=False)
    write_json(run_dir / "final_evaluation.json", result, exclusive=True)
    return result


def infer_study(run_dir, features_path=None):
    """Predict tomorrow with the frozen artifact; no target labels are required."""
    run_dir = Path(run_dir)
    selection, candidates = locked_models(run_dir)
    path = Path(features_path) if features_path is not None else run_dir / "future_features.csv"
    protected = {run_dir / "forecast.csv", run_dir / "summary.txt", run_dir / "index.html", run_dir / "forecast.png", run_dir / "residuals.png"}
    if path.resolve() in {p.resolve() for p in protected}:
        raise ValueError("Keep inference inputs separate from generated outputs.")
    frame = pd.read_csv(path)
    if TARGET in frame.columns:
        raise ValueError("Inference requires features only; remove target_requests.")
    origin = pd.to_datetime(frame["origin_date"], format="%Y-%m-%d", errors="raise")
    target = pd.to_datetime(frame["target_date"], format="%Y-%m-%d", errors="raise")
    if frame.empty or not (target - origin).eq(pd.Timedelta(days=1)).all():
        raise ValueError("Each forecast target must be one day after its origin.")
    output = frame[["origin_date", "target_date"]].copy()
    output["model"] = selection["selected"]
    output["predicted_requests"] = predict_artifact(candidates["models"][selection["selected"]], frame)
    output.to_csv(run_dir / "forecast.csv", index=False)
    return output


def leakage_demo(training, validation):
    """INVALID example: target itself as input, deliberately outside selection."""
    model = LinearRegression().fit(training[[TARGET]], training[TARGET])
    value = float(mean_absolute_error(validation[TARGET], model.predict(validation[[TARGET]])))
    return {"invalid_validation_mae": value, "warning": "The input is tomorrow's actual count, unavailable at forecast origin. This score is unusable; it is never a candidate."}


def _html_table(frame, caption):
    head = "".join('<th scope="col">' + escape(str(c)) + "</th>" for c in frame.columns)
    rows = "".join("<tr>" + "".join("<td>" + escape(str(v)) + "</td>" for v in row) + "</tr>" for row in frame.itertuples(index=False, name=None))
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="' + escape(caption) + '"><table><caption>' + escape(caption) + "</caption><thead><tr>" + head + "</tr></thead><tbody>" + rows + "</tbody></table></div>"


def report_study(run_dir, plots=False, dataset_label="Original synthetic smoke fixture"):
    """Named values and tables are primary evidence; PNGs are optional companions."""
    run_dir = Path(run_dir)
    result = read_json(run_dir / "final_evaluation.json")
    scores = pd.DataFrame(result["scores"])
    predictions = pd.read_csv(run_dir / "final_predictions.csv")
    selected = predictions.loc[predictions["model"] == result["selected"]].copy()
    selected.to_csv(run_dir / "selected_predictions.csv", index=False)
    biggest = selected.loc[selected["residual"].abs().idxmax()]
    selected_score = next(row for row in result["scores"] if row["model"] == result["selected"])
    lines = [
        "One-day-ahead regression study", "Dataset: " + dataset_label,
        "Selected on validation: " + result["selected"],
        f"Final observations: {result['test_rows']}",
        f"Selected final MAE: {selected_score['mae']:.3f} requests per day",
        f"Mean residual: {selected_score['mean_residual']:.3f} requests; positive means underprediction",
        f"Largest absolute residual: {abs(biggest['residual']):.3f} requests on {biggest['target_date']}",
        "Predictions remain real-valued, with no unannounced rounding or clipping.",
        "Final results do not justify changing the frozen selection. The public fixture is an evaluation rehearsal, not a hidden benchmark.",
    ]
    descriptions = {
        "forecast": f"Actual and predicted daily requests for {len(selected)} final-test dates. Final MAE is {selected_score['mae']:.3f} requests/day. Exact values are in the selected-predictions table; a close line match does not establish reliable future performance.",
        "residuals": f"Residuals are actual minus predicted; above zero means underprediction. Mean residual is {selected_score['mean_residual']:.3f} requests. Largest absolute residual is {abs(biggest['residual']):.3f} on {biggest['target_date']}. Inspect the full table for changing error direction, runs, and isolated errors; errors need not be independent.",
    }
    if plots:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        dates = pd.to_datetime(selected["target_date"])
        with plt.rc_context({"font.size": 11}):
            fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
            ax.plot(dates, selected["actual_requests"], label="Actual", color="#245080", marker="o", markersize=3)
            ax.plot(dates, selected["predicted_requests"], label="Predicted", color="#895124", linestyle="--")
            ax.set(title="Frozen forecast: final-test observations", xlabel="Target calendar date", ylabel="Daily rentals or requests (count)")
            ax.legend(); ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=4, maxticks=6))
            ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %d"))
            fig.savefig(run_dir / "forecast.png", dpi=150); plt.close(fig)
            fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
            ax.plot(dates, selected["residual"], marker="o", markersize=3, color="#245080")
            ax.axhline(0, color="black", linestyle="--")
            ax.set(title="Final-test residuals: actual minus predicted", xlabel="Target calendar date", ylabel="Residual (count)")
            ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=4, maxticks=6))
            ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %d"))
            fig.savefig(run_dir / "residuals.png", dpi=150); plt.close(fig)
    sections = []
    for name, detail in descriptions.items():
        figure = '<figure><img src="' + name + '.png" alt="' + ("Actual and predicted requests by date." if name == "forecast" else "Residuals by date with a zero reference.") + '" aria-describedby="' + name + '-description"><figcaption id="' + name + '-description">' + escape(detail) + "</figcaption></figure>" if plots else "<p>" + escape(detail) + "</p>"
        sections.append("<section><h2>" + name.title() + "</h2>" + figure + "</section>")
    text = "\n".join(lines) + "\n\n" + "\n\n".join(descriptions.values()) + "\n"
    (run_dir / "summary.txt").write_text(text, encoding="utf-8")
    html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Module 5 regression evidence</title><style>body{font:1.1rem/1.6 system-ui,sans-serif;max-width:76ch;margin:auto;padding:1rem;color:#18232d;background:white}img{max-width:100%;height:auto}pre{white-space:pre-wrap}table{border-collapse:collapse}th,td{border:1px solid #718096;padding:.4rem}.table-wrap{overflow-x:auto;max-width:100%}a{color:#075985}a:focus-visible,pre:focus-visible,.table-wrap:focus-visible{outline:3px solid currentColor;outline-offset:3px}.skip{position:absolute;top:-6rem}.skip:focus{top:0;background:white}</style></head><body><a class="skip" href="#main">Skip to main content</a><main id="main" tabindex="-1"><h1>Module 5: regression evidence</h1><pre tabindex="0" aria-label="Named study results">' + escape("\n".join(lines)) + '</pre><p><a href="selected_predictions.csv">Selected predictions and residuals (CSV)</a> · <a href="final_predictions.csv">Selected and baseline predictions (CSV)</a> · <a href="summary.txt">Text report</a> · <a href="split_manifest.json">Split and source provenance</a></p><h2>Frozen model and baseline scores</h2>' + _html_table(scores, "Final-test errors; not a model-selection table") + "".join(sections) + "<h2>Exact selected-model observations</h2>" + _html_table(selected, "Each selected prediction, actual count, and residual") + "</main><footer><p>Original educational content: CC BY 4.0. External dataset retains its cited license. Results are available as text, tables and downloads; consult the course accessibility guide for interface test scope.</p></footer></body></html>"
    (run_dir / "index.html").write_text(html + "\n", encoding="utf-8")
    return result


def run_study(input_path, run_dir, holdout_days=14, plots=False, dataset_label="Original synthetic smoke fixture"):
    prepare_study(input_path, run_dir, holdout_days)
    train_study(run_dir)
    validate_study(run_dir)
    result = evaluate_study(run_dir)
    infer_study(run_dir)
    report_study(run_dir, plots=plots, dataset_label=dataset_label)
    return result


def main():
    parser = argparse.ArgumentParser(description="One-day-ahead forecasting with explicit evaluation boundaries.")
    parser.add_argument("stage", choices=["download", "prepare", "train", "validate", "evaluate", "predict", "report", "all"])
    parser.add_argument("--input", type=Path)
    parser.add_argument("--run", type=Path, required=True, help="Fresh study directory, or data cache for download")
    parser.add_argument("--holdout-days", type=int, default=14)
    parser.add_argument("--plots", action="store_true")
    parser.add_argument("--dataset-label", default="User-supplied daily counts")
    args = parser.parse_args()
    try:
        if args.stage == "download":
            print(download_bike_data(args.run)); return
        if args.stage in {"prepare", "all"}:
            if args.input is None:
                raise ValueError("--input is required for preparation.")
            if args.stage == "all":
                run_study(args.input, args.run, args.holdout_days, args.plots, args.dataset_label)
            else:
                prepare_study(args.input, args.run, args.holdout_days)
        elif args.stage == "train":
            train_study(args.run)
        elif args.stage == "validate":
            print(json.dumps(validate_study(args.run), indent=2))
        elif args.stage == "evaluate":
            print(json.dumps(evaluate_study(args.run), indent=2))
        elif args.stage == "predict":
            print(infer_study(args.run, args.input).to_string(index=False))
        elif args.stage == "report":
            report_study(args.run, args.plots, args.dataset_label)
        print(f"Completed stage: {args.stage}. Artifacts: {args.run}")
        if (args.run / "summary.txt").exists():
            print((args.run / "summary.txt").read_text(encoding="utf-8"))
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(2, f"Regression workflow failed: {error}\n")


if __name__ == "__main__":
    main()
