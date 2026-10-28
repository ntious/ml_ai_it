# Module 7: Clustering and learning paradigms

Read the overview and learning outcomes here, then follow the learning route. Return to this page’s run instructions for the complete study.

Discover and describe chemistry groups without pretending that clusters are known classes or quality ranks.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 90–150 minutes plus practice. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M07.1:** Distinguish supervised, unsupervised, and reinforcement learning by the information available.
- **M07.2:** Fit training-only scaling and k-means without quality labels.
- **M07.3:** Compare predefined cluster counts using a validation geometry criterion.
- **M07.4:** Describe clusters through counts and original-unit profiles.
- **M07.5:** Explain why internal scores and observational data do not validate actions or rewards.

## Learning route

Follow [foundation](foundation.md) → [concepts and small cases](concepts.md) → [guided construction](guided.md) → [independent practice](practice.md). Use [solutions](solutions.md) after your attempt, then connect your work to the complete reference below.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

K-means minimizes squared distances to centers, so units and scaling affect the result. Silhouette contrasts within-cluster closeness with separation from other clusters. It is not classification accuracy. Cluster IDs can be permuted without changing the partition.

## Real data and its limits

UCI Wine Quality; real red-wine chemistry and human ratings. See the central source register for citation, rights, archive hash, and limitations.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

The same disjoint chemistry groups support training/validation/final description. StandardScaler is fitted on training. K=2,3,4 are fitted there and compared by validation silhouette; quality is excluded. The selected partition assigns final records, with counts and mean profiles in original units. No test label selects K.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the [core environment instructions](../../../QUICKSTART.md) and install the regression extra. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/wine-clustering/scripts/run.py --output runs/module07
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

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 8](../08-neural-networks/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).

## Optional project connection

Read [training-seed versus split stability](../../advanced/stability.md) before proposing a clustering stability study. The executable capstone uses classification; clustering needs its own partition-comparison measures.
