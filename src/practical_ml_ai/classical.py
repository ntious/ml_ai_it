"""Real-data classification, clustering, and fairness audit (Modules 6, 7, 13)."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

from .continuation_data import (
    binary_metrics, fetch_source, new_run, publish_report, wine_splits, write_json,
)


def classification_bundle():
    """Freeze model and threshold on validation, before evaluating test records."""
    split, features, manifest = wine_splits()
    train, validation = split["train"], split["validation"]
    models = {"dummy": make_pipeline(SimpleImputer(), DummyClassifier(strategy="prior")),
              "logistic": make_pipeline(SimpleImputer(), StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))}
    for depth in [2, 4, 8]:
        models["tree_depth_" + str(depth)] = make_pipeline(SimpleImputer(), DecisionTreeClassifier(max_depth=depth, min_samples_leaf=10, random_state=42))
    scores = []
    for name, model in models.items():
        model.fit(train[features], train.label)
        probability = model.predict_proba(validation[features])[:, 1]
        for threshold in [.3, .5, .7]:
            metric = binary_metrics(validation.label, probability >= threshold)
            scores.append({"model": name, "threshold": threshold, **metric})
    scores.sort(key=lambda item: (-item["balanced_accuracy"], item["model"], item["threshold"]))
    chosen = scores[0]
    return {"split": split, "features": features, "manifest": manifest, "models": models,
            "model": models[chosen["model"]], "selection": chosen, "validation_scores": pd.DataFrame(scores)}


def run_classification(output):
    directory = new_run(output)
    bundle = classification_bundle()
    test, features = bundle["split"]["test"], bundle["features"]
    chosen = bundle["selection"]
    probability = bundle["model"].predict_proba(test[features])[:, 1]
    predictions = pd.DataFrame({"record_id": test.record_id, "actual": test.label,
                                "probability": probability, "predicted": (probability >= chosen["threshold"]).astype(int)})
    test_scores = [{"model": chosen["model"], **binary_metrics(test.label, predictions.predicted)}]
    if chosen["model"] != "dummy":
        dummy = bundle["models"]["dummy"].predict(test[features])
        test_scores.append({"model": "dummy_majority", **binary_metrics(test.label, dummy)})
    # Always expose a shallow tree as an interpretable comparison, even if it loses.
    tree = bundle["models"]["tree_depth_2"][1]
    (directory / "tree_rules.txt").write_text(export_text(tree, feature_names=features), encoding="utf-8")
    write_json(directory / "split_manifest.json", bundle["manifest"])
    summary = {"module": 6, "dataset": "UCI red wine quality", "rows": bundle["manifest"]["raw_rows"],
               "chosen_model": chosen["model"], "threshold": chosen["threshold"],
               "selection_metric": "validation balanced accuracy", "test": test_scores[0],
               "split_group_overlap": False, "label": "human score >=7"}
    return publish_report(directory, "Module 6: classification and decision trees", summary,
                          {"validation_scores": bundle["validation_scores"], "test_scores": pd.DataFrame(test_scores),
                           "test_predictions": predictions,
                           "tree_importance": pd.DataFrame({"feature": features, "importance": tree.feature_importances_})},
                          ["Chemistry-identical rows stay in one split. No physical sample IDs exist; independence cannot be guaranteed.",
                           "Quality >=7 is a declared classroom label, not a safety/quality certification. Thresholds are selected on validation only.",
                           "Confusion counts, denominators, and rates are explicit. Feature importance and tree rules describe this fit, not causal effects."])


def run_clustering(output):
    directory = new_run(output)
    split, features, manifest = wine_splits()
    scaler = StandardScaler().fit(split["train"][features])
    training = scaler.transform(split["train"][features])
    validation = scaler.transform(split["validation"][features])
    choices, models = [], {}
    for clusters in [2, 3, 4]:
        model = KMeans(n_clusters=clusters, n_init=10, random_state=42).fit(training)
        labels = model.predict(validation)
        score = float(silhouette_score(validation, labels)) if 1 < len(np.unique(labels)) < len(labels) else -1.0
        choices.append({"clusters": clusters, "validation_silhouette": score})
        models[clusters] = model
    choices.sort(key=lambda row: (-row["validation_silhouette"], row["clusters"]))
    k = choices[0]["clusters"]
    model = models[k]
    test = split["test"].copy()
    labels = model.predict(scaler.transform(test[features]))
    # Quality is deliberately absent from fitting and k selection.
    profiles = test[features].copy()
    profiles["cluster"] = labels
    profile = profiles.groupby("cluster", as_index=False).mean()
    counts = profiles.groupby("cluster").size().rename("observations").reset_index()
    assignments = pd.DataFrame({"record_id": test.record_id, "cluster": labels})
    write_json(directory / "split_manifest.json", manifest)
    summary = {"module": 7, "dataset": "UCI red wine chemistry", "selected_k": k,
               "selection": "validation silhouette after training-fitted scaling",
               "test_observations": len(test), "inertia_train": float(model.inertia_),
               "quality_used_for_fit_or_selection": False}
    return publish_report(directory, "Module 7: clustering and learning paradigms", summary,
                          {"k_comparison": pd.DataFrame(choices), "cluster_profiles": profile,
                           "cluster_counts": counts, "test_assignments": assignments},
                          ["Cluster numbers are arbitrary IDs, not ranks or taste classes. Different scales, seeds, and shapes can change the partition.",
                           "Silhouette is an internal geometry criterion, not ground-truth accuracy or an operational benefit measure.",
                           "This static observational dataset supports supervised/unsupervised comparison. It has no action/reward interaction needed to validate a reinforcement-learning policy."])


ADULT_COLUMNS = ["age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"]


def adult_parts():
    folder = fetch_source("adult")
    training = pd.read_csv(folder / "adult.data", names=ADULT_COLUMNS, skipinitialspace=True)
    test = pd.read_csv(folder / "adult.test", names=ADULT_COLUMNS, skipinitialspace=True, comment="|")
    for frame in [training, test]:
        frame.dropna(how="all", inplace=True)
        for column in frame.select_dtypes("object"):
            frame[column] = frame[column].str.strip()
        frame["income"] = frame["income"].str.rstrip(".")
    # Remove exact full-record repetitions across the provided files, without
    # claiming that every distinct row represents a distinct identifiable person.
    signatures = lambda part: pd.util.hash_pandas_object(part[ADULT_COLUMNS].astype(str), index=False).astype(str)
    training = training.drop_duplicates().copy()
    train_keys = set(signatures(training))
    test = test.loc[~signatures(test).isin(train_keys)].drop_duplicates().copy()
    from sklearn.model_selection import train_test_split
    fit, validation = train_test_split(training, test_size=.2, stratify=training.income, random_state=42)
    return fit, validation, test


def run_fairness(output):
    directory = new_run(output)
    train, validation, test = adult_parts()
    features = ["age", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
    target = lambda part: (part.income == ">50K").astype(int)
    model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    model.fit(train[features], target(train))
    comparison = []
    for threshold in [.3, .5, .7]:
        prediction = model.predict_proba(validation[features])[:, 1] >= threshold
        comparison.append({"threshold": threshold, **binary_metrics(target(validation), prediction)})
    comparison.sort(key=lambda row: (-row["balanced_accuracy"], row["threshold"]))
    threshold = comparison[0]["threshold"]
    probability = model.predict_proba(test[features])[:, 1]
    predicted = probability >= threshold
    metrics = []
    for attribute in ["sex", "race"]:
        for value in sorted(test[attribute].unique()):
            mask = test[attribute].eq(value).to_numpy()
            row = binary_metrics(target(test).to_numpy()[mask], predicted[mask])
            metrics.append({"attribute": attribute, "recorded_group": value, **row})
    table = pd.DataFrame(metrics)
    summary = {"module": 13, "dataset": "UCI Adult historic census extract", "train_rows": len(train),
               "validation_rows": len(validation), "test_rows": len(test), "selected_threshold": threshold,
               "features": features, "protected_attributes_used_for_fitting": False,
               "overall": binary_metrics(target(test), predicted),
               "interpretation": "Descriptive audit of a historical income-label task, not a decision rule for people."}
    write_json(directory / "protocol.json", {"features": features, "threshold_selection": "validation balanced accuracy", "provided_split": "adult.data development; adult.test evaluation after exact full-row overlap removal", "same_person_independence": "not established", "missingness": "Numeric selected fields imputed on training only; unused categorical '?' values are not recoded into numerical values."})
    return publish_report(directory, "Module 13: ethics and fairness across the lifecycle", summary,
                          {"validation_thresholds": pd.DataFrame(comparison), "group_audit": table},
                          ["Historical income is not a measure of merit, need, or a justified allocation outcome. Do not deploy this model for eligibility or targeting.",
                           "The source records limited sex/race categories. They do not capture identity, intersectional experience, or all affected groups. Differences are descriptive, not causal findings.",
                           "Excluding protected columns does not remove proxy effects or label bias. A metric does not establish fairness or legal compliance.",
                           "Rates include group counts and confusion denominators; undefined rates remain unavailable. Small groups and uncertainty require investigation before comparison."])
