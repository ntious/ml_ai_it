# Teach and adapt Module 11

Link the [entry page](index.md) as additional reading/practice. Its reading-site route is /lessons/11-fine-tuning/ relative to the served site base. For a repository link, select a tested commit or release.

## Facilitation and access

Use the same outcomes and written evidence for in-person/asynchronous learners. Begin with the foundation bridge, predict-before-run questions, and the shared script/notebook. Discussion has a solo equivalent. Optional depth is skippable, and GenAI is not required.

Interpretation can use named values and exact tables; code/artefacts demonstrate execution or authoring when those are assessed. A screenshot cannot substitute for an explanation, and a script does not prove notebook-interface operation. Verify the learner's actual assistive-technology route and provide private help.

## Adaptation decisions

A real organization needs consent/rights, a data-retention policy, versioned adapters, regression evaluation, and rollback. This tiny adaptation is not a production support model.

When changing a dataset, define its license/provenance, observation unit, target if any, availability, split, and limits first. Update preprocessing, inference contracts, examples, feedback, and tests together. Preserve the original source and disclose transformations. Do not label a tiny mechanics check as a credible production evaluation.

## Outcome/evidence alignment

- **M11.1:** Distinguish prompting, inference, supervised fine-tuning, and LoRA.
- **M11.2:** Prepare completion labels with prompt-token loss masking.
- **M11.3:** Update a small adapter on training-only real annotations.
- **M11.4:** Compare predeclared base/adapted held-out completion losses without promising improvement.
- **M11.5:** Save/reload adapter arrays with the exact model revision and disclose limits.

Course alignment opportunities: **CLO4, CLO5, CLO8**. Advisory computing-outcome opportunities from the planning register: **A1, A2, A3, A4**. These are opportunities for evidence, not proof of master's-level attainment or accreditation compliance. The original-module crosswalk remains in the previously prepared planning resources. Confirm adopted program criteria before formal use.

## Verification limits

Actual framework training/inference, the public script, and notebook are exercised in the Linux CPU job. Windows/macOS framework execution is not inferred from that run. Exact counts/results are recorded in DEVELOPMENT.md and commit-specific CI. Consult the [accessibility evidence log](../../accessibility/review-log.md) for human interface-review coverage. Public feedback is for self-study; local grading/AI-use rules remain the adopting instructor's responsibility.
