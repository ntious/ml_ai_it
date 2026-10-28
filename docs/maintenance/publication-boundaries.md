# What belongs in the public repository

Publish original teaching code, clean notebooks, lesson pages, citations, schemas, synthetic teaching fixtures and blank review templates. Keep downloaded external datasets, model weights and generated runs in `runs/`; it is ignored by Git. The RT-IoT scripts download directly from UCI and do not require committing the dataset.

## Confidential work

Use the ignored root folders `private/`, `review-notes/`, `student-records/` or `pilot-records/` for completed reviews containing personal information, student submissions, grades, identifiable pilot observations, consent records and unpublished planning. Restricted institutional source documents remain in `documentations/`. Keep credentials in ignored environment files or an appropriate credential store.

Blank review templates and de-identified technical findings can be public. The existing dated technical reviews in `docs/maintenance/reviews/` are intentionally tracked transparency records; they are not confidential student reviews. The owner review guide is also public source. Put completed personal review notes in `review-notes/`, not beside the public guide. The accessibility email was explicitly approved for publication.

## Git and downloads are separate checks

`.gitignore` prevents ordinary addition of untracked files; it does not remove tracked files, erase history or prevent deliberate forced addition. Before committing, inspect `git diff --cached --stat`, `git diff --cached` and `git ls-files -ci --exclude-standard`. The last command should print nothing. Never paste credential contents into a review log.

The site source archive is assembled from an explicit folder/file allowlist and checked against tracked source. Confidential folders belong at the root outside that allowlist. Do not place private notes inside `docs/`, `notebooks/`, `projects/` or other publication folders, even if an editor hides them. Check the generated archive before publishing. Reports can also contain source rows: inspect them for personal information before distribution.

If confidential content was already committed, adding an ignore rule is insufficient. Stop publication of the affected artifact, identify the affected history and rotate exposed credentials where applicable. Coordinate any history rewrite with the owner rather than silently rewriting shared commits.
