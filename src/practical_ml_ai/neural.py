"""Actual TensorFlow training on real tabular/text data (Modules 8–9).

A small explicit loop makes fitting, validation-only checkpoint selection, and
final prediction visible. It avoids implicit dataset/thread behavior and does
not claim that a small neural model must beat the simpler baseline.
"""
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .continuation_data import binary_metrics, new_run, publish_report, sms_splits, wine_splits, write_json


def tensorflow_runtime():
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    import tensorflow as tf
    try:
        tf.config.threading.set_inter_op_parallelism_threads(2)
        tf.config.threading.set_intra_op_parallelism_threads(2)
    except RuntimeError:
        pass  # A notebook may already have initialized the same TF runtime.
    tf.keras.utils.set_random_seed(42)
    return tf


def train_network(model, inputs, labels, validation, validation_labels, epochs, patience=5):
    """Only validation loss selects a checkpoint. Final labels are not arguments."""
    tf = tensorflow_runtime()
    loss_function = tf.keras.losses.BinaryCrossentropy()
    optimizer = tf.keras.optimizers.Adam(learning_rate=.005)
    initial = [value.copy() for value in model.get_weights()]
    history, best_loss, best_weights, best_epoch = [], float("inf"), None, None
    rng = np.random.default_rng(42)
    for epoch in range(epochs):
        order = rng.permutation(len(labels))
        weighted_loss = 0.0
        for start in range(0, len(order), 32):
            ids = order[start:start + 32]
            x = tf.gather(inputs, ids)
            y = tf.convert_to_tensor(labels[ids].reshape(-1, 1), dtype=tf.float32)
            with tf.GradientTape() as tape:
                probability = model(x, training=True)
                loss = loss_function(y, probability)
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))
            weighted_loss += float(loss) * len(ids)
        val_probability = model(validation, training=False)
        val_loss = float(loss_function(validation_labels.reshape(-1, 1), val_probability))
        if not np.isfinite(val_loss) or not np.isfinite(weighted_loss):
            raise ValueError("Nonfinite training loss; inspect empty-token inputs before comparing models.")
        history.append({"epoch": epoch + 1, "training_loss": weighted_loss / len(labels), "validation_loss": val_loss})
        if val_loss < best_loss:
            best_loss, best_epoch = val_loss, epoch + 1
            best_weights = [value.copy() for value in model.get_weights()]
        if epoch + 1 - best_epoch >= patience:
            break
    model.set_weights(best_weights)
    change = float(np.sqrt(sum(float(np.square(a - b).sum()) for a, b in zip(initial, model.get_weights()))))
    return pd.DataFrame(history), best_epoch, change


def select_threshold(actual, probability):
    """Validation-only balanced accuracy; smallest threshold breaks exact ties."""
    rows = [{"threshold": round(float(t), 2), **binary_metrics(actual, probability >= round(float(t), 2))}
            for t in np.linspace(.05, .95, 19)]
    rows.sort(key=lambda row: (-row["balanced_accuracy"], row["threshold"]))
    return rows[0]["threshold"], pd.DataFrame(rows)


