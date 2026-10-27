"""Download current UCI client data locally for exploration; never commit data."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


def download(destination):
    from ucimlrepo import fetch_ucirepo

    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(f"Choose a new destination: {destination}")
    dataset = fetch_ucirepo(id=942)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None or len(features) != len(targets):
        raise ValueError("UCI did not supply aligned features and targets")
    destination.mkdir(parents=True)
    features.to_csv(destination / "features.csv", index=False)
    targets.to_csv(destination / "targets.csv", index=False)
    dataset.variables.to_csv(destination / "variables.csv", index=False)
    (destination / "metadata.json").write_text(json.dumps(dataset.metadata, indent=2, default=str) + "\n")
    manifest = {
        "uci_id": 942,
        "citation": "S., B. & Nagapadma, R. (2023). RT-IoT2022 [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5P338.",
        "license": "CC BY 4.0",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "ucimlrepo_version": version("ucimlrepo"),
        "rows": len(features),
        "scope": "Current UCI client export for exploration; not the pinned archive used by run.py.",
        "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.iterdir())},
    }
    (destination / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Downloaded {len(features)} rows to {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="runs/datasets/rt-iot2022-client")
    args = parser.parse_args()
    download(args.output)
