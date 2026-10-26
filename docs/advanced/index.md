# Optional advanced investigations

The 14 core modules remain the main route. These investigations add depth after
the relevant foundations; they do not add a mandatory Module 15 or change an
adopting course's grading, prerequisites or model-count requirements.

Start with the [separate completed project](../../projects/phishing-triage/README.md).
It uses CPU/core dependencies, runs without earlier notebooks, and produces a
completed report as well as machine-readable artifacts.

| Investigation | Prerequisite connection | Current form |
| --- | --- | --- |
| [Bounded hyperparameter tuning](tuning.md) | Modules 5–6 | Executed grouped-CV search with every candidate/fold recorded |
| [Training-seed and split stability](stability.md) | Modules 6–9 | Executed multi-seed study and optional separate split experiment |
| [Uncertainty, calibration and error costs](evaluation.md) | Modules 6, 12–13 | Executed bootstrap/reliability/cost evidence with interpretation tasks |
| [Complete project assessment](capstone-assessment.md) | Project companion | Annotated exemplar and evidence crosswalk for independent transfer |

## Further depth, without pretending it is already implemented

These are discussion/extension proposals, not verified additional workflows:

- **Nested grouped CV:** distinguish selection-reused search scores from an outer estimate of the entire tuning procedure. The exemplar currently uses inner training CV plus separate outer validation/final partitions.
- **Ablation:** predeclare feature/component removals on development data, then explain paired differences and computation costs. Avoid choosing removals from final-test scores.
- **Distribution shift:** design a prospective temporal or external validation study with permitted records. Source-order batches in the exemplar are not drift-over-time evidence.
- **Tracking and recovery at larger scale:** translate the local hash ledger into a team registry with access control, scheduling and retention requirements. No external tracking service is needed for the current project.
- **LLM and agent robustness:** build new permitted adversarial/control sets and compare intent errors with executor permissions. Module 14's finite controls do not establish general safety.

Choose an extension because it answers a research or operational question. A
larger model, paid infrastructure or another metric does not automatically make
the work more advanced. Every extension should name its question, boundary,
expected evidence, compute budget and failure interpretation.
