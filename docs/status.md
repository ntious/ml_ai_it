# Edition and verification scope

Edition 0.7.0 contains all 14 modules, six teaching pages per module, public scripts, clean notebooks, worked feedback, instructor guidance and the independent phishing case. Begin with [readiness and learning routes](start-here.md). Reviewers should use the [independent-review guide](review-guide.md).

## Reference environments and evidence

| Area | Evidence for this edition | Scope |
| --- | --- | --- |
| Core processing/modeling | Windows and Linux CI, Python 3.12 | Scripts, behavioral tests and fresh-kernel notebooks |
| Frameworks | Linux CPU CI, Python 3.12 | TensorFlow learning/reload, local LLM generation, adapters, app forms and health |
| Notebook execution | All 14 module notebooks and the phishing notebook | Clean-kernel execution; interface usability is a separate question |
| Reading site | Source/generated links, HTML structure, HTTP routes and downloads | Five pages also receive scripted focus, 320px reflow and selected axe checks |
| Distribution | Tracked-source archive integrity, attributed data caches and installed-wheel inference | Source/provenance/schema/cache behavior |

Use the [successful workflow runs](https://github.com/ntious/ml_ai_it/actions/workflows/checks.yml) for exact commit-specific results. The [maintainer guide](../DEVELOPMENT.md) gives reproduction commands. macOS, Windows framework execution and live hosted-provider sessions are outside the demonstrated platform scope; use the Linux CPU reference for framework work.

## Interpreting the examples

Early fixtures are labeled teaching data. Later modeling uses attributed public datasets and a fixed local-model revision. Tiny neural/LLM runs demonstrate mechanisms and may underperform simple baselines. The SMS generation check rejected invalid JSON; the small adapter check changed completion loss without improving generated labels. Those outcomes are retained for critical interpretation.

Adult results are descriptive audits, batch replay is not a measured timeline, and a legal tool plan may misunderstand intent. Historical benchmark performance and successful execution do not establish operational suitability.

## Independent-review questions

Review learner workload, unaided task completion, explanations, feedback and transfer across starting experience. Human screen-reader/keyboard/real-zoom sessions and notebook/app interface evaluation have no recorded human test results in this edition; the [accessibility evidence log](accessibility/review-log.md) identifies their scope. Automated checks do not establish WCAG conformance or learner effectiveness. Use the [pilot instrument](instructor/pilot.md) to record observations rather than treating an unperformed study as a pass.

The [architecture](../REPOSITORY_STRUCTURE.md), [source register](data-sources.md) and archived [learning-support review](maintenance/reviews/learning-support-0.7.0.md) provide implementation context.
