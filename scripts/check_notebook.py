"""Execute this repository's curated plain-Python notebook cells in order.

This is a clean code-path check, not a notebook UI or assistive-technology test.
Never use this script to execute an untrusted uploaded notebook.
"""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/lessons/03-data-processing/complete_walkthrough.ipynb"
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
assert notebook["nbformat"] == 4
assert len({cell["id"] for cell in notebook["cells"]}) == len(notebook["cells"])
namespace = {"__name__": "__main__"}
output = io.StringIO()
previous = Path.cwd()
count = 0
try:
    os.chdir(ROOT)
    with redirect_stdout(output):
        for i, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                exec(compile(source, f"{NOTEBOOK.name}:cell-{i + 1}", "exec"), namespace)
                count += 1
finally:
    os.chdir(previous)
assert namespace["result"].report["rows_accepted"] == 6
assert namespace["result"].report["accepted_missing_latency"] == 1
assert namespace["np"].allclose(namespace["solution"], [3, 2])
assert "Accepted records: 6" in output.getvalue()
print(f"Executed {count} curated Python cells from a clean namespace; report and linear-system results verified.")
