# Module 7: Clustering and learning paradigms

## Your route through this module

1. **Read:** start with the [foundation](foundation.md) and [concepts](concepts.md); use the [guided activity](guided.md) to work through an example.
2. **Run:** follow the complete-example commands on this page and inspect the saved output.
3. **Practice:** attempt the [practice tasks](practice.md) before opening answers.
4. **Check:** compare [practice notebook answers](solutions.md) and [interpretation feedback](feedback.md), then explain any corrections.


Discover and describe chemistry groups without pretending that clusters are known classes or quality ranks.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 90–150 minutes plus practice. Small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M07.1:** Distinguish supervised, unsupervised, and reinforcement learning by the information available.
- **M07.2:** Fit training-only scaling and k-means without quality labels.
- **M07.3:** Compare predefined cluster counts using a validation geometry criterion.
- **M07.4:** Describe clusters through counts and original-unit profiles.
- **M07.5:** Explain why internal scores and observational data do not validate actions or rewards.

## Course outcomes and evidence

<!-- OUTCOME_EVIDENCE_START -->

<details>
<summary>For instructors: course outcomes and evidence</summary>

- **Direct evidence:** CLO1 (Learning paradigms), CLO4 (Frameworks and evaluation), CLO8 (Communication)
- **Supporting practice:** CLO2 (Applying ML/AI to IT operations), CLO3 (Interpreting network data)
- **Additional direct-evidence route (complete separately):** [NETWORK (CLO3)](../../cases/network-record-interpretation.md)
- **Data and tools:** <span class="data-label">Real public</span>
- **Evidence you produce:** Cluster-count choice made without labels, with an interpretation and its limits. See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).
- **Boundary:** Wine groupings support interpretation technique; they do not demonstrate network-data interpretation.
- **Responsible-AI check:** Does the data support the name given to a cluster, or does the name imply more than it shows?

See the [outcome map](../../outcome-map.md) for all modules and the label definitions. These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.

</details>
<!-- OUTCOME_EVIDENCE_END -->



## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

K-means minimizes squared distances to centers, so units and scaling affect the result. Silhouette contrasts within-cluster closeness with separation from other clusters. It is not classification accuracy. Cluster IDs can be permuted without changing the partition.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. The reference study uses attributed public observations. Practice fixtures, derived task labels and authored evaluation controls are identified separately; they are not additional real-world observations. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The same disjoint chemistry groups support training/validation/final description. StandardScaler is fitted on training. K=2,3,4 are fitted there and compared by validation silhouette; quality is excluded. The selected partition assigns final records, with counts and mean profiles in original units. No test label selects K.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the [core environment instructions](../../../QUICKSTART.md) and install the regression extra. Commands below start with the core environment's Python, `.venv`, which you created in [first run](../../../QUICKSTART.md#module-3-add-the-data-libraries). **The first run downloads the public dataset or model, so it needs internet**; later runs reuse the verified cache. If a download link does not open, use the [offline access route](../../setup/student-workspace.md#if-a-download-link-does-not-open).

macOS/Linux:

~~~sh
.venv/bin/python examples/wine-clustering/scripts/run.py --output runs/module07
~~~

Windows PowerShell:

~~~powershell
.\.venv\Scripts\python.exe examples/wine-clustering/scripts/run.py --output runs/module07
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module07/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module07/example/index.html "site-download:module07/example/index.html") without installing an execution interface.

Key artifacts:

- k_comparison.csv
- cluster_profiles.csv
- cluster_counts.csv
- test_assignments.csv

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module07/walkthrough.ipynb "site-download:module07/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [scikit-learn clustering](https://scikit-learn.org/stable/modules/clustering.html) — k-means assumptions and silhouette evaluation. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Compare another seed or an alternative distance/cluster method using development data. Discuss stability and non-spherical structure. Do not repeatedly pick a method because its held-out partition looks appealing.

## Practice and continue

Complete [original practice](practice.md), then compare [interpretation feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 8](../08-neural-networks/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

## Optional project connection

Read [training-seed versus split stability](../../advanced/stability.md) before proposing a clustering stability study. The executable capstone uses classification; clustering needs its own partition-comparison measures.

## Check before continuing

You have completed this module’s core learning route when you can:

- Save and explain this evidence: Cluster-count choice made without labels, with an interpretation and its limits.
- Attempt the practice tasks and explain a correction or why your original answer was sound.
- Explain this limitation in your own words: Wine groupings support interpretation technique; they do not demonstrate network-data interpretation.

Use the answer pages to resolve gaps before continuing. Optional extensions are separate from this checklist.

## Connect this module to the whole study

Compare supervised classification with clustering and reinforcement learning. Use the [course-wide lifecycle map](../../connections.md#module-7-choose-the-learning-paradigm) and the [research-case connection](../../cases/three-tier-lstm/07-paradigms.md). This is a short reading/reflection route; use this module's existing practice for implementation evidence.
