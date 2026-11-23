"""Thin entry point: the notebook uses the same package functions."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.data.events import main

if __name__ == "__main__":
    main()
