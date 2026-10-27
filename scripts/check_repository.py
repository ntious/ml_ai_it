"""Fail on missing curriculum assets, undocumented paths, or archive omissions.

This inspects structure and source syntax; behavioral tests and real notebook
execution remain separate. It never executes arbitrary discovered Python files.
"""
import ast
import json
from pathlib import Path
import subprocess
import sys
import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_downloads import ROOT_FILES, SOURCE_FOLDERS, ALLOWED_SUFFIXES

modules = json.loads((ROOT / "curriculum/modules.json").read_text(encoding="utf-8"))["modules"]
assert [module["id"] for module in modules] == list(range(1, 15))
assert len({module["slug"] for module in modules}) == 14
registered_notebooks, registered_scripts = set(), set()
for module in modules:
    assert module["profile"] in {"core", "frameworks"}
    for key in ["lesson", "notebook", "script"]:
        path = ROOT / module[key]
        assert path.is_file() and path.resolve().is_relative_to(ROOT), path
    for name in module["pages"]:
        assert (ROOT / module["lesson"]).with_name(name).is_file(), (module["id"], name)
    notebook = nbformat.read(ROOT / module["notebook"], as_version=4)
    nbformat.validate(notebook)
    ids = [cell.id for cell in notebook.cells]
    assert len(set(ids)) == len(ids)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None and not cell.outputs, module["notebook"]
            ast.parse(cell.source)
    registered_notebooks.add(module["notebook"])
    registered_scripts.add(module["script"])
assert registered_notebooks == {p.relative_to(ROOT).as_posix() for p in (ROOT / "notebooks/lessons").rglob("*.ipynb")}
assert registered_scripts == {p.relative_to(ROOT).as_posix() for p in (ROOT / "examples").glob("*/scripts/*.py")}
from check_practice import validate_sources as validate_practice_sources
validate_practice_sources()
for case in (ROOT / "notebooks/cases").glob("*.ipynb"):
    notebook = nbformat.read(case,as_version=4); nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None and not cell.outputs
            ast.parse(cell.source)
for project in (ROOT / "projects").glob("*"):
    assert (project / "README.md").is_file()
    for source in (project / "notebooks").glob("*.ipynb"):
        notebook = nbformat.read(source, as_version=4); nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                assert cell.execution_count is None and not cell.outputs
                ast.parse(cell.source)
tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
tracked = [name for name in tracked if name]
for name in tracked:
    path = Path(name)
    allowed = name in ROOT_FILES or (path.parts[0] in SOURCE_FOLDERS and path.suffix in ALLOWED_SUFFIXES)
    assert allowed, f"Tracked file omitted from source-download policy: {name}"
    if path.suffix == ".py":
        ast.parse((ROOT / path).read_text(encoding="utf-8"), filename=name)
required = ["REPOSITORY_STRUCTURE.md", "docs/maintenance/reviews/baseline-0.6.0.md", "CITATION.cff",
            "templates/accessibility-review.md", "templates/lesson.md",
            "docs/instructor/assessment.md", "docs/instructor/canvas-linking.md",
            "docs/accessibility/review-log.md", "docs/release-checklist.md"]
assert all((ROOT / name).is_file() for name in required)
subprocess.run([sys.executable,str(ROOT/"scripts/check_source_links.py")],check=True)
print(f"Verified {len(modules)} complete module packages, registered scripts/notebooks, Python syntax, and publication coverage for {len(tracked)} tracked source files.")
