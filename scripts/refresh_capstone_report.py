"""Copy a verified completed report into the authored project for reading."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai.capstone import verify

run = ROOT / "runs/verified/capstone"
verify(run, "report")
destination = ROOT / "projects/phishing-triage/reports/annotated-report.md"
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text((run / "report.md").read_text(encoding="utf-8"), encoding="utf-8")
print("Refreshed the annotated report from verified capstone execution.")
