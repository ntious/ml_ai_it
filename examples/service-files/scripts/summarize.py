"""Run Module 2 using the same functions as its guided notebook."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.python_workflow import main

if __name__ == "__main__":
    main()
