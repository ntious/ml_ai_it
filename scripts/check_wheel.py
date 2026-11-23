"""Exercise the built wheel without an editable checkout on the import path."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
wheels = list((ROOT / "dist").glob("practical_ml_ai-*.whl"))
assert len(wheels) == 1, wheels
with tempfile.TemporaryDirectory() as temporary:
    base = Path(temporary)
    target, runtime = base / "installed", base / "runtime"
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "--target", str(target), str(wheels[0])], check=True)
    # Reuse reviewed real records, preserving the same archive/digest validation.
    shutil.copytree(ROOT / "runs/datasets/wine", runtime / "datasets/wine")
    code = """
import json, os, sys
from pathlib import Path
target = Path(sys.argv[1])
sys.path.insert(0, str(target))
import practical_ml_ai
from practical_ml_ai.continuation_data import RUNS_ROOT, runtime_directory
from practical_ml_ai.classical import classification_bundle
from practical_ml_ai.deployment import checked_predict
from practical_ml_ai.agent_study import requests_frame
from practical_ml_ai.practice import check as practice_check
assert practice_check('m08_checkpoint', lambda train, validation: min(range(len(validation)), key=validation.__getitem__) + 1)['state'] == 'passed'
assert Path(practical_ml_ai.__file__).is_relative_to(target)
controls = requests_frame()
assert (controls.split == "test").sum() == 26
assert not controls.request.duplicated().any()
assert RUNS_ROOT == Path(os.environ["ML_AI_RUNS_DIR"])
bundle = classification_bundle()
row = bundle["split"]["test"].iloc[0]
record = {name: float(row[name]) for name in bundle["features"]}
prediction = checked_predict(bundle, record)
assert 0 <= prediction["probability"] <= 1
try:
    checked_predict(bundle, {**record, "quality": 7})
except ValueError:
    pass
else:
    raise AssertionError("Target leakage input was accepted")
del os.environ["ML_AI_RUNS_DIR"]
fallback = runtime_directory()
assert not fallback.is_relative_to(target)
assert fallback.name == "ml-ai-it"
print(json.dumps({"installed_file": str(practical_ml_ai.__file__), "prediction": prediction, "fallback": str(fallback)}))
"""
    environment = dict(os.environ, ML_AI_RUNS_DIR=str(runtime))
    subprocess.run([sys.executable, "-I", "-c", code, str(target)], cwd=base, env=environment, check=True)
    assert not (target / "runs").exists()
print("Verified isolated installed-wheel inference, schema rejection, real-data replay, explicit cache directory, and user-cache fallback.")
