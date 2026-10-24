# Practical Machine Learning and AI Systems

Learn to inspect data, implement reliable workflows, evaluate results, and explain decisions. These original educational resources support independent learners and instructors who want to link a single module from Canvas or another learning platform.

**Development edition 0.1.0:** Module 3, Data Processing, is the first implemented module. The remaining modules and prediction/deployment cases are planned; they are not advertised as available lessons.

## Start here

1. Follow [setup and first run](QUICKSTART.md).
2. Read [Module 3](docs/lessons/03-data-processing/index.md).
3. Run the separated preparation script or the [guided notebook](notebooks/lessons/03-data-processing/complete_walkthrough.ipynb). Both call the same Python functions.
4. Complete the module's original practice and inspect its worked feedback.

The example interprets synthetic authentication-gateway and network-monitor events. It validates records, records reasons for rejection, preserves missing latency, and produces CSV, JSON, and plain-text results. It performs no ML training and makes no claims about real network performance.

## Repository contents

- `src/practical_ml_ai/`: reusable implementation.
- `examples/network-events/scripts/`: thin command-line entry point.
- `data/`: synthetic sample, data contract, and provenance.
- `notebooks/`: runnable walkthrough calling shared functions.
- `docs/`: reading-site source, practice, setup, accessibility, and adoption guidance.
- `tests/`: behavior and clean-run checks.
- `scripts/`: site/download generation and validation.

See [development status](docs/status.md) for the exact verified scope. See [accessibility requirements](ACCESSIBILITY.md): keyboard/screen-reader and third-party runtime testing remain to be completed. The site uses semantic HTML, a skip link, text-first explanations, and named results; those choices alone do not establish accessibility conformance.

## Development checks

```sh
python -m unittest discover -s tests -v
python scripts/check_notebook.py
npm install --ignore-scripts
npm run build
npm run check
```

The site is generated from trusted local Markdown using a small Marked-based builder. It is static reading content; it does not execute notebooks in a browser. GitHub Pages deployment is deliberately not enabled in this first private development increment. The CI workflow builds and checks an artifact.

## Teaching and reuse

The public resource has its own activities, discussion prompts, feedback, and an adaptable rubric. No original Canvas assignments, student records, university branding, or master course documents are included. Adopting instructors choose which activities to use and publish their own assessment/AI-use rules. [Instructor guide](docs/instructor/index.md)

Original code: [MIT](LICENSE). Original educational prose and synthetic sample data: [CC BY 4.0 with component boundaries](OER_LICENSE.md). External documentation, dependencies, and services retain their own terms.
