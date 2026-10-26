"""Independent, staged capstone: tuning, seed stability and frozen evaluation.

No earlier notebook state, model pickle or orchestration service is needed.
Each completion marker hashes its outputs and parents. Interrupted partial
stages require a new run; resume skips only verified completed stages.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import time

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, brier_score_loss
from sklearn.model_selection import GroupShuffleSplit, ParameterGrid, StratifiedGroupKFold

from .capstone_models import candidate, export_model, numeric_predict
from .continuation_data import ROOT, binary_metrics, fetch_source, publish_report
from .learning import calibration_table
from .phishing import prepare as prepare_case

PARENTS = {"prepare": [], "tune": ["prepare"], "stability": ["tune"],
           "split-study": ["tune"], "freeze": ["stability"], "evaluate": ["freeze"],
           "deliver": ["evaluate"], "report": ["deliver"]}
SOURCES = ["capstone.py", "capstone_models.py", "capstone_report.py", "phishing.py", "continuation_data.py", "learning.py"]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as output:
        json.dump(value, output, indent=2, allow_nan=False)
        output.write("\n")


def csv(path, frame):
    frame.to_csv(path, index=False, mode="x")


def source_hashes():
    return {name: digest(Path(__file__).with_name(name)) for name in SOURCES}


def verify(run, stage):
    run = Path(run)
    marker = read_json(run / (stage + ".done.json"))
    for name, expected in marker["outputs"].items():
        if digest(run / name) != expected:
            raise ValueError(f"Changed evidence: {name}; use the original run or a new directory.")
    for parent, expected in marker["parents"].items():
        if digest(run / (parent + ".done.json")) != expected:
            raise ValueError("Parent evidence changed.")
        verify(run, parent)
    if stage == "prepare" and read_json(run / "environment.json")["source_hashes"] != source_hashes():
        raise ValueError("Implementation changed since preparation; start a new run.")
    return marker


def begin(run, stage):
    run = Path(run)
    if stage == "split-study" and (run / "freeze.done.json").exists():
        raise ValueError("Choose the optional split study before freezing; start a new run to add it.")
    if (run / (stage + ".done.json")).exists():
        raise ValueError(f"{stage} already completed. Use all --resume to verify/skip it.")
    for parent in PARENTS[stage]:
        verify(run, parent)
    return time.perf_counter()


def finish(run, stage, files, started):
    run = Path(run)
    parents = list(PARENTS[stage])
    if stage == "report" and (run / "split-study.done.json").exists():
        parents.append("split-study")
    save(run / (stage + ".done.json"), {
        "stage": stage, "completed_utc": datetime.now(timezone.utc).isoformat(),
        "seconds": time.perf_counter() - started,
        "parents": {parent: digest(run / (parent + ".done.json")) for parent in parents},
        "outputs": {str(name): digest(run / name) for name in files},
    })


def config_check(config):
    expected = {"schema_version", "cv_folds", "cv_seed", "search_seed", "training_seeds", "split_seeds", "thresholds",
                "false_negative_cost", "false_positive_cost", "bootstrap_repetitions", "bootstrap_seed", "max_cv_fits", "search"}
    if set(config) != expected or type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ValueError("Unexpected study configuration schema.")
    whole = lambda value: isinstance(value, int) and not isinstance(value, bool) and 0 <= value < 2**32
    for name in ["cv_seed", "search_seed", "bootstrap_seed"]:
        if not whole(config[name]):
            raise ValueError("Seeds must be nonnegative integers below 2**32.")
    for name in ["training_seeds", "split_seeds"]:
        values = config[name]
        if not isinstance(values, list) or not 2 <= len(values) <= 10 or len(set(values)) != len(values) or not all(whole(x) for x in values):
            raise ValueError("Predeclare 2–10 distinct seeds.")
    if config["cv_folds"] not in [3, 5] or not whole(config["cv_folds"]):
        raise ValueError("Use three or five group-aware folds.")
    if not whole(config["bootstrap_repetitions"]) or not 50 <= config["bootstrap_repetitions"] <= 1000:
        raise ValueError("Use 50–1000 bootstrap repetitions.")
    for name in ["false_negative_cost", "false_positive_cost"]:
        if isinstance(config[name], bool) or not isinstance(config[name], (int, float)) or not np.isfinite(config[name]) or not 0 < config[name] <= 100:
            raise ValueError("Costs must be finite positive numbers up to 100.")
    thresholds = config["thresholds"]
    if not isinstance(thresholds, list) or not 2 <= len(thresholds) <= 19 or not all(isinstance(x, (float, int)) and not isinstance(x, bool) and np.isfinite(x) and 0 < x < 1 for x in thresholds) or len(set(thresholds)) != len(thresholds):
        raise ValueError("Declare 2–19 distinct thresholds strictly between zero and one.")
    keys = {"logistic": {"C"}, "tree": {"max_depth"}, "forest": {"max_depth", "min_samples_leaf", "n_estimators"}}
    if set(config["search"]) != set(keys):
        raise ValueError("The exemplar compares logistic, tree and forest families.")
    for family, grid in config["search"].items():
        if set(grid) != keys[family]:
            raise ValueError("Unexpected search parameter.")
        for key, values in grid.items():
            if not isinstance(values, list) or not 1 <= len(values) <= 5:
                raise ValueError("Each search dimension needs 1–5 values.")
            for value in values:
                if key == "C":
                    valid = isinstance(value, (int, float)) and not isinstance(value, bool) and np.isfinite(value) and 0 < value <= 1000
                else:
                    limit = 200 if key == "n_estimators" else 30
                    valid = whole(value) and 1 <= value <= limit
                if not valid:
                    raise ValueError("Search value outside the bounded CPU study.")
    fits = sum(len(ParameterGrid(grid)) for grid in config["search"].values()) * config["cv_folds"]
    if not whole(config["max_cv_fits"]) or not fits <= config["max_cv_fits"] <= 150:
        raise ValueError("Search exceeds the declared fit budget (maximum 150).")
    return config


def protocol(run):
    return read_json(Path(run) / "protocol.json"), read_json(Path(run) / "config.json")


def part(run, name):
    return pd.read_csv(Path(run) / (name + ".csv"), dtype={"profile_id": str})


def scores(actual, probability, threshold, config):
    result = binary_metrics(np.asarray(actual), probability >= threshold)
    result["cost_per_1000"] = 1000 * (config["false_negative_cost"] * result["fn"] + config["false_positive_cost"] * result["fp"]) / result["n"]
    result["brier"] = float(brier_score_loss(actual, probability))
    return result


def prepare(run, config_path):
    config = config_check(read_json(config_path))
    if Path(run).resolve().is_relative_to(ROOT / "projects"):
        raise ValueError("Keep generated evidence under runs/ or another directory outside projects/.")
    started = time.perf_counter()
    run = prepare_case(run)  # Reuse acquisition/group boundaries, not the shorter case's modeling stages.
    # Replace the shorter case's selection note before locking this new run.
    outer = read_json(run / "protocol.json")
    outer["selection"] = "Training-only group CV; mean validation cost across predeclared seeds; frozen ensemble. See config.json and selection.json."
    outer["project"] = "Independent optional capstone; the shorter case is unchanged."
    (run / "protocol.json").write_text(json.dumps(outer, indent=2) + "\n", encoding="utf-8")
    save(run / "config.json", config)
    save(run / "environment.json", {"python": platform.python_version(), "platform": platform.platform(),
         "packages": {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scikit-learn"]},
         "source_hashes": source_hashes(), "data_provenance": read_json(fetch_source("phishing") / "provenance.json")})
    train = part(run, "train")
    profile = []
    for column in protocol(run)[0]["features"]:
        for value, count in train[column].value_counts().sort_index().items():
            positives = int(train.loc[train[column] == value, "label"].sum())
            profile.append({"feature": column, "value": int(value), "observations": int(count),
                            "positives": positives, "observed_positive_rate": positives / int(count)})
    csv(run / "training_profile.csv", pd.DataFrame(profile))
    save(run / "data_audit.json", {"training_rows": len(train), "training_positives": int(train.label.sum()),
         "training_missing_cells": int(train.isna().sum().sum()), "features": protocol(run)[0]["features"],
         "split_policy": "Fixed outer chemistry-profile groups, seeds 42/43, reused from the historical phishing case; no campaign/time-independence claim."})
    finish(run, "prepare", ["train.csv", "validation.csv", "test.csv", "protocol.json", "config.json", "environment.json", "training_profile.csv", "data_audit.json"], started)


def tune(run):
    run = Path(run); started = begin(run, "tune")
    info, config = protocol(run); train = part(run, "train"); features = info["features"]
    folds = list(StratifiedGroupKFold(n_splits=config["cv_folds"], shuffle=True, random_state=config["cv_seed"]).split(train, train.label, train.profile_id))
    fold_manifest = []
    for index, (fit, check) in enumerate(folds):
        if set(train.iloc[fit].profile_id) & set(train.iloc[check].profile_id):
            raise ValueError("A profile crossed an inner fold.")
        fold_manifest.append({"fold": index, "fit_record_ids": train.iloc[fit].record_id.tolist(), "check_record_ids": train.iloc[check].record_id.tolist()})
    rows, selected = [], {}
    for family, grid in config["search"].items():
        options = []
        for parameters in ParameterGrid(grid):
            key = json.dumps(parameters, sort_keys=True)
            fold_scores = []
            for fold, (fit, check) in enumerate(folds):
                model = candidate(family, parameters, config["search_seed"])
                start = time.perf_counter(); model.fit(train.iloc[fit][features], train.iloc[fit].label)
                probability = model.predict_proba(train.iloc[check][features])[:, 1]
                score = float(balanced_accuracy_score(train.iloc[check].label, probability >= .5))
                fold_scores.append(score)
                rows.append({"family": family, "parameters": key, "fold": fold, "balanced_accuracy": score,
                             "seconds": time.perf_counter() - start, "training_seed": config["search_seed"]})
            options.append({"parameters": parameters, "mean_cv_balanced_accuracy": float(np.mean(fold_scores)), "std_cv": float(np.std(fold_scores, ddof=1))})
        options.sort(key=lambda item: (-item["mean_cv_balanced_accuracy"], json.dumps(item["parameters"], sort_keys=True)))
        selected[family] = options[0]
    csv(run / "search_trials.csv", pd.DataFrame(rows)); save(run / "inner_folds.json", fold_manifest)
    save(run / "tuning.json", {"selected": selected, "fits": len(rows), "selection": "training-only group CV balanced accuracy at 0.5; stable JSON tie-break"})
    finish(run, "tune", ["search_trials.csv", "inner_folds.json", "tuning.json"], started)


def stability(run):
    run = Path(run); started = begin(run, "stability")
    info, config = protocol(run); features = info["features"]
    train, validation = part(run, "train"), part(run, "validation")
    tuning = read_json(run / "tuning.json")["selected"]
    (run / "models").mkdir()
    outputs, probability_rows, summary_rows, threshold_rows = [], [], [], []
    for family in ["dummy", *tuning]:
        seeds = [config["training_seeds"][0]] if family == "dummy" else config["training_seeds"]
        probabilities = {}
        for seed in seeds:
            parameters = {} if family == "dummy" else tuning[family]["parameters"]
            model = candidate(family, parameters, seed)
            model.fit(train[features], train.label)
            artifact = export_model(model, family, features, seed)
            np.testing.assert_allclose(numeric_predict(artifact, train.iloc[:64]), model.predict_proba(train.iloc[:64][features])[:, 1], atol=1e-10)
            name = f"models/{family}-{seed}.json"; save(run / name, artifact); outputs.append(name)
            probabilities[seed] = numeric_predict(read_json(run / name), validation)
            for record, value in zip(validation.record_id, probabilities[seed]):
                probability_rows.append({"family": family, "seed": seed, "record_id": int(record), "probability": float(value)})
        choices = []
        for threshold in config["thresholds"]:
            values = [scores(validation.label, prediction, threshold, config) for prediction in probabilities.values()]
            row = {"family": family, "threshold": threshold, "mean_cost_per_1000": float(np.mean([v["cost_per_1000"] for v in values])),
                   "mean_balanced_accuracy": float(np.mean([v["balanced_accuracy"] for v in values]))}
            choices.append(row); threshold_rows.append(row)
        chosen = min(choices, key=lambda row: (row["mean_cost_per_1000"], -row["mean_balanced_accuracy"], row["threshold"]))
        for seed, prediction in probabilities.items():
            summary_rows.append({"family": family, "seed": seed, "threshold": chosen["threshold"], **scores(validation.label, prediction, chosen["threshold"], config)})
    csv(run / "validation_probabilities.csv", pd.DataFrame(probability_rows))
    csv(run / "validation_thresholds.csv", pd.DataFrame(threshold_rows))
    csv(run / "validation_runs.csv", pd.DataFrame(summary_rows))
    table = pd.DataFrame(summary_rows)
    aggregates = table.groupby("family")["cost_per_1000"].agg(["count", "mean", "std", "min", "max"]).reset_index()
    for metric in ["balanced_accuracy", "recall", "precision"]:
        group = table.groupby("family")[metric]
        for statistic in ["mean", "std", "min", "max"]:
            aggregates[metric + "_" + statistic] = aggregates.family.map(group.agg(statistic))
    csv(run / "validation_stability.csv", aggregates)
    outputs += ["validation_probabilities.csv", "validation_thresholds.csv", "validation_runs.csv", "validation_stability.csv"]
    finish(run, "stability", outputs, started)


def split_study(run):
    run = Path(run); started = begin(run, "split-study")
    info, config = protocol(run); train = part(run, "train")
    rows = []
    for seed in config["split_seeds"]:
        fit, check = next(GroupShuffleSplit(n_splits=1, test_size=.25, random_state=seed).split(train, groups=train.profile_id))
        for family, choice in read_json(run / "tuning.json")["selected"].items():
            model = candidate(family, choice["parameters"], config["search_seed"])
            model.fit(train.iloc[fit][info["features"]], train.iloc[fit].label)
            prediction = model.predict_proba(train.iloc[check][info["features"]])[:, 1]
            rows.append({"family": family, "split_seed": seed, "training_seed": config["search_seed"],
                         "fit_rows": len(fit), "check_rows": len(check), **scores(train.iloc[check].label, prediction, .5, config)})
    csv(run / "split_sensitivity.csv", pd.DataFrame(rows))
    finish(run, "split-study", ["split_sensitivity.csv"], started)


def freeze(run):
    run = Path(run); started = begin(run, "freeze")
    info, config = protocol(run); rows = pd.read_csv(run / "validation_runs.csv")
    choices = rows.groupby("family").agg(cost=("cost_per_1000", "mean"), accuracy=("balanced_accuracy", "mean"), threshold=("threshold", "first")).reset_index()
    chosen = choices.sort_values(["cost", "accuracy", "family"], ascending=[True, False, True]).iloc[0]
    family = str(chosen.family)
    seeds = [config["training_seeds"][0]] if family == "dummy" else config["training_seeds"]
    models = [f"models/{family}-{seed}.json" for seed in seeds]
    save(run / "selection.json", {"family": family, "threshold": float(chosen.threshold), "seeds": seeds, "models": models,
         "aggregation": "arithmetic mean of all predeclared seed probabilities; never select the best seed",
         "baseline": f"models/dummy-{config['training_seeds'][0]}.json",
         "model_hashes": {name: digest(run / name) for name in models}, "features": info["features"],
         "selection": "minimum mean validation cost, then maximum mean balanced accuracy, then family name; no refit"})
    finish(run, "freeze", ["selection.json"], started)


def profile_intervals(test, probability, threshold, config):
    rng = np.random.default_rng(config["bootstrap_seed"])
    groups = [np.asarray(ids) for ids in test.groupby("profile_id", sort=True).indices.values()]
    samples = []
    for _ in range(config["bootstrap_repetitions"]):
        ids = np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))])
        samples.append(scores(test.label.to_numpy()[ids], probability[ids], threshold, config))
    return pd.DataFrame([{"metric": metric, "low": float(np.quantile([s[metric] for s in samples], .025)),
                          "high": float(np.quantile([s[metric] for s in samples], .975)), "repetitions": len(samples)}
                         for metric in ["balanced_accuracy", "recall", "cost_per_1000"]])


def evaluate(run):
    run = Path(run); started = begin(run, "evaluate")
    info, config = protocol(run); chosen = read_json(run / "selection.json"); test = part(run, "test")
    predictions, rows = [], []
    for seed, name in zip(chosen["seeds"], chosen["models"]):
        probability = numeric_predict(read_json(run / name), test); predictions.append(probability)
        rows.append({"method": "selected_seed", "seed": seed, **scores(test.label, probability, chosen["threshold"], config)})
    ensemble = np.mean(predictions, axis=0)
    baseline = numeric_predict(read_json(run / chosen["baseline"]), test)
    dummy_threshold = float(pd.read_csv(run / "validation_runs.csv").query('family == "dummy"').threshold.iloc[0])
    rows += [{"method": "frozen_ensemble", "seed": None, **scores(test.label, ensemble, chosen["threshold"], config)},
             {"method": "training_prior", "seed": None, **scores(test.label, baseline, dummy_threshold, config)}]
    table = test[["record_id", "profile_id", "label"]].copy()
    table["probability"] = ensemble; table["predicted"] = (ensemble >= chosen["threshold"]).astype(int)
    csv(run / "final_predictions.csv", table); csv(run / "final_scores.csv", pd.DataFrame(rows))
    csv(run / "profile_bootstrap.csv", profile_intervals(test, ensemble, chosen["threshold"], config))
    csv(run / "final_calibration.csv", calibration_table(test.label, ensemble))
    seed_frame = pd.DataFrame(rows).query('method == "selected_seed"')
    seed_summary = []
    for metric in ["balanced_accuracy", "precision", "recall", "cost_per_1000", "brier"]:
        values = seed_frame[metric]
        seed_summary.append({"metric": metric, "count": len(values), "mean": float(values.mean()),
                             "std": float(values.std(ddof=1)) if len(values) > 1 else None,
                             "min": float(values.min()), "max": float(values.max())})
    csv(run / "final_seed_stability.csv", pd.DataFrame(seed_summary))
    errors = table.loc[table.label != table.predicted].copy()
    errors["error"] = np.where(errors.predicted == 1, "false_positive", "false_negative")
    csv(run / "error_analysis.csv", errors)
    save(run / "evaluation.json", {"selected": chosen["family"], "threshold": chosen["threshold"], "test_rows": len(test),
         "ensemble": rows[-2], "baseline": rows[-1], "test_labels_used_for_selection": False,
         "uncertainty": "Illustrative exact-profile bootstrap conditional on this split and fixed models; not domain/campaign independence or population coverage."})
    finish(run, "evaluate", ["final_predictions.csv", "final_scores.csv", "final_seed_stability.csv", "profile_bootstrap.csv", "final_calibration.csv", "error_analysis.csv", "evaluation.json"], started)


def predict(bundle, record):
    if not isinstance(record, dict) or set(record) != set(bundle["features"]):
        raise ValueError("Supply exactly the declared 30 features, without targets or extra fields.")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value) or value not in [-1, 0, 1] for value in record.values()):
        raise ValueError("Source-encoded features must be finite -1, 0 or 1, never booleans.")
    frame = pd.DataFrame([record])
    probability = float(np.mean([numeric_predict(model, frame)[0] for model in bundle["models"]]))
    return {"probability": probability, "review_flag": bool(probability >= bundle["threshold"]),
            "threshold": bundle["threshold"], "family": bundle["family"], "purpose": "historical triage demonstration; no automatic blocking"}


def deliver(run):
    run = Path(run); started = begin(run, "deliver")
    info, config = protocol(run); chosen = read_json(run / "selection.json")
    bundle = {"schema_version": 1, "family": chosen["family"], "features": chosen["features"], "threshold": chosen["threshold"],
              "models": [read_json(run / name) for name in chosen["models"]]}
    save(run / "inference_bundle.json", bundle)
    train, test = part(run, "train"), part(run, "test")
    record = {name: int(test.iloc[0][name]) for name in info["features"]}
    save(run / "example_request.json", record)
    begin_prediction = time.perf_counter(); response = predict(bundle, record)
    response["measured_seconds"] = time.perf_counter() - begin_prediction
    save(run / "example_response.json", response)
    checks = []
    for mutation in ["missing", "target", "boolean", "unknown_category"]:
        invalid = dict(record)
        if mutation == "missing": invalid.pop(info["features"][0])
        if mutation == "target": invalid["label"] = 1
        if mutation == "boolean": invalid[info["features"][0]] = True
        if mutation == "unknown_category": invalid[info["features"][0]] = 2
        try:
            predict(bundle, invalid)
        except ValueError:
            checks.append({"case": mutation, "rejected": True})
        else:
            raise ValueError("Invalid input unexpectedly accepted.")
    save(run / "service_checks.json", checks)
    probabilities = np.mean([numeric_predict(model, test) for model in bundle["models"]], axis=0)
    np.testing.assert_allclose(probabilities, pd.read_csv(run / "final_predictions.csv").probability, atol=1e-10)
    rows = []
    for number, ids in enumerate(np.array_split(np.arange(len(test)), 4), 1):
        shift = max(abs(float((test.iloc[ids][feature] == category).mean()) - float((train[feature] == category).mean()))
                    for feature in info["features"] for category in [-1, 0, 1])
        rows.append({"batch": number, "rows": len(ids), "maximum_category_rate_shift": shift,
                     **scores(test.iloc[ids].label, probabilities[ids], chosen["threshold"], config)})
    csv(run / "monitoring_rehearsal.csv", pd.DataFrame(rows))
    save(run / "release_decision.json", {"live_deployment_approved": False, "bundle_sha256": digest(run / "inference_bundle.json"),
         "owner_role": "adopting service owner and security/data-governance reviewers", "fallback": "manual review queue; do not silently allow or block on schema failure",
         "before_live_use": ["prospective permitted data and decision-time feature audit", "validated error costs/capacity", "measured service objectives and human oversight"],
         "rollback": "stop automated flags, retain version/hash and incident record, return to manual queue",
         "monitoring": "four source-order batches are offline rehearsal, not a measured time series or drift detection validation"})
    finish(run, "deliver", ["inference_bundle.json", "example_request.json", "example_response.json", "service_checks.json", "monitoring_rehearsal.csv", "release_decision.json"], started)


def report(run):
    from .capstone_report import write_report
    run = Path(run); started = begin(run, "report")
    if (run / "split-study.done.json").exists():
        verify(run, "split-study")
    files = write_report(run)
    finish(run, "report", files, started)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Optional independent capstone; no earlier notebook state required.")
    parser.add_argument("stage", choices=[*PARENTS, "all", "predict", "verify"])
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "projects/phishing-triage/configs/study.json")
    parser.add_argument("--resume", action="store_true", help="Verify and skip completed stages; partial outputs are never overwritten.")
    parser.add_argument("--advanced", action="store_true", help="Also run the separate training-only split-sensitivity study.")
    parser.add_argument("--input", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.stage == "predict":
            verify(args.run, "deliver")
            print(json.dumps(predict(read_json(args.run / "inference_bundle.json"), read_json(args.input)), indent=2)); return
        if args.stage == "verify":
            verify(args.run, "report"); print("Verified the complete stage ledger and source identities."); return
        stages = ["prepare", "tune", *(["split-study"] if args.advanced else []), "stability", "freeze", "evaluate", "deliver", "report"] if args.stage == "all" else [args.stage]
        for stage in stages:
            if args.resume and (args.run / (stage + ".done.json")).exists():
                verify(args.run, stage)
                if stage == "prepare" and read_json(args.run / "config.json") != config_check(read_json(args.config)):
                    raise ValueError("Resume configuration differs from the prepared study.")
                print("VERIFIED_SKIP", stage); continue
            if stage == "prepare": prepare(args.run, args.config)
            else: {"split-study": split_study}.get(stage, globals().get(stage))(args.run)
            print("COMPLETED", stage, flush=True)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, f"Capstone failed: {error}\n")


if __name__ == "__main__":
    main()
