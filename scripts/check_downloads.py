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
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    expected = {"ml_ai_it/" + name for name in tracked if name}
    assert set(names) == expected, {"missing": sorted(expected - set(names)), "extra": sorted(set(names) - expected)}
    for name in names:
        relative = Path(name).relative_to("ml_ai_it")
        assert not relative.is_absolute() and ".." not in relative.parts
        # Only repository-root output/private folders are excluded. A tracked
        # nested folder such as tests/site contains authored source, not a build.
        assert relative.parts[0] not in {"runs", "site", "analysis", "project_sources", "project_resources"}, name
        assert "__pycache__" not in relative.parts, name
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

practice = json.loads((ROOT / "curriculum/practice.json").read_text())["modules"]
for entry in practice:
    target = ROOT / "site/downloads" / f'module{entry["id"]:02d}'
    evidence = json.loads((target / "practice-verification.json").read_text())
    for kind in ["practice", "solutions"]:
        source = ROOT / entry[kind]
        assert (target / (kind + ".ipynb")).read_bytes() == source.read_bytes()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == evidence["notebooks"][kind]["sha256"]
        assert (target / (kind + "-executed.ipynb")).is_file()
print("Checked 28 separate practice/solution sources, matching execution identities and downloadable executed copies.")

with zipfile.ZipFile(ROOT / "site/downloads/module05/bike-sharing-cache.zip") as cache:
    metadata = json.loads(cache.read("provenance.json"))
    assert hashlib.sha256(cache.read("day.csv")).hexdigest() == metadata["day_csv_sha256"]
    assert hashlib.sha256(cache.read("original.zip")).hexdigest() == metadata["archive_sha256"]
    assert metadata["license"] == "CC-BY-4.0"
    assert "Fanaee-T" in cache.read("ATTRIBUTION.txt").decode()
print("Checked the separate attributed public-data cache and source digests.")

# Verify all newly attributed cache members, not merely the presence of a ZIP.
for source in ["wine", "sms", "adult", "phishing"]:
    with zipfile.ZipFile(ROOT / "site/downloads" / (source + "-cache.zip")) as cache:
        metadata = json.loads(cache.read("provenance.json"))
        assert hashlib.sha256(cache.read("original.zip")).hexdigest() == metadata["archive_sha256"]
        for member, expected in metadata["files"].items():
            assert hashlib.sha256(cache.read(member)).hexdigest() == expected
        assert metadata["license"] == "CC-BY-4.0"
        assert cache.read("ATTRIBUTION.txt")
print("Checked all four additional real-data caches and their attribution/digests.")
with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory() as temporary:
    archive.extractall(temporary)
    extracted = Path(temporary) / "ml_ai_it"
    process = subprocess.run(
        [sys.executable, str(extracted / "examples/wine-classification/scripts/run.py"),
         "--output", str(Path(temporary) / "classifier")],
        cwd=temporary, capture_output=True, text=True,
    )
    assert process.returncode == 0, process.stderr
    assert (Path(temporary) / "classifier/summary.json").is_file()
    assert (extracted / "apps/wine_quality.py").is_file()
print("Checked the extracted new-module CLI and included app source.")

# The optional project must survive a complete source-archive download too.
with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory() as temporary:
    archive.extractall(temporary)
    extracted = Path(temporary) / "ml_ai_it"
    project = extracted / "projects/phishing-triage/scripts/run.py"
    evidence = ROOT / "site/downloads/capstone/example"
    for stage, options in [("verify", []), ("predict", ["--input", str(evidence / "example_request.json")])]:
        process = subprocess.run([sys.executable, str(project), stage, "--run", str(evidence), *options],
                                 cwd=temporary, text=True, capture_output=True)
        assert process.returncode == 0, process.stderr
    prediction = json.loads(process.stdout)
    assert 0 <= prediction["probability"] <= 1
print("Checked the extracted capstone CLI, complete evidence ledger and frozen bundle inference.")
