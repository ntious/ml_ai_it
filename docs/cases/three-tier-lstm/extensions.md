# Connect NLP LLMs fine tuning and agents

**Optional synthesis bridge.** Revisit the relevant section when you reach Modules 9–11 or 14.

The same lifecycle can support different tasks. Connecting topics does not require putting every architecture into the tumor classifier. Keep the question, data, output contract, evaluation, and human responsibility explicit when adding a component.

## Module 9 changes the representation

The LSTM case receives numeric measurements at one timestep. The [NLP module](../../lessons/09-neural-nlp/index.md) receives real messages and learns a vocabulary/representation under text-deduplicated splits. Sharing a layer family does not make the tumor model an NLP system. Carry forward the discipline of training-only representation learning, a simple lexical baseline, and meaningful error counts.

## Module 10 adds a distinct generative task

A language model might help draft an explanation of an already verified evidence table. That is a proposed support component, not a feature implemented in the LSTM case. Keep its claims tied to a source and human review, and assess schema compliance and factual grounding separately from the classifier's accuracy. Do not send patient or student records to an external assistant.

Use the existing [LLM module](../../lessons/10-llm-workflows/index.md) for actual local generation/evaluation. A generated summary is not a newly measured experiment.

## Module 11 asks whether adaptation is worth doing

Fine-tuning changes model parameters for a justified objective. Training the hybrid classifier from its initial weights is not the same as the course's language-model adapter experiment. An LLM support component would need its own permitted supervised examples, disjoint evaluation, baseline prompting comparison, and resource budget before fine-tuning is warranted.

Use [Module 11](../../lessons/11-fine-tuning/index.md) to study the implemented adapter route. No fine-tuned LLM or copied patient-data training set is added by this reading companion.

## Module 14 changes who selects the next action

The research controller follows calls written by a programmer. An LLM agent can select a plan or permitted tool; that introduces intent errors and an executor boundary. They are different forms of orchestration.

A proposed read-only assistant could retrieve a permitted experiment summary and cite it, under an allowlist and call budget, while leaving model fitting and use decisions with the existing workflow and people. It must not execute arbitrary generated commands or make a diagnosis. Use the existing [bounded-agent module](../../lessons/14-agents/index.md) for an actual implementation and its limits.

## Fit the components into one explanation

“Data and modeling create the evidence; a separately evaluated assistant may help people inspect it; a checked application exposes a defined function; monitoring tests whether its assumptions still hold.” Each component needs its own output contract and evidence. The [course-wide handoff map](../../connections.md#watch-the-handoffs-rather-than-memorizing-the-files) shows what must remain connected.

## Try one design decision

Choose **no generative component**, **an evidence-summary component**, or **a bounded retrieval assistant** for your own task. Explain the need, inputs, permitted outputs, evaluation, and reason to reject the alternatives. All three can be defensible. Compare [extension feedback](feedback.md#extensions).

[Case overview](index.md) · [Optional deployment connection](12-deployment.md) · [Responsibility checkpoint](13-responsibility.md) · [Project transfer](transfer.md)
