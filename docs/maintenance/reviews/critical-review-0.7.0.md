# Critical pre-publication review: edition 0.7.0

Reviewed commit `05dd081` on `main` (clean tree), 25 October 2026, following [the review guide](../../review-guide.md). The review takes three perspectives: (1) an experienced ML engineer, (2) a seasoned instructor and instructional designer, and (3) a student.

**What was executed.** Windows 11, Python 3.13.14, scikit-learn 1.8.0, pandas 2.2.3. I ran Modules 1–5 from the written commands, ran the core test suite (`76 tests OK, 14 skipped`) and ran `scripts/check_repository.py` (passed). I did **not** execute the framework modules (8–11, 14) locally. For those, I read the code and the CI-verified outputs already in `runs/verified/`. No human assistive-technology session was performed.

---

## 1. Executive summary

The engineering discipline is unusually strong for teaching material. It includes frozen stage-by-stage studies, hash-verified data provenance, leakage-safe splits grouped by duplicate profiles, explicit denominators, pickle-free model artifacts and CI that executes every notebook. Modules 1–5 worked exactly as documented, and the readiness check is excellent.

Three problems should be fixed before a public launch:

1. **The framework half of the course shows only failures, so students never see a model working.** In the verified outputs, the Module 9 neural model flags 0 of 30 spam messages. The Module 10 LLM produces 0 of 8 valid answers. Module 11 fine-tuning changes loss by 0.003 and accuracy stays 0 → 0. The Module 14 "agent" answers "How many observations?" with the alcohol summary. The course says these results are "retained for critique", but there is no working example to contrast them with. Students cannot learn what good looks like, and an ML engineer reviewing the course will read this as broken.
2. **Students cannot reach the reports and downloads from GitHub.** Every module page sends "verified worked report", "commented notebook" and "complete source archive" links to a setup page. That page tells the student to download an expiring CI artifact while signed in. For a public repo this is the single biggest source of friction.
3. **The prose is boilerplate-heavy and defensive.** 37% of long sentences in lesson pages (851 of 2,300) are repeated on five or more pages. The docs contain 79 "does not establish / prove / guarantee / demonstrate" disclaimers and 69 Canvas references. This buries the teaching and reads as auto-generated. It also ties a public OER to one institution's LMS.

### Top 10 actions, in priority order

| # | Action | Perspective | Effort |
| --- | --- | --- | --- |
| 1 | Publish the reading site with GitHub Pages and point every `site-download:` link to it | Student | S |
| 2 | Re-tune Modules 9, 10, 11 and 14 so each shows one credible working result next to its failure modes | ML | M–L |
| 3 | Make the worked feedback for Modules 8–14 interpret the *actual* numbers (for example, "why recall is 0") | Instructor | S |
| 4 | Fix claims the evidence contradicts ("strong lexical baseline"; "results recorded in DEVELOPMENT.md") | ML/Instructor | XS |
| 5 | Add confidence intervals (the existing `wilson_interval`) to every reported rate, especially the fairness group audit | ML | S |
| 6 | Move repeated guidance into one "How every module works" page; cut disclaimers to a single scope page | Instructor | M |
| 7 | Give Modules 5–7 a learned model that legitimately beats its baseline, plus a realistic leakage demo | ML | S |
| 8 | Turn notebooks into exercise and solution pairs with real blanks; stop stating results before cells run | Instructor/Student | M |
| 9 | Give Windows and macOS students a tested route for Modules 8–14 (a framework devcontainer or Colab) | Student | M |
| 10 | Prepare for going public: remove "repository access" wording, add a description, Discussions and a Release with a DOI | All | XS |

Effort: XS < 1 h, S ≈ half a day, M ≈ 1–3 days, L ≈ a week.

---

## 2. Perspective 1: experienced ML engineer

### Strengths worth keeping

