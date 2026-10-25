"""Explicit module dispatcher. Optional frameworks are imported only when used."""
import argparse
from pathlib import Path


def run_module(number, output, **options):
    if number == 6:
        from .classical import run_classification
        return run_classification(output)
    if number == 7:
        from .classical import run_clustering
        return run_clustering(output)
    if number == 13:
        from .classical import run_fairness
        return run_fairness(output)
    if number in {8, 9}:
        from .neural import run_neural
        return run_neural(number, output, **options)
    if number in {10, 11, 14}:
        from .language import run_language
        return run_language(number, output, **options)
    if number == 12:
        from .deployment import run_monitoring
        return run_monitoring(output)
    raise ValueError("Unknown module.")


def main(number):
    parser = argparse.ArgumentParser(description=f"Run the real-data Module {number} example.")
    parser.add_argument("--output", type=Path, required=True, help="A new directory for evidence; existing runs are not overwritten.")
    if number in {8, 9}:
        parser.add_argument("--epochs", type=int, default=8 if number == 8 else 3)
    if number == 11:
        parser.add_argument("--steps", type=int, default=8)
    args = parser.parse_args()
    options = {key: value for key, value in vars(args).items() if key != "output"}
    try:
        run_module(number, args.output, **options)
    except (ValueError, OSError, KeyError, ImportError) as error:
        parser.exit(2, f"Module {number} failed: {error}\n")
