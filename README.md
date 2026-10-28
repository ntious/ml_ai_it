# Practical Machine Learning and AI Systems

**[Course website on GitHub Pages](https://ntious.github.io/ml_ai_it/)** · [Start here](docs/start-here.md) · [Course outline](docs/modules.md)

The website address is the publication target; until its first successful deployment, use the lessons and notebooks in this repository.

Learn to frame a useful problem, work with data, build and evaluate models, and explain whether an AI system should be used. This open educational resource combines short lessons, runnable Python examples, guided notebooks, independent practice and worked feedback across 14 modules.

**Start with [the readiness check and learning routes](docs/start-here.md).** If you have never programmed, begin with [Python Foundation](https://ntious.github.io/python_foundation/), then return for our [Python-to-ML bridge](docs/setup/python-bridge.md). You can learn through this resource independently or use it alongside an instructor's course.

Edition 0.7.0. [Current status and tested scope](docs/status.md).

Modules [5](docs/lessons/05-regression/index.md), [6](docs/lessons/06-classification/index.md) and [8](docs/lessons/08-neural-networks/index.md) now offer an applied explanation–practice–feedback prototype with separate learner notebooks and worked solutions. Start with the concept sequence, attempt the functions, then use the complete reference study. [Human pilot and review guide](docs/instructor/teaching-prototype-pilot.md).

## Who this is for

- MSIT and other graduate students encountering ML and AI for the first time.
- Learners from non-IT disciplines who want practical, explainable examples.
- Students with programming or ML experience who want to strengthen evaluation and explore deeper experiments.
- Instructors adapting individual modules or a complete sequence.

You do not need prior ML knowledge, calculus, a GPU or a paid AI account for the documented core activities. New programmers need planned preparation time. Python Foundation estimates about 12 guided hours plus practice; our bridge then adds dictionaries, packages, paths, CSV/JSON and dataframes. Experienced students can use the readiness check to skip familiar preparation. This support does not create a formal prerequisite course.

## What you will learn

You will practice how to:

- Define a task, its stakeholder, observation, inputs, outcome and error costs.
- Read, validate, clean and explore data while preserving its meaning and provenance.
- Construct a model and compare it with a relevant simple baseline.
- Keep training, validation and final evaluation separate, and explain leakage and uncertainty.
- Work with classification, regression, clustering, neural networks and text representations.
- Evaluate local LLM outputs, small fine-tuning experiments and bounded tool workflows.
- Demonstrate checked inference, monitoring and a rollback plan.
- Communicate numerical evidence, limitations, ethical concerns and reasons not to deploy.

These are resource learning goals. The [module outcomes](docs/modules.md) identify more specific evidence; an adopting course sets its own official outcomes and assessments.

## Get your first result

1. **Choose support:** complete [readiness](docs/start-here.md) and any needed Python preparation.
2. **Get the complete source:** follow [download, extraction and folder instructions](docs/setup/student-workspace.md). A notebook downloaded alone does not include the shared code and data.
3. **Run Module 1:** open a terminal in the extracted project folder, where README.md and examples are visible. Python 3.11–3.13 are supported for the core modules; CI checks 3.12 and 3.13. The first script uses only the standard library.

Windows PowerShell:

```powershell
py examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

Linux or macOS:

```sh
python3 examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

Expect **Review storage**. Open runs/module01/first-run.txt, change 85 to 70, save to a different output filename and explain the changed decision. This is a human-written rule; it does not train a model.

Continue with [Module 1](docs/lessons/01-foundations/index.md) and [first-run setup](QUICKSTART.md). If a command fails, use [troubleshooting](docs/setup/troubleshooting.md) before reinstalling unrelated software.

## Choose how to work

| Route | How to begin | Execution scope |
| --- | --- | --- |
| Notebook | Keep it inside the complete source folder, install the matching environment and select its kernel | Interactive construction and saved explanations |
| Script | Run the public script from the complete source folder with the matching environment | Same shared implementation; text/CSV/HTML evidence |
| Reading | Use the lesson pages and verified worked reports | Interpretation practice; implementation outcomes still need execution |

Core execution is checked on Windows and Linux. Framework modules 8–12 and 14 use a separate **Linux CPU** environment for TensorFlow, PyTorch/Transformers and Streamlit. For framework work on other platforms, use the Linux CPU reference environment. First installation and data/model downloads need connectivity; keep valid caches for later replay. Framework work needs additional disk and memory; see the [framework requirements](docs/setup/frameworks.md).

[Environment choices](docs/setup/hosted.md) explains Codespaces, Colab, Binder and local setup, including access, saving and verification limits. Select a service that can access the complete source and meets the documented environment requirements. Use an instructor's verified workspace when available.

## Module map

| Module | Focus |
| --- | --- |
| 1 | [ML and AI foundations](docs/lessons/01-foundations/index.md) |
| 2 | [Python workflows, files and reusable functions](docs/lessons/02-python-workflows/index.md) |
| 3 | [Data processing and validation](docs/lessons/03-data-processing/index.md) |
| 4 | [Exploration and visual communication](docs/lessons/04-exploration/index.md) |
| 5 | [Regression and reliable evaluation](docs/lessons/05-regression/index.md) |
| 6 | [Classification and decision trees](docs/lessons/06-classification/index.md) |
| 7 | [Clustering and learning paradigms](docs/lessons/07-clustering/index.md) |
| 8 | [Neural networks with TensorFlow](docs/lessons/08-neural-networks/index.md) |
| 9 | [Neural NLP and lexical baselines](docs/lessons/09-neural-nlp/index.md) |
| 10 | [Local LLM workflows and evaluation](docs/lessons/10-llm-workflows/index.md) |
| 11 | [Small parameter-efficient fine-tuning experiments](docs/lessons/11-fine-tuning/index.md) |
| 12 | [Deployment demonstrations and monitoring](docs/lessons/12-deployment/index.md) |
| 13 | [Ethics, fairness and uncertainty](docs/lessons/13-ethics-fairness/index.md) |
| 14 | [Bounded agents and tool workflows](docs/lessons/14-agents/index.md) |

The [historical phishing-detection case](docs/cases/phishing.md) adds an authentic IT security example with separate preparation, training, validation, evaluation and reporting stages, plus a combined notebook. The [project companion](docs/project.md) helps you connect concepts across an existing course project or independent study.

## A repeatable learning workflow

For an optional view of the entire lifecycle, use the [complete capstone exemplar](projects/phishing-triage/README.md): a separate CPU project with grouped tuning, multi-seed and split-sensitivity experiments, frozen evaluation, a numeric inference bundle, monitoring rehearsal and an annotated completed report. The [advanced route](docs/advanced/index.md) explains these investigations and distinguishes implemented experiments from further extensions. The existing 14 modules and their commands remain independently usable.

1. Read the outcomes and decide what evidence you need to produce.
2. Review the foundation bridge; use the [glossary](docs/glossary.md) for unfamiliar terms.
3. Predict the result of the guided construction before running it.
4. Execute the notebook or script, inspect saved evidence and check a calculation independently.
5. Make the required purposeful change, diagnose a failure and explain what happened.
6. Attempt practice before comparing worked feedback; try a changed example if an answer was unfamiliar.
7. Save code, commands, versions, source identities, readable results and your explanation. For notebooks, restart and run all to expose hidden state.
8. Attempt optional depth after meeting the core outcome. Preserve evaluation boundaries when experimenting.

All modules include outcomes, a foundation bridge, guided construction, practice, public feedback and instructor notes. A copied report or successful run alone does not demonstrate independent mastery. Small models can perform poorly; those results are retained so you can critique them.

## Data, reports and responsible AI use

Early modules use clearly labeled original teaching fixtures. Regression and the later modeling modules use attributed public datasets; the phishing case uses real historical security attributes. The [source register](docs/data-sources.md) documents rights, reviewed hashes, transformations and model provenance. Historical benchmark results do not establish current operational performance.

Lesson source is readable directly on GitHub. The [reading-site publication address](https://ntious.github.io/ml_ai_it/) provides verified reports, executed notebook copies and source/data downloads once the owner enables publication and the first deployment succeeds. CI builds the complete site separately from deployment. Until publication, use the site archive supplied for your review or class; see [reading the reports](docs/setup/student-workspace.md#reading-reports-from-github). You do not need to build the full site to study one module.

GenAI assistance is optional. Verify suggestions against code and evidence, protect private data, and follow the [AI collaboration guidance](docs/ai-collaboration.md) and your instructor's disclosure rules. Public feedback supports self-study; it is not a confidential answer key.

## Repository guide

| Location | Purpose |
| --- | --- |
| docs/start-here.md | Readiness, Python preparation and learning routes |
| docs/lessons/ | Student lessons, guided construction, practice, feedback and instructor notes |
| notebooks/ | Interactive companions; use inside the complete source tree |
| examples/ | Public scripts calling the shared implementation |
| src/practical_ml_ai/ | Shared Python processing, modeling and reporting code |
| data/ | Original fixtures, schemas and source manifests; downloaded external records stay in ignored runtime caches |
| docs/setup/ | Acquisition, environments, Python bridge and troubleshooting |
| docs/instructor/ | Adoption, assessment, pacing, alignment and learner-pilot guidance |
| templates/ | Reusable lesson, practice, data/model-card and review templates |
| tests/, scripts/, environments/ | Maintainer checks, build tools and tested dependency constraints |
| docs/maintenance/ | Repository hygiene and historical review evidence |

Generated site files, runtime results, environment folders, credentials, student submissions and private institutional planning sources do not belong in tracked course source. See the [inventory audit and retention rules](docs/maintenance/repository-hygiene.md).

## Instructors, contributors and help

Independent reviewers can use the [review guide](docs/review-guide.md). Start with [teach and adapt](docs/instructor/index.md), [assessment guidance](docs/instructor/assessment.md) and [pacing](docs/instructor/teaching-plan.md). The resource does not replace Canvas grading, deadlines, accommodations or official course policies. Pilot preparation and workload with your actual learners. Text/table and script routes support access; [accessibility status](docs/accessibility/index.md) records remaining human testing.

For a nonsensitive reproducible software problem, [open an issue](https://github.com/ntious/ml_ai_it/issues) with the module, environment, command and error text. Report accessibility barriers to [ntiik@ucmail.uc.edu](mailto:ntiik@ucmail.uc.edu); see the [reporting guide](docs/accessibility/index.md). Use the institution's established channels for course assessment or accommodation decisions.

Maintainers should use [DEVELOPMENT.md](DEVELOPMENT.md) for the separate core/framework test profiles, notebook verification, site assembly, archive checks and browser checks. Read [CONTRIBUTING.md](CONTRIBUTING.md), the [architecture](REPOSITORY_STRUCTURE.md) and [release checklist](docs/release-checklist.md) before extending the course. Students do not need the maintainer toolchain for their first lesson.

## Maintainer and license

Maintained by [Isaac K. Nti](https://github.com/ntious). Code is licensed under [MIT](LICENSE); original educational content is [CC BY 4.0 with component boundaries](OER_LICENSE.md). External datasets and models retain their own rights. Use [citation metadata](CITATION.cff) and cite the datasets/models used in your work.

## Authorship and course relationship

Isaac K. Nti developed these supplementary instructional materials for students in the University of Cincinnati course he teaches. The original explanations, activities, worked examples, code and supporting materials are distinguished from the university’s official course description, course learning outcomes and module learning outcomes, which he does not claim as his own. The resource supports those requirements; it does not replace the official syllabus. See [licensing and institutional boundaries](OER_LICENSE.md).
