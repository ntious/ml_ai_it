"""Real-source acquisition and transparent reporting for Modules 6–14.

Dataset archives are retained unmodified, with attribution and observed hashes.
Only named members are read: arbitrary ZIP paths are never extracted. Reviewed
hashes can be added to SOURCES after inspecting a successful acquisition run.
"""
from datetime import datetime, timezone
import hashlib
from html import escape
import io
import json
import os
from pathlib import Path
import urllib.request
import zipfile

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split

ROOT = Path(__file__).resolve().parents[2]


def runtime_directory():
    """Keep installed-package caches outside package files; allow explicit control."""
    configured = os.environ.get("ML_AI_RUNS_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    if (ROOT / "pyproject.toml").is_file() and (ROOT / "src/practical_ml_ai").is_dir():
        return ROOT / "runs"
    base = (Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
            if os.name == "nt" else Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")))
    return base / "ml-ai-it"


RUNS_ROOT = runtime_directory()
SOURCES = {
    "phishing": {"id":327,"slug":"phishing+websites","members":["Training Dataset.arff"],
        "citation":"Mohammad, R. & McCluskey, L. (2012). Phishing Websites. UCI. DOI:10.24432/C51W2X.",
        "sha256":"514f582cb44cba17251baf1d59f64cddff16efa2b644d091ce8d2a1e8d492940"},
    "wine": {"id": 186, "slug": "wine+quality", "members": ["winequality-red.csv", "winequality.names"],
             "citation": "Cortez, P., et al. (2009). Wine Quality. UCI. DOI:10.24432/C56S3T.", "sha256": "3ed56667f4b828242bd732d7d1dd7f2861e54432239d7fa63877014cbb0304d4"},
    "sms": {"id": 228, "slug": "sms+spam+collection", "members": ["SMSSpamCollection", "readme"],
            "citation": "Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection. UCI. DOI:10.24432/C5CC84.", "sha256": "1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3"},
    "adult": {"id": 2, "slug": "adult", "members": ["adult.data", "adult.test", "adult.names"],
              "citation": "Becker, B. & Kohavi, R. (1996). Adult. UCI. DOI:10.24432/C5XW20.", "sha256": "7537312dd56c2b98035880805ce99e68183a30ee468aa5329d6df0fbb3cc21bb"},
}


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def fetch_source(name):
    """Download once. A changed cached file is an error, not a silent refresh."""
    spec = SOURCES[name]
    directory = RUNS_ROOT / "datasets" / name
    meta_path = directory / "provenance.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if spec["sha256"] and meta["archive_sha256"] != spec["sha256"]:
            raise ValueError("Cache differs from the reviewed archive; use the reviewed source.")
        if set(meta["files"]) != set(spec["members"]):
            raise ValueError("Cached member schema changed.")
        if sha_bytes((directory / "original.zip").read_bytes()) != meta["archive_sha256"]:
            raise ValueError("Cached original archive changed.")
        for member, expected in meta["files"].items():
            if sha_bytes((directory / member).read_bytes()) != expected:
                raise ValueError("Cached source changed: " + member)
        return directory
    if directory.exists():
        raise ValueError("Incomplete source cache; inspect it or choose a clean cache before retrying.")
    url = f"https://archive.ics.uci.edu/static/public/{spec['id']}/{spec['slug']}.zip"
    with urllib.request.urlopen(url, timeout=60) as response:
        raw = response.read(10_000_001)
    if len(raw) > 10_000_000:
        raise ValueError("Unexpected archive size.")
    checksum = sha_bytes(raw)
    if spec["sha256"] and checksum != spec["sha256"]:
        raise ValueError("Upstream archive changed; review before updating the recorded source.")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = {member: archive.read(member) for member in spec["members"]}
    directory.mkdir(parents=True)
    (directory / "original.zip").write_bytes(raw)
    for member, data in members.items():
        (directory / member).write_bytes(data)
    meta = {
        "dataset": name, "source": f"https://archive.ics.uci.edu/dataset/{spec['id']}/{spec['slug']}",
        "citation": spec["citation"], "license": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "archive_sha256": checksum, "files": {key: sha_bytes(value) for key, value in members.items()},
        "changes": "Original archived files unchanged; each module documents its derived selection/transformation.",
    }
    write_json(meta_path, meta)
    (directory / "ATTRIBUTION.txt").write_text(spec["citation"] + "\n" + meta["source"] + "\nCC BY 4.0\nOriginal files unchanged. Derived transformations are documented in the lesson.\n", encoding="utf-8")
    print("REAL_SOURCE", json.dumps(meta, sort_keys=True))
    return directory


def wine_splits():
    """Group identical chemistry profiles so they cannot cross split boundaries.

    There are no subject IDs. This is a conservative duplicate-profile boundary,
    not a claim that the physical samples/people are independently identified.
    """
    folder = fetch_source("wine")
    frame = pd.read_csv(folder / "winequality-red.csv", sep=";")
    features = [column for column in frame if column != "quality"]
    if len(features) != 11 or frame[features + ["quality"]].isna().any().any():
        raise ValueError("Unexpected wine schema.")
    if not np.isfinite(frame[features].to_numpy()).all():
        raise ValueError("Nonfinite chemistry measurement.")
    frame["record_id"] = np.arange(len(frame))
    frame["label"] = (frame["quality"] >= 7).astype(int)
    groups = pd.util.hash_pandas_object(frame[features], index=False).astype(str)
    outer = GroupShuffleSplit(n_splits=1, test_size=.30, random_state=42)
    train_ids, other_ids = next(outer.split(frame, groups=groups))
    inner = GroupShuffleSplit(n_splits=1, test_size=.5, random_state=43)
    validation_local, test_local = next(inner.split(frame.iloc[other_ids], groups=groups.iloc[other_ids]))
    indices = {"train": train_ids, "validation": other_ids[validation_local], "test": other_ids[test_local]}
    split = {name: frame.iloc[ids].copy() for name, ids in indices.items()}
    group_sets = {name: set(groups.iloc[ids]) for name, ids in indices.items()}
    if any(group_sets[a] & group_sets[b] for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]):
        raise ValueError("Chemistry-group overlap.")
    if any(part["label"].nunique() != 2 for part in split.values()):
        raise ValueError("Both labels must be observed in every split.")
    manifest = {"source": "UCI red wine quality", "raw_rows": len(frame), "features": features,
                "target": "human quality score >=7; classroom threshold, not a certification",
                "split": "Seeded grouped chemistry profiles; approximately 70/15/15; no temporal claim",
                "record_ids": {name: [int(x) for x in part.record_id] for name, part in split.items()},
                "group_overlap": False}
    return split, features, manifest


def sms_splits(limit=1200):
    """Use human-labeled real SMS, removing ambiguous/duplicate normalized texts."""
    folder = fetch_source("sms")
    records = []
    for line in (folder / "SMSSpamCollection").read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        label, text = line.split("\t", 1)
        if label not in {"ham", "spam"}:
            raise ValueError("Unexpected SMS label.")
        normalized = " ".join(text.casefold().split())
        records.append({"text": text, "label": int(label == "spam"), "text_id": sha_bytes(normalized.encode())})
    frame = pd.DataFrame(records)
    counts = frame.groupby("text_id")["label"].nunique()
    conflicts = set(counts[counts > 1].index)
    frame = frame.loc[~frame.text_id.isin(conflicts)].drop_duplicates("text_id").reset_index(drop=True)
    if len(frame) > limit:
        chosen, _ = train_test_split(frame, train_size=limit, stratify=frame.label, random_state=42)
        frame = chosen.sort_values("text_id").reset_index(drop=True)
    training, other = train_test_split(frame, test_size=.4, stratify=frame.label, random_state=43)
    validation, test = train_test_split(other, test_size=.5, stratify=other.label, random_state=44)
    split = {"train": training.reset_index(drop=True), "validation": validation.reset_index(drop=True), "test": test.reset_index(drop=True)}
    if any(set(split[a].text_id) & set(split[b].text_id) for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]):
        raise ValueError("Text overlap.")
    manifest = {"source": "UCI SMS Spam Collection", "sample_rows": len(frame), "conflicting_text_ids_removed": len(conflicts),
                "sampling": "Seeded label-stratified sample after text deduplication; not a population estimate",
                "record_ids": {name: part.text_id.tolist() for name, part in split.items()},
                "privacy": "Public messages can contain phone numbers/personal content. Local processing; reports show hashes, not raw messages."}
    return split, manifest


