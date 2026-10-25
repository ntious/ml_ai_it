"""Run only listed trusted notebooks; groups isolate optional frameworks.

Fresh namespaces check code, not notebook-interface or assistive-technology
usability. Never execute untrusted uploaded notebooks with this script.
"""
import argparse
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ("01-foundations/first_steps.ipynb", "core", 1),
    ("02-python-workflows/workflow.ipynb", "core", 2),
    ("03-data-processing/complete_walkthrough.ipynb", "core", 3),
    ("04-exploration/exploration.ipynb", "core", 4),
    ("05-regression/regression.ipynb", "core", 5),
    ("06-classification/walkthrough.ipynb", "core", 6),
    ("07-clustering/walkthrough.ipynb", "core", 7),
    ("08-neural-networks/walkthrough.ipynb", "frameworks", 8),
    ("09-neural-nlp/walkthrough.ipynb", "frameworks", 9),
    ("10-llm-workflows/walkthrough.ipynb", "frameworks", 10),
    ("11-fine-tuning/walkthrough.ipynb", "frameworks", 11),
    ("12-deployment/walkthrough.ipynb", "frameworks", 12),
    ("13-ethics-fairness/walkthrough.ipynb", "core", 13),
    ("14-agents/walkthrough.ipynb", "frameworks", 14),
]


def check(relative, number):
    path = ROOT / "notebooks/lessons" / relative
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    assert len({cell["id"] for cell in notebook["cells"]}) == len(notebook["cells"])
    namespace = {"__name__": "__main__"}
    output = io.StringIO()
    previous = Path.cwd()
    count = 0
    try:
        os.chdir(ROOT)
        with redirect_stdout(output):
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] == "code":
                    assert cell["execution_count"] is None and cell["outputs"] == []
                    exec(compile("".join(cell["source"]), f"{relative}:cell-{index+1}", "exec"), namespace)
                    count += 1
    finally:
        os.chdir(previous)
    if number == 1:
        assert namespace["boundary_results"] == {80: False, 81: True}
        assert namespace["result"]["review_needed"]
    elif number == 2:
        assert namespace["report"]["tickets"]["total_minutes"] == 60
        assert namespace["saved_report"] == namespace["report"]
    elif number == 3:
        assert namespace["result"].report["rows_accepted"] == 6
        assert namespace["np"].allclose(namespace["solution"], [3, 2])
    elif number == 4:
        assert namespace["result"]["total_requests"] == 4180
        assert namespace["custom_plot"].is_file()
    elif number == 5:
        assert namespace["result"]["selected"] == namespace["selection"]["selected"] == "previous_day"
        assert namespace["result"]["test_rows"] == 110
        assert abs(namespace["result"]["scores"][0]["mae"] - 926.5727272727273) < 1e-6
        assert namespace["invalid_example"]["invalid_validation_mae"] < 1e-8
    else:
        result = namespace["result"]
        assert result["module"] == number
        if number == 6: assert not result["split_group_overlap"]
        if number == 7: assert not result["quality_used_for_fit_or_selection"]
        if number in {8, 9}: assert result["saved_model_replay_verified"] and result["weight_change_norm"] > 0
        if number == 10: assert result["real_examples"] == 8
        if number == 11: assert result["adapter_replay_verified"] and result["adapter_update_norm"] > 0
        if number == 12: assert result["real_heldout_rows"] == 243
        if number == 13: assert not result["protected_attributes_used_for_fitting"]
        if number == 14: assert result["destructive_request_refused"]
        source = namespace["run_dir"]
        assert (source / "index.html").is_file() and (source / "summary.json").is_file()
        destination = ROOT / "runs/verified" / f"module{number:02d}"
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        print("VERIFIED_MODULE", number, json.dumps(result, sort_keys=True))
    print(f"Verified {relative}: {count} curated code cells.")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=["core", "frameworks", "all"], default="all")
    group = parser.parse_args().group
    selected = [item for item in NOTEBOOKS if group == "all" or item[1] == group]
    total = sum(check(relative, number) for relative, _, number in selected)
    print(f"Verified {len(selected)} notebooks, {total} code cells; group={group}. UI testing is separate.")
