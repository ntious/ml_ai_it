"""Transparent candidate construction and numeric-only inference artifacts."""
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


def candidate(family, parameters, seed):
    estimators = {
        "logistic": lambda: LogisticRegression(max_iter=1000, class_weight="balanced", random_state=seed, **parameters),
        "tree": lambda: DecisionTreeClassifier(min_samples_leaf=5, random_state=seed, **parameters),
        "forest": lambda: RandomForestClassifier(random_state=seed, n_jobs=1, **parameters),
    }
    if family == "dummy":
        return DummyClassifier(strategy="prior")
    return make_pipeline(OneHotEncoder(handle_unknown="ignore", sparse_output=False), estimators[family]())


def tree_arrays(model):
    tree = model.tree_
    values = tree.value[:, 0, :]
    return {"left": tree.children_left.tolist(), "right": tree.children_right.tolist(),
            "feature": tree.feature.tolist(), "threshold": tree.threshold.tolist(),
            "positive_probability": (values[:, 1] / values.sum(axis=1)).tolist()}


def export_model(model, family, features, seed):
    if list(model.classes_) != [0, 1]:
        raise ValueError("Both binary classes are required.")
    artifact = {"schema_version": 1, "family": family, "features": features, "training_seed": seed}
    if family == "dummy":
        artifact["constant"] = float(model.class_prior_[1])
        return artifact
    artifact["categories"] = [values.tolist() for values in model[0].categories_]
    fitted = model[-1]
    if family == "logistic":
        artifact.update(coefficient=fitted.coef_[0].tolist(), intercept=float(fitted.intercept_[0]))
    else:
        artifact["trees"] = [tree_arrays(tree) for tree in fitted.estimators_] if family == "forest" else [tree_arrays(fitted)]
    return artifact


def numeric_predict(artifact, frame):
    values = frame[artifact["features"]].to_numpy(dtype=float)
    if artifact["family"] == "dummy":
        return np.full(len(values), artifact["constant"])
    encoded = np.concatenate([(values[:, index, None] == np.array(categories)).astype(float)
                              for index, categories in enumerate(artifact["categories"])], axis=1)
    if artifact["family"] == "logistic":
        logit = encoded @ np.array(artifact["coefficient"]) + artifact["intercept"]
        return 1 / (1 + np.exp(np.clip(-logit, -700, 700)))
    predictions = []
    # sklearn's tree predictor casts features to float32 before traversal.
    encoded = encoded.astype(np.float32)
    for tree in artifact["trees"]:
        left, right = np.array(tree["left"]), np.array(tree["right"])
        feature, threshold = np.array(tree["feature"]), np.array(tree["threshold"])
        nodes = np.zeros(len(values), dtype=int)
        for _ in range(len(left)):
            active = np.flatnonzero(left[nodes] != -1)
            if not len(active):
                break
            current = nodes[active]
            go_left = encoded[active, feature[current]] <= threshold[current]
            nodes[active] = np.where(go_left, left[current], right[current])
        else:
            raise ValueError("Tree traversal did not terminate.")
        predictions.append(np.array(tree["positive_probability"])[nodes])
    return np.mean(predictions, axis=0)
