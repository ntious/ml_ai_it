"""Execute trusted registered notebooks in fresh Jupyter kernels.

Source stays clean; executed copies retain outputs in runs/verified. This is
runtime/format evidence, not manual notebook-interface or screen-reader review.
Never use this command to run untrusted uploaded notebooks.
"""
import argparse
import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
MODULES = json.loads((ROOT / "curriculum/modules.json").read_text(encoding="utf-8"))["modules"]
# Learning-result checks run inside the notebook kernel after its own cells.
VALIDATION = r"""if number == 1:
    assert globals()["boundary_results"] == {80: False, 81: True}
    assert globals()["result"]["review_needed"]
elif number == 2:
    assert globals()["report"]["tickets"]["total_minutes"] == 60
    assert globals()["saved_report"] == globals()["report"]
elif number == 3:
    assert globals()["result"].report["rows_accepted"] == 6
    assert globals()["np"].allclose(globals()["solution"], [3, 2])
elif number == 4:
    assert globals()["result"]["total_requests"] == 4180
    assert globals()["custom_plot"].is_file()
elif number == 5:
    assert globals()["result"]["selected"] == globals()["selection"]["selected"] == "previous_day"
    assert globals()["result"]["test_rows"] == 110
    assert abs(globals()["result"]["scores"][0]["mae"] - 926.5727272727273) < 1e-6
    assert globals()["invalid_example"]["invalid_validation_mae"] < 1e-8
else:
    result = globals()["result"]
    assert result["module"] == number
    if number == 6: assert not result["split_group_overlap"]
    if number == 7: assert not result["quality_used_for_fit_or_selection"]
    if number in {8, 9}: assert result["saved_model_replay_verified"] and result["weight_change_norm"] > 0
    if number == 10: assert result["real_examples"] == 8
    if number == 11: assert result["adapter_replay_verified"] and result["adapter_update_norm"] > 0
    if number == 12: assert result["real_heldout_rows"] == 243
    if number == 13: assert not result["audited_sex_race_used_for_fitting"]
    if number == 14: assert result["destructive_request_refused"]
    source = globals()["run_dir"]
    assert (source / "index.html").is_file() and (source / "summary.json").is_file()
    destination = ROOT / "runs/verified" / f"module{number:02d}"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    print("VERIFIED_MODULE", number, json.dumps(result, sort_keys=True))
"""


def check(module, kernel):
    source = ROOT / module["notebook"]
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None and cell.outputs == [], source
    count = sum(cell.cell_type == "code" for cell in notebook.cells)
    # The temporary final cell validates the same in-kernel variables learners
    # produced. It is excluded from the saved tutorial, not counted as curriculum.
    validation = "import json, shutil\nfrom pathlib import Path\nROOT = Path(" + repr(str(ROOT)) + ")\nnumber = " + str(module["id"]) + "\n" + VALIDATION
    notebook.cells.append(nbformat.v4.new_code_cell(validation))
    NotebookClient(notebook, timeout=900, kernel_name=kernel, resources={"metadata": {"path": str(ROOT)}}).execute()
    evidence = notebook.cells.pop()
    for output in evidence.outputs:
        if output.output_type == "stream":
            print(output.text, end="")
    nbformat.validate(notebook)
    destination = ROOT / "runs/verified" / f'module{module["id"]:02d}'
    destination.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, destination / "executed.ipynb")
    print(f'Verified {module["notebook"]}: {count} code cells in a fresh {kernel} kernel.')
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=["core", "frameworks", "all"], default="all")
    parser.add_argument("--kernel", default="python3", help="Installed Jupyter kernel matching the selected environment.")
    args = parser.parse_args()
    selected = [m for m in MODULES if args.group == "all" or m["profile"] == args.group]
    total = sum(check(module, args.kernel) for module in selected)
    if args.group in {"core", "all"}:
        source = ROOT / "notebooks/cases/phishing.ipynb"
        notebook = nbformat.read(source,as_version=4)
        nbformat.validate(notebook)
        NotebookClient(notebook,timeout=900,kernel_name=args.kernel,resources={"metadata":{"path":str(ROOT)}}).execute()
        destination = ROOT / "runs/verified/phishing"
        destination.mkdir(parents=True,exist_ok=True)
        nbformat.write(notebook,destination / "executed.ipynb")
        print("Verified independent phishing case in a fresh kernel.")
    print(f"Verified {len(selected)} notebooks, {total} code cells; group={args.group}. Manual interface review remains separate.")
