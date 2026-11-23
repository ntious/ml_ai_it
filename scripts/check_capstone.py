"""Execute the independent project notebook in a fresh core kernel."""
import argparse
from pathlib import Path
import shutil

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "projects/phishing-triage/notebooks/complete-study.ipynb"


def check(kernel):
    notebook = nbformat.read(SOURCE, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None and cell.outputs == []
    notebook.cells.append(nbformat.v4.new_code_cell('''from practical_ml_ai.capstone import verify
verify(run_dir, "report")
assert evaluation["test_labels_used_for_selection"] is False
assert selection["seeds"] == configuration["training_seeds"] or selection["family"] == "dummy"
assert len(pd.read_csv(run_dir / "search_trials.csv")) == 30
assert len(pd.read_csv(run_dir / "final_seed_stability.csv")) == 5
assert not json.loads((run_dir / "release_decision.json").read_text())["live_deployment_approved"]
import shutil
destination = ROOT / "runs/verified/capstone"
if destination.exists():
    shutil.rmtree(destination)
shutil.copytree(run_dir, destination)
print("VERIFIED_CAPSTONE", json.dumps(json.loads((run_dir / "summary.json").read_text()), sort_keys=True))'''))
    NotebookClient(notebook, timeout=1200, kernel_name=kernel,
                   resources={"metadata": {"path": str(ROOT)}}).execute()
    evidence = notebook.cells.pop()
    for output in evidence.outputs:
        if output.output_type == "stream":
            print(output.text, end="")
    destination = ROOT / "runs/verified/capstone"
    nbformat.write(notebook, destination / "executed.ipynb")
    print("Verified separate capstone notebook in a fresh kernel; all original module notebooks remain independent.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel", default="ml-ai-core")
    check(parser.parse_args().kernel)
