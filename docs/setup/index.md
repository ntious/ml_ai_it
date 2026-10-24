# Setup and execution routes

Start with the [first-run guide](../../QUICKSTART.md). Modules 1 and 2 need Python 3.11 or newer and no third-party libraries. Module 3 adds an isolated environment and NumPy/pandas. Each guide supplies commands, expected output, saving, and recovery steps.

## Current support status

- Local scripts: checked in Linux with Python 3.12. Modules 1 and 2 are also run with Python's site-package loading disabled to verify standard-library-only execution. Windows/Linux CI checks the expanded sequence after a push; inspect its commit-specific results. macOS is pending.
- Jupyter: three curated notebooks' plain Python cells are executed in fresh namespaces. Notebook interface, installation journey, and assistive-technology compatibility are not verified by this check.
- Codespaces: configuration is experimental; installation and first-run verification are pending.
- Colab: authorized private-repository access or source upload is required. The [source archive](../downloads/ml_ai_it-source.zip) includes code/data; retain the folder structure. Module 3 needs the extracted package installed in that runtime. This is an untested route, not one-click support.
- Binder: experimental requirements are included. Public mybinder.org cannot launch this private repository through an ordinary public-repository link. Revisit after public release authorization.

## Source and interfaces

Extract the [complete source archive](../downloads/ml_ai_it-source.zip) into a working folder. It contains an `ml_ai_it` directory with source, scripts, data, notebooks, reading content, and checks. A standalone notebook download does not include its shared imports.

The reading site is static HTML, not a browser Python runtime. The script route supplies named text and saved files for the same implementation used in the notebook. Review [accessibility status](../accessibility/index.md) before choosing an interface; test the actual editor/terminal/browser and assistive technology.

## Reading-site development

With Node.js 20 or newer and Python available on the command path:

```sh
npm install --ignore-scripts
npm run build
npm run check
python -m http.server 8000 --directory site
```

Here `python` denotes your project environment executable. Open `http://localhost:8000`. Edit Markdown under `docs/` and rebuild; `site/` is generated output. The build creates downloads from a source allowlist. It does not publish or change visibility.