- **Stage separation with frozen artifacts.** `regression.py` writes `split_manifest.json → candidates.json → selection.json → final_evaluation.json` with exclusive file creation and hash chaining. A student cannot accidentally reselect on test data. This is better practice than most production code.
- **Leakage awareness.** The splits group identical chemistry and phishing profiles. SMS text is deduplicated after normalization, and conflicting labels are removed. Adult test rows that duplicate training rows are removed. The vectorizer is adapted on training data only. The imputer is fitted inside the folds.
- **Honest metrics.** `binary_metrics` returns `None` instead of a fabricated 0 for an undefined rate. Confusion counts are always reported. Baselines (dummy and persistence) are allowed to win.
- **Safe artifacts.** The regression models are numeric JSON. Keras loads with `safe_mode=True`. The adapter is saved with `allow_pickle=False`. Downloads are size-capped, and only named ZIP members are extracted.
- **Reproducibility.** The model revision is pinned, seeds and thread counts are fixed, constraint files are kept per profile, and CI executes every notebook.

### Findings

| ID | Location | Observation (evidence) | Learner impact | Severity | Recommendation and how to verify |
| --- | --- | --- | --- | --- | --- |
| ML-1 | `src/practical_ml_ai/neural.py:229`, `continuation_data.py:140`; `runs/verified/module09/summary.json` | The Module 9 neural model predicts all ham: TP 0, FN 30 (recall 0.0, balanced accuracy 0.50). The cause is 3 epochs, a 1,200-message cap and a fixed 0.5 threshold on an imbalanced label (about 12.5% spam). The TF-IDF/logistic "baseline" reaches only recall 6/30 = 0.20, because default `C=1` with a 0.5 threshold suppresses the minority class. TF-IDF+LR on this dataset normally reaches recall above 0.85. | Students conclude that neural NLP "doesn't work" and that TF-IDF is weak. Both conclusions are artifacts of configuration. Outcome M09.4 (compare errors) has nothing meaningful to compare. | **Substantial** | Use the full deduplicated corpus (about 5.1k messages). Train 20–30 epochs with the existing validation-loss checkpoint. Choose the threshold on validation, as Module 6 already does. Give the baseline `class_weight="balanced"` or a validation-selected threshold. Keep the current 3-epoch run as a "diagnose the under-trained model" exercise. *Verify:* test recall for both methods is above 0.8, and the heavy test asserts recall > 0.5. |
| ML-2 | `language.py:59-126`; `runs/verified/module10/generation_evaluation.csv` | The LLM classifier has a strict schema rate of 0/8 and accuracy of 0/8. The 135M model echoes the `<sms>` wrapper or answers unrelated questions (for example, "The plural of the noun 'research'…"). Evaluation uses only 8 messages. | Module 10's learning goal (evaluate an LLM workflow against a baseline) becomes "the LLM never answers". 8 examples cannot support any rate: a Wilson 95% interval at 0/8 is 0–0.32. | **Substantial** | (a) Add a **label-likelihood classifier** as the primary method. Score `{"label":"ham"}` against `{"label":"spam"}` with the same model; `bounded_agent` already does this at `language.py:280`. Keep free generation as a second, contrasting method, so students see that constrained decoding fixes format failures. (b) Add 2–3 few-shot examples to the prompt. (c) Evaluate at least 100 test messages: about 0.6 s per message, so about 1 minute on CPU. Expose `--examples N`. (d) Optionally allow `SmolLM2-360M-Instruct`. *Verify:* the report shows schema validity and accuracy with confidence intervals for both methods. |
| ML-3 | `language.py:151-244`; `runs/verified/module11/summary.json` | The "fine-tuning" is a rank-2 adapter on one projection (layer 0 `q_proj`), trained for 8 steps with batch size 1. Validation loss goes from 1.9836 to 1.9809, and generation accuracy goes from 0 to 0. | The module teaches mechanics but shows fine-tuning achieving nothing. That is the opposite of the real lesson: small adapters fix *format compliance* very effectively. | **Substantial** | Keep the hand-written `LowRankQuery` as a "look inside" construction cell. For the study itself, use `peft` LoRA (r=8, `q_proj`,`v_proj`, all layers), 150–300 steps, batch size 8, on the JSON completion. Report the **schema-valid rate before and after**; this is the measurable win. Budget about 5–10 CPU minutes, or offer that budget as a flagged option. *Verify:* adapted schema rate is above the base rate, and replay of the reloaded adapter still matches. |
| ML-4 | `language.py:263-316`; `runs/verified/module14/request_trace.csv` | The router sends "How many real wine observations…" to the **alcohol** tool, so one of the two answerable requests is wrong. The destructive request is refused by the keyword gate at line 271 before the model runs, so `destructive_request_refused: true` tests a string match, not the agent. Only 3 requests are run, and the plan list hard-codes `alcohol`. | Students see a "bounded agent" whose only correct behaviour comes from an `if` statement. Nothing measures routing quality. | **Substantial** | Build a labelled evaluation set of 20–30 requests with expected tools, including paraphrased destructive requests that slip past the keyword list ("wipe the table", "remove rows"). Report routing accuracy and a confusion table. Make the gate's misses a teaching moment: put the policy in an allowlist, not a keyword denylist. Add one plan → observe → answer loop with `max_steps`, so it is an agent rather than a one-shot router. *Verify:* `request_trace.csv` has an `expected_tool` column and a summary accuracy with a confidence interval. |
| ML-5 | `docs/lessons/09-neural-nlp/index.md:3`; 9 `instructor.md` files (Modules 6–14) | Module 9 promises "a strong lexical baseline" (its recall is 0.20). Nine instructor pages say "Exact counts/results are recorded in DEVELOPMENT.md", but DEVELOPMENT.md contains no results. | Reviewers lose trust when a claim contradicts the evidence, and instructors following the pointer find nothing. | **Substantial** (low effort) | Correct the wording. Either add a results table to `docs/status.md`, generated from `runs/verified/*/summary.json` during the site build, or point to the reading site. *Verify:* `git grep "recorded in DEVELOPMENT.md"` returns nothing. |
| ML-6 | `classical.py:134-167`; `runs/verified/module13/group_audit.csv` | Group rates appear without uncertainty. For example, Amer-Indian-Eskimo recall is 8/19 = 0.42 (Wilson 95% about 0.23–0.64), the "Other" group has n=135, and test sets of n=243 drive the headline numbers. `learning.wilson_interval` exists but is used only in a hand-count exercise. | Module 13's central lesson (compare groups responsibly) is undercut. Students compare point estimates whose intervals overlap heavily. | **Substantial** | Add `*_ci_low`/`*_ci_high` columns to `binary_metrics`, or a wrapper, using `wilson_interval`. Flag groups whose denominator is below about 30. Add bootstrap confidence intervals for balanced accuracy and MAE in Modules 5, 6 and 8. *Verify:* `group_audit.csv` includes interval columns, and the HTML report says which differences are within noise. |
| ML-7 | `regression.py:28-31`; my run of Module 5 | Only two lag features are used. Persistence wins (validation MAE 733 vs `linear_day` 889 vs `linear_week` 1103), so the core regression module never shows a learned model beating a baseline. `day.csv` also contains `workingday`, `holiday` and `weekday`, which are known in advance, and weather fields (usable with a forecast-availability caveat). The largest final residual is on **2012-10-31, the aftermath of Hurricane Sandy**. That is a real-world teaching moment the lesson does not mention. | "Baselines can win" is a valuable lesson once. Showing it in every core study leaves students without a model of how feature engineering helps. | **Substantial** | Add a `linear_calendar` candidate (both lags plus `workingday`/`holiday`) and a model of the change from yesterday. Report a skill score relative to persistence (MASE). Name the Sandy residual in the feedback as an error-analysis example. *Verify:* at least one learned candidate beats persistence on validation, or the lesson explains why none does. |
| ML-8 | `regression.py:369-373` | `leakage_demo` uses the target as its own input, so MAE is about 0. That is too obvious to teach detection. The feedback already names the realistic leak: `casual + registered == cnt`. | Students learn to spot cartoon leakage, not the subtle kind they will meet in practice. | Minor | Add a code demo that uses target-day `casual`/`registered`. Show the "too good to be true" validation MAE, then show the feature unavailable at forecast time. |
| ML-9 | `neural.py:272`, `classical.py:30`, `phishing.py:64` | Thresholds differ: Module 6 selects 0.3 on validation (logistic balanced accuracy 0.757), while Modules 8 and 9 and the phishing case fix 0.5. Module 8 then reports the same logistic model at 0.629. | Students comparing modules conclude the models differ when only the threshold differs. | Minor | Use one rule everywhere (validation-selected threshold). Also report threshold-free ROC-AUC and PR-AUC, which suit imbalanced labels. |
| ML-10 | `runs/verified/module08/summary.json` | `best_validation_epoch = 8 = epochs_requested`, so the model was still improving when training stopped. The misconception exercise asks whether the lowest training-loss epoch can be the wrong checkpoint, but the evidence never shows the curves diverging. | The overfitting concept has no supporting evidence. | Minor | Default to about 40 epochs with a patience rule. The history table will then show validation loss turning up. |
| ML-11 | `classical.py:44-47` | The calibration table uses the validation split, which also selected the model and threshold, so it is optimistically biased. | Students may over-trust it. | Minor | Label it as "optimistic, selection-reused", or compute it from cross-validated training predictions. |
| ML-12 | `regression.py:246-258` | `training_cv` evaluates only `linear_week`, and selection ignores the result. | Students see cross-validation computed and then discarded, which is confusing. | Minor | Either run CV for every candidate and show how it relates to the validation choice, or explain in the lesson why the output exists. |
| ML-13 | `classical.py:22-25` | Classical candidates omit gradient boosting (`HistGradientBoostingClassifier`), which is the standard strong tabular baseline in industry. | Students miss the method they are most likely to use at work. | Minor | Add it to the Module 6 candidate set. |
| ML-14 | `regression.py:432`, `continuation_data.py:218`, `phishing.py` throughout | Large HTML string literals sit inside modeling code. `_html_table` is duplicated. `phishing.py` packs several statements per line with `;`. No formatter or linter runs in CI. | Lessons tell students to "read `src/…`", and the code is harder to read than it needs to be. It also models a style that students should not copy. | Minor | Extract `reporting.py` (or Jinja templates). Add `ruff format` and `ruff check` to `checks.yml`. Reformat `phishing.py`. *Verify:* CI fails on lint errors. |
| ML-15 | Module 12, `apps/wine_quality.py` | "Deployment" is a Streamlit form plus an in-process function. There is no HTTP inference contract, container or health endpoint, apart from Streamlit's own. | IT/MSIT students expect a service boundary they can call. | Minor | Add an optional `apps/api.py` (FastAPI and pydantic schema mirroring `checked_predict`), plus a Dockerfile, as advanced depth. |
| ML-16 | `docs/status.md`, `QUICKSTART.md:50` | Docs claim Python 3.12 as the tested version and pin `py -3.12`. Core tests pass on 3.13.14 (this review). | Students with only 3.13 installed (now the default download) hit an error at `py -3.12`. | Minor | Add 3.13 to the Windows core CI matrix. Change the commands to `py -m venv .venv`. |

