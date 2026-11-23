"""Thin entry point; all stage behavior lives in the shared regression module."""
from pathlib import Path
import sys

# A checkout/extracted source archive works without copying implementation here.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.regression import main

if __name__ == "__main__":
    main()
