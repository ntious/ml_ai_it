# Review of the LSTM Canvas integration guide

Review date: November 23, 2026. The aim is to help students explain how course topics connect inside a study while preserving the standalone resource and the master Canvas assessments.

## Sources and review scope

The supplied *3-Tier-LSTM Canvas Integration Guide v2*, all original course/module text, the master syllabus, dataset-link document, project overview, and both project PDFs were read from the supplied attachments. The Word guide was rendered to 29 pages and its layout inspected. The original files and private institutional instructions remain outside the repository.

The linked research source was checked at `a6ca70ada14ce6b98f8ffccc71164d549c733dbb`. Source/configuration/helper tests and stored reports/figures were inspected; upstream training, SHAP, LIME, or clinical validity were not reproduced. [Source notes](../../cases/three-tier-lstm/source-notes.md) locate the technical evidence. This is an educational/methodological review, not an independent evaluation of the associated research article.

## Overall recommendation

Retain the repeated, bounded research encounters and add one course-wide map that explains the common lifecycle, its handoffs, and where alternative branches belong. Keep the existing runnable IT project as the implementation exemplar. Present the LSTM code as a source to trace and critique; do not imply that one advanced model implements every course topic or is a validated production recipe.

## Instructional and technical observations

| Observation | Recommendation applied |
| --- | --- |
| Strong progressive reveal, selected file lists, low-installation reading route, and one reflection | Preserve short encounters with a concrete target, a current focus, bounded source links, one question, and public feedback. |
| The original per-page learning target repeats the same generic wording | Give each connection a distinct observable action: identify, trace, reconcile, compare, or justify. |
| “Three tier” can be mistaken for difficulty levels, three LSTMs, or evidence of temporal data | Name Dense feature extraction, the single-step LSTM, and the Dense head; explain the actual N by 1 by F input. |
| The guide does not connect Modules 9–11 and 14, and only contrasts Module 7 | Add the all-14-module lifecycle map and an explicitly complementary NLP/LLM/fine-tuning/agent bridge. Do not invent those implementations in the tumor repository. |
| Test splitting occurs before learned preparation, but internal validation is taken after resampling | Explain the difference and provide a proposed training/validation/test redesign. Do not call the entire protocol leakage-free. |
| Feature-importance names and weights can be mispaired | Flag the name/value contract; avoid presenting the existing bar ranking as verified. |
| The guide suggests outputs organize generated models, while the reviewed controller does not serialize one | Teach the deployment gap using the missing model/scaler/schema bundle; link the existing course inference/monitoring exemplar. |
| Input data are not tracked or hash-pinned; pip and Conda specifications differ | Keep execution optional and separate. Do not claim one-command reproduction was verified. No fabricated replacement dataset was created. |
| Stored metrics are interpretable but not linked by a full run manifest | Label them upstream committed results; give an accessible confusion-count table and arithmetic without claiming reproduction. |
| Explanation images/widgets and color-coded callouts alone are insufficient access evidence | Provide text lifecycle, shape/metric tables, named links, ordinary headings, and feedback; do not require upstream image interpretation. |
| Reading is sometimes conflated with implementation mastery | State that the connection activities assess recognition/reasoning. Existing script/notebook/project work supplies execution evidence. |
| Guide recommends new tabs for external links | Use normal descriptive links by default; let learners choose their preferred browser behavior. |
| The guide assumes synchronous online teaching | Supply the same short explanation as a live discussion, asynchronous reflection, or in-person task. |

## Word layout observations

The rendered guide has 29 pages. Page 27 contains only running header/footer material; page 5 has a short continuation and a large unused area. Several student pages split the “open these files” list across a page break. These are observations from the render, not a complete Word accessibility certification. The new HTML/Markdown pages avoid those pagination dependencies and preserve the numbered source locations in the original review record. The original Word file is unchanged.

## Course and program alignment

The supplied course documents confirm the 14-module sequence and eight outcome domains. The new companion uses existing summary labels and does not republish official institutional wording. Research-source reading supports CLO4/CLO7/CLO8 and supervised-paradigm discussion; it does not establish implementation mastery, genuine IT/network application, GenAI integration, deployment performance, or teamwork. The existing IT/network and LLM/agent routes supply distinct supporting work. See [instructor evidence map](../../instructor/connected-research-case.md).

A1/A2/A3/A4 remain the repository's advisory planning categories for analysis, solution evaluation, communication, and ethical judgment, not official ABET outcome numbers or attainment claims. The adopting program owns formal assessment and criteria.

## Completion and verification record

Authored content includes the course-wide map, 15 source-pinned case/feedback pages, instructor placement/evidence guidance, module-entry links, and a reusable pipeline-passport template. The external repository and all existing course outcomes, scripts, notebooks, and master assessments are unchanged.

The dedicated Reading resource checks workflow reuses artifacts only from a successful full verification at the PR base commit, after an allowlist confirms that computational sources are unchanged. It has no deployment permission and does not replace the full course workflow. New checks verify the 14-module route map, optional/complementary statuses, source pin/path validity, reciprocal navigation, source links, and the rendered reader journey. Static source/site and browser results are recorded with the integration pull request. The current main commit's verified artifacts are reused only for unchanged computational content during local site assembly; no new upstream LSTM training or full framework rerun is claimed by this document. Human screen-reader and learner-pilot evidence remain separate from technical checks.
