# Working glossary and notation

| Term | Meaning and small example |
| --- | --- |
| Observation | One unit being studied: a wine sample, message or service-day |
| Feature / X | Information available when making a prediction; X has rows by input columns |
| Target / y | Outcome to predict; one label/value per observation |
| Parameter | A learned number, such as a coefficient or neural weight |
| Hyperparameter | A chosen setting, such as tree depth or epoch budget |
| Training | Fit parameters and learned preprocessing using development examples |
| Validation | Compare choices before freezing the final method |
| Test | Evaluate a frozen choice; viewing it repeatedly does not create fresh evidence |
| Leakage | Information enters learning/selection that would be unavailable in the intended decision |
| Baseline | A simple relevant alternative the proposed method must be compared with |
| Residual | Actual minus predicted; positive means underprediction |
| Probability / calibration | A score in 0–1; calibration asks whether comparable scores match observed frequencies |
| Precision / recall | TP/(TP+FP) versus TP/(TP+FN); denominators answer different questions |
| Batch / epoch | A subset used in one update versus one pass through training examples |
| Loss / metric | Objective used for fitting versus a measure used for evaluation; they may differ |
| Gradient | Directional sensitivity of loss to parameters; an optimizer uses it to update weights |
| Tensor / shape | An array and its dimensions; (32,11) means 32 rows of 11 values |
| Token / embedding | A text unit's identifier versus a learned numeric vector representing it |
| Inference | Apply fixed parameters; it does not require an unknown target |
| Drift | A change needing investigation; input change alone does not establish changed outcome relationships |
| Tool / plan | An implemented operation and a proposed invocation; a legal plan can still misunderstand intent |

Use the module's foundation page for worked arithmetic and guided construction for execution. Units and available information remain part of every definition.

## Terms used in the exercises

| Term | Meaning and example | Continue |
| --- | --- | --- |
| Kernel | The Python process executing notebook cells; restart clears its variables. Course notebooks use **Python (course core)** or **Python (course frameworks)** | [Notebook setup](../QUICKSTART.md#notebook-option) |
| Boolean | True or False, such as `85 > 80` | [Module 1](lessons/01-foundations/index.md) |
| JSON | A text format for structured values, such as `{"label":"spam"}` | [Module 2](lessons/02-python-workflows/index.md) |
| Pipeline | Ordered transformations and a model fitted together on training data | [Module 5](lessons/05-regression/concepts.md) |
| Imputation | Replacing missing inputs using a declared rule, such as a training median | [Module 5](lessons/05-regression/concepts.md) |
| MAE | Mean absolute error: errors −2 and 4 give MAE 3 in target units | [Module 5](lessons/05-regression/concepts.md) |
| Scaler | A fitted transformation of numerical units; learn its statistics on training | [Module 6](lessons/06-classification/concepts.md) |
| Threshold | Cutoff converting a score into a decision; this course uses score ≥ cutoff | [Module 6](lessons/06-classification/concepts.md) |
| Confusion matrix | Counts of TP, FP, FN and TN comparing predictions with actual labels | [Module 6](lessons/06-classification/concepts.md) |
| False positive / FP | A positive prediction for an actual negative; a false alert | [Module 6](lessons/06-classification/concepts.md) |
| False negative / FN | A negative prediction for an actual positive; a missed case | [Module 6](lessons/06-classification/concepts.md) |
| Balanced accuracy | Average of recall and specificity; gives both actual classes equal weight | [Module 6](lessons/06-classification/concepts.md) |
| Silhouette | Compares within-cluster closeness with separation from other clusters | [Module 7](lessons/07-clustering/concepts.md) |
| ReLU | Activation `max(0,x)`; −2 becomes 0, while 3 stays 3 | [Module 8](lessons/08-neural-networks/concepts.md) |
| Sigmoid | Maps a real number into 0–1; zero maps to 0.5 | [Module 8](lessons/08-neural-networks/concepts.md) |
| Prompt | Instructions and context supplied to a language model | [Module 10](lessons/10-llm-workflows/concepts.md) |
| Adapter / LoRA | A small trainable update alongside frozen base weights; LoRA uses low-rank matrices | [Module 11](lessons/11-fine-tuning/concepts.md) |
| Wilson interval | A binomial uncertainty calculation conditional on suitable sampling assumptions; not a correction for biased data | [Module 13](lessons/13-ethics-fairness/concepts.md) |