---

## 3. Perspective 2: seasoned instructor and instructional designer

### Strengths worth keeping

- **Every module has measurable outcomes** (M01.1 …), and those outcomes connect to evidence in the practice criteria.
- **The readiness check with routing** (`docs/start-here.md`) is excellent. It is attempted before answers are shown, routes students to specific preparation, and says plainly "routing aid, not a validated test".
- **Practice comes before feedback** and is followed by transfer. Mastery levels are explicit (Developing / Meets / Extends). Solo alternatives replace discussion. GenAI disclosure is optional, with a route that needs no assistant.
- Accessibility is planned from the start: text and CSV equivalents for every chart, no screenshot requirement, and an honest log of tests not yet run.
- The phishing case is a well-framed authentic IT task, explicitly presented as a historical benchmark.

### Findings

| ID | Location | Observation | Learner impact | Severity | Recommendation and how to verify |
| --- | --- | --- | --- | --- | --- |
| ID-1 | `docs/lessons/*/*.md` | 851 of 2,300 long sentences (37%) are repeated on five or more pages, and six sentences appear in all 14 modules. Examples: "Having already viewed a public final report, treat a rerun as rehearsal…", "Cover the worked code, implement the central step again…", the Developing/Meets/Extends block, and the "A satisfactory response includes…" paragraph. | Students learn to skim, so the module-specific content that matters gets skipped. The resource reads as generated, which hurts credibility with adopters. | **Substantial** | Create `docs/how-modules-work.md` covering the learning cycle, mastery levels, evaluation-boundary rule, restart-and-run-all and GenAI rule. Link it in one line per page and delete the copies. *Verify:* rerun the duplicate-sentence count (script in §6); the target is below 10%. |
| ID-2 | Whole `docs/` tree | There are 79 hedges of the "does not establish / prove / guarantee / demonstrate" kind and 69 references to Canvas. The voice is defensive and written for reviewers, not encouraging and written for learners. One example: "A successful script exit establishes execution, not a model's usefulness or fairness" appears in some form on most pages. | Public learners outside UC have no Canvas. Novices feel warned rather than taught. The key limits get lost among dozens of ritual ones. | **Substantial** | Keep one `docs/scope-and-limits.md`. On student pages, state limits once and positively ("This run checks the mechanics; Module 13 shows how to judge usefulness"). Replace "Canvas" with "your course" on student pages, and keep LMS specifics in `docs/instructor/`. *Verify:* `git grep -ci canvas -- docs/lessons` returns 0 outside `instructor.md`. |
| ID-3 | `docs/lessons/08…11/foundation.md` | The conceptual explanations are thin where students need them most. The Module 8 foundation covers dense layers, ReLU, sigmoid, cross-entropy, gradients and epochs in 328 words. It never explains gradient descent intuitively or covers learning rate, overfitting or regularization. Its "Worked mental model" paragraph is copied word for word into `guided.md`. Modules 9–11 cover tokenization, embeddings, attention and LoRA in about 300–350 words each. | Students with no ML background (a stated audience) cannot build mental models from this text alone. | **Substantial** | For each framework module, add a 900–1,500-word concept page with one diagram (computation graph, attention, or the LoRA low-rank update), 2–3 worked numerical checks and 3 self-check questions with hidden answers. Remove the duplicate paragraph from `guided.md`. |
| ID-4 | Module page structure (for example, `docs/lessons/01-foundations/*`) | The six pages per module form a confusing loop. `guided.md` says to use it "before the complete walkthrough (index)", yet `index.md` is the entry page. `index.md` ends with "Build understanding step by step", which should come first. `practice.md` ends with a "Required independent construction" that duplicates `guided.md`. `feedback.md` puts its "Construction check" *after* "Continue to Module 2". These are signs of edits layered on top of each other. | Students don't know what order to read in, and the next step is ambiguous. | **Substantial** | Fix one sequence for all modules: **Overview (index) → 1 Concepts (foundation) → 2 Build it (guided) → 3 Full study (run) → 4 Practice → 5 Feedback**. Add a generated "◀ Previous · Next ▶" footer from `curriculum/modules.json` in `build_site.mjs`. Move the appended sections into their proper place. |
| ID-5 | `notebooks/lessons/06…14/*.ipynb` | Notebooks 6–14 share one template: 9 markdown and 8 code cells, about 7.8k characters each. The study runs as one black box (`run_module(6, run_dir)`). None of the 15 notebooks has an exercise cell (0 TODOs or blanks). The Module 6 notebook states "TP 19, FP 30… balanced accuracy about 0.7575" *before* the cells run, which contradicts "predict before running". Generic text leaks between modules ("Small-model mechanics…" appears in Module 6, which has no small model). | The notebooks are something students read, not something they practise in. Predict-then-run loses its force when the answer is printed above the cell. | **Substantial** | Ship `notebooks/exercises/` with scaffolded blanks (`# TODO: fit the scaler on training only`) and keep the current notebooks as solutions. Put stated results inside collapsed `<details>` blocks *after* the run cell. Write module-specific intro text. Extend `check_notebook.py` to run the solutions and check that exercises raise `NotImplementedError` or have their TODOs filled. |
| ID-6 | Feedback pages for Modules 8–14 | The feedback is mostly generic. Modules 9 and 10 quote their failure counts but don't diagnose causes. The others never discuss the actual observed results: Module 11's change of 0.003, the Module 14 misroute, the Module 12 batch swings. | The richest diagnostic moments in the course go unused. "Why did the network flag no spam?" is a great exam question. | **Substantial** (low effort) | For each framework module, add a "Diagnose the verified run" section that quotes the actual numbers and walks through causes (imbalance, threshold, epochs) and a fix. Regenerate it whenever the verified run changes, or reference values from `summary.json`. |
| ID-7 | `docs/modules.md:26-30`, every `instructor.md` | CLO1–CLO8 and A1–A4 labels refer to a private syllabus ("The supplied local module and syllabus sources were reread…"). | External adopters can't interpret the labels. It also signals institution-specific planning in a public OER. | Minor | Move the CLO and ABET mapping into `docs/instructor/alignment.md` only. Present repository outcomes (M01.1…) as the public framework. |
| ID-8 | Module time estimates; `docs/instructor/pilot.md` | Every estimate is "needs learner piloting", and there is no course-level total. My estimate: about 12 h of Python Foundation, roughly 14 × 2–3 h of modules, plus framework installation, so about 50–60 h. | Instructors can't plan a term, and self-learners can't pace themselves. | Minor | Publish a total-hours table in `teaching-plan.md`. Run a small pilot of Modules 1–5 with 3–5 learners before or right after launch, and record the results in `pilot.md`. |
| ID-9 | Accessibility log | All human task-based rows are "NOT RUN". | The resource cannot claim accessible core tasks. | Minor (well disclosed) | Before launch, run one NVDA+Firefox pass through Module 1 and Module 5 (read, run, modify, save, read feedback) and record it. |
| ID-10 | Dataset mix | The audience is IT/MSIT, but the core modeling uses wine, SMS and census data. Only the phishing case is IT. | It weakens CLO "apply to IT operations" and student motivation. | Minor | Consider one IT-native public dataset with a clear license for Modules 6–7 or 12; for example, UCI *Internet Firewall Data* (check its license and terms). Alternatively, reuse the phishing data for Module 12 monitoring. |

