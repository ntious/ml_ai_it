# Teach and adapt Module 12

Link the [entry page](index.md) as additional reading/practice. Its reading-site route is /lessons/12-deployment/ relative to the served site base. For a repository link, select a tested commit or release.

## Facilitation and access

Use the same outcomes and written evidence for in-person/asynchronous learners. Begin with the foundation bridge, predict-before-run questions, and the shared script/notebook. Discussion has a solo equivalent. Optional depth is skippable, and GenAI is not required.

Interpretation can use named values and exact tables; code/artefacts demonstrate execution or authoring when those are assessed. A screenshot cannot substitute for an explanation, and a script does not prove notebook-interface operation. Verify the learner's actual assistive-technology route and provide private help.

## Adaptation decisions

Before real IT deployment, add suitable access controls, data governance, observability, failure recovery, and prospectively measured service objectives.

When changing a dataset, define its license/provenance, observation unit, target if any, availability, split, and limits first. Update preprocessing, inference contracts, examples, feedback, and tests together. Preserve the original source and disclose transformations. Do not label a tiny mechanics check as a credible production evaluation.

## Outcome/evidence alignment

- **M12.1:** Define an input/output contract and reject invalid requests.
- **M12.2:** Serve the same trained classifier and a bounded local LLM workflow through Streamlit.
- **M12.3:** Replay actual held-out records and measure prediction duration/outcomes.
- **M12.4:** Distinguish batch diagnostics from genuine time drift and production service guarantees.
- **M12.5:** Propose ownership, escalation, monitoring, and rollback criteria.

Course alignment opportunities: **CLO2, CLO5, CLO6, CLO8**. Advisory computing-outcome opportunities from the planning register: **A1, A2, A3, A4**. These are opportunities for evidence, not proof of master's-level attainment or accreditation compliance. The original-module crosswalk remains in the previously prepared planning resources. Confirm adopted program criteria before formal use.

## Verification limits

Actual framework training/inference, the public script, and notebook are exercised in the Linux CPU job. Windows/macOS framework execution is not inferred from that run. Exact counts/results are recorded in DEVELOPMENT.md and commit-specific CI. Consult the [accessibility evidence log](../../accessibility/review-log.md) for human interface-review coverage. Public feedback is for self-study; local grading/AI-use rules remain the adopting instructor's responsibility.
