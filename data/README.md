# Data boundaries and provenance

Tracked data/ contains contracts, manifests, and explicitly labeled small introductory teaching fixtures. It does not contain real operational student/user records.

## Real sources

Module 5 downloads UCI Bike Sharing. Modules 6–14 use reviewed UCI Wine Quality, SMS Spam Collection, or Adult records. See [sources and rights](../docs/data-sources.md) for citations, licenses, hashes, model identity, and transformations.

Preserve original archive bytes, named members, attribution, retrieval metadata, and digests together. A changed reviewed hash is an error requiring review. Do not silently replace a source or invent synthetic records while describing them as measured.

## Runtime storage

External datasets/models belong in generated ignored caches, separate from original-source distribution. In a checkout the later modules default to runs/. Installed packages use a user cache; ML_AI_RUNS_DIR overrides that cache location when set before import. Explicit run-output paths remain separate.

Source downloads contain original code/teaching fixtures/contracts; external-data cache ZIPs retain their own attribution. Model weights are not silently bundled in the source archive.

## Adaptations

Document observation, units, target/labels, privacy, missingness, duplicates, availability, transformations, and split. Fit learned preprocessing on training data only. Use real permitted sources for new applied illustrations. Keep any synthetic control unmistakably labeled and separate from operational claims.

Public SMS can include personal content; process locally and use bounded de-identified evidence. Historical income categories do not authorize decisions about people. Never add student records, credentials, private logs, or restricted assessments.
