"""Report the selected course environment without importing heavy frameworks."""
import argparse
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE = ["numpy","pandas","scikit-learn","matplotlib","seaborn","nbformat","nbclient","ipykernel"]
FRAMEWORKS = ["tensorflow-cpu","torch","transformers","streamlit"]


def inspect(profile):
    versions, missing = {}, []
    for name in CORE + (FRAMEWORKS if profile == "frameworks" else []):
        try: versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError: missing.append(name)
    problems=[]
    if sys.version_info < (3,11): problems.append("Python 3.11 or newer is required; 3.12 and 3.13 are checked in CI.")
    if profile == "frameworks" and platform.system() != "Linux": problems.append("The verified framework reference requires Linux CPU.")
    return {"profile":profile,"python":platform.python_version(),"executable":sys.executable,"platform":platform.platform(),
            "project_root":str(ROOT),"working_folder":str(Path.cwd()),"packages":versions,"missing":missing,
            "problems":problems,"free_disk_gb":round(shutil.disk_usage(ROOT).free/1e9,2),
            "resource_note":"Allow several GB for CPU frameworks/models; measure actual memory/runtime on your route. Hosted service/AT usability is not tested by this command."}


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--profile",choices=["core","frameworks"],default="core")
    args=parser.parse_args();report=inspect(args.profile);print(json.dumps(report,indent=2))
    return int(bool(report["missing"] or report["problems"]))

if __name__ == "__main__": raise SystemExit(main())
