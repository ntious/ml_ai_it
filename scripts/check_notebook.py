"""Execute only the three trusted, curated plain-Python notebooks named below.

Fresh namespaces check code paths, not notebook UI or assistive technology.
Do not use this executor for untrusted notebooks.
"""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "01-foundations/first_steps.ipynb",
    "02-python-workflows/workflow.ipynb",
    "03-data-processing/complete_walkthrough.ipynb",
]


def check(relative):
    path = ROOT / "notebooks/lessons" / relative
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4, path
    assert len({cell["id"] for cell in notebook["cells"]}) == len(notebook["cells"]), path
    namespace = {"__name__": "__main__"}
    output = io.StringIO()
    previous = Path.cwd()
    count = 0
    try:
        os.chdir(ROOT)
        with redirect_stdout(output):
            for i, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] == "code":
                    assert cell["execution_count"] is None and cell["outputs"] == [], path
                    exec(compile("".join(cell["source"]), f"{relative}:cell-{i + 1}", "exec"), namespace)
                    count += 1
    finally:
        os.chdir(previous)
    if relative.startswith("01-"):
        assert namespace["result"]["review_needed"] is True
        assert namespace["boundary_results"] == {80: False, 81: True}
        assert "no model was trained" in output.getvalue()
    elif relative.startswith("02-"):
        assert namespace["total_minutes"](namespace["records"]) == 35
        assert namespace["report"]["tickets"]["count"] == 4
        assert namespace["report"]["tickets"]["total_minutes"] == 60
        assert namespace["report"]["events"]["count"] == 3
        assert namespace["saved_report"] == namespace["report"]
        assert "Total handling minutes: 60" in output.getvalue()
    else:
        assert namespace["result"].report["rows_accepted"] == 6
        assert namespace["result"].report["accepted_missing_latency"] == 1
        assert namespace["np"].allclose(namespace["solution"], [3, 2])
        assert "Accepted records: 6" in output.getvalue()
    print(f"Verified {relative}: {count} curated Python cells and expected results.")
    return count


if __name__ == "__main__":
    total = sum(check(relative) for relative in NOTEBOOKS)
    print(f"Verified {len(NOTEBOOKS)} notebooks, {total} code cells. Notebook UI testing remains separate.")
