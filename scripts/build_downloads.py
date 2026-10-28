"""Publish only original/cleared source paths, never arbitrary workspace files."""
from pathlib import Path
import shutil
import json
import subprocess
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
ROOT_FILES = ["playwright.config.mjs", "CODE_OF_CONDUCT.md", "REPOSITORY_STRUCTURE.md", "CITATION.cff", "README.md", "QUICKSTART.md", "ACCESSIBILITY.md", "LICENSE", "OER_LICENSE.md", "CONTRIBUTING.md", "DEVELOPMENT.md", "CHANGELOG.md", "pyproject.toml", "package.json", "package-lock.json", ".gitignore", ".gitattributes"]
SOURCE_FOLDERS = ["curriculum", "templates", "apps", "src", "examples", "data", "notebooks", "projects", "docs", "scripts", "tests", "environments", ".devcontainer", ".binder", ".github"]
ALLOWED_SUFFIXES = {".cff", ".py", ".md", ".json", ".toml", ".csv", ".txt", ".ipynb", ".css", ".js", ".svg", ".mjs", ".yml", ".yaml"}


def build():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    from check_practice import validate_sources as validate_practice_sources, checks_digest
    import hashlib
    validate_practice_sources()
    practice_registry = json.loads((ROOT / "curriculum/practice.json").read_text(encoding="utf-8"))["modules"]
    for entry in practice_registry:
        verified = ROOT / "runs/verified/practice" / f'module{entry["id"]:02d}'
        summary = json.loads((verified / "summary.json").read_text(encoding="utf-8"))
        assert summary["checks_sha256"] == checks_digest(), "Practice checks changed; rerun scripts/check_practice.py"
        target = DESTINATION / f'module{entry["id"]:02d}'
        target.mkdir(parents=True, exist_ok=True)
        for kind in ["practice", "solutions"]:
            source = ROOT / entry[kind]
            evidence = summary["notebooks"][kind]
            assert evidence["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest(), "Practice evidence is stale; rerun scripts/check_practice.py"
            assert evidence["state"] == ("not_attempted" if kind == "practice" else "passed")
            shutil.copyfile(source, target / (kind + ".ipynb"))
            shutil.copyfile(verified / (kind + "-executed.ipynb"), target / (kind + "-executed.ipynb"))
        shutil.copyfile(verified / "summary.json", target / "practice-verification.json")
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
    capstone = ROOT / "runs/verified/capstone"
    if not (capstone / "report.done.json").is_file():
        raise FileNotFoundError("Missing capstone execution; run scripts/check_capstone.py in the core environment.")
    from practical_ml_ai.capstone import verify as verify_capstone
    verify_capstone(capstone, "report")
    shutil.copytree(capstone, DESTINATION / "capstone/example")
    shutil.copyfile(ROOT / "projects/phishing-triage/notebooks/complete-study.ipynb", DESTINATION / "capstone/walkthrough.ipynb")
    shutil.copyfile(capstone / "executed.ipynb", DESTINATION / "capstone/executed.ipynb")
    for name in ["wine", "sms", "adult", "phishing"]:
        cache = fetch_source(name)
        with zipfile.ZipFile(DESTINATION / (name + "-cache.zip"), "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for member in sorted(cache.iterdir()):
                if member.is_file():
                    archive.write(member, arcname=member.name)
    build_source_archive(DESTINATION / "ml_ai_it-source.zip")
    print("Built source, notebook, contract, and sample downloads from the publication allowlist.")


def publishable(relative):
    """Apply the publication allowlist to one repository-relative path."""
    path = Path(relative)
    if relative in ROOT_FILES:
        return True
    return (path.parts[0] in SOURCE_FOLDERS and path.suffix in ALLOWED_SUFFIXES
            and not any(part in {"__pycache__", ".ipynb_checkpoints"} or part.endswith(".egg-info") for part in path.parts))


def source_members(root=ROOT):
    """Archive members: tracked files in a Git checkout, so untracked notes or outputs never ship.

    An extracted archive has no Git metadata; it falls back to the allowlist walk.
    """
    root = Path(root)
    try:
        listed = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout.decode()
        names = [name for name in listed.split(chr(0)) if name]
    except (OSError, subprocess.CalledProcessError):
        names = [name for name in ROOT_FILES if (root / name).is_file()]
        for folder in SOURCE_FOLDERS:
            names.extend(p.relative_to(root).as_posix() for p in (root / folder).rglob("*") if p.is_file())
    return sorted(root / name for name in set(names) if publishable(name))


def build_source_archive(path):
    """Write the complete course source from the publication allowlist; no runs or caches."""
    files = source_members()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(set(files)):
            if not source.is_file():
                raise FileNotFoundError(source)
            name = "ml_ai_it/" + source.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 24, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, source.read_bytes())
    return Path(path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build reading-site downloads, or only the course source archive.")
    parser.add_argument("--source-only", metavar="ZIP", help="Write just the source archive (for an instructor to share when the site is unavailable).")
    arguments = parser.parse_args()
    if arguments.source_only:
        print("Wrote", build_source_archive(arguments.source_only))
    else:
        build()
