"""Run Module 1 with Python alone, before installing data libraries."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.foundations import main

if __name__ == "__main__":
    main()
