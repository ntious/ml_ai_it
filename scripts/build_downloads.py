"""Publish only original/cleared source paths, never arbitrary workspace files."""
from pathlib import Path
import shutil
import json
import zipfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from practical_ml_ai.exploration import run_exploration
from practical_ml_ai.regression import download_bike_data, run_study
from practical_ml_ai.continuation_data import fetch_source
from practical_ml_ai.phishing import prepare, train, validate, evaluate, report

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "site/downloads"
MODULES = json.loads((ROOT / "curriculum/modules.json").read_text(encoding="utf-8"))["modules"]
ROOT_FILES = ["CODE_OF_CONDUCT.md", "REPOSITORY_STRUCTURE.md", "REPOSITORY_REVIEW.md", "CITATION.cff", "README.md", "QUICKSTART.md", "ACCESSIBILITY.md", "LICENSE", "OER_LICENSE.md", "CONTRIBUTING.md", "DEVELOPMENT.md", "CHANGELOG.md", "pyproject.toml", "package.json", "package-lock.json", ".gitignore", ".gitattributes"]
SOURCE_FOLDERS = ["curriculum", "templates", "apps", "src", "examples", "data", "notebooks", "docs", "scripts", "tests", "environments", ".devcontainer", ".binder", ".github"]
ALLOWED_SUFFIXES = {".cff", ".py", ".md", ".json", ".toml", ".csv", ".txt", ".ipynb", ".css", ".mjs", ".yml", ".yaml"}


def build():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for source, name in [
        (ROOT / "data/samples/network-events/events.csv", "events.csv"),
        (ROOT / "data/schemas/network-events.schema.json", "network-events.schema.json"),
        (ROOT / "notebooks/lessons/03-data-processing/complete_walkthrough.ipynb", "complete_walkthrough.ipynb"),
        (ROOT / "data/samples/service-files/tickets.csv", "module02/tickets.csv"),
        (ROOT / "data/samples/service-files/events.json", "module02/events.json"),
        (ROOT / "data/samples/service-workload/daily.csv", "module04/daily.csv"),
        (ROOT / "data/samples/forecast-demand/daily.csv", "module05/synthetic_daily.csv"),
    ]:
        target = DESTINATION / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    for module in MODULES:
        target = DESTINATION / module["download"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / module["notebook"], target)
        executed = ROOT / "runs/verified" / f'module{module["id"]:02d}' / "executed.ipynb"
        if not executed.is_file():
            raise FileNotFoundError(f"Missing actual kernel execution: {executed}")
        shutil.copyfile(executed, target.with_name("executed.ipynb"))
    run_exploration(ROOT / "data/samples/service-workload/daily.csv", DESTINATION / "module04/example")
    # External data stay in a separate attributed download, outside original source.
    daily = download_bike_data(ROOT / "runs/datasets/bike-sharing")
    run_study(daily, DESTINATION / "module05/example", holdout_days=110, plots=True,
              dataset_label="UCI Bike Sharing daily counts, CC BY 4.0")
    cache_files = ["day.csv", "original.zip", "Readme.txt", "provenance.json", "ATTRIBUTION.txt"]
    with zipfile.ZipFile(DESTINATION / "module05/bike-sharing-cache.zip", "w", compression=zipfile.ZIP_DEFLATED) as cache:
        for name in cache_files:
            cache.write(daily.parent / name, arcname=name)
    shutil.copyfile(daily.parent / "ATTRIBUTION.txt", DESTINATION / "module05/ATTRIBUTION.txt")
    # Reports are outputs of actual notebook execution in tested profiles.
    for number in range(6, 15):
        source = ROOT / "runs/verified" / f"module{number:02d}"
        if not (source / "summary.json").is_file():
            raise FileNotFoundError(f"Missing verified Module {number} report; run its notebook check before building.")
        shutil.copytree(source, DESTINATION / f"module{number:02d}/example")
    case = DESTINATION / "phishing/example"
    for stage in [prepare, train, validate, evaluate, report]: stage(case)
    shutil.copyfile(ROOT / "notebooks/cases/phishing.ipynb", DESTINATION / "phishing/walkthrough.ipynb")
    shutil.copyfile(ROOT / "runs/verified/phishing/executed.ipynb", DESTINATION / "phishing/executed.ipynb")
    for name in ["wine", "sms", "adult", "phishing"]:
        cache = fetch_source(name)
        with zipfile.ZipFile(DESTINATION / (name + "-cache.zip"), "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for member in sorted(cache.iterdir()):
                if member.is_file():
                    archive.write(member, arcname=member.name)
    files = [ROOT / name for name in ROOT_FILES]
    for folder in SOURCE_FOLDERS:
        files.extend(p for p in (ROOT / folder).rglob("*") if p.is_file() and p.suffix in ALLOWED_SUFFIXES and not any(part in {"__pycache__", ".ipynb_checkpoints"} or part.endswith(".egg-info") for part in p.parts))
    with zipfile.ZipFile(DESTINATION / "ml_ai_it-source.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(set(files)):
            if not source.is_file():
                raise FileNotFoundError(source)
            name = "ml_ai_it/" + source.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 24, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, source.read_bytes())
    print("Built source, notebook, contract, and sample downloads from the publication allowlist.")


if __name__ == "__main__":
    build()
