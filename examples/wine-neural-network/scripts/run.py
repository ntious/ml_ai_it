"""Module 8 CLI: import the shared implementation, retaining one tested code path."""
from pathlib import Path
import sys

# Shared source is resolved from this script, independent of current directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.course_runner import main

if __name__ == "__main__":
    main(8)
