# Edition and verification scope

Edition 0.7.0 contains all 14 modules, eight teaching pages per module, public scripts, clean notebooks, worked feedback, instructor guidance and the independent phishing case. Begin with [readiness and learning routes](start-here.md). Reviewers should use the [independent-review guide](review-guide.md).

## Revision-specific verification

At the October 28, 2026 review, main revision `fdd5a70` had failed Windows encoding checks and a framework timeout. PR #11 (`12e49bb`) corrects these paths; its three core CI jobs pass, while framework and downstream site verification were still pending when this note was written. A proposed fix is not evidence that main is verified. Consult the exact workflow revision before adopting a release.

## Reference environments and evidence

| Area | Evidence for this edition | Scope |
| --- | --- | --- |
| Core processing/modeling | PR #11 core jobs pass on Linux 3.12 and Windows 3.12/3.13; main requires the fixes | Scripts, behavioral tests and fresh-kernel notebooks |
| Frameworks | Linux CPU Python 3.12 reference; current PR jobs pending | TensorFlow learning/reload, local LLM generation, adapters, app forms and health |
| Notebook execution | All 14 module notebooks and the phishing notebook | Clean-kernel execution; interface usability is a separate question |
| Reading site | Source/generated links, HTML structure, HTTP routes and downloads | Selected core, optional-project and advanced pages also receive scripted focus, 320px reflow and selected axe checks |
| Distribution | Tracked-source archive integrity, attributed data caches and installed-wheel inference | Source/provenance/schema/cache behavior |

Use the [workflow results](https://github.com/ntious/ml_ai_it/actions/workflows/checks.yml) for exact commit-specific results. The [maintainer guide](../DEVELOPMENT.md) gives reproduction commands. macOS, Windows framework execution and live hosted-provider sessions are outside the demonstrated platform scope; use the Linux CPU reference for framework work.

## Interpreting the examples

Early fixtures are labeled teaching data. Later modeling uses attributed public datasets and a fixed local-model revision. Tiny neural/LLM runs demonstrate mechanisms and may underperform simple baselines. Current framework results include successful adaptation as well as adverse comparisons; use the linked results and protocol-specific denominators.

Adult results are descriptive audits, batch replay is not a measured timeline, and a legal tool plan may misunderstand intent. Historical benchmark performance and successful execution do not establish operational suitability.

## Recorded results

Use [the current framework results](framework-results.md) for Modules 8–11 and 14. The [archived framework baseline](maintenance/reviews/framework-baseline-0.7.0.md) describes earlier weak configurations and is not the current result. Core module feedback and actual generated reports retain their own measured results.

Recorded development executions and current CI status are separate evidence. Check the exact commit in Actions: a failed, cancelled or timed-out job does not verify that revision. Human pilot and accessibility tasks remain pending.

## Independent-review questions

Review learner workload, unaided task completion, explanations, feedback and transfer across starting experience. Human screen-reader/keyboard/real-zoom sessions and notebook/app interface evaluation have no recorded human test results in this edition; the [accessibility evidence log](accessibility/review-log.md) identifies their scope. Automated checks do not establish WCAG conformance or learner effectiveness. Use the [pilot instrument](instructor/pilot.md) to record observations rather than treating an unperformed study as a pass.

The [architecture](../REPOSITORY_STRUCTURE.md), [source register](data-sources.md) and archived [learning-support review](maintenance/reviews/learning-support-0.7.0.md) provide implementation context.
