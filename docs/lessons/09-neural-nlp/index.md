# Module 9: Neural NLP for real messages

Read the overview and learning outcomes here, then follow the learning route. Return to this page’s run instructions for the complete study.

Build a training-only vocabulary and neural text classifier on human-labeled messages, and compare it with a TF-IDF/logistic baseline.

This module works independently: no earlier notebook state, Canvas assignment, paid AI account, or GPU is required. Allow approximately 2–3 hours plus first installation/downloads. Estimates need learner piloting; small CPU runs demonstrate mechanisms, not production readiness.

## Learning outcomes

- **M09.1:** Explain tokenization, vocabulary, padding, embeddings, and pooling.
- **M09.2:** Deduplicate real texts before a declared sample/split.
- **M09.3:** Adapt text preprocessing only on training and train a TensorFlow text model.
- **M09.4:** Compare neural errors with TF-IDF/logistic regression.
- **M09.5:** Document privacy, prevalence, vocabulary limits, and reproducibility.

## Learning route

Follow [foundation](foundation.md) → [concepts and small cases](concepts.md) → [guided construction](guided.md) → [independent practice](practice.md). Use [solutions](solutions.md) after your attempt, then connect your work to the complete reference below.

## Entry support and topics

Use the [foundation bridge](foundation.md) if these concepts are new. Basic Python/functions/files and the train/validation/test distinction are assumed with support from [Module 2](../02-python-workflows/index.md) and [Module 5](../05-regression/index.md).

Tokens are discrete representations; embeddings are learned numeric vectors. Padding supports fixed-length batches and should not become a real word signal. Global average pooling summarizes token vectors. Unknown words and truncated messages limit what the model can use.

## Real data and its limits

UCI SMS Spam Collection; real human-labeled messages. Public messages may contain personal content; processing stays local and reports use hashes/contact masking. See the source register.

[Sources, licenses, hashes, and model provenance](../../data-sources.md) distinguish external records from original teaching code. No generated dataset or invented labels are used in this module. Public files still require responsible handling. Source versions are fixed after verified acquisition; changed cached/upstream bytes cause an error. The first data/model download requires internet; retain the cache for offline replay.

## The complete workflow

Normalized text hashes remove duplicates and conflicting labels before a seeded 60/20/20 split of all 5,159 usable messages. TextVectorization adapts on training only, with at most 6,000 tokens and length 96. Lowercasing retains punctuation so emoticon-only messages do not become all-padding inputs. A 16-dimensional embedding, masked pooling and sigmoid output train for at most 25 epochs with patience 5. A class-balanced TF-IDF/logistic baseline fits the same training partition. Each method selects its threshold using validation balanced accuracy before final evaluation.

## Run and inspect

Download the [complete source](https://ntious.github.io/ml_ai_it/downloads/ml_ai_it-source.zip "site-download:ml_ai_it-source.zip") or use a checkout. Work from its ml_ai_it folder. Use the isolated [CPU framework environment](../../setup/frameworks.md). Run framework commands in the Linux CPU reference environment; see the [support matrix](../../status.md) for platform coverage. Reading the reports needs no framework installation. In commands below, **python means your environment executable**; use its full path if not activated.

~~~sh
python examples/sms-neural-nlp/scripts/run.py --output runs/module09
~~~

Use a fresh output directory for a new run; completed studies are not silently overwritten. Open runs/module09/index.html or read summary.txt/summary.json and the companion CSV tables. [Read the verified worked report](https://ntious.github.io/ml_ai_it/downloads/module09/example/index.html "site-download:module09/example/index.html") without installing an execution interface.

Key artifacts:

- learning_history.csv
- comparison.csv
- test_predictions.csv
- vocabulary.json
- vocabulary_preview.csv
- model.keras

The shared implementation is under src/practical_ml_ai; scripts and [commented notebook](https://ntious.github.io/ml_ai_it/downloads/module09/walkthrough.ipynb "site-download:module09/walkthrough.ipynb") call the same functions. Keep the notebook inside the complete source tree. Named results and captioned/scoped tables support interpretation without a chart or screenshot. For interface choices and test coverage, see the [accessibility guide](../../accessibility/index.md).

## Read selectively

- **Core concept/reference:** [TensorFlow text classification](https://www.tensorflow.org/tutorials/keras/text_classification) — vectorization, embeddings, padding, and evaluation. Read these named sections, not an entire external course.
- **Source/model context:** [central source register](../../data-sources.md), including the relevant official card and license.
- **Optional depth:** Study a CNN/recurrent encoder, a larger vocabulary, or a length change with a predefined development protocol. Measure compute and errors. A different encoder is optional, not an entrance requirement.

## Practice and continue

Complete [original practice](practice.md), then compare [worked feedback](feedback.md). [Instructor notes](instructor.md) map evidence and explain adaptation.

Next: [Module 10](../10-llm-workflows/index.md).

## Build understanding step by step

Use the [guided construction and mastery check](guided.md) before the full study. New programmers should start with [Python Foundation and readiness](../../start-here.md); use the [glossary](../../glossary.md) for notation.

**Reading on GitHub?** Report, notebook and archive links open the [published reading site](https://ntious.github.io/ml_ai_it/). Source notebooks are also under notebooks/lessons in the repository; see [workspace and report access](../../setup/student-workspace.md).

## Optional project connection

Use the [optional stability investigation](../../advanced/stability.md) to design a multi-seed extension. Keep training seeds, data splits and evaluation boundaries distinct.
