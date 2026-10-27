# Owner review: applied ML and AI course

Review the feature branch before merging. Record findings with a path, module, reproduction steps, observed result, expected result, learner impact and priority. The human review and student pilot remain separate from automated checks.

## A. Confirm the revision

Run `git status --short` and `git log -1 --oneline`. Record the commit and environment. Preserve personal changes before updating your checkout. Use the same revision for an independent review.

## B. Start as a new learner

Follow README → start-here → Python Foundation/readiness → environment setup. Check that a learner outside IT can understand the prerequisites, locate help and determine the next action. Record actual setup time and any assistance.

## C. Check all fourteen learning routes

For each module, follow index → foundation → concepts → guided construction → practice → solutions → recorded feedback. Confirm that learning outcomes remain appropriate and unchanged. Identify terms introduced without explanation, missing steps, contradictory instructions and excessive repetition. Evaluate the examples rather than judging depth by word count alone.

## D. Attempt the practice before the solution

Open `notebooks/practice/moduleNN-practice.ipynb` in the documented environment. Restart and run all. Unfinished functions should report `not_attempted`, not pass. Implement the three functions, rerun checks and try an input different from the visible cases. Open the separate solution only afterward. Explain why it works. The small checks do not assess every module outcome: also complete the reference and transfer tasks.

## E. Run the full module experiments

Use each module's documented command and a fresh output directory. Confirm that the notebook and script describe the same study. Trace a numerical claim to its CSV or JSON artifact. Check training-only preprocessing, validation selection, final-test boundaries, baselines and adverse results. Record failures with the full command and relevant exception.

## F. Inspect fairness evidence

Run Module 13. In group_audit.csv, check recall, false-positive-rate and selection-rate denominators. Confirm illustrative interval bounds are ordered and between zero and one; undefined rates retain unavailable intervals. Small-denominator flags must use the relevant denominator. Ask whether the explanation makes clear that independent population sampling is not established and that interval overlap is not a test of fairness.

## G. Review the authentic IT transfer

Read `projects/rt-iot-triage/README.md`. Run its study with a new output path. Confirm UCI attribution, checksum verification, exclusion of the unnamed index, normal/attack mapping and no identical selected-input group overlap. Compare model alerts and costs against both constant policies. Explain why full-flow features support a completed-flow decision and why the dataset cannot establish future-device, session-independent or prospective performance.

Run the UCI-client download command separately. Confirm it writes only to the ignored runs directory and records metadata and checksums. Its current export and the fixed study archive are different reproducibility routes.

## H. Review research reasoning

Use `docs/advanced/research-comparison.md`. Require a primary source location for each empirical claim. Compare task, population, target, split, baseline, metric and uncertainty before comparing scores. Distinguish an implemented technique from a replication of a published result. Flag unsupported claims and missing worked comparisons.

## I. Review the complete capstone

Follow `projects/phishing-triage/README.md`. Inspect tuning, all-seed reporting, split sensitivity, frozen evaluation, delivery and monitoring. Use the checkpoint table in `docs/advanced/capstone-assessment.md` and `templates/project-revision.md`. Confirm a learner can identify the next deliverable, revise an inadequate protocol and explain one design decision independently.

## J. Check downloads and accessibility

From a signed-out browser, test README entry, readiness, one early and one framework lesson, starter/solution downloads, worked reports and source archive. Record the exact hosted revision. Local builds do not prove public availability. Test keyboard navigation, visible focus, narrow viewport, zoom and an actual screen reader with representative tasks. Record assistance and failures; automated checks do not substitute for these observations.

## K. Technical reproduction

In the core environment:

```sh
python scripts/check_repository.py
python -m unittest discover -s tests
python scripts/check_practice.py --group core --kernel ml-ai-core
```

In the framework environment:

```sh
python scripts/check_practice.py --group frameworks --kernel ml-ai-frameworks
```

After generating the documented verified module and capstone artifacts:

```sh
npm run build
python scripts/check_site.py
python scripts/check_http_routes.py
python scripts/check_downloads.py
node scripts/check_browser.mjs
npm run check:browser
```

Consult DEVELOPMENT.md for environment variables and the complete execution sequence. Keep logs with the reviewed revision. A skipped test is not a pass for its feature.

## L. Return findings and decide the next step

Use one row per finding: ID, location, reproduction, impact, recommended correction, owner and retest evidence. Prioritize broken learner paths and incorrect scientific claims, then missing explanation and feedback. After corrections, retest affected tasks. Approve the implementation for student piloting only after owner and independent review; use observed pilot evidence to revise workload and teaching claims before Spring 2027 delivery.