---

## 4. Perspective 3: student

I followed the written route as a learner with some Python who is new to ML, on Windows.

| Step | What happened |
| --- | --- |
| README → start-here | The readiness check is clear and fair. The answers come after the questions, and the routes are concrete. 👍 |
| Get the source | The README says "If GitHub requests authentication, use an account with repository access". That is confusing: as a public learner, I wondered whether I'm allowed in at all. |
| Module 1 | The command worked first time and the output matched the docs exactly. Running again with the same `--output` silently overwrote the file, as the docs warn. Later modules refuse an existing directory instead, which is inconsistent but harmless. |
| Module 2 | Worked: 4 tickets, 60 minutes, 3 events, as documented. 👍 |
| Module 3 | `py -3.12 -m venv` fails if only 3.13 is installed, which is now Python.org's default. The code itself works on 3.13. |
| Module 4 | Worked: the HTML report and the text/CSV equivalents were generated. |
| Module 5 | Worked: 110 final rows. The selected model was **previous_day**, and the "regression" module's winner is copying yesterday. I was confused whether I had done something wrong. |
| Click "Read the verified worked report" on GitHub | It took me to a setup page that asks me to find a CI run and download an artifact while signed in, and says artifacts expire. **This is where most students give up.** |
| Modules 8–14 | "Use the Linux CPU reference environment." On Windows or macOS I get no concrete step-by-step route. After a multi-GB install, the verified results show the neural NLP model finding no spam and the LLM never answering correctly. My honest reaction: "Is this broken, or am I?" |
| Notebooks | They mostly call one function and print tables. I never write the ML code myself. The answers are printed above the cells I'm asked to predict. |
| Reading level | The Flesch–Kincaid grade is about 11–13, which is fine for graduate students. The difficulty is abstraction, not vocabulary. A sentence like "Having already viewed a public final report, treat a rerun as rehearsal; a fresh generalization claim needs a new evaluation design" took me three reads. |

