# Module 5 practice: a reproducible forecasting study

This original companion activity is independently usable and does not replace an official Canvas assignment. Allow 60–90 minutes after the [walkthrough](index.md).

## Core task P05

1. Define stakeholder, target/unit, origin time, horizon, and each feature's availability. Name one feature to exclude and why.
2. Download the real data and retain attribution/provenance. Execute prepare, train, and validate separately. Record source digest, versions, split dates/counts, and validation scores.
3. Before reading final results, record the selected method and selection rule. Explain where imputation was fitted. A baseline winner is valid.
4. Run final evaluation, inference, and the report. Compare the frozen method with the predefined baselines. Verify one residual by hand. Do not replace the selection after seeing final scores.
5. Identify the largest absolute residual and a date-ordered error pattern. If there is no persistent directional pattern, support that interpretation with values. Propose an investigation without claiming causation.
6. Write a 150–250-word stakeholder memo with the question, baseline comparison, limitation, and next action. Include the supporting table and useful descriptions for any figures.
7. Explain why the feature-only future row has no calculable error here. Retain commands, versions, provenance, selected artifact, and outputs for reproduction.

When the download is unavailable, the bundled synthetic route supports the same protocol. Clearly label its source and limitations; do not substitute synthetic values for real-data findings.

## Investigate leakage

Run the notebook's explicitly invalid demonstration on training/validation only. It supplies the actual target as an input and obtains almost-zero error. Explain why that score is unusable, and check that it never enters the candidate, selection, or final model set.

Audit these proposed features: target-day registered rentals, target-day measured weather, the previous day's total, and the same weekday last week. State availability assumptions; a pipeline does not make late information timely.

## Discussion or solo reflection

A colleague wants to rename the final-test winner as the selected method. Explain what that does to the role of the test and how a genuinely new evaluation could be organized. In class, compare reasoning; alone, write and answer a counterargument.

## Work with GenAI

Optional prompt: “Review this protocol for unavailable features, fitting on holdouts, and selection using final scores. Identify the relevant code or artifact.” Verify suggestions yourself and record what you accepted/rejected. No assistant is required: apply that checklist using worked feedback. The public aggregate data are sufficient; do not upload personal records or credentials.

## Optional extension

Use expanding-window CV inside training, or declare a two-feature/ridge candidate before final evaluation. The notebook provides the CV pattern; broad tuning is not required. Explain every additional choice and fitting boundary.

For an IT transfer, frame tomorrow's ticket-volume forecast. Identify count-finalization time, repeated/group structure, data rights, and a relevant baseline. Bike-rental results do not establish ticket-forecast accuracy.

Starting another directory does not make already viewed final data fresh. A changed method needs appropriate new evaluation data or a clearly labeled development-only experiment.

## Self-check and adaptable criteria

| Criterion | Evidence |
| --- | --- |
| Concepts, M05.1 | Correct equation, residual direction, and hand calculation |
| Implementation, M05.2 | Reproducible pipeline and baseline comparison |
| Feature timing, M05.3 | Explicit origin/horizon and justified exclusions |
| Evaluation, M05.4 | Chronological boundaries, frozen choice, interpreted errors |
| Communication, M05.5 | Source/license/versions, concise memo, usable descriptions |

Instructors set local weights and submission rules. Compare [worked feedback](feedback.md) after your attempt.

## Required independent construction

Implement previous-day persistence on development records. Explain input availability at the forecast origin and compare with the provided development baseline.

Use the [guided construction](guided.md) for a worked example, then reconstruct its central step without copying it. Retain changed code, expected/observed evidence and an explanation. This clarifies companion practice; Canvas remains the authority for assessed submissions.