def balanced_real_subset(frame, count):
    """Select actual rows, with equal label counts for tiny mechanics checks.

    These class-balanced subsets change prevalence and cannot estimate deployment
    accuracy; they are explicitly disclosed in the small-LLM lessons.
    """
    each = count // 2
    return pd.concat([frame.loc[frame.label == label].head(each) for label in [0, 1]]).reset_index(drop=True)


def binary_metrics(actual, predicted):
    """Explicit denominators prevent an undefined rate being fabricated as zero."""
    actual, predicted = np.asarray(actual), np.asarray(predicted)
    tp = int(((actual == 1) & (predicted == 1)).sum())
    tn = int(((actual == 0) & (predicted == 0)).sum())
    fp = int(((actual == 0) & (predicted == 1)).sum())
    fn = int(((actual == 1) & (predicted == 0)).sum())
    ratio = lambda a, b: float(a / b) if b else None
    recall, specificity = ratio(tp, tp + fn), ratio(tn, tn + fp)
    return {"n": len(actual), "tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "precision": ratio(tp, tp + fp), "recall": recall, "specificity": specificity,
            "selection_rate": ratio(tp + fp, len(actual)), "fpr": ratio(fp, fp + tn),
            "balanced_accuracy": (recall + specificity) / 2 if recall is not None and specificity is not None else None,
            "f1": ratio(2 * tp, 2 * tp + fp + fn)}


