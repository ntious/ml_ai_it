# Teach and adapt Module 5

Link the [entry page](index.md) directly. Its planned route is /lessons/05-regression/, relative to the eventual site base URL. Until site publication, use repository Markdown at a tested commit/release.

## Support independent learners

Start with the forecast contract and hand arithmetic, then the stage scripts, commented notebook, and memo practice. Learners need functions, paths, and dataframe selection; the foundation bridge supplies the numerical concepts. Pilot pacing.

The script/text route can demonstrate training and interpretation without an inaccessible notebook UI or screenshot requirement. Notebook-interface operation is a separate skill if locally required. Discussion has a solo equivalent; GenAI is optional and local policies govern submissions.

## Adapt the data and model together

Retain the UCI attribution/provenance. The synthetic fixture is an openly labeled offline alternative, with limited claims. For another dataset, specify unit, target, origin, horizon, feature availability, rights/privacy, and split before fitting. Repeated users/sites may need group boundaries; time series may need gaps or other availability modeling.

When changing features/models, update the contract, pipeline/exporter, inference checks, feedback, and tests. Numeric JSON supports only the narrow model kinds implemented here. Public historical test labels cannot become a blind benchmark through a script guard.

## Alignment opportunities

| Outcome | Original register | Course alignment | Advisory ABET opportunity | Evidence |
| --- | --- | --- | --- | --- |
| M05.1 | O05.1 | CLO1 support; CLO4 support | A1 | Equation/residual/loss |
| M05.2 | O05.2 | CLO2; CLO4 | A2 | Pipeline and baselines |
| M05.3 | O05.3 | CLO2; CLO4 | A1, A2 | Feature timing audit |
| M05.4 | O05.4; explicit evaluation added | CLO4; CLO8 | A1, A2 | Split, frozen choice, errors |
| M05.5 | O05.4 | CLO2; CLO8 | A3 | Reproducibility and memo |

These labels follow the separate curriculum planning register, not universal course identifiers. A1/A2/A3 are advisory computing-outcome opportunities for problem analysis, solution evaluation, and communication. Introductory artifacts do not prove master's-level attainment or accreditation compliance. Confirm adopted criteria before formal program use.

## Verification and accessibility

CI exercises real-data download/workflow, synthetic behavior tests, notebook code, and site/report generation. Consult DEVELOPMENT.md and commit-specific results. Notebook code checks are not interface usability tests.

Reports supply named values, scoped/captioned tables, CSV/text evidence, and descriptions alongside optional plots. Manual screen-reader, keyboard, zoom/reflow, notebook-interface, and rendered-figure review remain pending for this increment. Provide a private help route and test actual learner tasks before requiring an interface.
