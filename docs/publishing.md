# Publish the GitHub Pages website

The repository contains a static reading website linked to the same module registry, teaching files, source code, notebooks, and verified outputs. Its intended GitHub Pages address is https://ntious.github.io/ml_ai_it/. That address is a publication target, not a claim that Pages is currently enabled.

## Review the finished site

A successful Learning resource checks run uploads complete-reading-site and site-browser-evidence. In a repository checkout, download and extract the site artifact into site/, then run:

~~~sh
python scripts/serve_site.py --port 4173
~~~

Open http://127.0.0.1:4173/ml_ai_it/. The server includes project-prefix and custom-404 behavior. Reading pages and course links work without JavaScript; filtering and browser-local search are optional enhancements. The Python apps still run locally through their own setup instructions.

The browser evidence includes screenshots and failure traces when applicable. Inspect the rendered pages at reading size, then record the human tasks in the [accessibility review log](accessibility/review-log.md). Automated Chromium/axe checks cannot establish screen-reader usability or full conformance.

## One-time repository setup

After reviewing the source changes, merge the integration pull request so both workflows and the complete project exist on main. Let its default-branch Learning resource checks run pass.

In repository Settings, open Pages and select GitHub Actions as the build/deployment source. If appropriate for your governance, configure a required reviewer and allowed deployment branches for the github-pages environment.

This repository is currently private. GitHub Pages support depends on the account plan; private repository status does not itself make the published site private. Confirm the intended audience before enabling publication. The connected repository tools used for this development do not expose the Pages administration setting.

## Publish a reviewed version

1. Open the successful main-branch Learning resource checks run. Record its numeric run ID and full source commit SHA.
2. Complete the human/owner decisions in the [release checklist](release-checklist.md).
3. In Actions, select Publish reviewed GitHub Pages site, choose Run workflow on main, and provide run_id and reviewed_sha.
4. The workflow verifies the successful default-branch push, workflow identity, repository, exact reviewed SHA, and unexpired complete site artifact.
5. It downloads that already-tested artifact, verifies its embedded source/run manifest, packages it with GitHub's Pages action, and deploys it. Check the returned deployment URL and a learner's direct module link.

The workflow does not rebuild or invent results during publication. A pull-request artifact, failed run, mismatched commit, expired artifact, or different workflow is rejected. There is no automatic publication on a draft pull request.

If the artifact expired, run verification again rather than bypassing provenance checks. For rollback, select an earlier successful default-branch run whose reviewed artifact remains available.

## Keep links transferable

The default project prefix is /ml_ai_it/, recorded in curriculum/site.json. Normal page/asset/download links are relative. The custom 404 page uses this prefix so recovery links work even at a deep missing URL. Update the configuration and repeat browser/HTTP checks if the repository name, domain layout, or prefix changes.

For another instructor, link the relevant lesson entry URL directly. See [Canvas linking](instructor/canvas-linking.md). Repository/source links pin the built revision; live site links reflect the selected published edition.

## Sources

- [GitHub: configure the publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub: use custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Playwright: continuous integration](https://playwright.dev/docs/ci)