### Student-facing findings

| ID | Location | Observation | Severity | Recommendation |
| --- | --- | --- | --- | --- |
| ST-1 | All module `index.md` pages (`site-download:` links) and `docs/setup/student-workspace.md:41-45` | Reports, notebooks and the source ZIP are reachable only through expiring, sign-in-gated CI artifacts. | **Blocking for a public launch** | Add a `deploy-pages` job to `checks.yml`, triggered on `main` after `build-site`. Set the repository homepage to the Pages URL. Make the source-mode links point to the Pages URL (for example, `https://ntious.github.io/ml_ai_it/downloads/module09/example/index.html`). Attach `ml_ai_it-source.zip` to a GitHub Release. |
| ST-2 | `README.md:36`, `docs/setup/student-workspace.md:3,7,35` | The "repository access / sign in" wording implies the repo is private. | Substantial | Remove it at the moment the repo goes public. |
| ST-3 | `docs/setup/frameworks.md`, `docs/setup/hosted.md` | There is no tested framework route for Windows or macOS students. | Substantial | Add `.devcontainer/frameworks/devcontainer.json`, which runs `bootstrap.py --profile frameworks`, and document "Open in Codespaces (frameworks)" as the default for Modules 8–14. Optionally add Colab badges with a setup cell that clones the repo and installs the CPU wheels. |
| ST-4 | `QUICKSTART.md:50,58` | Commands are pinned to `py -3.12` / `python3.12`. | Minor | Use `py -m venv .venv` and say "3.11–3.13". |
| ST-5 | Notebooks: `ROOT` discovery | In Colab, the notebook fails unless the user changes into the extracted folder (documented in prose only). | Minor | Add a first cell that, in Colab only, clones the repository and runs `%cd`. |
| ST-6 | Lesson pages | There is too much meta-instruction (how to learn, what not to claim) relative to content (what the thing is and why). | Substantial | Covered by ID-1, ID-2 and ID-3. |

