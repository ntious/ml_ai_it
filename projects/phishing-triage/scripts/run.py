"""Run the optional capstone from a complete checkout or extracted source."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from practical_ml_ai.capstone import main

if __name__ == "__main__":
    main()
