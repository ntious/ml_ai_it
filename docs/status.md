# Edition and verification scope

Edition 0.7.0 contains all 14 modules, eight teaching pages per module, public scripts, clean notebooks, worked feedback, instructor guidance and the independent phishing case. Begin with [readiness and learning routes](start-here.md). Reviewers should use the [independent-review guide](review-guide.md).

## How this edition is verified

Every change to `main` runs the full workflow: core checks on Linux (Python 3.12) and Windows (Python 3.12 and 3.13), framework tests and notebooks on Linux CPU, and the complete site, download and browser checks. Check the [workflow results](https://github.com/ntious/ml_ai_it/actions/workflows/checks.yml) for the exact commit you use; a failed, cancelled or timed-out run does not verify that revision.

## Reference environments and evidence

| Area | Evidence for this edition | Scope |
| --- | --- | --- |
| Core processing/modeling | Linux CI, Python 3.12; Windows CI, Python 3.12 and 3.13 | Scripts, behavioral tests and fresh-kernel notebooks |
| Frameworks | Linux CPU CI, Python 3.12 | TensorFlow learning/reload, local LLM generation, adapters, app forms and health |
| Notebook execution | All 14 module notebooks and the phishing notebook | Clean-kernel execution; interface usability is a separate question |
| Reading site | Source/generated links, HTML structure, HTTP routes and downloads | Selected core, optional-project and advanced pages also receive scripted focus, 320px reflow and selected axe checks |
| Distribution | Tracked-source archive integrity, attributed data caches and installed-wheel inference | Source/provenance/schema/cache behavior |

Use the [workflow results](https://github.com/ntious/ml_ai_it/actions/workflows/checks.yml) for exact commit-specific results. The [maintainer guide](../DEVELOPMENT.md) gives reproduction commands. macOS, Windows framework execution and live hosted-provider sessions are outside the demonstrated platform scope; use the Linux CPU reference for framework work.

## Interpreting the examples

Early fixtures are labeled teaching data. Later modeling uses attributed public datasets and a fixed local-model revision. Tiny neural/LLM runs demonstrate mechanisms and may underperform simple baselines. Current framework results include successful adaptation as well as adverse comparisons; use the linked results and protocol-specific denominators.

Adult results are descriptive audits, batch replay is not a measured timeline, and a legal tool plan may misunderstand intent. Historical benchmark performance and successful execution do not establish operational suitability.

## Verified results

**Modules 8–11 and 14:** use [the current framework results](framework-results.md). The [archived framework baseline](maintenance/reviews/framework-baseline-0.7.0.md) describes earlier weak configurations and is not the current result.

The core rows below were re-executed from the pinned sources during the October 28, 2026 review (Windows, Python 3.13). Module 12 is quoted from its worked feedback; its framework run is covered by the Linux framework CI job.

| Module | Data and split | Selected method | Final result | Comparison |
| --- | --- | --- | --- | --- |
| 5 | UCI Bike Sharing; 504/110/110 days | `previous_day` persistence (validation MAE 733.3) | MAE 926.6 rentals/day; largest residual 4,470 on 2012-10-31 | Both linear candidates lost to persistence on validation (888.5 and 1,102.9) |
| 6 | UCI red wine, quality ≥ 7; 243 test | Logistic regression, threshold 0.3 | TP 19, FP 30, FN 10, TN 184; recall 0.66, balanced accuracy 0.757 | Dummy predicts no positives |
| 7 | UCI red wine chemistry; 243 test | k = 2 (validation silhouette 0.206) | Cluster IDs are not quality classes | k = 3: 0.184; k = 4: 0.162 |
| 12 | Module 6 model replayed on 243 held-out records in 4 batches | Logistic, threshold 0.3 | Batch recall 0.40–0.73; batch 3 selection rate 0.41 vs 0.10–0.16 | Batches follow record order, not time |
| 13 | UCI Adult; 16,253 test | Logistic on 5 numeric fields, threshold 0.3 | Recall 0.62, balanced accuracy 0.729 | Selection rate: female 0.20, male 0.31; smallest group n = 135 |
| Phishing | UCI Phishing Websites; 2,107 test | Random forest, threshold 0.5 | TP 844, FN 60, FP 58; recall 0.934, balanced accuracy 0.943 | Dummy predicts no phishing |

Recorded development executions and current CI status are separate evidence. Check the exact commit in Actions: a failed, cancelled or timed-out job does not verify that revision. A learner pilot and human accessibility reviews have not yet been carried out; see below.

## Independent-review questions

Review learner workload, unaided task completion, explanations, feedback and transfer across starting experience. Human screen-reader/keyboard/real-zoom sessions and notebook/app interface evaluation have no recorded human test results in this edition; the [accessibility evidence log](accessibility/review-log.md) identifies their scope. Automated checks do not establish WCAG conformance or learner effectiveness. Use the [pilot instrument](instructor/pilot.md) to record observations rather than treating an unperformed study as a pass.

The [architecture](../REPOSITORY_STRUCTURE.md), [source register](data-sources.md) and archived [learning-support review](maintenance/reviews/learning-support-0.7.0.md) provide implementation context.
