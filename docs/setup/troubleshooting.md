# Troubleshooting and getting help

Keep a copy of your work before changing environments. Use exact text errors and commands; remove secrets and personal records.

| Symptom | Small check | Recovery |
| --- | --- | --- |
| Python command not found | Try py --version on Windows, python3 --version on Unix | Install a supported interpreter or use the instructor's workspace |
| File not found | Print Path.cwd() and list the folder | Change into the extracted project root; check extraction and filename |
| ModuleNotFoundError | Print sys.executable inside the failing notebook | Install the documented extra with that interpreter or select its kernel |
| Wrong numeric type | Inspect the CSV field and conversion | Correct the input or document rejection; do not invent missing values |
| Existing output directory | Inspect the named folder | Choose a new run directory; preserve completed evidence |
| Source hash mismatch | Retain provenance and error text | Report the changed source; do not disable the checksum |
| Incomplete source cache | Inspect original.zip and provenance | Preserve the incomplete cache for diagnosis and use a clean explicit cache location |
| Kernel dies or memory runs out | Stop other kernels and inspect resources | Use the Linux CPU workspace, smaller documented mechanics budget, or instructor support |
| Model download fails | Check connectivity and available disk | Retry the documented source; keep complete verified caches |
| Report link fails on GitHub | Check whether its path contains downloads | Use the built reading artifact described in workspace setup |
| Binder session disappears | Check your downloaded files | Restore saved notebook/source; hosted sessions are temporary |

Run `python scripts/preflight.py --profile core` from the project root with the environment's interpreter. Choose frameworks for the Linux CPU environment. Save its version report with your work. Free disk warnings are planning guidance, not measured resource guarantees.

When requesting help, provide the module, route, OS, Python executable/version, exact command, expected result, actual error and one attempted fix. State whether the task is blocked. For an enrolled class, use Canvas's instructor/support contact and its stated response expectations. Independent learners can report nonsensitive reproducible software problems through repository issues. Assessment, disability and personal-data questions need a private institutional route.
