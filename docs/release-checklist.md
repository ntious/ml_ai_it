# Release and semester-adoption checklist

Use this record for an exact commit. A green workflow is necessary for technical integration, but it does not replace human accessibility review or authorize publication.

## Automated gates

- Registry covers 14 ordered modules; each has five teaching pages, one notebook, and one example script.
- All tracked Python parses; source notebooks validate and contain no saved execution state.
- Core Windows/Linux behavior passes; framework skips are reported separately.
- Linux CPU framework tests pass with actual learning, generation, adapter updates/replay, app forms, and health checks.
- Both notebook groups execute in fresh matching kernels, preserving executed copies.
- Site/report generation succeeds using actual outputs from both profiles.
- Every local page/link/fragment and defined semantic/table property passes.
- HTTP routes work under the project prefix, including downloads.
- Source archive membership equals tracked source, bytes match, extracted CLIs run, and external cache digests/attribution pass.
- Wheel builds in its declared build environment and performs isolated installed inference using real records and the runtime cache override.

Use the exact check names in the workflow. Constraints record exercised direct packages, not a complete transitive lock; do not claim offline installation from them alone.

## Human gates and owner decisions

- Record keyboard/screen-reader/zoom/reflow/contrast tasks and any effective alternatives in the [review log](accessibility/review-log.md).
- Inspect executed notebooks, report figures, tables, app errors/results, and downloadable outputs at reading size. Repair clipped labels, unreadable output, and unsupported conclusions.
- Pilot core work with learners; confirm prerequisites, pacing, feedback, and optional depth.
- Confirm the authoritative course-outcome crosswalk and locally adopted program criteria before formal assessment claims.
- Configure a private accessible reporting contact and document moderation responsibility.
- Check original/third-party rights and attribution; retain source and model identities.
- Select an approved semester edition and test learner permissions and direct links.
- Review current dependency advisories and updates through the institution's maintenance process; no security audit is implied by this educational review.
- Obtain the owner's release/deployment decision. Do not change visibility, merge, tag a public release, or enable Pages merely because the build passed.

## Build and inspect

Install the verification extra in each appropriate environment and register its kernel. Execute the core and framework commands separately. The site needs outputs from both profiles; use the complete workflow if both environments are not available on one machine.

~~~sh
python scripts/check_repository.py
python -m unittest discover -s tests -v
python scripts/check_notebook.py --group core --kernel ml-ai-core
python scripts/check_notebook.py --group frameworks --kernel ml-ai-frameworks
npm install --ignore-scripts
npm run build
npm run check
python scripts/check_http_routes.py
python scripts/check_downloads.py
python -m pip wheel . --no-deps --wheel-dir dist
python scripts/check_wheel.py
~~~

Framework tests require the ML_AI_HEAVY=1 environment setting and the dependencies in the framework guide; normal core discovery intentionally skips them. The workflow is the precise executable sequence.

For a local reading preview, serve site/ with python -m http.server --directory site 8000 and open the loopback address. The HTTP prefix checker separately tests /ml_ai_it/. Previewing is not a public deployment. Retrieve complete-reading-site and the verified execution artifacts from the successful workflow, then perform the manual tasks.

## Decision record

Record commit, workflow URL, test counts/skips, kernel/runtime versions, source/model hashes, manual review records, unresolved issues, owner, semester edition, and decision date. Use NOT RUN for missing evidence. A blocked human gate must not be converted into a pass by repeating automated checks.

## Website publication

Use the [GitHub Pages guide](publishing.md) for one-time settings, artifact preview, reviewed-run selection, and the manual publishing workflow. Check the home/module/search/download/404 browser routes and inspect the generated screenshots; passing browser assertions is not human visual review. Publication requires a successful default-branch run and matching embedded manifest.
