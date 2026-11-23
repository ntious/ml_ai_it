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

## Checkpoints and revision

| Checkpoint | Bring for review | Feedback and required response |
| --- | --- | --- |
| Proposal | Stakeholder, decision time, target, non-ML alternative and permitted source | If the target is unavailable or inappropriate, revise the question before collecting more data. |
| Data audit | Dictionary, missingness, entity/time boundaries and label delay | Trace one record into a feature; remove unavailable fields and rerun preparation. |
| Protocol | Baselines, candidate budget, validation rule, seeds and final holdout | Resolve leakage or selection ambiguity before training the full study. |
| Development | All candidate results, adverse cases and compute cost | Explain one failed hypothesis; revise using development evidence only. |
| Draft report | Locked evaluation, uncertainty, limitations and delivery policy | Have a reviewer trace each main claim to an artifact. Correct unsupported claims rather than tuning on final results. |
| Final defense | Revised report, reproducible commands and revision log | Explain a changed-case decision independently and identify remaining deployment evidence. |

Use [the revision log](../../templates/project-revision.md) at every checkpoint. A solo learner should take a separate review pass against the same criteria and explicitly record self-review. In teams, record each contributor's implementation, review and explanation; running the shared notebook alone does not demonstrate everyone's understanding. Official weights and deadlines remain with the adopting instructor.

## Reproduction and justified-use assessment

Use the [evidence rubric](../instructor/evidence-assessment.md) and [reproduction worksheet](../../templates/evidence-review.md) to require an independently recalculated result, a reconstruction attempt and a bounded use decision. Preserve failed attempts and distinguish calculation audits from independent-environment reproduction.
