"""Schema-checked prediction and actual held-out-record monitoring replay."""
import time
import numpy as np
import pandas as pd
from .classical import classification_bundle
from .continuation_data import binary_metrics, new_run, publish_report, write_json


def checked_predict(bundle, record):
    """Use exactly the trained feature schema, without coercion or target input."""
    features = bundle["features"]
    if not isinstance(record, dict) or set(record) != set(features):
        raise ValueError("Supply exactly the eleven chemistry features; no quality/label/extra fields.")
    for name, value in record.items():
        if isinstance(value, bool) or not isinstance(value, (int, float, np.number)):
            raise ValueError(name + " must be numeric.")
        if not np.isfinite(value) or not 0 <= value <= 1_000_000:
            raise ValueError(name + " must be finite, nonnegative, and within the technical input bound.")
    frame = pd.DataFrame([record], columns=features)
    training = bundle["split"]["train"][features]
    outside = [name for name in features if not training[name].min() <= record[name] <= training[name].max()]
    started = time.perf_counter()
    probability = float(bundle["model"].predict_proba(frame)[0, 1])
    return {"probability": probability, "predicted": int(probability >= bundle["selection"]["threshold"]),
            "threshold": bundle["selection"]["threshold"], "model": bundle["selection"]["model"],
            "prediction_seconds": time.perf_counter() - started, "outside_training_range": outside}


def run_monitoring(output):
    directory = new_run(output)
    bundle = classification_bundle()
    test = bundle["split"]["test"].sort_values("record_id")
    features = bundle["features"]
    training = bundle["split"]["train"][features]
    rows, batches = [], []
    for batch_id, positions in enumerate(np.array_split(np.arange(len(test)), 4), start=1):
        part = test.iloc[positions]
        estimates, durations = [], []
        for _, record in part.iterrows():
            result = checked_predict(bundle, {name: float(record[name]) for name in features})
            estimates.append(result["predicted"]); durations.append(result["prediction_seconds"])
            rows.append({"record_id": int(record.record_id), "batch": batch_id, "actual": int(record.label),
                         "predicted": result["predicted"], "probability": result["probability"],
                         "prediction_seconds": result["prediction_seconds"]})
        scale = training.std(ddof=0).replace(0, np.nan)
        shift = ((part[features].mean() - training.mean()) / scale).abs().fillna(0)
        batches.append({"batch": batch_id, "rows": len(part), "mean_prediction_seconds": float(np.mean(durations)),
                        "largest_standardized_mean_shift": float(shift.max()),
                        **binary_metrics(part.label, estimates)})
    write_json(directory / "service_contract.json", {"features": features, "numeric_bounds": [0, 1000000],
               "selected_model": bundle["selection"]["model"], "threshold": bundle["selection"]["threshold"],
               "scope": "Local demonstration; no authentication or production availability guarantee."})
    summary = {"module": 12, "real_heldout_rows": len(test), "batches": len(batches),
               "model": bundle["selection"]["model"], "threshold": bundle["selection"]["threshold"],
               "replay_order": "source record order, not a measured event-time stream",
               "labels": "Offline known labels for delayed-outcome monitoring rehearsal",
               "monitoring": "Measured duration, input statistics, and outcome metrics; no fabricated telemetry"}
    return publish_report(directory, "Module 12: deployment and monitoring", summary,
                          {"batch_monitoring": pd.DataFrame(batches), "prediction_log": pd.DataFrame(rows)},
                          ["Batches contain actual held-out records. Dataset order is not a temporal sequence; batch differences are not evidence of time drift.",
                           "Measured local durations depend on hardware/warm-up and are not production latency guarantees.",
                           "A mean-shift diagnostic prompts investigation; it does not prove concept drift. Operational use needs privacy, ownership, delayed labels, and rollback.",
                           "The Streamlit app uses this checked inference function and a local-LLM form that rejects invalid output schemas."])
