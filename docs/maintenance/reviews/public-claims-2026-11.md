# Public claims and explanation review — November 2, 2026

This review concerns the working changes on `outcome-evidence-map`, based on `4782b57`. It is an editorial and evidence-consistency review, not a new model benchmark, security audit, institutional approval or learner study.

## Scope and method

The review searched repository Markdown, notebook prose and report/site generators for absolute claims, causal explanations, model comparisons, data descriptions and verification statements. Detailed checks covered learner entry pages, the outcome map and bridge activities, model-use summaries, lesson feedback and solutions, advanced investigations, the project reports and historical review wording. Framework figures were compared with the existing `runs/verified/module08`, `module09`, `module10`, `module11` and `module14` summaries; Module 12 explanations were checked against `batch_monitoring.csv`. Regeneration used those saved outputs, not new training runs.

This process can identify inconsistencies; it does not certify that every statement is correct. Dated independent reviewer opinions remain historical records, not current course guarantees.

## Corrections

| Location | Issue | Correction |
| --- | --- | --- |
| Homepage and its diagram | “Every result” checked through a once-only final test; universal laptop claim | Describe the taught modeling workflow, distinguish historical replay and link environment requirements |
| Model-use summaries | Old SMS failure and eight-step adapter configuration presented alongside current protocols | Identify current recorded results and link the earlier baseline separately |
| Module 3 solutions | An unchanged score attributed to the engineered feature's directional assumption | Report the unchanged score and plausible limitations without claiming an isolated cause |
| Module 6 solutions | Spread ratio treated as an effect; validation difficulty inferred from resplits; fold SD treated as a difference test | Describe observed variation, note changing training records and distinguish fold dispersion from paired uncertainty |
| Module 10 retrieval solutions | Predicted a confident generated answer without running a generator | Identify the measured retrieval failure and frame downstream generation as an untested risk |
| Module 11 feedback and generator | Explanation implied which protocol change caused improvement | Identify simultaneous changes and the absence of an isolating comparison |
| Module 12 feedback | Batch composition described as “likely causes” | Report exact positive counts and observed batch differences |
| Module introductions | Blanket denial of invented labels or data overlooked authored controls and derived tasks | Separate public observations, authored fixtures/controls and derived labels |
| Framework-result generator | Wine baseline called lexical; regeneration could restore obsolete phase wording | Name the baseline correctly and retain current headings and interpretation |
| Status and historical completion record | Workflow configuration and old review findings could read as current guarantees | Identify commit-specific execution and date-bound review scope |
| Outcome map and bridge tools | Unsupported direct evidence and ambiguous artifacts | Link separately completed evidence activities; correct network-record extraction, output validation and unavailable monitoring values |
| Homepage authorship | Owner's README wording absent from the homepage | Carry the owner's existing wording into the homepage, including the School of Information Technology and University of Cincinnati |

The original learning outcomes, numerical benchmark results and unfavorable model comparisons are retained. A completed linked activity supplies evidence for its stated task; it does not establish every part of a course outcome or learner attainment automatically.

## Verification and release boundary

- The RT-IoT study and documented network-record extraction were executed locally during this branch review. The logistic policy's recorded assumed cost is 63.924 per 1,000 test flows and its review workload is 954.309 per 1,000. These use illustrative costs and within-capture data.
- The framework-results page and five feedback sections were regenerated from saved summaries. This checks rendering of recorded evidence, not fresh framework reproducibility.
- Source consistency checks retain the unchanged outcome text in all 14 modules. The local Python 3.12 suite completed 198 tests: 172 passed and 26 skipped. All eight site release-provenance tests passed. These do not include fresh framework training or human testing.
- The attempted full site build stopped because cached practice verification has a different checker digest. Do not edit verification hashes to force publication. Rerun the registered practice notebooks in their documented core and framework environments, then rerun the complete site, download and browser checks for the release commit. Other cached evidence may also need renewal; the first failure does not establish that everything else is current.
- The build renders reading pages before assembling downloads. Those local pages are a preview, not a complete verified distribution. Nothing in this review deploys the branch or changes `main`.

Human learning, workload and assistive-technology findings still need recorded sessions. Current dependency advisories and external-source availability need their own dated checks. Preserve that distinction when describing readiness.

## Release follow-up — November 2, 2026

The stale-artifact blockers above were resolved by fresh execution, without changing recorded verification hashes. All 28 practice/solution notebooks met their expected states in isolated core and TensorFlow environments; the capstone notebook also reran successfully in a fresh core kernel. The complete local build produced 208 reading pages. Download checks verified 404 byte-matched source files, notebook execution identities, attributed caches and the capstone evidence ledger. Scripted focus, narrow-screen and selected accessibility-rule checks passed on 54 reading pages; these are not human accessibility tests.

The build exposed a repository-relative test-file link that escaped the website prefix; the API guide now links to that source file on GitHub. The homepage browser assertion was updated to the reviewed diagram title. Publication must use the successful verification run for the actual merged commit; local cached model results do not replace that run.
