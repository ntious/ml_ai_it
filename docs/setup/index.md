# Setup and execution routes

Start with the [first-run guide](../../QUICKSTART.md). It has explicit Windows PowerShell and macOS/Linux commands, expected output, and saving/troubleshooting steps.

## Current support status

- Local Python: the data example and software tests have been exercised in the recorded Linux/Python 3.12 development environment. Windows/macOS require verification; a CI workflow is included to exercise Windows and Linux after a push.
- Jupyter notebook: the curated Python cells are checked sequentially in a clean process. Notebook UI and assistive-technology compatibility have not been verified.
- Codespaces: configuration is included as an experimental route, with installation and first-run verification still required.
- Colab: a private repository requires authorized access or a source upload. The [source archive](../downloads/ml_ai_it-source.zip) includes code/data; unzip it, install the extracted package in that runtime, and open the notebook. This route has not been tested and is not represented as one-click support.
- Binder: the experimental requirements are included, but public mybinder.org cannot use this private repository as a normal public launch. Revisit and test when a public release is authorized.

No launch badge is used to imply an unverified route works.

## Source archive

The [downloadable source archive](../downloads/ml_ai_it-source.zip) contains an `ml_ai_it` folder. Extract its contents into a working folder. It includes the package, sample, scripts, notebook, reading source, and checks. Installation still requires the declared Python dependencies.

## Accessibility

Read [accessibility status](../accessibility/index.md) before selecting an execution interface. The shared script offers the same data decisions and result evidence as the notebook. Test the actual screen-reader/browser/editor combination; no hosted provider's accessibility is assumed.

## Reading-site development

With Node.js 20 or newer and Python available on the command path:

```sh
npm install --ignore-scripts
npm run build
npm run check
python -m http.server 8000 --directory site
```

Open `http://localhost:8000`. `site/` is generated output. Edit source Markdown under `docs/` and rebuild. Building creates downloads from an explicit source allowlist. It does not publish or change repository visibility.
