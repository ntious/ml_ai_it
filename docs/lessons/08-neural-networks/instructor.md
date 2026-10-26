# Teach and adapt Module 8

Link the [entry page](index.md) as additional reading/practice. Its reading-site route is /lessons/08-neural-networks/ relative to the served site base. For a repository link, select a tested commit or release.

## Facilitation and access

Use the same outcomes and written evidence for in-person/asynchronous learners. Begin with the foundation bridge, predict-before-run questions, and the shared script/notebook. Discussion has a solo equivalent. Optional depth is skippable, and GenAI is not required.

Interpretation can use named values and exact tables; code/artefacts demonstrate execution or authoring when those are assessed. A screenshot cannot substitute for an explanation, and a script does not prove notebook-interface operation. Verify the learner's actual assistive-technology route and provide private help.

## Adaptation decisions

For IT telemetry, preserve host/time boundaries and final-test discipline before replacing numeric inputs. More layers do not replace data-quality or availability checks.

When changing a dataset, define its license/provenance, observation unit, target if any, availability, split, and limits first. Update preprocessing, inference contracts, examples, feedback, and tests together. Preserve the original source and disclose transformations. Do not label a tiny mechanics check as a credible production evaluation.

## Outcome/evidence alignment

- **M08.1:** Explain input, hidden activation, output probability, loss, and gradient updates.
- **M08.2:** Fit training-only numeric preprocessing and a TensorFlow network.
- **M08.3:** Select a checkpoint using validation loss without fitting to final labels.
- **M08.4:** Compare held-out errors with a logistic baseline.
- **M08.5:** Save/reload a trained model and document compute and limitations.

Course alignment opportunities: **CLO2, CLO4, CLO8**. Advisory computing-outcome opportunities from the planning register: **A1, A2, A3**. These are opportunities for evidence, not proof of master's-level attainment or accreditation compliance. The original-module crosswalk remains in the previously prepared planning resources. Confirm adopted program criteria before formal use.

## Verification limits

Actual framework training/inference, the public script, and notebook are exercised in the Linux CPU job. Windows/macOS framework execution is not inferred from that run. Exact counts/results are in the [verified results table](../../status.md#verified-results) and commit-specific CI. Consult the [accessibility evidence log](../../accessibility/review-log.md) for human interface-review coverage. Public feedback is for self-study; local grading/AI-use rules remain the adopting instructor's responsibility.