---

## 5. Pre-publication checklist (repository going public)

The repository is currently **PRIVATE**, with no description, no homepage and Discussions disabled.

- [x] The private institutional folder `/documentations/` (syllabus, Canvas text, project PDFs) is git-ignored and **absent from all history** (`git log --all -- documentations` returns nothing). No blobs over 500 KB are in history.
- [ ] Remove the "repository access / authenticate" wording (ST-2).
- [ ] Enable GitHub Pages and deploy the reading site (ST-1).
- [ ] Add a repository description, topics (`machine-learning`, `oer`, `education`, `python`, `scikit-learn`) and the homepage URL.
- [ ] Enable Discussions for learner questions, and keep Issues for reproducible defects. Add a "lesson error / unclear explanation" issue template.
- [ ] Cut a `v0.7.0` (or `v0.8.0`) Release with the source ZIP and the verified reports. Connect Zenodo for a DOI, and update `CITATION.cff` with it.
- [ ] Decide whether `docs/maintenance/reviews/*` (including this file) should be public. They are useful for transparency but noisy for learners. Consider linking them only from `DEVELOPMENT.md`.
- [ ] Confirm the decision to publish `ntiik@ucmail.uc.edu` in 6 public files. It is deliberate, but it will attract spam once the repo is public.
- [ ] Run the five browser checks and one human accessibility pass (ID-9).

