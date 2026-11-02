"""Draft a monitoring decision record from a Module 12 batch_monitoring.csv.

This module reports observed values and compares them with thresholds the
learner declares. It does not choose thresholds or a decision.
"""
import argparse
import csv
from pathlib import Path

COLUMNS = ["batch", "rows", "mean_prediction_seconds", "largest_standardized_mean_shift", "fp", "fn", "recall", "precision", "selection_rate"]


def read_batches(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    missing = [name for name in COLUMNS if rows and name not in rows[0]]
    if not rows or missing:
        raise ValueError(f"{path} is empty or lacks columns: {missing}")
    return rows


def number(value):
    # The shift is blank or NaN when a feature has no variance; keep that visible.
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return None if result != result else result


def draft_record(rows, latency_limit=None, shift_limit=None):
    def flag(value, limit):
        if limit is None:
            return "no threshold declared"
        if value is None:
            return "unavailable"
        return "ABOVE" if value > limit else "within"
    lines = ["| Batch | Rows | Mean seconds | Latency vs threshold | Largest shift | Shift vs threshold | FP | FN | Recall | Precision |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        seconds, shift = number(row["mean_prediction_seconds"]), number(row["largest_standardized_mean_shift"])
        fmt = lambda v, p=4: "unavailable" if v is None else f"{v:.{p}f}"
        lines.append(f"| {row['batch']} | {row['rows']} | {fmt(seconds, 6)} | {flag(seconds, latency_limit)} | {fmt(shift, 3)} | "
                     f"{flag(shift, shift_limit)} | {row['fp']} | {row['fn']} | {fmt(number(row['recall']), 3)} | {fmt(number(row['precision']), 3)} |")
    lines += ["", "Complete these parts yourself in docs/advanced/monitoring-decision-record.md:",
              "service and owner; why each threshold was chosen; decision and what would change it; escalation and rollback; limits.",
              "A source-order batch shift is a diagnostic, not time drift."]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_csv", help="batch_monitoring.csv from a Module 12 run")
    parser.add_argument("--latency-limit", type=float, help="mean prediction seconds you consider too slow")
    parser.add_argument("--shift-limit", type=float, help="standardized mean shift that should trigger investigation")
    args = parser.parse_args(argv)
    print(draft_record(read_batches(args.batch_csv), args.latency_limit, args.shift_limit))


if __name__ == "__main__":
    main()
