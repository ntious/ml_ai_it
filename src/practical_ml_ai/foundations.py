"""A standard-library-only first Python example: an explicit storage rule.

This is deliberately not an ML model or a call to a generative AI service.
"""
import argparse
import math
from pathlib import Path


def storage_rule(storage_percent: float, threshold: float = 80) -> bool:
    """Request human review only when usage is strictly above the threshold."""
    for name, value in [("storage_percent", storage_percent), ("threshold", threshold)]:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number from 0 through 100.")
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"{name} must be a finite number from 0 through 100.")
    return storage_percent > threshold


def describe_first_run(result: dict) -> str:
    action = "Review storage" if result["review_needed"] else "Within the chosen threshold"
    return (
        "Fictional teaching server: storage rule\n"
        f"Storage used: {result['storage_percent']:g} percent\n"
        f"Review threshold: {result['threshold']:g} percent\n"
        f"Decision: {action}\n"
        "Method: a human-written rule; no model was trained and no AI service was called.\n"
    )


def run_first_example(storage_percent: float = 85, output_path: str | Path | None = None) -> dict:
    result = {"storage_percent": storage_percent, "threshold": 80, "review_needed": storage_rule(storage_percent)}
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(describe_first_run(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run and explain a simple storage rule. No ML training is performed.")
    parser.add_argument("--storage-percent", type=float, default=85, help="Fictional storage usage, 0 through 100")
    parser.add_argument("--output", type=Path, help="Optional text file for your result; replaced on rerun")
    args = parser.parse_args()
    try:
        result = run_first_example(args.storage_percent, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"First example failed: {error}\n")
    print(describe_first_run(result), end="")


if __name__ == "__main__":
    main()
