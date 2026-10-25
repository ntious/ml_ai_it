# Obtain and navigate the student workspace

Repository access may require your instructor's GitHub invitation. Never request or share another person's credentials. A private repository cannot be launched anonymously by a public notebook service.

## Download route

1. Open [the repository](https://github.com/ntious/ml_ai_it) while signed into an account with access.
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

If you already use Git, clone https://github.com/ntious/ml_ai_it.git, then change into ml_ai_it. Authentication is required while the repository is private. Downloaded archives do not have Git history and do not require Git for learning.

## Open a notebook

Install the core environment and notebook interface using first run. Launch the interface with that environment's Python. In the browser file list, open notebooks/lessons and the selected module. Run cells in order with Shift+Enter, save with Ctrl+S or the File menu, then restart the kernel and run all. Download your saved notebook and results before leaving an ephemeral hosted session.

## Reading reports from GitHub

Relative downloads links in lesson source refer to the generated reading site. They are not tracked files in GitHub. Until an instructor distributes a hosted reading site, use Actions, select a successful Learning resource checks run, and download complete-reading-site from its artifacts. GitHub sign-in and repository access are required. Artifacts expire under the repository's retention policy. Extract it and open index.html; the site includes worked reports and source/notebook downloads. If the artifact expired, ask the maintainer for a rebuilt copy. Running the public scripts locally produces the same report format from real execution.

Do not build the entire site just to study one module. Site assembly is a maintainer workflow requiring both notebook execution profiles. See [troubleshooting](troubleshooting.md) for common errors.
