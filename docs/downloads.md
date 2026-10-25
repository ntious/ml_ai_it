# Downloads and runnable resources

Choose the complete source when you want to run or adapt the course. A notebook on its own does not install the shared package, dependencies, or data.

## Complete project

[Download the complete source ZIP](downloads/ml_ai_it-source.zip). Extract it, keep its folder structure, and follow [first-run setup](../QUICKSTART.md). It includes the Python package, all module scripts/notebooks, teaching pages, contracts, fixtures, tests, and authoring templates.

The GitHub links on each reading page identify its exact source revision. Use a tested commit or semester edition when adapting.

## Notebooks

Start with a clean source notebook when working through the steps. Use the executed copy to inspect saved outputs without rerunning. Executed copies come from the actual verified CI kernels, not invented results. Their saved presentation still requires manual review.

<!-- NOTEBOOK_DOWNLOADS -->

On GitHub, the source notebooks are in notebooks/lessons/. The built site supplies the individual download links above. Keep a notebook inside the complete source tree when running locally.

## Reviewed external data caches

Initial data downloads require internet. These separately attributed caches preserve the reviewed original archive/member bytes and provenance. Follow the module's cache instructions rather than scattering extracted files into its source.

- [Bike Sharing cache, Module 5](downloads/module05/bike-sharing-cache.zip)
- [Wine Quality cache](downloads/wine-cache.zip)
- [SMS Spam Collection cache](downloads/sms-cache.zip)
- [Adult benchmark cache](downloads/adult-cache.zip)

Read [source rights and provenance](data-sources.md) before reuse. Public messages and historic demographic labels have privacy and interpretation limits. Model weights are not bundled in the source ZIP.

## Choose an execution environment

Modules 1–2 can start with Python alone. The [core setup](setup/index.md) supports data processing and classical ML. TensorFlow, local language models, and the app use the [separate framework environment](setup/frameworks.md), currently verified on Linux CPU.

Use scripts and text/table reports when they fit your access needs. Reading a saved result is useful preparation but does not itself demonstrate implementation.
