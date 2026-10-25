# Repository inventory and retention rules

Audit date: October 25, 2026. Scope: the 228 tracked files at main commit 3f2eba09a6e8d5a6ed546c8ba89b69a1af7b9b0b, plus this documentation cleanup. The GitHub tree and local tracked inventory agreed. Ignored working files were distinguished from published source.

## Findings and actions

No tracked private institutional source documents, runtime output folders, installed environments, downloaded model caches, dependency folders or executed notebook outputs were found. A targeted scan found no common GitHub-token/AWS-key/private-key patterns; this is repository hygiene evidence, not an exhaustive security audit or a guarantee of absence of secrets.

Two historical review reports were legitimate maintainer evidence but distracting in learner entry paths. They now live under maintenance/reviews, labeled with the edition they describe. Links, the site builder and source-download policy were updated. The baseline report's chat-specific wording was removed; historical execution details remain labeled as historical.

The private local documentations folder was already excluded by the local Git configuration and source-archive allowlist. Its exclusion is now shared in .gitignore so another checkout receives the same default. The documents themselves remain local and are not redistributed.

The README was rewritten around audience, learning goals, a first successful run, execution choices, module map, learning workflow, help and reuse. This adopts the learner-oriented organization of Python Foundation while preserving this repository's actual platform/access limits.

## Keep, generate or exclude

| Material | Policy and reason |
| --- | --- |
| Lesson source, clean notebooks, shared code and examples | Track: required to teach, run and adapt the resource |
| Tests, CI workflow, constraints and package-lock.json | Track: required to reproduce and validate the source |
| .binder and .devcontainer configuration | Track: execution configuration; presence alone is not live service verification |
| LICENSE, OER_LICENSE.md, CITATION.cff and source manifests | Track: rights, attribution and provenance |
| Accessibility, conduct, contribution and release guidance | Track: access, support and maintenance responsibilities |
| Historical audit records | Retain in maintainer archive; do not present historical counts as current status |
| site, runs, build, dist, node_modules and Python environments | Generate locally/CI and ignore; do not commit runtime artifacts |
| Downloaded data/models | Keep in ignored caches; distribute only through attributed, verified artifact packaging |
| Private planning documents, official source attachments, student submissions and credentials | Exclude from tracked source and publication |

## Repeat the check

Use git ls-files for publication scope and git status --ignored when diagnosing local-only files. Run scripts/check_repository.py, which verifies clean notebook cells and allowlisted tracked paths, and source/site link checks after moving documentation. Archive verification must match tracked source membership and bytes. Review unfamiliar additions by purpose and content; a matching extension alone does not establish suitability or permission to publish.

For current functionality and known limits, use [status](../status.md). Historical evidence: [baseline 0.6.0](reviews/baseline-0.6.0.md) and [learning support 0.7.0](reviews/learning-support-0.7.0.md).
