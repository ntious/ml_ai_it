"""Optional end-of-day anomaly triage on chronological bike-demand observations."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from .regression import download_bike_data, UCI_ARCHIVE_SHA256

FEATURES = ["log_count", "weekly_change", "temp"]
QUANTILE = .95


def study(raw):
    frame = raw[["dteday", "cnt", "temp"]].copy()
    frame["dteday"] = pd.to_datetime(frame.dteday, errors="raise")
    frame = frame.sort_values("dteday").reset_index(drop=True)
    if frame.dteday.duplicated().any() or not frame.dteday.diff().dropna().eq(pd.Timedelta(days=1)).all():
        raise ValueError("Require unique consecutive daily observations; do not silently bridge gaps.")
    if not np.isfinite(frame[["cnt", "temp"]].to_numpy(dtype=float)).all() or (frame.cnt < 0).any():
        raise ValueError("Counts and temperature must be finite; counts must be nonnegative.")
    frame["log_count"] = np.log1p(frame.cnt)
    frame["weekly_change"] = frame.log_count - frame.log_count.shift(7)
    frame = frame.iloc[7:].copy()
    frame["partition"] = np.where(frame.dteday < "2012-01-01", "train", np.where(frame.dteday < "2012-07-01", "validation", "test"))
    parts = {name: frame[frame.partition == name] for name in ("train", "validation", "test")}
    if any(len(part) < 30 for part in parts.values()):
        raise ValueError("Need at least 30 daily rows in each declared calendar partition.")
    train, validation = parts["train"], parts["validation"]
    model = IsolationForest(n_estimators=100, max_samples="auto", contamination="auto", random_state=42, n_jobs=1)
    model.fit(train[FEATURES])
    center = float(train.weekly_change.median())
    scale = float((train.weekly_change - center).abs().median())
    if scale == 0:
        raise ValueError("Training weekly-change MAD is zero; baseline scale is unavailable.")
    def scores(part):
        return {"isolation_forest": -model.score_samples(part[FEATURES]),
                "weekly_change_baseline": (part.weekly_change - center).abs().to_numpy() / scale}
    # Budget is predeclared, not estimated anomaly prevalence or optimized test accuracy.
    thresholds = {name: float(np.quantile(values, QUANTILE)) for name, values in scores(validation).items()}
    rows = []
    for partition, part in parts.items():
        for method, values in scores(part).items():
            for date, count, score in zip(part.dteday, part.cnt, values):
                rows.append({"date": date.strftime("%Y-%m-%d"), "count": int(count), "partition": partition,
                             "method": method, "score": float(score), "threshold": thresholds[method],
                             "flagged": bool(score > thresholds[method])})
    predictions = pd.DataFrame(rows)
    workload = predictions.groupby(["partition", "method"]).flagged.agg(["size", "sum", "mean"]).reset_index()
    workload.columns = ["partition", "method", "days", "flagged_days", "flagged_fraction"]
    monthly = parts["test"].groupby(parts["test"].dteday.dt.strftime("%Y-%m")).cnt.agg(["size", "mean"]).reset_index()
    train_sd = float(train.cnt.std(ddof=0))
    monthly["mean_shift_training_sd"] = (monthly["mean"] - train.cnt.mean()) / train_sd if train_sd > 0 else None
    protocol = {"features": FEATURES, "training_end": "2011-12-31", "validation_end": "2012-06-30",
                "threshold_quantile": QUANTILE, "strict_greater_than": True, "thresholds": thresholds,
                "baseline_center": center, "baseline_mad": scale, "model_parameters": model.get_params(),
                "decision_time": "end of observed day; not a forecast", "labels_available": False,
                "interpretation": "Flags measure unusual observations and review workload, not incident accuracy. Monthly mean differences may reflect seasonality, growth or other factors; they do not establish concept drift."}
    return predictions, workload, monthly, protocol


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--cache", default="runs/datasets/bike-sharing")
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        parser.error("Choose a new output directory.")
    source = download_bike_data(args.cache)
    predictions, workload, monthly, protocol = study(pd.read_csv(source))
    protocol.update(source_archive_sha256=UCI_ARCHIVE_SHA256, source_csv_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    output.mkdir(parents=True)
    predictions.to_csv(output / "scores.csv", index=False)
    workload.to_csv(output / "workload.csv", index=False)
    monthly.to_csv(output / "monthly_context.csv", index=False)
    (output / "protocol.json").write_text(json.dumps(protocol, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(workload.to_string(index=False))
    print(protocol["interpretation"])


if __name__ == "__main__":
    main()
