# Practical Machine Learning and AI Systems

Learn to frame problems, implement reliable workflows, evaluate evidence, and explain decisions. These original educational resources support independent learners and instructors linking a single module from Canvas or another learning platform.

**Development edition 0.4.0:** Modules 1–5 are implemented. Follow them in order if you are new to Python and ML; use a direct module link if you already have its prerequisites. Modules 6–14 and deployment cases remain in development.

## Start here

1. Follow the [first-run guide](QUICKSTART.md): the first two modules need only Python, with no third-party package installation.
2. [Module 1: ML and AI foundations](docs/lessons/01-foundations/index.md): compare methods, run a written rule, predict a change, and save a result.
3. [Module 2: Python for reproducible workflows](docs/lessons/02-python-workflows/index.md): process synthetic CSV/JSON files with functions and labeled summaries.
4. [Module 3: Data processing](docs/lessons/03-data-processing/index.md): install NumPy/pandas, validate events, and explain accepted/rejected records.
5. [Module 4: Exploration and visual communication](docs/lessons/04-exploration/index.md): add the visualization extra, create labeled plots, and communicate evidence through paired tables/descriptions.

6. [Module 5: Regression and reliable evaluation](docs/lessons/05-regression/index.md): train real pipelines, audit forecast-time features, compare baselines, freeze selection, and evaluate/infer separately.

Each module has a script route, a notebook using the same implementation, original practice/discussion, public worked feedback, and adaptable criteria. Modules 1–4 establish foundations and data processing. Module 5 trains scikit-learn models on real, attributed UCI data with an explicit forecasting protocol; no AI service is called.

## Repository contents

- `src/practical_ml_ai/`: reusable implementation.
- `examples/`: thin command-line entry scripts.
- `data/`: original synthetic samples, contracts, and external-data provenance. Downloaded UCI originals remain under ignored `runs/` with attribution/checksums.
- `notebooks/lessons/`: guided walkthroughs calling shared functions.
- `docs/`: reading-site source, practice, feedback, setup, and adoption guidance.
- `tests/`: behavior and script checks.
- `scripts/`: site/download generation and validation.

See [development status](docs/status.md) for the verified scope and [accessibility requirements](ACCESSIBILITY.md) for authoring expectations. Semantic HTML, a skip link, text-first explanations, and script alternatives are implemented. Manual keyboard, screen-reader, and zoom/reflow testing remain pending; accessibility conformance is not claimed.

## Development checks

Install the package with its regression and visualization extras as explained in the first-run guide, then run:

```sh
python -m unittest discover -s tests -v
python scripts/check_notebook.py
npm install --ignore-scripts
npm run build
npm run check
python scripts/check_downloads.py
```

Here `python` is your project environment's executable. Module 5's notebook and worked-site report require the first public-data download (subsequent runs reuse a verified cache); see its setup. CI additionally enables the real-data integration test. The static reading site does not execute notebooks in the browser. CI builds and checks a downloadable site artifact on Windows and Linux. GitHub Pages deployment is not enabled; no live site is implied.

## Teaching and reuse

No original Canvas assignments, student records, university branding, or master course documents are included. Instructors select activities and publish local assessment and AI-use rules. See the [instructor guide](docs/instructor/index.md). Optional depth is clearly labeled and skippable.

Original code: [MIT](LICENSE). Original educational prose and synthetic data: [CC BY 4.0 with component boundaries](OER_LICENSE.md). External documentation, dependencies, and services retain their own terms.
