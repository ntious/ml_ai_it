# Edition and verification scope

Edition 0.7.0 contains all 14 modules, six teaching pages per module, public scripts, clean notebooks, worked feedback, instructor guidance and the independent phishing case. Begin with [readiness and learning routes](start-here.md). Reviewers should use the [independent-review guide](review-guide.md).

## Reference environments and evidence

| Area | Evidence for this edition | Scope |
| --- | --- | --- |
| Core processing/modeling | Windows and Linux CI, Python 3.12; Windows CI, Python 3.13 | Scripts, behavioral tests and fresh-kernel notebooks |
| Frameworks | Linux CPU CI, Python 3.12 | TensorFlow learning/reload, local LLM generation, adapters, app forms and health |
| Notebook execution | All 14 module notebooks and the phishing notebook | Clean-kernel execution; interface usability is a separate question |
| Reading site | Source/generated links, HTML structure, HTTP routes and downloads | Five pages also receive scripted focus, 320px reflow and selected axe checks |
| Distribution | Tracked-source archive integrity, attributed data caches and installed-wheel inference | Source/provenance/schema/cache behavior |

Use the [successful workflow runs](https://github.com/ntious/ml_ai_it/actions/workflows/checks.yml) for exact commit-specific results. The [maintainer guide](../DEVELOPMENT.md) gives reproduction commands. macOS, Windows framework execution and live hosted-provider sessions are outside the demonstrated platform scope; use the Linux CPU reference for framework work.

## Interpreting the examples

Early fixtures are labeled teaching data. Later modeling uses attributed public datasets and a fixed local-model revision. Tiny neural/LLM runs demonstrate mechanisms and may underperform simple baselines. The SMS generation check rejected invalid JSON; the small adapter check changed completion loss without improving generated labels. Those outcomes are retained for critical interpretation.

Adult results are descriptive audits, batch replay is not a measured timeline, and a legal tool plan may misunderstand intent. Historical benchmark performance and successful execution do not establish operational suitability.

## Verified results

The table below preserves the earlier edition 0.7.0 snapshot. **For the revised framework protocols and current measured results, use [Phase B results](framework-results.md).** The worked reports on the [reading site](https://ntious.github.io/ml_ai_it/) contain every count. Earlier weak framework runs are archived for diagnosis; current module feedback discusses the revised runs. Rates on 8 examples cannot estimate population performance.

| Module | Data and split | Selected method | Verified final result | Comparison |
| --- | --- | --- | --- | --- |
| 5 | UCI Bike Sharing; 504/110/110 days | `previous_day` persistence (validation MAE 733.3) | MAE 926.6 rentals/day; largest residual 4,470 on 2012-10-31 | Both linear candidates lost to persistence on validation (888.5 and 1,102.9) |
| 6 | UCI red wine, quality ≥ 7; 243 test | Logistic regression, threshold 0.3 | TP 19, FP 30, FN 10, TN 184; recall 0.66, balanced accuracy 0.757 | Dummy predicts no positives |
| 7 | UCI red wine chemistry; 243 test | k = 2 (validation silhouette 0.206) | Cluster IDs are not quality classes | k = 3: 0.184; k = 4: 0.162 |
| 8 | UCI red wine, quality ≥ 7; 243 test | 11→16→1 network, 8 epochs, threshold 0.5 | TP 7, FN 22; recall 0.24, balanced accuracy 0.593 | Logistic at 0.5: recall 0.31, balanced accuracy 0.629 |
| 9 | UCI SMS, 1,200-message sample; 240 test | Embedding + pooling network, 3 epochs, threshold 0.5 | **TP 0, FN 30: no spam flagged**; recall 0.00 | TF-IDF/logistic at 0.5: TP 6, FN 24, FP 0; recall 0.20 |
| 10 | 8 balanced SMS test messages | SmolLM2-135M-Instruct, greedy JSON prompt | **Valid schema 0/8; correct 0/8** | TF-IDF/logistic on the same 8: 5/8 correct |
| 11 | 24 training, 8 validation, 8 test SMS | Rank-2 adapter on one query projection, 8 steps | Validation loss 1.9836 → 1.9809; generated accuracy 0/8 → 0/8 | Base model 0/8 |
| 12 | Module 6 model replayed on 243 held-out records in 4 batches | Logistic, threshold 0.3 | Batch recall 0.40–0.73; batch 3 selection rate 0.41 vs 0.10–0.16 | Batches follow record order, not time |
| 13 | UCI Adult; 16,253 test | Logistic on 5 numeric fields, threshold 0.3 | Recall 0.62, balanced accuracy 0.729 | Selection rate: female 0.20, male 0.31; smallest group n = 135 |
| 14 | 3 authored requests over UCI wine | Log-likelihood router over 3 legal plans | **Count request routed to the alcohol tool (wrong)**; destructive request refused by the keyword gate before the model ran | 1 of 2 answerable requests correct |
| Phishing | UCI Phishing Websites; 2,107 test | Random forest, threshold 0.5 | TP 844, FN 60, FP 58; recall 0.934, balanced accuracy 0.943 | Dummy predicts no phishing |

## Independent-review questions

Review learner workload, unaided task completion, explanations, feedback and transfer across starting experience. Human screen-reader/keyboard/real-zoom sessions and notebook/app interface evaluation have no recorded human test results in this edition; the [accessibility evidence log](accessibility/review-log.md) identifies their scope. Automated checks do not establish WCAG conformance or learner effectiveness. Use the [pilot instrument](instructor/pilot.md) to record observations rather than treating an unperformed study as a pass.

The [architecture](../REPOSITORY_STRUCTURE.md), [source register](data-sources.md) and archived [learning-support review](maintenance/reviews/learning-support-0.7.0.md) provide implementation context.
