# Framework baseline before Phase B

These diagnostics describe the earlier edition 0.7.0 defaults. They are retained for comparison, not presented as the current protocol or fresh evaluation. See the [current status](../../status.md) and current module feedback.


## Module 8


**Evidence.** The [verified run](../../status.md#verified-results) found 7 of 29 higher-rated wines (recall 0.24, balanced accuracy 0.593). Logistic regression on the same rows at the same 0.5 threshold found 9 of 29 (balanced accuracy 0.629). The best validation epoch was 8, the last allowed: validation loss was still falling (0.3111 at epoch 6, 0.3021 at epoch 8).

**Likely causes.**

1. **The threshold, not only the model.** Only about 12% of wines are positive, so most predicted probabilities sit below 0.5. Module 6 chose 0.3 on validation for the same label and reached balanced accuracy 0.757. Comparing a 0.5 network with a 0.3 logistic model would mix up two separate decisions.
2. **The search ended at its boundary.** Validation loss selected epoch 8 from the eight observed checkpoints. Because the best checkpoint is also the final epoch, a larger budget might find a better checkpoint, but this run cannot establish what happens later. Longer training need not produce a visible rise in validation loss.

**A fair diagnostic experiment.** On validation only, list the predicted probabilities for actual positives and choose a threshold with the rule Module 6 uses. Separately, declare a larger epoch budget (for example `--epochs 30`) in a new output directory and find the epoch where validation loss is lowest. Change one factor at a time, and record both results before you look at final-test counts again. The public final results are already known, so treat any rerun as rehearsal.


## Module 9


**Evidence.** The neural model flagged no spam (TP 0, FN 30 among 240 test messages). Validation loss fell at every epoch (0.428, 0.338, 0.286), and the best epoch was 3, the last allowed. The TF-IDF/logistic baseline flagged 6 messages, all correct (precision 1.00, recall 0.20).

**Likely causes.**

1. **Check the scores before blaming the representation.** A constant prediction of 12.5% spam has cross-entropy about 0.377 on a split with that prevalence. The recorded validation loss of 0.286 improves on that reference, but loss alone does not establish ranking quality. Inspect validation score distributions and ROC-AUC or precision–recall performance to test whether a different threshold could help. Zero test recall tells us that none of the 30 actual spam messages crossed 0.5; it does not describe every predicted probability.
2. **Too few updates.** 720 training messages and 3 epochs give about 70 gradient steps. Loss was still falling steeply when training stopped.
3. **The baseline also needs a threshold check.** Perfect precision with low recall describes a conservative decision rule on this sample. Compare validation thresholds before attributing the missed spam to weak lexical features.

**A fair diagnostic experiment.** Using validation messages only, compare the probability distributions for spam and ham, then choose one threshold rule for both methods. As a separate declared experiment, run `--epochs 20` in a new output directory. Report recall and precision with their denominators; accuracy (87.5% for predicting nothing) would hide the failure.


## Module 10


**Evidence.** None of the 8 responses matched the required schema: seven repeated the message back inside its `<sms>` wrapper, and one answered an unrelated grammar question. The TF-IDF/logistic baseline was correct on 5 of the same 8 messages. With only 8 examples, a 95% Wilson interval for 0/8 runs from 0 to 0.32, and for 5/8 from 0.31 to 0.86, so this run cannot rank the methods precisely.

**Likely causes.**

1. **A 135-million-parameter model follows instructions weakly.** It continues the pattern it sees, including the tags, instead of obeying the system message.
2. **Free generation is the hardest way to classify.** The strict parser correctly rejects near misses, so every format slip counts as an error.

**A fair diagnostic experiment.** Keep the strict parser, and separately score the two legal answers. Compute the model's log-likelihood of `{"label":"ham"}` and of `{"label":"spam"}` for each message and choose the higher; Module 14 already uses this method to rank plans. Run it on validation messages first. Report schema validity for free generation and accuracy for scoring as separate results, never as one combined success rate. Use more than 8 messages before comparing methods.


## Module 11


**Evidence.** The adapter has 2,304 trainable parameters and took 8 single-example steps. Validation completion loss moved from 1.9836 to 1.9809, a 0.14% change. Generated accuracy stayed at 0 of 8 for both the base and adapted model, because neither produced the required JSON.

**Likely causes.**

1. **The budget is far too small to change behavior.** Eight steps show only 8 of the 24 training messages, once each, and update one projection in one layer.
2. **Accuracy cannot move until the format does.** The base model fails the schema on every example (as in Module 10), so a tiny loss improvement cannot appear as correct labels.

**A fair diagnostic experiment.** Treat the step budget as the declared variable: run `--steps 48` (the allowed maximum) in a new output directory and compare **validation** completion loss, not final scores. The current script records schema validity only on the final subset in generation_comparison.csv; it does not provide validation schema validity. Adding generation evaluation on validation messages would be a separate extension. Predict what a larger adapter on more layers would change, then explain why completion loss, format compliance and label correctness need separate measurements.


## Module 14


**Evidence.** For "How many real wine observations are in the dataset?", the router chose the alcohol `feature` plan instead of `summary`. That answer is legal but wrong. For "Summarize alcohol measurements." it chose the same plan, correctly this time. The destructive request was refused by the keyword gate before the model ran, so that refusal tests a string match, not the model.

**Likely cause.** The mean log-probabilities in `tool_trace.json` barely change with the request: `feature` scored -3.40 and -3.37, and `summary` scored -4.41 and -4.08. The model prefers the `feature` plan's text regardless of the question, so the router behaves like a fixed choice that happens to be right for one request.

**A fair diagnostic experiment.** Write 10 new requests, each with the tool you expect, including paraphrases of destructive requests that avoid the gate's words ("wipe the table", "remove every row"). Run them, and report routing accuracy with its denominator. Note which requests the keyword gate misses, and explain why an allowlist of permitted actions is stronger than a list of forbidden words.
