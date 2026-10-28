# Module 8: practice solutions and diagnostic feedback

Attempt the [practice](practice.md), then open the [worked solution notebook](https://ntious.github.io/ml_ai_it/downloads/module08/solutions.ipynb "site-download:module08/solutions.ipynb"). These solutions expose the mechanism; they do not replace an independently explained change or the complete module's baseline comparison. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

## Dense layer: preserve observations as rows

Use matrix multiplication `x @ weights`, add one bias per hidden unit, then apply `np.maximum(0, ...)`. The result has shape batch-by-hidden. Multiplying elements without summing over the input dimension or summing the whole batch gives a different operation. ReLU retains positive values and replaces negatives with zero; sigmoid is a different activation.

For the supplied two-row/two-unit example, both hidden activations are zero. The changed one-row example produces `[2,1]`; returning an all-zero array cannot pass both. Explain one element by hand and account for the dimensions before relying on the check.

## Checkpoint: validation chooses, training updates

The authored validation losses `[.69,.51,.48,.55]` select epoch 3. Training loss continues downward to epoch 4, so selecting its minimum would answer the wrong question. The earliest epoch wins a tied validation minimum. Use one-based epoch numbers in the returned answer.

The sandbox stores weights at each epoch, calls the learner's selection function, and restores those weights before saving. Choosing an epoch number without restoring its parameters would leave the last model in memory. The complete study adds its own patience rule, full declared budget and final evaluation.

## Network: distinguish width, batch size and parameters

For eleven inputs and sixteen hidden units, parameters are `11*16 +16 +16 +1 =209`. For three inputs and four hidden units they are `3*4 +4 +4 +1 =21`. A flexible batch dimension does not create parameters. The model must have one ReLU hidden layer and one sigmoid output under this exercise contract.

The bounded Wine Quality sandbox fits a scaler on the training slice, trains eight epochs on at most 256 training observations and evaluates validation loss on at most 64 validation observations. Its development plot may or may not show rising validation loss. Report the observed pattern rather than copying the authored illustration.

## Replay is a different claim from performance

Reloaded probabilities matching the saved model support serialization correctness for those inputs. They do not establish useful recall, fairness or generalization. The complete reference separately compares the network with logistic regression, using validation-selected thresholds and held-out confusion counts.

| Problem | Likely cause to investigate | Recovery |
| --- | --- | --- |
| Parameter count changes with batch size | Batch dimension confused with features | Write input-by-hidden and hidden-by-output dimensions |
| Lowest training loss chosen | Selection evidence confused with gradient objective | Compare validation losses and restore that epoch's weights |
| Model saves but predictions differ after reload | Wrong checkpoint, different preprocessing or inference mode | Reuse transformed inputs and compare probabilities numerically |
| Extra width gives no better validation result | More capacity is not automatically useful | Report actual evidence; keep final evaluation out of the choice |

## Compare the quality of explanations

**Developing:** “The network trained and the file saved, so it is accurate.” No independent performance claim follows from those facts.

**Meets:** “The batch shape is [shape], there are [count] parameters, and only training labels drive gradient updates. Validation selected epoch [number]. I restored it and verified saved-model replay. In the complete reference, [neural/baseline error counts] imply [specific tradeoff].” Include actual values and changed code.

**Extends:** Declare a width or learning-rate comparison on development data before running it, preserve the selection rule and explain measured compute/error tradeoffs. Mathematical derivations are optional; accountable applied reasoning remains required.

Return to [practice](practice.md), then the [complete reference study](index.md) and [recorded feedback](feedback.md).
