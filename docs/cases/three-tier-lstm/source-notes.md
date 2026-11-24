# Source identity and reading limits

This companion links an external educational research repository. It does not replace its source, alter its implementation, or report a fresh training experiment.

## Reviewed source

- Repository: [ntious/3-Tier-LSTM](https://github.com/ntious/3-Tier-LSTM/tree/a6ca70ada14ce6b98f8ffccc71164d549c733dbb).
- Reviewed commit: `a6ca70ada14ce6b98f8ffccc71164d549c733dbb`, checked November 23, 2026.
- Credit: Isaac Kofi Nti and the upstream project authors; consult its [citation metadata](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/CITATION.cff) and [MIT software license](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/LICENSE) for the exact attribution and terms.
- Upstream software version DOI: [10.5281/zenodo.24046766](https://doi.org/10.5281/zenodo.24046766). The commit link above identifies the source actually inspected; no equivalence between that commit and every published experiment is assumed.
- Scope: source, configuration, tests, and committed report/figure inspection. Upstream training and explanation generation were not rerun. Existing course modules and their environments are unchanged.

## What was verified and what a learner should question

| Source evidence | Consequence for this companion |
| --- | --- |
| [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py) splits the outer test before feature selection, scaling, and SMOTE, then supplies `validation_split` after resampling | Distinguish outer-test protection from independent internal validation. The [integrity page](05-integrity.md) proposes reserving real validation earlier. |
| [src/models/lstm_model.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/models/lstm_model.py) receives shape `(1, input_dim)` | Explain a one-timestep numeric model; do not describe it as patient-history or text-sequence learning. |
| [src/preprocess.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/preprocess.py) returns sorted feature names and the original importance array; the controller slices that array | Name/value alignment needs repair before relying on the feature-importance ranking. We do not copy that ranking as validated evidence. |
| [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py) creates directories but does not serialize model, scaler, feature order, or an inference contract | Describe outputs as reports/figures, not a complete deployable model bundle. |
| [src/explain.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/explain.py) writes SHAP arrays/feature text and LIME HTML into reports; the controller catches failures | Ask which artifacts actually exist. Do not infer explanation success from a completed command or call site. |
| [config.yaml](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/config.yaml) expects `data/data.csv`; no input data file is tracked; README structure also names a different spreadsheet path | No install or reproduction is required for the reading route. A future reproduction needs a permitted source, schema, and reviewed provenance before execution. |
| [requirements.txt](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/requirements.txt) and [environment.yml](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/environment.yml) choose different scikit-learn versions | Keep upstream optional execution separate from the course environments; record the actual tested environment. |
| The controller sets NumPy's seed but not TensorFlow's complete random/determinism state | Do not promise bitwise-repeatable training from the configuration seed alone. |
| [tests/test_research_pipeline.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/tests/test_research_pipeline.py) checks helpers, not a full model training/replay workflow | Passing helper tests is narrower evidence than reproducing the stored research results. |

Unknown labels becoming missing values and the metric helper's accepted score shapes are additional audit topics. They are not certified as fixed by this companion.

## Committed output evidence

The [numeric metrics](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/outputs/reports/metrics_numeric.json) and [classification report](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/outputs/reports/classification_report.txt) describe 114 final records in the stored output. We inspected the source confusion-matrix image: actual-label rows are `[71, 1]` for benign and `[3, 39]` for malignant. The [accessible table](04-figures.md) preserves these values without requiring the image.

These files are not accompanied here by a verified input hash, run manifest, or saved inference bundle tying every output to this exact execution. Treat them as **upstream committed results**, not independently reproduced or clinical-validation evidence. Metrics can be checked arithmetically; their population and provenance cannot be reconstructed from arithmetic alone.

## Reading and access

Use the bounded file links in each connection. No student needs to reproduce a figure or operate a visual-only LIME widget to answer the core questions. If public GitHub is unavailable, the course pages still contain the lifecycle, interface explanations, metric table, caveats, and public feedback. For a code-location task, an instructor can supply a permitted attributed excerpt or arrange another accessible source reader; reading prose alone does not establish code-navigation or execution outcomes.

Primary concept references: [training-only preprocessing](https://scikit-learn.org/stable/common_pitfalls.html), [resampling leakage](https://imbalanced-learn.org/stable/common_pitfalls.html), [Keras fit/validation](https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit), and [LSTM input shape](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM). The upstream pins TensorFlow 2.15.1; current documentation is a concept reference, not evidence that its package set works unchanged in the course's newer environment.

[Case overview](index.md) · [All-module map](../../connections.md) · [Instructor integration](../../instructor/connected-research-case.md)
