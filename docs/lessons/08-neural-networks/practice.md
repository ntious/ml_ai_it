# Module 8: independent implementation practice

Use [concepts](concepts.md) and [guided construction](guided.md) first. Work in the existing module environment. These tasks support the same outcomes as the complete reference; your instructor's assessment requirements remain authoritative.

## Start with the clean practice notebook

- [Practice notebook](https://ntious.github.io/ml_ai_it/downloads/module08/practice.ipynb "site-download:module08/practice.ipynb") — complete three function bodies and record predictions.
- In a source checkout: `notebooks/practice/module08-practice.ipynb`.
- The notebook must stay inside the complete source tree and use its installed package/kernel. It does not install dependencies for you.

Run Setup, then define a function and run its check. `not_attempted` means the placeholder remains; `needs_revision` supplies feedback; `passed` covers the visible cases. Repeating a check replaces its earlier state. When all three pass, run the supplied real-development sandbox. Partial work deliberately skips that sandbox rather than pretending it ran.

## Implement, check and explain

### Task 1: Dense ReLU layer

Implement `dense_relu(x, weights, bias)` preserving batch-by-hidden shape. Reconcile one activation by hand.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 1</summary><p>A batch multiplies the input-by-hidden weight matrix; add the hidden bias vector and replace negative activations with zero.</p></details>

### Task 2: Validation checkpoint

Implement `select_checkpoint(train_loss, validation_loss)`. Return a one-based minimum-validation-loss epoch; ties retain the earliest.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 2</summary><p>The training curve helps interpretation, but its minimum must not choose the checkpoint.</p></details>

### Task 3: Configurable network

Implement `build_network(inputs, width)` with one ReLU hidden layer and one sigmoid output. Predict the parameter count for two widths.

Before checking, write an expected output and explain one likely mistake. After checking, try a changed case and record what the feedback helped you diagnose.

<details><summary>Hint if stuck on task 3</summary><p>Count input-hidden weights, hidden biases, hidden-output weights and output bias; batch size is not a learned dimension.</p></details>

## Transfer with less support

In a separate development run, change width from 8 to 4 or 16 and predict the parameter count before training. Keep the data slice, eight-epoch budget and checkpoint rule fixed. Report observed validation loss and compute; a width increase is not guaranteed to help. Use a fresh notebook/kernel or reset all model/optimizer/checkpoint state.

For a hypothetical IT alert queue, describe which false-alarm workload evidence would be needed before preferring a high-recall network. Do not treat the chemistry target as an incident label. Complete the original Module 8 study to compare the actual network with logistic regression on the declared final evaluation.

## Evidence for the unchanged outcomes

| Outcome | Evidence to retain |
| --- | --- |
| M08.1 | Explained activation, probability/loss update and batch/parameter calculations |
| M08.2 | Constructed TensorFlow model and training-only preprocessing in the development scaffold |
| M08.3 | Selected validation epoch and restoration of its actual saved weights |
| M08.4 | Complete-reference neural/logistic confusion comparison with a justified tradeoff |
| M08.5 | Saved/reloaded probabilities, bounded compute record and limitations |

Keep your changed code, one hand-checked numerical claim, expected versus observed output, one diagnosed failure and a short decision memo. Record source/environment/command evidence when using real data. Interpretive reading alone does not replace an implementation outcome.

## Get feedback, then revisit

Open [practice solutions](solutions.md) after your first attempt. Compare the reasoning and a changed case, not only the final number. Return to your original notebook and reproduce the central operation without copying. Use [recorded-study feedback](feedback.md) after the complete reference run.

If using GenAI, keep a short disclosure of the help used and what you verified. Be able to explain and change the code independently; an equivalent no-assistant route uses the same hints and feedback. Never upload student records or credentials.
