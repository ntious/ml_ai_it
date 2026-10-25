# Repository architecture and file inventory

This document describes the implemented edition. It is the maintained architecture reference for contributors and adopting instructors. The [review report](docs/maintenance/reviews/baseline-0.6.0.md) records gaps, corrections, and verification limits.

## Design goals

Support complete beginners through advanced optional work; let an instructor link one module directly; keep independent use separate from institutional assessments; teach reproducible implementation with shared tested code; preserve data/model rights; and provide reading, script, notebook, and text/table evidence routes.

## Source layout

| Path | Responsibility | What belongs elsewhere |
| --- | --- | --- |
| curriculum/modules.json | Canonical 14-module paths, profiles, titles, and required pages | Official syllabus wording is owner-verified, not inferred |
| docs/lessons/ | Six-page teaching package per module | Restricted Canvas tasks and submissions |
| src/practical_ml_ai/ | Shared validation, analysis, learning, inference, and reporting behavior | Duplicated algorithms in notebooks |
| examples/ | Thin, commented script entry points | Copied model implementations |
| notebooks/lessons/ | Clean, commented, independently executable tutorials | Generated execution state in source control |
| apps/ | Local interactive teaching interface | Public production service |
| data/ | Contracts, manifests, explicitly labeled earlier teaching fixtures | Downloaded external archives or invented real records |
| environments/ | Exercised core/framework constraints | A claim of a complete transitive lock |
| scripts/ | Curriculum, kernel, site, archive, HTTP, and package verification | Unreviewed arbitrary notebook execution |
| tests/ | Behavioral, real-data, framework, replay, CLI, and app checks | Accessibility conformance claims |
| templates/ | Reusable lesson, case, instructor, provenance, AI, and review records | Completed results invented from a checklist |
| docs/instructor/ | Adoption, assessment, pacing, and alignment status | Changes to master grading rules |
| docs/accessibility/ | Access routes, limitations, and manual-review evidence | An untested compatibility promise |
| .github/ | CI and contribution/reporting templates | Automatic public deployment |
| .binder/ and .devcontainer/ | Optional environment definitions | Verified hosted accessibility or universal support |

Root files provide setup, contribution guidance, change history, licensing, citation and architecture. Historical audits are archived under docs/maintenance/reviews. All authored tracked files belong in the source archive; generated outputs and private planning sources do not.

## One implementation, several routes

A script or notebook calls shared package functions. The functions validate inputs and produce named evidence. Reading pages explain the workflow and link downloadable source/notebooks and actual reports. The app calls the same checked inference behavior. Adaptations should change shared behavior and its evidence together rather than maintaining a second algorithm in a tutorial.

The registry drives site navigation, notebook execution selection, notebook downloads, and structure verification. Narrative lesson content and the course-outcome crosswalk remain reviewed prose; they are not generated from guessed institutional outcomes.

## Module inventory

Every row requires entry, foundation, guided construction, practice, feedback, instructor notes, one registered notebook, and one public example script. The verifier rejects missing or unregistered lesson notebooks/scripts.

| Module | Title and entry | Profile |
| --- | --- | --- |
| 1 | [ML and AI foundations for practical decisions](docs/lessons/01-foundations/index.md) | core |
| 2 | [Python for reproducible ML workflows](docs/lessons/02-python-workflows/index.md) | core |
| 3 | [Data processing and trustworthy inputs](docs/lessons/03-data-processing/index.md) | core |
| 4 | [Exploration and visual communication](docs/lessons/04-exploration/index.md) | core |
| 5 | [Regression and reliable evaluation](docs/lessons/05-regression/index.md) | core |
| 6 | [Classification and decision trees](docs/lessons/06-classification/index.md) | core |
| 7 | [Clustering and learning paradigms](docs/lessons/07-clustering/index.md) | core |
| 8 | [Neural networks with TensorFlow](docs/lessons/08-neural-networks/index.md) | frameworks |
| 9 | [Neural NLP for real messages](docs/lessons/09-neural-nlp/index.md) | frameworks |
| 10 | [LLMs and evaluated generative workflows](docs/lessons/10-llm-workflows/index.md) | frameworks |
| 11 | [Fine-tuning language models responsibly](docs/lessons/11-fine-tuning/index.md) | frameworks |
| 12 | [Deployment and monitoring](docs/lessons/12-deployment/index.md) | frameworks |
| 13 | [Ethics and fairness across the lifecycle](docs/lessons/13-ethics-fairness/index.md) | core |
| 14 | [Bounded agents and AI workflows](docs/lessons/14-agents/index.md) | frameworks |

Core and framework profiles are separate environments. Framework execution is currently checked on Linux CPU. Core behavior and kernels are checked on Windows and Linux. Additional platform and human-interface coverage is specified in the [support matrix](docs/status.md).

## Data and generated artifacts

Read [sources and rights](docs/data-sources.md). Modules 6–14 use real UCI records; the model revision is fixed. Earlier introductory fixtures remain explicitly synthetic. Preserve reviewed hashes, archive bytes, attribution, split boundaries, and transformations. Generated reports cannot establish that a demonstration is suitable for deployment.

In a checkout, default dataset/model caches are under runs/. An installed package uses a user cache directory. ML_AI_RUNS_DIR explicitly overrides that location for Modules 6–14; choose a writable absolute path before Python starts. This controls caches, not output-directory arguments or the separate explicit bike-download destination.

Generated runs/, site/, dist/, environment folders, and caches are excluded from source control. Source notebooks remain output-free; actual kernel-executed copies are retained in CI artifacts and site downloads. External cache ZIPs are distributed separately from original source.

## Build and verification boundaries

CI checks the registry and Python syntax, behavior on Windows/Linux, actual Linux CPU framework learning/generation, 14 notebooks in real Jupyter kernels, generated page semantics and links, project-prefix HTTP routes, archive completeness/digests, extracted CLIs, and an isolated installed-wheel inference path.

The site is static HTML/CSS without required browser JavaScript. Its build requires verified outputs from both execution profiles; it fails instead of inventing missing results. The complete site artifact supports reading, review and hosting through the chosen distribution process.

Automated checks do not establish screen-reader usability, plot quality, reflow, educational effectiveness, formal course alignment, or production fitness. Follow the [release checklist](docs/release-checklist.md).

## Maintenance rules

Update registry, teaching pages, examples, tests, and provenance together. Check core and framework dependencies independently before a version change. Retain observed failures in worked examples. Keep optional depth optional, preserve a no-GenAI route, and test the actual learner task.

No empty slide/video/production folders are created to imply missing material exists. Record future work with acceptance criteria; add its files when authored. Original private planning attachments remain outside the open source archive. Institutional assessment mappings are maintained by the adopting course owner.

## Learning-support extension

Student entry: docs/start-here.md; preparation: docs/setup/python-bridge.md; workspace/hosted/troubleshooting pages explain acquisition and platform boundaries. Each module adds guided.md and a runnable construction cell. scripts/preflight.py reports dependencies/resources; scripts/bootstrap.py installs explicit profiles. learning.py exposes uncertainty/calibration arithmetic. The independent phishing case lives in phishing.py, scripts/phishing_study.py, notebooks/cases/phishing.ipynb and docs/cases/phishing.md. Its stages separate preparation, fitting, validation selection, final evaluation and reporting. docs/project.md and docs/instructor/pilot.md support cumulative work and actual learner validation.
