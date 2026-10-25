# Obtain and navigate the student workspace

Use the public repository or the complete source archive supplied for your class. No GitHub account is needed to download, read or run the course.

## Download route

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

If you already use Git, clone https://github.com/ntious/ml_ai_it.git, then change into ml_ai_it. Downloaded archives do not have Git history and do not require Git for learning.

## Open a notebook

Install the core environment and notebook interface using first run. Launch the interface with that environment's Python. In the browser file list, open notebooks/lessons and the selected module. Run cells in order with Shift+Enter, save with Ctrl+S or the File menu, then restart the kernel and run all. Download your saved notebook and results before leaving an ephemeral hosted session.

## Reading reports from GitHub

Open the [published reading site](https://ntious.github.io/ml_ai_it/). It contains every lesson page plus the worked reports, executed notebook copies and the [complete source archive](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip"), rebuilt by CI from each checked commit on main. Report, notebook and archive links in the lesson source on GitHub open the matching file on that site. Running the public scripts locally produces the same report format from real execution. If the site is temporarily unavailable, maintainers and reviewers can download the complete-reading-site artifact from a successful Learning resource checks run under Actions, extract it and open index.html.

Do not build the entire site just to study one module. Site assembly is a maintainer workflow requiring both notebook execution profiles. See [troubleshooting](troubleshooting.md) for common errors.
