# Module 14 foundation bridge

Return to the [lesson](index.md) after this short preparation. You can use explanations and tables before running code.

## Essential idea

A valid tool call is not necessarily the right action for the user's intent. This core deliberately constrains routing to three enumerated plans and one read-only call. Mean completion log-probability ranks plans; it is not calibrated confidence. Hard policy checks live outside the model.

## Work through the evidence

A plan proposes an action, a tool returns evidence, and an answer uses that evidence. Schema validity, policy validity, and semantic correctness are separate checks. A small legal plan set reduces action space but does not solve intent interpretation or every injection risk.

Before running, write what the output would need to show for your interpretation to be justified. After running, identify the exact field, denominator, unit, or record boundary supporting your claim. A successful script exit establishes execution, not a model's usefulness or fairness.

## Reproducible habits

Use the documented source and environment, retain the printed run directory, and read the named text results. Keep data/cache originals unchanged. The module's notebook separates setup, source inspection, execution, evidence, and reflection. Run cells in order, then restart and run all; old kernel variables are not evidence of a clean run.

If packages are missing, install the documented extra with the same Python executable used to run the module. If a source hash fails, investigate the version rather than bypassing the check. First downloads need connectivity; later runs can reuse the verified cache. [Setup](../../setup/index.md) records platform limits.

## Worked mental model

The model ranks three permitted plans. The policy and exact schema are enforced by code; the model does not grant itself permissions. A request may still be routed to the wrong legal operation. This bounded router has no general planning or memory implementation.

Work through the [numerical construction](guided.md) before using the complete runner. Explain every new symbol using the [glossary](../../glossary.md).

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
