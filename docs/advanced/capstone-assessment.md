# Using the exemplar for independent capstone work

The [complete worked project](../../projects/phishing-triage/README.md) illustrates
the standard of evidence, not a mandatory topic or a submission to copy. Keep
official assessment formats, model-count rules, deadlines, accommodations and
individual/team contribution requirements with the adopting instructor.

| Student deliverable | Worked-example evidence | Independent explanation to require |
| --- | --- | --- |
| Proposal | Report questions, stakeholder and error-cost policy | Why this task and why a model rather than a nonautomated response? |
| Literature/source review | Dataset context and primary method references | Which claims are supported, and which experiment is not being replicated? |
| Data dictionary and preparation | Source encodings, profile counts, missingness and boundaries | When is each input available, and what leakage remains possible? |
| Modeling/search | Full candidate/fold results and bounded configuration | Why these candidates, metric, budget and tie-break? |
| Reproducibility/stability | Fixed protocol, all training seeds and separate split study | Which randomness changes, and what cannot be inferred from its spread? |
| Evaluation | Locked family/threshold/ensemble, baseline, raw errors and uncertainty | Which decision is justified by the evidence, including adverse results? |
| Delivery | Numeric bundle, schema checks, monitoring and rollback decision | What does local inference establish, and what is missing before live use? |
| Communication | Annotated completed report and artifact registry | Can the learner defend a changed decision and reproduce the result? |

## Suggested adoption

Use the example first as a critique exercise: ask learners to identify a source
limitation, explain one error-cost choice and reject one unsupported claim.
Then assign a changed task or permitted dataset/protocol and require actual
code/configuration differences, evidence and an oral or written explanation.

Beginners can follow the core route before selecting an extension. Experienced
learners can investigate tuning, seed stability, split sensitivity or calibration.
Do not require optional depth to pass unless the published course assessment
explicitly adopts it. Pilot workload and access with the actual learners.

An independent study should distinguish a reproduction from a new empirical
claim. Reusing this public benchmark and its known results is a reproduction or
development exercise, even when the student supplies a fresh run identifier.
Teamwork evidence, where required, must be assessed separately from technical
execution by one person.