def new_run(path):
    path = Path(path)
    if path.exists():
        raise ValueError("Use a fresh output directory; do not overwrite a completed study.")
    path.mkdir(parents=True)
    return path


def publish_report(directory, title, summary, tables, notes):
    """Text/JSON, CSV, and captioned/scoped HTML tables carry the same evidence."""
    directory = Path(directory)
    write_json(directory / "summary.json", summary)
    text = title + "\n\n" + json.dumps(summary, indent=2) + "\n\n" + "\n\n".join(notes) + "\n"
    (directory / "summary.txt").write_text(text, encoding="utf-8")
    sections = []
    for name, frame in tables.items():
        frame.to_csv(directory / (name + ".csv"), index=False)
        head = "".join('<th scope="col">' + escape(str(c)) + "</th>" for c in frame.columns)
        rows = "".join("<tr>" + "".join("<td>" + escape(str(v)) + "</td>" for v in row) + "</tr>" for row in frame.itertuples(index=False, name=None))
        caption = name.replace("_", " ")
        sections.append('<section><h2>' + escape(caption.title()) + '</h2><p><a href="' + name + '.csv">Download ' + escape(caption) + ' (CSV)</a></p><div class="table-wrap" tabindex="0" role="region" aria-label="' + escape(caption) + '"><table><caption>' + escape(caption) + '</caption><thead><tr>' + head + '</tr></thead><tbody>' + rows + '</tbody></table></div></section>')
    html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + escape(title) + '</title><style>body{font:1.1rem/1.6 system-ui,sans-serif;max-width:78ch;margin:auto;padding:1rem;color:#18232d;background:white}table{border-collapse:collapse}th,td{border:1px solid #718096;padding:.4rem;text-align:left}.table-wrap{overflow-x:auto;max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#075985}a:focus-visible,pre:focus-visible,.table-wrap:focus-visible{outline:3px solid currentColor;outline-offset:3px}.skip{position:absolute;top:-6rem}.skip:focus{top:0;background:white}</style></head><body><a class="skip" href="#main">Skip to main content</a><main id="main" tabindex="-1"><h1>' + escape(title) + '</h1><pre tabindex="0" aria-label="Named results">' + escape(json.dumps(summary, indent=2)) + '</pre>' + "".join("<p>" + escape(n) + "</p>" for n in notes) + "".join(sections) + '</main><footer><p>Original educational content: CC BY 4.0. External data retain their source attribution. Results are available as text, tables and downloads; consult the course accessibility guide for interface test scope.</p></footer></body></html>'
    (directory / "index.html").write_text(html + "\n", encoding="utf-8")
    print("MODULE_RESULT", title, json.dumps(summary, sort_keys=True))
    return summary
