# Setup and execution routes

Start with the [first-run guide](../../QUICKSTART.md). Modules 1 and 2 need Python 3.11 or newer and no third-party libraries. Module 3 adds an isolated environment and NumPy/pandas. Module 4 adds Matplotlib/Seaborn using the visualization extra. Module 5 adds scikit-learn through the regression extra and a public-data cache. Each guide supplies commands, expected output, saving, and recovery steps.

## Current support status

- Local scripts: checked in Linux with Python 3.12. Modules 1 and 2 are also run with Python's site-package loading disabled to verify standard-library-only execution. Windows/Linux CI checks the expanded sequence after a push; inspect its commit-specific results. macOS is pending.
- Jupyter: five curated notebooks' plain Python cells are executed in fresh namespaces. Notebook interface, installation journey, and assistive-technology compatibility are not verified by this check.
- Codespaces: configuration is experimental; installation and first-run verification are pending.
- Colab: authorized private-repository access or source upload is required. The [source archive](../downloads/ml_ai_it-source.zip) includes code/data; retain the folder structure. Modules 3–5 need the extracted package installed in that runtime. Module 4 needs visualization; Module 5 needs regression and optionally visualization. This is an untested route, not one-click support.
- Binder: experimental requirements are included. Public mybinder.org cannot launch this private repository through an ordinary public-repository link. Revisit after public release authorization.

## Source and interfaces

Extract the [complete source archive](../downloads/ml_ai_it-source.zip) into a working folder. It contains an `ml_ai_it` directory with source, scripts, data, notebooks, reading content, and checks. A standalone notebook download does not include its shared imports.

The reading site is static HTML, not a browser Python runtime. The script route supplies named text and saved files for the same implementation used in the notebook. Review [accessibility status](../accessibility/index.md) before choosing an interface; test the actual editor/terminal/browser and assistive technology.

## Reading-site development

The site build generates Modules 4–5 reports from shared code. Install `python -m pip install -e ".[visualization,regression]" -c environments/constraints-tested.txt` first. Module 5 downloads the reviewed UCI archive if no valid cache exists; its download command can populate that cache before an offline build. Then, with Node.js 20 or newer and the environment Python on the command path:

```sh
npm install --ignore-scripts
npm run build
npm run check
python -m http.server 8000 --directory site
```

Here `python` denotes your project environment executable. Open `http://localhost:8000`. Edit Markdown under `docs/` and rebuild; `site/` is generated output. The build creates downloads from a source allowlist. It does not publish or change visibility.
