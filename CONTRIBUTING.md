# Contributing

Start with a small, inspectable improvement. Explain the learning goal, what changes for learners, and how the relevant behavior was checked.

## Quality requirements

- Keep reusable behavior in `src/`; scripts and notebooks call those functions.
- Preserve raw input and explain transformations, rejection, missingness, and units.
- Give each module a standalone entry, prerequisite help, a runnable example, practice, and feedback.
- Label optional depth and resource requirements clearly.
- Follow [ACCESSIBILITY.md](ACCESSIBILITY.md). Verify the whole task and document limitations; automated scans are supporting evidence.
- Do not introduce student records, credentials, institutional assessments, or copied solutions from an adopting course.
- Record data/model provenance and rights. Include a small, permitted sample and limitations.
- Add behavioral tests for meaningful changes and run the affected checks.

## Verification

Run the commands in [README.md](README.md). Notebook code checks do not replace notebook UI testing. Site structural checks do not establish screen-reader usability. Record exactly what was verified.

## Review and releases

Use a development branch and a pull request with a concrete behavior summary and validation. Keep generated `site/`, `runs/`, caches, and local environments out of commits. Preserve stable module links or supply redirects when changing published paths. Do not change an adopting institution's grading rules through repository edits.

## Naming conventions

Use neutral, descriptive names for repository folders and branches. Prefer topic/task names such as `data-processing`, `development/module-03-foundation`, or `feature/model-evaluation`. Avoid tool- or vendor-branded naming prefixes. Preserve the project's existing author attribution and license notices.