---

## 6. Concrete improvement plan in this repo

### Phase A: before going public (about 1–2 days)

1. **Pages deploy (ST-1).** In `.github/workflows/checks.yml`, add a job after `build-site`:
   ```yaml
   deploy-pages:
     if: github.ref == 'refs/heads/main'
     needs: build-site
     permissions: { pages: write, id-token: write }
     environment: { name: github-pages }
     runs-on: ubuntu-latest
     steps:
       - uses: actions/download-artifact@v4
         with: { name: complete-reading-site, path: site }
       - uses: actions/upload-pages-artifact@v3
         with: { path: site }
       - uses: actions/deploy-pages@v4
   ```
   Then change `scripts/build_site.mjs` and `scripts/check_source_links.py` so that a source-mode `site-download:` link resolves to the absolute Pages URL instead of `student-workspace.md#reading-reports-from-github`.
2. **Truthfulness fixes (ML-5).** Edit `docs/lessons/09-neural-nlp/index.md:3`. Replace "recorded in DEVELOPMENT.md" in the nine `instructor.md` files. Add a results table to `docs/status.md`, ideally generated by `build_site.mjs` from `runs/verified/*/summary.json`.
3. **Access wording and Python versions (ST-2, ST-4, ML-16).** Update `README.md`, `QUICKSTART.md` and `docs/setup/student-workspace.md`. Add Python 3.13 to the Windows core matrix.
4. **"Diagnose the verified run" sections (ID-6)** in `docs/lessons/08…14/feedback.md`.

