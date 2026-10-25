# Choose an execution environment

The default executable reference is Linux CPU, Python 3.12. Core workflows also run on Windows in CI. Hosted account creation, provider quotas, private-repository access and assistive-technology interfaces need separate verification; a configuration or launch link does not establish live service usability.

| Route | Core | Framework modules 8–12 and 14 | Saving and limits |
| --- | --- | --- | --- |
| Local Linux CPU | Automated execution reference | Separate environment tested | Persistent files; allow download space and memory |
| Local Windows | Core CI exercised | Installation recipe; no complete platform claim | Use explicit environment executable |
| Local macOS | Recipe; unverified platform | Unverified | Use instructor support if installation fails |
| Codespaces | Core devcontainer configured | Run framework bootstrap in a separate environment | Account/access/usage allowance required; download work before deleting workspace |
| Colab | Import complete source and core bootstrap | Conditional separate-kernel setup, unverified hosted execution | Upload/archive access needed for private source; download runs and notebooks |
| Binder | Core requirements configured | Heavy frameworks excluded | Public source required by ordinary launch; ephemeral and quota-dependent |

## Codespaces

With repository access, choose Code, Codespaces, Create codespace. The checked-in devcontainer installs the core dependencies and notebook kernel. Open the desired notebook and select the installed Python. Run `python scripts/preflight.py --profile core`. To use frameworks in the Linux terminal, run `python scripts/bootstrap.py --profile frameworks`, then select the ml-ai-frameworks kernel. This installs several large packages; review your provider's available resources first.

## Colab

Obtain the complete source ZIP through the authenticated GitHub download route, upload it using Colab's Files panel, and extract it. Never embed an access token in a notebook. In a notebook cell, use pathlib to find the folder containing pyproject.toml, then os.chdir into it. In the runtime's Python, run `!python scripts/bootstrap.py --profile core --current`. Restart the session if existing imported packages were changed, then rerun setup and open the course notebook in that complete tree. Colab's default package/kernel versions change; validate preflight and the selected module before assigning this route. The local separate-venv framework recipe does not automatically switch Colab's kernel.

## Binder

An ordinary mybinder.org GitHub launch needs public source. While this repository remains private, use the instructor's authorized workspace or a cleared source distribution; do not make the repository public as a workaround. The .binder requirements install only the core profile. Binder build success, capacity and interface accessibility remain service checks. Save notebooks and runs outside the session before it closes.

## Local setup

Follow [workspace acquisition](student-workspace.md), [first run](../../QUICKSTART.md) and [framework setup](frameworks.md). A report-reading route can support interpretation, but required implementation outcomes need actual execution through an effective interface. [Preflight and troubleshooting](troubleshooting.md) support all routes.
