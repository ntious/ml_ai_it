# Practical Machine Learning and AI Systems

A modular companion for independent learners and instructors linking lessons from Canvas or another platform. **Development edition 0.6.0 implements Modules 1–14.** Implementation and automated checks do not replace learner piloting, manual accessibility review, or production validation.

## Start and choose a route

Begin with [first run](QUICKSTART.md) or select a [module from the curriculum map](docs/modules.md). Each module provides outcomes, prerequisite support, commented shared-code scripts/notebooks, practice, public feedback, optional depth, and adaptation guidance.

Modules 1–5 establish concepts, Python, data processing/exploration, and regression. Modules 6–14 cover classification, clustering, TensorFlow, neural NLP, local LLMs, actual parameter-efficient fine-tuning, deployment/monitoring, fairness, and bounded agents.

**All new Modules 6–14 use actual external records and human labels.** [Sources, rights, reviewed hashes, and model revision](docs/data-sources.md) are documented. Earlier foundation fixtures remain labeled separately; no synthetic dataset is created for the remaining modules.

## Execution profiles

- Core: Python 3.12, NumPy/pandas/scikit-learn and plotting where needed. Windows/Linux execution is checked.
- Frameworks: a [separate Linux CPU environment](docs/setup/frameworks.md) for TensorFlow, PyTorch/Transformers, and Streamlit. Other framework platforms are unverified.
- Reading: static explanations and tables with actual verified reports. Interpretation alone does not demonstrate execution.

First downloads require internet; retain valid caches. Core routes require no paid API account or GPU. Tiny model checks can produce poor task results: failures remain visible in reports.

## Verification

Install the verification extra and register a matching kernel as described in [development setup](DEVELOPMENT.md). In the appropriate profiles:

~~~sh
python -m unittest discover -s tests -v
python scripts/check_notebook.py --group core --kernel ml-ai-core
python scripts/check_notebook.py --group frameworks --kernel ml-ai-frameworks
npm install --ignore-scripts
npm run build
npm run check
python scripts/check_downloads.py
~~~

CI explicitly enables framework tests, actual training/generation, adapter updates/reload, public scripts, app interactions, and HTTP health. Both notebook groups execute in fresh Jupyter kernels and retain executed copies. The site assembles their verified reports, checks links/structure, verifies original-source/data archives, exercises extracted source, builds a package, and exercises isolated installed-wheel inference.

See [DEVELOPMENT.md](DEVELOPMENT.md), commit-specific CI, [accessibility policy](ACCESSIBILITY.md), and [remaining limitations](docs/accessibility/index.md). HTML checks do not establish WCAG conformance; kernel execution does not establish interface usability.

Read the [architecture and inventory](REPOSITORY_STRUCTURE.md), [audit findings](REPOSITORY_REVIEW.md), and [release checklist](docs/release-checklist.md) for the implemented scope and pending human review.

## GitHub Pages website

The website provides a learning-path homepage, searchable reading pages, a module directory, lesson tabs, worked examples, downloads, and links to the exact source revision. [Preview and publishing instructions](docs/publishing.md) explain the tested artifact and manual Pages deployment workflow. GitHub Pages must be enabled in repository settings before a live URL exists.

## Teach and reuse

The resource's original activities do not require original Canvas tasks. Local grading and AI-use rules remain with adopting instructors. Student records, master documents, institutional branding, and restricted assessments are excluded.

Original code: [MIT](LICENSE). Original educational content: [CC BY 4.0 with component boundaries](OER_LICENSE.md). External data/model rights remain separate. [Instructor guide](docs/instructor/index.md).

The site build produces a reviewable artifact. Merging, publication, and visibility changes are separate actions.
