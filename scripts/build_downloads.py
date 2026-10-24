"""Publish only original/cleared source paths, never arbitrary workspace files."""
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "site/downloads"
ROOT_FILES = ["README.md", "QUICKSTART.md", "ACCESSIBILITY.md", "LICENSE", "OER_LICENSE.md", "CONTRIBUTING.md", "DEVELOPMENT.md", "CHANGELOG.md", "pyproject.toml", "package.json", ".gitignore"]
SOURCE_FOLDERS = ["src", "examples", "data", "notebooks", "docs", "scripts", "tests", "environments", ".devcontainer", ".binder", ".github"]
ALLOWED_SUFFIXES = {".py", ".md", ".json", ".toml", ".csv", ".txt", ".ipynb", ".css", ".mjs", ".yml", ".yaml"}


def build():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for source, name in [
        (ROOT / "data/samples/network-events/events.csv", "events.csv"),
        (ROOT / "data/schemas/network-events.schema.json", "network-events.schema.json"),
        (ROOT / "notebooks/lessons/03-data-processing/complete_walkthrough.ipynb", "complete_walkthrough.ipynb"),
    ]:
        shutil.copyfile(source, DESTINATION / name)
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
