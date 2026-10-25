# Setup and execution routes

Begin with [workspace acquisition](student-workspace.md), [Python preparation](python-bridge.md), [environment choices](hosted.md) and [troubleshooting](troubleshooting.md).

Use [first run](../../QUICKSTART.md) for foundational commands. Modules 6, 7, and 13 use core regression dependencies. Modules 8–12 and 14 use the [separate CPU framework environment](frameworks.md).

## Support and evidence

- Core execution: Python 3.12 on Windows/Linux and Python 3.13 on Windows.
- Framework execution: isolated Linux CPU actual training/inference/app checks. Use the Linux CPU reference for framework work.
- Notebooks: curated cells execute in fresh namespaces; interface and assistive-technology behavior need separate manual checks.
- Hosted routes: choose a provider that can access the complete source and supplies a matching runtime. Validate the selected module in that session; provider execution is outside the recorded CI platform scope.
- Reading: static explanations, tables, and actual verified reports; no browser Python execution is implied.

The [original-source ZIP](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") includes scripts, notebooks, shared implementation, and the app. A notebook alone lacks imports. External data/model caches are separate and retain [provenance](../data-sources.md).

## Full site reproduction

The build requires reports from both notebook groups, retained in runs/verified. It fails rather than inventing missing results. Follow [framework setup](frameworks.md) for the full sequence.

CI assembles complete-reading-site only after core/framework execution succeeds, then checks links, structure, archives, extracted source, and package building. Use the resulting artifact directly or serve it through your chosen hosting process. Review [accessibility status](../accessibility/index.md) before requiring an interface.
