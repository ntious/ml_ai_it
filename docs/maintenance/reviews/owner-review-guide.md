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

## M. Independent review dispositions, October 2026

The independent review of `fdd5a70` (October 28, 2026) reported findings F1–F14. PR #11 addresses them on branch `fix/ci-encoding-and-rt-iot-baselines`. "Implemented" means changed and checked by the evidence named; it does not mean a learner has used it. The final CI result for the branch head is recorded in the [completion record](course-completion-status.md).

| ID | Finding | Disposition | Evidence | Remaining owner or human action |
| --- | --- | --- | --- | --- |
| F1 | Site downloads return 404; the repository is private | Implemented: offline access route, `build_downloads.py --source-only`, offline link required before the first site download on every page | `tests/test_offline_access.py`; `check_source_links.py` rule tested against a removed link | Owner decides visibility and publication. Then verify the site and downloads from a signed-out browser (section J) |
| F2 | CI failed: Windows default encoding; framework timeout | Implemented: explicit UTF-8 I/O; framework tests and notebooks as parallel jobs; fail-fast off | `tests/test_text_encoding.py` fails on unfixed `main` and passes on the branch; PR CI core jobs pass on Linux 3.12 and Windows 3.12/3.13 | Confirm the framework jobs stay within 90 minutes on later runs |
| F3 | Windows `pathlib` answers failed the Module 2 path check | Implemented: declared POSIX normalization; second case | `tests/test_practice.py` | None |
| F4 | RT-IoT model lost to always-review under its own cost rule | Implemented: constant policies compete on validation; wider fixed grid; prevalence and interpretation recorded | `tests/test_rt_iot_triage.py` (synthetic plus real archive) | Owner review of the README interpretation |
| F5 | Status page contradicted current results | Implemented: verified-results table limited to re-executed core rows; framework rows point to current results | Core rows re-executed on October 28, 2026 | None |
| F6 | Kernel not registered in the learner route; no Windows framework route | Implemented: one kernel name and display name per profile; ordered QUICKSTART steps; WSL Ubuntu 24.04 route | Windows learner route executed in a fresh venv; notebooks found `ml-ai-core` from metadata | Test the WSL steps 1–3 on a real Windows machine; review the measured resource allowance |
| F7 | Template text, argument-list notation, generic links | Implemented for Modules 1–4, 7 and 9–14: module-specific trace and connection text, descriptive links, reasoning tasks with feedback | `tests/test_course_pages.py`; worked values checked against authored solutions; outcome hashes unchanged | Instructor review of explanation quality; learner pilot |
| F8 | Glossary lacked core terms | Implemented (local changes, reviewed) plus kernel link | Entries checked against lesson definitions | None |
| F9 | Swapped false alerts and misses passed | Implemented: asymmetric case | `tests/test_practice.py` | None |
| F10 | Misleading or cryptic feedback | Implemented: NaN lag accepted, pipeline step names explained, call notation, non-numeric results | `tests/test_practice.py` | None |
| F11 | Module 1 boundary contrast and split-role scope | Implemented: contrast signposted; split roles labelled as a Module 5 preview | Outcome hashes unchanged | None |
| F12 | Stale three-module scope statements | Implemented | Repository search | None |
| F13 | No worked research comparison | Implemented: located comparison with Bouthillier et al. (2021) | `tests/test_course_pages.py`; locations read from arXiv:2103.03098 v1 | Instructor review of the course decision |
| F14 | Output formatting and notebook artifacts | Implemented: Module 4 rounding, `N != 8` artifact, console dash, readiness semicolon | `tests/test_exploration.py` | None |

### New items found while correcting

| ID | Observation | Status | Owner decision |
| --- | --- | --- | --- |
| N1 | `deployment.py` reported a zero-variance feature's shift as 0, while the practice `shift_score` returns unavailable | Owner decision: report the standardized shift as unavailable with a reason, and the raw difference separately. Implemented as `mean_shift`; `batch_monitoring.csv` adds `standardized_shift_unavailable` | `tests/test_deployment_monitoring.py`; the Module 12 replay reproduces the recorded results | None |
| N2 | `curriculum/exercises.json` is an authoring record that no script reads | Owner decision: keep the synchronization test for this correction cycle | `tests/test_practice.py` | Future refactor: one declarative source for shared exercise contracts, generating the duplicated material |
| N3 | A deep extraction folder can exceed the Windows 260-character path limit while installing notebook dependencies | Reproduced in the reviewer's environment; the troubleshooting page advises a short folder | None beyond the existing note |

Human learner piloting, workload measurement and assistive-technology testing have not been performed. Do not approve student delivery from these technical results alone.
