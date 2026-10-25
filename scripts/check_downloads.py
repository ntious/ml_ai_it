"""Verify source/data downloads, then run the extracted source without copies.

This checks this repository's generated allowlisted archive, not arbitrary ZIPs.
It runs the actual smoke workflow through its public CLI and keeps generated
data/cache artifacts separate from the original source archive.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
archive_path = ROOT / "site/downloads/ml_ai_it-source.zip"
with zipfile.ZipFile(archive_path) as archive:
    names = archive.namelist()
    assert len(names) == len(set(names))
    for name in names:
        relative = Path(name).relative_to("ml_ai_it")
        assert not relative.is_absolute() and ".." not in relative.parts
        assert not set(relative.parts) & {"runs", "site", "analysis", "project_sources", "project_resources", "__pycache__"}
        assert archive.read(name) == (ROOT / relative).read_bytes(), name
    with tempfile.TemporaryDirectory() as temporary:
        archive.extractall(temporary)
        extracted = Path(temporary) / "ml_ai_it"
        output = Path(temporary) / "smoke-study"
        process = subprocess.run(
            [sys.executable, str(extracted / "examples/bike-demand/scripts/study.py"), "all",
             "--input", str(extracted / "data/samples/forecast-demand/daily.csv"),
             "--run", str(output)],
            cwd=temporary, capture_output=True, text=True,
        )
        assert process.returncode == 0, process.stderr
        result = json.loads((output / "final_evaluation.json").read_text())
        assert result["test_rows"] == 14
        assert result["selected"] == "linear_week"
        assert (output / "forecast.csv").is_file()
print(f"Checked {len(names)} byte-matched original-source files and the extracted regression CLI.")

with zipfile.ZipFile(ROOT / "site/downloads/module05/bike-sharing-cache.zip") as cache:
    metadata = json.loads(cache.read("provenance.json"))
    assert hashlib.sha256(cache.read("day.csv")).hexdigest() == metadata["day_csv_sha256"]
    assert hashlib.sha256(cache.read("original.zip")).hexdigest() == metadata["archive_sha256"]
    assert metadata["license"] == "CC-BY-4.0"
    assert "Fanaee-T" in cache.read("ATTRIBUTION.txt").decode()
print("Checked the separate attributed public-data cache and source digests.")
