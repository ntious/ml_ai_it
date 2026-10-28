# Obtain and navigate the student workspace

Use a repository checkout or the complete source archive supplied for your class. Running the downloaded course locally does not require a GitHub account.

## If a download link does not open

Lesson pages link to downloads on the reading site. Until the site is published, those links return "404 Not Found". The GitHub repository is also visible only to people the owner has given access to. Nothing is wrong with your computer; use the route below.

1. **Get the complete course source.** Ask your instructor for the course source archive, `ml_ai_it-source.zip`, through the course's usual file channel (for example Canvas). If you have been given repository access, the download route below gives the same files. Extract the archive and keep its folder structure.
2. **Use the in-source copy of each download.**

| Link on a lesson page | Where it is in the source, or how to produce it |
| --- | --- |
| Complete source archive | The archive from step 1 |
| Module notebook | `notebooks/lessons/<module folder>/`, for example `notebooks/lessons/05-regression/regression.ipynb` |
| Practice or solutions notebook | `notebooks/practice/moduleNN-practice.ipynb` and `moduleNN-solutions.ipynb` |
| Worked report (`example/index.html`) | Run the module's command; open `index.html` in the output folder you named |
| Executed notebook copy | Open the source notebook, restart the kernel and run all cells |
| Sample data and schemas | `data/samples/` and `data/schemas/` |
| Attributed data cache | The module's download command saves the same files under `runs/datasets/` and checks them against the reviewed checksums |
| Capstone notebook or report | `projects/phishing-triage/notebooks/complete-study.ipynb`; run it to produce the report |

Instructors can build the archive from a checkout with `python scripts/build_downloads.py --source-only ml_ai_it-source.zip`. It contains only the published source allowlist, with no run outputs, caches or environments.

## Download route

Use this route only if you have been given access to the repository.

1. Open [the repository](https://github.com/ntious/ml_ai_it).
2. Choose Code, then Download ZIP. Extract the archive; opening the compressed view is insufficient.
3. Open the extracted folder containing README.md, pyproject.toml, examples and data. Its download name may include main; commands work from that folder regardless of its name.
4. On Windows, open Terminal/PowerShell in that folder. On Linux/macOS, open a terminal and use cd followed by the folder path. Quote paths containing spaces.
5. Run the folder check below, then follow [first run](../../QUICKSTART.md).

Windows PowerShell:

```powershell
Get-Location
Get-ChildItem
py --version
py examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

Linux/macOS:

```sh
pwd
ls
python3 --version
python3 examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

Expected result: Review storage. Find runs/module01/first-run.txt in the same extracted project. Change 85 to 70, save to another output filename and explain the changed decision.

## Git route

If you already use Git and have repository access, clone https://github.com/ntious/ml_ai_it.git, then change into ml_ai_it. Downloaded archives do not have Git history and do not require Git for learning.

## Open a notebook

Install the core environment and notebook interface using first run. Launch the interface with that environment's Python. In the browser file list, open notebooks/lessons and the selected module. Run cells in order with Shift+Enter, save with Ctrl+S or the File menu, then restart the kernel and run all. Download your saved notebook and results before leaving an ephemeral hosted session.

## Reading reports from GitHub

The [reading-site address](https://ntious.github.io/ml_ai_it/) is the publication target for lesson pages, worked reports, executed notebook copies and the [complete source archive](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip"). These links become available after the owner enables publication and the first deployment succeeds. CI builds the complete site from checked source; building it does not itself publish it.

Before deployment, use the complete site archive supplied for your review or class. Maintainers and reviewers with access can also download the complete-reading-site artifact from a successful Learning resource checks run under Actions, extract it and open index.html. That fallback may require GitHub authentication and artifacts have limited retention. Running the scripts locally produces the same report format from real execution. After deployment, report, notebook and archive links in the lesson source open the matching files on the reading site without an Actions-artifact download.

Do not build the entire site just to study one module. Site assembly is a maintainer workflow requiring both notebook execution profiles. See [troubleshooting](troubleshooting.md) for common errors.
