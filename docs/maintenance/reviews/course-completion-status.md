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
| Full CI run at `12e49bb` | GitHub Actions: Linux 3.12, Windows 3.12 and 3.13, Linux framework | All jobs pass, including the site build, 200 page checks, 349 HTTP routes, download and archive checks, the installed wheel and 10 browser tests |
| Unit tests at the branch head | Windows 11, Python 3.13, UTF-8 mode off | 132 OK, 11 skipped (framework tests; not a pass) |
| Repository, practice (16 core notebooks), lesson notebooks, phishing case, capstone | Same, fresh learner venv with the `ml-ai-core` kernel | Pass |
| Encoding regression | Same | Fails on unfixed `main`; passes on the branch |
| Full CI at the branch head | GitHub Actions | See PR #11; a later commit is verified only by its own run |

## Not verified

- WSL installation steps on a real Windows machine; macOS; native Windows framework execution (unsupported).
- Public availability of the site and downloads: the site is unpublished and the repository is private. Verify anonymously after the owner enables publication.
- Human learning, workload, notebook-interface usability and assistive-technology testing. These have not been performed by any technical check.

## Owner actions before student delivery

1. Decide repository visibility and publication; then complete section J of the owner review guide from a signed-out browser.
2. Plan the future single-source refactor for exercise contracts (item N2 in section M).
3. Run the learner pilot and accessibility sessions, and revise workload estimates from observed evidence.
