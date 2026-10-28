# Security policy

This repository is an open learning resource. Its code runs on learners' own computers, so security problems matter even though nothing here is a hosted service.

## Report a vulnerability

Please report security problems privately, not in a public issue or discussion:

- Use **Report a vulnerability** on the repository's [Security tab](https://github.com/ntious/ml_ai_it/security), or
- email ntiik@ucmail.uc.edu with "Security" in the subject.

Include the file or command involved, what an attacker could do, and steps to reproduce. You will receive an acknowledgement, and fixes are made on `main`. This is a single-maintainer course resource, so responses are best effort rather than a guaranteed timeline.

Do not include personal data, student records or credentials in a report.

## Supported version

Only the current `main` branch is maintained. Older commits and archived reports are kept for reproducibility, not security support.

## What is in scope

- Code in `src/`, `scripts/`, `examples/`, `apps/` and `projects/`, including the data downloaders and the local API and app.
- The GitHub Actions workflows in `.github/workflows/`.
- Anything that could expose a learner's files, credentials or computer when they follow the documented instructions.

Weaknesses in the teaching models themselves, such as poor accuracy or biased results, are teaching material, not vulnerabilities; please open an ordinary issue for those.

## How the course limits risk

- Datasets are downloaded from the UCI Machine Learning Repository, size-limited, and checked against a reviewed SHA-256 before use. A changed source stops with an error.
- The language model is loaded from one pinned revision, in the `safetensors` format, with `trust_remote_code=False`.
- The documented commands start the local API and the Streamlit app on `127.0.0.1` only (the app needs `--server.address 127.0.0.1`, as shown in Module 12). Neither has authentication; do not expose them to a network.
- No credentials, tokens or paid services are needed, and none are stored in this repository.

## Known advisories in the framework environment

The optional framework environment (Modules 8–12 and 14) pins `transformers 4.46.3`, `torch 2.6.0` and `streamlit 1.44.1` so that recorded results stay reproducible. These versions have published advisories. Most concern loading untrusted models or checkpoints, model families the course does not use, or the `Trainer` class, which the course does not use. The course loads only the pinned model and runs the app locally.

Use this environment on your own computer for the course activities only. Do not load models or checkpoints from untrusted sources with it, and do not expose the app or API to other machines. Upgrading these pins is planned; it needs the framework results to be re-run and re-recorded. The core environment (Modules 1–7 and 13) has no known advisories at the time of writing.
