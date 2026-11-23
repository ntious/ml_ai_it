"""Lightweight experiment tracking: one JSON line per run, standard library only.

Each record keeps what is needed to compare and reproduce a run: when it ran,
the command's settings, its metrics, the Python and package versions, and the
SHA-256 of each input file. Tools such as MLflow add a server and a user
interface on top of the same idea.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import sys

PACKAGES = ["numpy", "pandas", "scikit-learn"]


def _versions():
    found = {"python": platform.python_version()}
    for name in PACKAGES:
        try:
            found[name] = version(name)
        except PackageNotFoundError:
            pass
    return found


def record(log, experiment, settings, metrics, inputs=()):
    """Append one run to a JSON-lines log and return the stored record."""
    entry = {"recorded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "experiment": experiment,
             "command": " ".join(sys.argv), "settings": settings, "metrics": metrics, "environment": _versions(),
             "inputs": {str(path): hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in inputs}}
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def read(log):
    with Path(log).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main(argv=None):
    parser = argparse.ArgumentParser(description="List tracked runs, one line each.")
    parser.add_argument("log")
    for entry in read(parser.parse_args(argv).log):
        metrics = ", ".join(f"{key}={value:.3f}" if isinstance(value, float) else f"{key}={value}" for key, value in entry["metrics"].items())
        print(f"{entry['recorded_utc']}  {entry['experiment']}  {json.dumps(entry['settings'], sort_keys=True)}  {metrics}")


if __name__ == "__main__":
    main()
