# Weekly external-resource maintenance

The `External links and pinned sources` workflow runs Mondays at 09:23 UTC and can be dispatched manually. GitHub schedules run from the default branch; merging the workflow is necessary before its schedule takes effect. This PR does not change repository visibility or deploy the site.

The standard-library script scans inline Markdown HTTP(S) links and angle-bracket autolinks in root Markdown, `docs/`, `projects/` and `templates/`. It removes fragments, deduplicates URLs, follows redirects and uses GET requests. Fenced code blocks are excluded; local development addresses and the documented TESTED_COMMIT placeholder are recorded as skipped. Bare prose URLs and reference-style Markdown links are outside this first checker’s scope. It does not verify remote fragment anchors, JavaScript-only navigation, citations embedded in notebooks or whether returned content still supports a claim. A successful HTTP response is reachability evidence only.

Each run freshly downloads all six UCI archives defined by the course's existing source constants: bike, wine, SMS, Adult, phishing and RT-IoT. The script streams bytes into SHA-256, caps download size and compares against the approved digest. It never edits a checksum, source or dataset. Checksum mismatches require a maintainer to investigate changes and licensing/provenance before a separate reviewed update.

Four concurrent requests, timeouts and up to three attempts bound the work. Transient failures are retried; the complete job has a 30-minute limit. Authentication failures, bot protection and rate limits can look like broken links. Private repository links and unpublished Pages links are expected to fail anonymously until publication; retain them in the report rather than claiming public access works.

The JSON artifact records URL, source location, outcome and observed digest where applicable. Failure opens one bot-owned issue with a stable title; later failures update it. A successful run closes that issue. The reporting job has issue-write permission; the check job has read-only repository access. No issues are opened by local tests or PR verification. If reporting itself fails, inspect the workflow failure; issue creation cannot be guaranteed when GitHub permissions or service availability prevent it.

Run locally with `python scripts/check_external_health.py`; use `--sources-only` for the six fresh archive checks. Results go under ignored `runs/`. Running this check does not publish data or approve a changed source.
