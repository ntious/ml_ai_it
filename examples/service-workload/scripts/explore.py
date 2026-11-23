"""Thin Module 4 entry point; run from a source checkout or extracted archive."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.exploration import main

if __name__ == "__main__":
    main()
