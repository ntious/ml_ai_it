# Course completion work record

This work extends the three-module teaching prototype to all 14 modules and applies the October 2026 independent-review corrections (F1–F14). Learning outcomes remain unchanged; the practice checker verifies their text for all 14 modules.

## Implemented

- Separate concepts, starter notebooks, solutions and diagnostic checks for every module. Modules 1–4, 7 and 9–14 have module-specific explanations and reasoning tasks; Modules 5, 6 and 8 keep the fuller prototype with real-data sandboxes.
- An offline access route and a source-only archive build for when the reading site or the private repository is unavailable.
- One kernel name per profile, ordered notebook setup steps and a WSL route for framework modules on Windows.
- A validation-based RT-IoT policy comparison, including constant review policies.
- A worked primary-study comparison in the research guide.
- Fairness report interval columns with rate-specific denominators, small-denominator flags and explicit conditional assumptions.

Each finding's disposition, evidence and remaining action is in section M of the [owner review guide](owner-review-guide.md).

## Verification evidence (October 28, 2026)

| Check | Environment | Result |
| --- | --- | --- |
| Full CI run 40697234797 at `f23e804` | GitHub Actions: Linux 3.12, Windows 3.12 and 3.13, Linux framework (2 vCPU, 7.9 GB RAM) | All jobs pass, including the site build, 200 page checks, 349 HTTP routes, 356 byte-matched source files, download and wheel checks and 10 browser tests. Framework tests took 71 of their 90 allowed minutes |
| Unit tests at `f23e804` | Windows 11, Python 3.13, UTF-8 mode off | 135 OK, 11 skipped (framework tests; not a pass) |
| Repository, practice (16 core notebooks), lesson notebooks, phishing case, capstone | Same, fresh learner venv with the `ml-ai-core` kernel | Pass |
| Encoding regression | Same | Fails on unfixed `main`; passes on the branch |
| Later commits | GitHub Actions | Verified only by their own run |

## Not verified

- WSL installation steps on a real Windows machine; macOS; native Windows framework execution (unsupported).
- Public availability of the site and downloads: verify from a signed-out browser after the repository is made public and the site is deployed.
- Human learning, workload, notebook-interface usability and assistive-technology testing. These have not been performed by any technical check.

## Further improvements (stacked PRs, October 28, 2026)

| PR | Scope | Local verification |
| --- | --- | --- |
| #12 | Archive built from tracked files; learner-first navigation and maintainer hub; shared rubric in the study workflow; self-checks; core stability exercise; complete-study exercises; Windows site-build path fix | 144 tests; site build, page, route, download and all 10 browser checks |
| #13 | Module 3 categorical encoding and Module 6 bounded tuning with gradient boosting | 150 tests; site build, page and download checks |
| #14 | Module 10 evaluated retrieval, Module 12 JSON API, experiment tracking, learning paths, IT case thread, what's new and community pages | Recorded in PR #14 |

Each PR's own CI run is the authoritative check. Deferred until learner evidence exists, as agreed: consolidating to one deep-learning framework, making hosted notebooks the default, and restructuring module pages.

## Public-readiness security review (October 28, 2026)

Scope: all 78 commits including the 17 retained pull-request refs (1,409 file versions), every PR description and review comment, repository settings, workflows, pinned dependencies and code patterns.

- No secrets, tokens, keys or passwords in any file version; all commits use the GitHub no-reply address.
- No institutional material: the private `documentations/` folder was never committed, and none of its syllabus, module texts or final-project documents shares a 10-word passage with any committed file.
- Workflows: no `pull_request_target`, read-only default token, write scopes limited to deploy, branch cleanup and issue creation; the release workflow validates its inputs.
- Dependencies: core and site tooling have no known advisories. The framework pins (`transformers 4.46.3`, `torch 2.6.0`, `streamlit 1.44.1`) have advisories of low exploitability for the course's pinned, local use; documented in `SECURITY.md`, upgrade planned.
- Hardened: a data source without a reviewed checksum, or a model without a pinned revision, is now refused instead of being used unverified.

## Owner actions before student delivery

1. Decide repository visibility and publication; then complete section J of the owner review guide from a signed-out browser.
2. Plan the future single-source refactor for exercise contracts (item N2 in section M).
3. Run the learner pilot and accessibility sessions, and revise workload estimates from observed evidence.
