"""Validate synthetic network events without learning model transformations.

Both the command-line script and lesson notebook call these functions.
Missing latency is retained, not imputed. Rejected records keep explanations.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

import numpy as np
import pandas as pd

FIELDS = ("event_id", "timestamp", "source", "latency_ms", "bytes_sent")
SOURCES = ("authentication_gateway", "network_monitor")


def _parse_bytes(value: str) -> int | None:
    """Parse exactly, avoiding float rounding or int64 overflow in byte counts."""
    try:
        number = Decimal(value)
        if not number.is_finite() or number < 0 or number > np.iinfo(np.int64).max:
            return None
        if number != number.to_integral_value():
            return None
        return int(number)
    except InvalidOperation:
        return None


@dataclass
class PreparedEvents:
    cleaned: pd.DataFrame
    rejected: pd.DataFrame
    report: dict


def prepare_events(raw: pd.DataFrame) -> PreparedEvents:
    """Apply the documented event contract; never alter the caller's data.

    Exact duplicates keep the first occurrence. Conflicting rows sharing the
    same (source, event_id) are all rejected, avoiding an arbitrary winner.
    Source-row numbers refer to a CSV with a header on line one.
    """
    missing = set(FIELDS) - set(raw.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    frame = raw.loc[:, list(FIELDS)].copy().reset_index(drop=True)
    frame = frame.fillna("").astype(str)
    frame = frame.apply(lambda column: column.str.strip())
    reasons: dict[int, list[str]] = {i: [] for i in frame.index}

    exact_duplicate = frame.duplicated(subset=list(FIELDS), keep="first")
    remaining = frame.loc[~exact_duplicate]
    conflict = remaining.duplicated(subset=["source", "event_id"], keep=False)
    conflicts = set(remaining.index[conflict])
    timestamps = pd.to_datetime(frame["timestamp"], errors="coerce", utc=True, format="ISO8601")
    latency = pd.to_numeric(frame["latency_ms"], errors="coerce")
    byte_counts = pd.Series([_parse_bytes(value) for value in frame["bytes_sent"]], dtype=object)

    for i, row in frame.iterrows():
        if exact_duplicate.loc[i]:
            reasons[i].append("exact_duplicate")
        if i in conflicts:
            reasons[i].append("conflicting_event_key")
        if not row["event_id"]:
            reasons[i].append("missing_event_id")
        if row["source"] not in SOURCES:
            reasons[i].append("unknown_source")
        if pd.isna(timestamps.loc[i]):
            reasons[i].append("invalid_timestamp")
        if row["latency_ms"] and (not np.isfinite(latency.loc[i]) or latency.loc[i] < 0):
            reasons[i].append("invalid_latency")
        value = byte_counts.loc[i]
        if value is None:
            reasons[i].append("invalid_bytes")

    accepted = [i for i in frame.index if not reasons[i]]
    rejected_indices = [i for i in frame.index if reasons[i]]
    cleaned = frame.loc[accepted].copy()
    cleaned["timestamp"] = timestamps.loc[accepted].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    cleaned["latency_ms"] = latency.loc[accepted].astype(float)
    cleaned["bytes_sent"] = byte_counts.loc[accepted].astype("int64")
    cleaned = cleaned.reset_index(drop=True)
    rejected = frame.loc[rejected_indices].copy()
    rejected.insert(0, "source_row", [i + 2 for i in rejected_indices])
    rejected["reasons"] = [";".join(reasons[i]) for i in rejected_indices]
    rejected = rejected.reset_index(drop=True)
    counts = Counter(reason for items in reasons.values() for reason in items)
    report = {
        "contract_version": "1.0",
        "rows_input": len(frame),
        "rows_accepted": len(cleaned),
        "rows_rejected": len(rejected),
        "rejection_reason_counts": dict(sorted(counts.items())),
        "accepted_missing_latency": int(cleaned["latency_ms"].isna().sum()),
        "latency_summary": summarize_latency(cleaned),
        "notes": [
            "Rejection counts can exceed rejected rows because a row can have multiple reasons.",
            "Missing latency is retained. No imputation or scaling has been fitted.",
            "Synthetic data demonstrates software behavior, not real network performance.",
        ],
    }
    return PreparedEvents(cleaned, rejected, report)


def summarize_latency(events: pd.DataFrame) -> dict:
    """Return named numeric evidence, including how many values are missing."""
    values = events["latency_ms"].to_numpy(dtype=float)
    observed = values[np.isfinite(values)]
    return {
        "observed_count": int(len(observed)),
        "mean_ms": float(np.mean(observed)) if len(observed) else None,
        "median_ms": float(np.median(observed)) if len(observed) else None,
    }


def summary_text(report: dict) -> str:
    """A compact text result usable without interpreting a plot."""
    lines = [
        "Synthetic network event quality report",
        f"Input records: {report['rows_input']}",
        f"Accepted records: {report['rows_accepted']}",
        f"Rejected records: {report['rows_rejected']}",
        f"Accepted records with missing latency: {report['accepted_missing_latency']}",
    ]
    for key, count in report["rejection_reason_counts"].items():
        lines.append(f"Rejection reason {key}: {count}")
    for key, value in report["latency_summary"].items():
        lines.append(f"Latency {key}: {value if value is not None else 'not available'}")
    lines.extend(report["notes"])
    return "\n".join(lines) + "\n"


def prepare_file(input_path: str | Path, output_dir: str | Path) -> PreparedEvents:
    """Read a CSV and save inspectable results, preserving the raw input."""
    input_path, output_dir = Path(input_path), Path(output_dir)
    names = ("cleaned_events.csv", "rejected_events.csv", "quality_report.json", "summary.txt")
    if any(input_path.resolve() == (output_dir / name).resolve() for name in names):
        raise ValueError("The input must be separate from generated output files.")
    raw = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    prepared = prepare_events(raw)
    output_dir.mkdir(parents=True, exist_ok=True)
    prepared.cleaned.to_csv(output_dir / names[0], index=False)
    prepared.rejected.to_csv(output_dir / names[1], index=False)
    (output_dir / names[2]).write_text(json.dumps(prepared.report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (output_dir / names[3]).write_text(summary_text(prepared.report), encoding="utf-8")
    return prepared


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate synthetic event data and explain rejected records.")
    parser.add_argument("--input", required=True, type=Path, help="Raw event CSV; left unchanged")
    parser.add_argument("--output", required=True, type=Path, help="Directory for generated results")
    args = parser.parse_args()
    try:
        result = prepare_file(args.input, args.output)
    except (ValueError, OSError, pd.errors.ParserError) as error:
        parser.exit(2, f"Data preparation failed: {error}\n")
    print(summary_text(result.report), end="")


if __name__ == "__main__":
    main()
