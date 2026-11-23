# Module 8 Bring the pieces together

**Integration checkpoint. Target:** trace the data, fitted state, predictions, and evidence through one controller. Allow 15–20 minutes after the neural-network lesson. No training run is required for this reading checkpoint.

**Where you are:** the complete research controller. Full case sequence: Question and data → fixed preparation → split → training-only selection and scaling → optional training-only balancing → model and validation → frozen evaluation → explanation and outputs.

Reading route: no installation, data download, or model execution is required. Open only the named source files. Use selectable code and this page's text/numerical evidence; an upstream image is not required to complete the core question.

## Trace five files in order

Start at [main.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/main.py). Open [src/preprocess.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/preprocess.py) when preparation is called, [src/models/lstm_model.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/models/lstm_model.py) at model construction, [src/evaluate.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/evaluate.py) after predictions, and [src/explain.py](https://github.com/ntious/3-Tier-LSTM/blob/a6ca70ada14ce6b98f8ffccc71164d549c733dbb/src/explain.py) at explanation. You may stop reading a function once you can identify its input, purpose, and output.

## Follow the shapes

Let F be the selected feature count; the configuration requests up to 25. N denotes the number of rows in the relevant partition. These symbols explain the interface, not newly observed dataset counts.

| Stage | Input | Output or state passed forward |
| --- | --- | --- |
| Load and fixed cleanup | A table of source columns | Named feature table X and label y |
| Split and learned preparation | Separate row partitions | Selected feature order plus training-fitted selector/scaler |
| Optional resampling | Training matrix and training labels | Resampled training rows; original test rows retained |
| Reshape | Numeric matrix with shape N by F | Model input with shape N by 1 by F |
| Tier 1 | One timestep containing F measurements | Learned Dense representation |
| Tier 2 | That representation at one timestep | LSTM output vector |
| Tier 3 | Output vector | Dense head with one sigmoid score |
| Evaluate | Scores and actual final labels | Named metrics, threshold decisions, and errors |
| Explain and write | Frozen model, background, selected names, outputs | Attribution files, report text/JSON, and figures |

**One timestep matters.** Reshaping numeric measurements to N by 1 by F does not create a medical history or text sequence. The code alone does not establish a temporal-learning advantage. A simpler model or Dense network is a legitimate comparison; complexity needs evidence.

## Carry the earlier lessons into the trace

Module 2 explains imports and calls. Module 3 explains the table-to-array boundary. Module 4 asks whether each view supports a claim. Module 5 protects fitting/evaluation boundaries. Module 6 distinguishes selection from prediction. Module 8 explains learned layers. Module 13 questions whether the evidence supports any use. Read the [validation-order caveat](05-integrity.md) before interpreting the curves.

## Make a pipeline passport

Write five short entries: source and target; preparation and split; model input/output; evidence and uncertainty; missing information before use. For each, identify the supplying function or file and the next consumer. Do not copy the source code or report a score without its source/run status.

For later text, generative, and agent topics, use the [optional extension bridge](extensions.md). It adds connections, not another required architecture.

## Complete one small explanation

If the hybrid model were replaced with a linear classifier, which three surrounding contracts must remain valid? Which model-specific step would change? Keep one or two sentences in your study notes, or follow your instructor's local completion rule. No separate submission is required by this resource. You can discuss your answer for 3–5 minutes in a live session or write the same explanation independently.

Compare [worked feedback](feedback.md#module-8) after your attempt. Advanced implementation is optional.

[Case overview](index.md) · [Next: Module 13 Scrutinize errors and explanations](13-responsibility.md) · [All-module map](../../connections.md)
