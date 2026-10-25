# Development status

Edition 0.7.0 implements all 14 modules with original teaching content, commented notebooks, shared scripts, practice/feedback, optional depth, and instructor guidance. Learner piloting and manual accessibility review remain necessary.

The [architecture](../REPOSITORY_STRUCTURE.md) and [audit record](maintenance/reviews/baseline-0.6.0.md) describe the registry-backed inventory, added authoring/adoption resources, and verification limits.

## Real sources and actual computation

New Modules 6–14 use UCI Wine Quality, SMS Spam Collection, and Adult. Original files, attribution, reviewed archive hashes, transformations, and a fixed local-model revision are documented. Earlier foundation fixtures remain labeled separately.

Actual TensorFlow training/reload, local generation, real adapter gradients/replay, app interactions/server health, and bounded model-based tool routing are implemented. No mocked model output or invented training records substitute for those demonstrations.

## Verification scopes

Core tests/notebooks execute on Windows/Linux; framework tests/notebooks execute on Linux CPU. Framework tests skipped in the smaller core environment are explicitly executed in the separate job. Both notebook groups execute in fresh Jupyter kernels with saved executed copies and must pass before site assembly.

The final integration run checks actual report artifacts, generated links/structure, source/data ZIPs, extracted CLI execution, project-prefix HTTP routes, package building, and isolated installed-wheel inference. Exact evidence is recorded in DEVELOPMENT.md and commit-specific CI.

## Observed limitations

The small neural NLP run missed all positives. The initial free-text LLM run failed the exact JSON contract on all eight cases. Those failures remain visible; they are not repaired into credited success. The tiny adapter experiment establishes gradient/replay mechanics, not deployable quality.

Adult results are descriptive audits, not justified decisions about people. Batch replay order is not a measured timeline. A constrained legal tool plan may still misunderstand intent.

Selected scripted browser checks cover skip-link focus, 320-pixel reflow and automated accessibility rules on five reading pages, including the course overview. Human keyboard, screen-reader, real zoom, notebook/app usability, macOS, Windows framework and live hosted routes remain pending. Automated execution does not certify accessibility or production readiness.

Merging, GitHub Pages publication, and visibility changes remain separate release actions.

See the [enhancement record](maintenance/reviews/learning-support-0.7.0.md) for Python preparation, construction practice, authentic IT and current verification scope.
