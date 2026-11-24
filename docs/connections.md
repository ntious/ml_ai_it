# How the course topics work together

A useful ML or AI system is a chain of decisions and evidence. Its inputs become a representation; a method turns that representation into an output; evaluation tells us what the output supports; people decide how it may be used. The algorithm is one part of that chain.

Use this page when a new topic feels disconnected. You can read the map without installing anything. Keep the existing module practice as your implementation route; this connection activity is ungraded unless an adopting instructor states otherwise.

## Follow one lifecycle

<ol class="pipeline-stages" aria-label="Shared machine learning lifecycle">
<li><strong>Frame</strong><span>Question, people affected, inputs, target, and error costs.</span></li>
<li><strong>Prepare and partition</strong><span>Source, rights, data meaning, and independent training, validation, and final evaluation.</span></li>
<li><strong>Learn</strong><span>Fit preprocessing and a baseline on training data; compare justified candidates on development evidence.</span></li>
<li><strong>Evaluate</strong><span>Freeze the choice, inspect final errors, and explain uncertainty.</span></li>
<li><strong>Explain and communicate</strong><span>Trace outputs to sources, useful descriptions, and a bounded claim.</span></li>
<li><strong>Serve and monitor when justified</strong><span>Validate new inputs, record outcomes, assign ownership, and prepare a fallback.</span></li>
</ol>

The list is the diagram's complete text equivalent. Responsibility, provenance, and communication apply throughout; they are not tasks postponed until the last box. An experiment may end with a justified decision not to deploy.

## Choose a connected example

- **Read one research pipeline:** follow the [3-Tier-LSTM case](cases/three-tier-lstm/index.md). Revisit small sections as the course advances. The main integration checkpoint is after Module 8. The reading route requires no dataset or model installation.
- **Run an IT study:** use the [phishing case](cases/phishing.md), or the [complete phishing-triage project](../projects/phishing-triage/README.md) after the core foundations. They supply the runnable preparation, comparison, evaluation, inference, and monitoring evidence.
- **Interpret genuine network records:** use the [network-record bridge](cases/network-record-interpretation.md). Tumor measurements and encoded website attributes do not establish network-flow interpretation.

These examples share engineering questions, not one universal dataset or model. Do not add an LSTM, LLM, or agent solely to include every course topic in one program.

## Connect all 14 modules

### Module 1 Frame the decision

Identify the observation, input, target, output, and error costs.

[Module 1 lesson](lessons/01-foundations/index.md) · [Research connection](cases/three-tier-lstm/01-study.md)

### Module 2 Make the workflow readable

Use functions, files, configuration, and a controller to connect stages.

[Module 2 lesson](lessons/02-python-workflows/index.md) · [Research connection](cases/three-tier-lstm/02-structure.md)

### Module 3 Preserve data meaning

Separate the table, target, feature names, and array shapes.

[Module 3 lesson](lessons/03-data-processing/index.md) · [Research connection](cases/three-tier-lstm/03-data.md)

### Module 4 Communicate the evidence

Choose a figure or table for a question and verify its labels.

[Module 4 lesson](lessons/04-exploration/index.md) · [Research connection](cases/three-tier-lstm/04-figures.md)

### Module 5 Protect the experiment

Split before fitting learned transformations; define validation before resampling.

[Module 5 lesson](lessons/05-regression/index.md) · [Research connection](cases/three-tier-lstm/05-integrity.md)

### Module 6 Compare decisions and errors

Distinguish feature selection from prediction; check a confusion matrix.

[Module 6 lesson](lessons/06-classification/index.md) · [Research connection](cases/three-tier-lstm/06-classification.md)

### Module 7 Choose the learning paradigm

Compare supervised classification with clustering and reinforcement learning.

[Module 7 lesson](lessons/07-clustering/index.md) · [Research connection](cases/three-tier-lstm/07-paradigms.md)

### Module 8 Trace the complete study

Follow shapes through Dense, one-step LSTM, prediction, evaluation, and explanation.

[Module 8 lesson](lessons/08-neural-networks/index.md) · [Research connection](cases/three-tier-lstm/08-integration.md)

### Module 9 Change the input representation

Move from numeric measurements to text tokens; the tumor case itself is not NLP.

[Module 9 lesson](lessons/09-neural-nlp/index.md) · [Choose and justify an extension](cases/three-tier-lstm/extensions.md)

### Module 10 Add a generative component only for a defined task

Evaluate a language model separately; do not treat generated text as measured model evidence.

[Module 10 lesson](lessons/10-llm-workflows/index.md) · [Choose and justify an extension](cases/three-tier-lstm/extensions.md)

### Module 11 Decide whether adaptation is justified

Fine-tune a language model only with a separate justified objective, dataset, and evaluation.

[Module 11 lesson](lessons/11-fine-tuning/index.md) · [Choose and justify an extension](cases/three-tier-lstm/extensions.md)

### Module 12 Separate training from serving

Identify the missing inference bundle, checked inputs, and monitoring contract.

[Module 12 lesson](lessons/12-deployment/index.md) · [Research connection](cases/three-tier-lstm/12-deployment.md)

### Module 13 Question whether to use the result

Connect errors, explanations, provenance, fairness limits, and human responsibility.

[Module 13 lesson](lessons/13-ethics-fairness/index.md) · [Research connection](cases/three-tier-lstm/13-responsibility.md)

### Module 14 Bound an automated assistant

Distinguish a fixed pipeline controller from an LLM that selects allowed tools.

[Module 14 lesson](lessons/14-agents/index.md) · [Choose and justify an extension](cases/three-tier-lstm/extensions.md)

## Watch the handoffs rather than memorizing the files

| Handoff | What must remain connected | What can go wrong |
| --- | --- | --- |
| Table to features | Observation IDs, target meaning, column names, units, and exclusions | A dropped identifier or target accidentally becomes a model input |
| Features to model | Training-fitted transformations, feature order, shape, and split identity | A model sees validation/test information during preparation |
| Model to evaluation | Score meaning, positive label, decision threshold, and actual labels | A probability, hard label, and generated explanation are treated as the same output |
| Evaluation to communication | Counts, denominators, source/run identity, uncertainty, and limitations | A high score becomes a claim about another population |
| Training to inference | Frozen model, preprocessing, schema, version, and rejected-input behavior | New inputs are transformed differently from training inputs |
| Inference to monitoring | Input/output contracts, observed outcomes, review owner, and recovery | A local demonstration is described as a measured production improvement |

## Make one connection yourself

Choose two adjacent modules. Write: “Module ___ produces ___; Module ___ needs it because ___. If that handoff is wrong, ___ could happen. I would check ___.” Name a real file, result, or function in the example you used. For example, a training-fitted scaler and feature order must travel with a model so inference transforms the same measurements consistently.

Use the [public synthesis feedback](cases/three-tier-lstm/feedback.md) after attempting the question, then complete the [project transfer](cases/three-tier-lstm/transfer.md). For the exact status of course-outcome evidence, use the [outcome map](outcome-map.md); identifying a relationship is not proof of implementation mastery.
