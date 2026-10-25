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