### Phase B: make the framework modules teach success *and* failure (about 1 week)

5. Module 9 (ML-1): edit `neural.py` and `continuation_data.sms_splits(limit=None)`. Default to about 25 epochs, select the threshold on validation, and use a balanced TF-IDF baseline. Update `tests/test_continuation_heavy.py` to assert recall > 0.5.
6. Module 10 (ML-2): in `language.py`, add `score_label()` (label likelihood), `--examples` (default 100), a few-shot prompt and Wilson intervals. Show the two methods side by side.
7. Module 11 (ML-3): add `peft` to the `language` extra and `constraints-neural.txt`. Train LoRA with r=8 on `q_proj`/`v_proj` for 200 steps. Report the schema rate before and after. Keep `LowRankQuery` as the construction cell.
8. Module 14 (ML-4): add `data/samples/agent-requests.csv` with columns request, expected_tool and category, including paraphrased destructive requests. Report routing accuracy and add a bounded multi-step loop.
9. Re-run CI and refresh `runs/verified`, the feedback numbers and the status table.

### Phase C: evaluation rigor (about 2–3 days)

10. ML-6: add `with_intervals()` to `continuation_data.py` and apply it in every `publish_report` table that contains rates. Flag groups with n below 30 in Module 13.
11. ML-7 and ML-8: add calendar-feature candidates and MASE to `regression.py`, a `casual/registered` leakage demo and a note on the Sandy residual in `docs/lessons/05-regression/feedback.md`.
12. ML-9, ML-10, ML-13: use one threshold rule everywhere, report ROC-AUC/PR-AUC, add patience-based epochs in Module 8, and add `HistGradientBoostingClassifier` in Module 6.

### Phase D: instructional rewrite (about 1–2 weeks, can run in parallel with B)

13. ID-1 and ID-2: create `docs/how-modules-work.md` and `docs/scope-and-limits.md`, then delete the repeated sentences. Use this check in CI or by hand:
    ```python
    # count sentences (>60 chars) repeated on >=5 lesson pages; target <10%
    import re, glob, collections
    c = collections.Counter()
    for p in glob.glob("docs/lessons/*/*.md"):
        c.update({s.strip() for s in re.split(r"(?<=[.!?])\s+", open(p, encoding="utf-8").read()) if len(s.strip()) > 60})
    ```
14. ID-3: write deeper concept pages for Modules 8–11, each with a diagram and self-checks.
15. ID-4: normalize page order and add generated Previous/Next navigation in `build_site.mjs`.
16. ID-5: split the notebooks into `notebooks/exercises/` and the existing solutions, and extend `scripts/check_notebook.py`.
17. ID-7: move CLO/ABET labels into `docs/instructor/alignment.md` only.

### Phase E: engineering hygiene (about 1 day)

18. ML-14: extract `src/practical_ml_ai/reporting.py`, add `ruff` to the `verification` extra and to CI, and reformat `phishing.py`.
19. ML-15: optionally add `apps/api.py` (FastAPI) and a `Dockerfile` as Module 12 depth.
20. ST-3: add the framework devcontainer and a hosted-route note in `docs/setup/hosted.md`.

---

## 7. Reporting notes

This review contains no personal or student records. Severity follows the review guide: *Blocking* means the core task cannot be completed through the documented route; *Substantial* means a learning outcome is weakened for many learners; *Minor* means a localized weakness with a workaround; *Editorial* means wording only. Grading, deadlines and institutional alignment remain the adopting instructor's decisions.