def run_neural(number, output, epochs=None, sample_limit=None):
    epochs = epochs if epochs is not None else (40 if number == 8 else 25)
    if isinstance(epochs, bool) or not isinstance(epochs, int) or not 1 <= epochs <= 50:
        raise ValueError("Choose 1–50 epochs before final evaluation.")
    directory = new_run(output)
    tf = tensorflow_runtime()
    if number == 8:
        split, features, manifest = wine_splits()
        scaler = StandardScaler().fit(split["train"][features])
        x = {name: tf.constant(scaler.transform(part[features]).astype("float32")) for name, part in split.items()}
        model = tf.keras.Sequential([tf.keras.layers.Input(shape=(len(features),)),
                                     tf.keras.layers.Dense(16, activation="relu"),
                                     tf.keras.layers.Dense(1, activation="sigmoid")])
        baseline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
        baseline.fit(split["train"][features], split["train"].label)
        baseline_validation = baseline.predict_proba(split["validation"][features])[:, 1]
        baseline_probability = baseline.predict_proba(split["test"][features])[:, 1]
        identifiers = split["test"].record_id
        preprocessing = {"features": features, "training_mean": scaler.mean_.tolist(), "training_scale": scaler.scale_.tolist()}
        write_json(directory / "numeric_preprocessing.json", preprocessing)
        vocabulary = None
    elif number == 9:
        split, manifest = sms_splits(limit=sample_limit)
        # Adapt exclusively on training text. Validation/test never build vocabulary.
        # Preserve punctuation: an emoticon-only real SMS must not become an
        # all-padding sequence (masked mean pooling would have denominator zero).
        vectorizer = tf.keras.layers.TextVectorization(max_tokens=6000, output_sequence_length=96, standardize="lower")
        data = tf.data.Dataset.from_tensor_slices(split["train"].text.tolist()).batch(32)
        options = tf.data.Options(); options.threading.private_threadpool_size = 1
        vectorizer.adapt(data.with_options(options))
        x = {name: tf.constant(part.text.tolist()) for name, part in split.items()}
        model = tf.keras.Sequential([tf.keras.layers.Input(shape=(), dtype=tf.string), vectorizer,
                                     tf.keras.layers.Embedding(len(vectorizer.get_vocabulary()), 16, mask_zero=True),
                                     tf.keras.layers.GlobalAveragePooling1D(),
                                     tf.keras.layers.Dense(1, activation="sigmoid")])
        baseline = make_pipeline(TfidfVectorizer(min_df=2, ngram_range=(1, 2)), LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
        baseline.fit(split["train"].text, split["train"].label)
        baseline_validation = baseline.predict_proba(split["validation"].text)[:, 1]
        baseline_probability = baseline.predict_proba(split["test"].text)[:, 1]
        identifiers = split["test"].text_id
        vocabulary = vectorizer.get_vocabulary()
        write_json(directory / "vocabulary.json", vocabulary)
    else:
        raise ValueError("Neural module must be 8 or 9.")
    y = {name: part.label.to_numpy(dtype="float32") for name, part in split.items()}
    history, best_epoch, change = train_network(model, x["train"], y["train"], x["validation"], y["validation"], epochs)
    validation_probability = model(x["validation"], training=False).numpy().ravel()
    threshold, neural_thresholds = select_threshold(y["validation"], validation_probability)
    baseline_threshold, baseline_thresholds = select_threshold(y["validation"], baseline_validation)
    # All model/checkpoint/threshold decisions are frozen before final prediction.
    probability = model(x["test"], training=False).numpy().ravel()
    prediction = (probability >= threshold).astype(int)
    metrics = binary_metrics(y["test"], prediction)
    baseline_metrics = binary_metrics(y["test"], baseline_probability >= baseline_threshold)
    for result, scores in [(metrics, probability), (baseline_metrics, baseline_probability)]:
        result.update(roc_auc=float(roc_auc_score(y["test"], scores)), pr_auc_average_precision=float(average_precision_score(y["test"], scores)))
    # Round-trip actual trained weights/architecture, including text vocabulary.
    model_path = directory / "model.keras"
    model.save(model_path)
    restored = tf.keras.models.load_model(model_path, safe_mode=True, compile=False)
    replay = restored(x["test"][:8], training=False).numpy().ravel()
    np.testing.assert_allclose(replay, probability[:8], atol=1e-6, rtol=1e-5)
    write_json(directory / "split_manifest.json", manifest)
    summary = {"module": number, "framework": "TensorFlow " + tf.__version__, "dataset": manifest["source"],
               "epochs_requested": epochs, "best_validation_epoch": best_epoch, "weight_change_norm": change,
               "threshold": threshold, "baseline_threshold": baseline_threshold,
               "selection": "validation loss checkpoint; validation balanced accuracy threshold; patience 5",
               "sample_rows": sum(len(part) for part in split.values()),
               "test": metrics, "linear_baseline": baseline_metrics,
               "saved_model_replay_verified": True, "vocabulary_fitted_on": "training only" if number == 9 else None}
    tables = {"learning_history": history,
              "validation_thresholds": pd.concat([neural_thresholds.assign(method="neural"), baseline_thresholds.assign(method="linear_baseline")], ignore_index=True),
              "validation_predictions": pd.DataFrame({"actual": y["validation"], "neural_probability": validation_probability, "baseline_probability": baseline_validation}),
              "comparison": pd.DataFrame([{"method": "neural", **metrics}, {"method": "linear_baseline", **baseline_metrics}]),
              "test_predictions": pd.DataFrame({"record_id": identifiers, "actual": y["test"], "probability": probability, "predicted": prediction})}
    if vocabulary:
        tables["vocabulary_preview"] = pd.DataFrame({"token_index": range(min(30, len(vocabulary))), "token": vocabulary[:30]})
    return publish_report(directory, f"Module {number}: " + ("neural networks with TensorFlow" if number == 8 else "neural NLP for real messages"), summary, tables,
                          ["Checkpoint selection uses validation loss with patience 5; each method selects its own threshold by validation balanced accuracy. Final labels never select weights or thresholds.",
                           "The learning-history table is the numerical alternative to a curve: compare training/validation loss and identify divergence without relying on a plotted line.",
                           "A small network may underperform the simpler baseline. These finite historical samples and small epoch budgets do not establish production readiness.",
                           "For NLP, text IDs replace raw messages in reports. Public messages can still contain personal content; processing is local."])
