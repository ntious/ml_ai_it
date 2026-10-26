# Real data and model source register

Modules 6–14 use actual external records and human annotations. No new synthetic illustration/training dataset is created. Earlier foundation fixtures remain labeled separately.

## External datasets

### wine

Cortez, P., et al. (2009). Wine Quality. UCI. DOI:10.24432/C56S3T. [Official source](https://archive.ics.uci.edu/dataset/186/wine+quality) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Reviewed archive SHA-256: 3ed56667f4b828242bd732d7d1dd7f2861e54432239d7fa63877014cbb0304d4.

Derived processing selects real red-wine chemistry, groups identical profiles, and declares a rating threshold for supervised cases. Clustering excludes the quality label.

### adult

Becker, B. & Kohavi, R. (1996). Adult. UCI. DOI:10.24432/C5XW20. [Official source](https://archive.ics.uci.edu/dataset/2/adult) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Reviewed archive SHA-256: 7537312dd56c2b98035880805ce99e68183a30ee468aa5329d6df0fbb3cc21bb.

Derived processing uses the provided benchmark files, removes exact full-row overlaps, fits five numeric inputs, and audits recorded groups. Person independence and a justified eligibility purpose are not established.

### sms

Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection. UCI. DOI:10.24432/C5CC84. [Official source](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Reviewed archive SHA-256: 1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3.

Derived processing hashes normalized text, removes duplicate/conflicting texts, selects a declared real sample, and preserves human labels. LLM cases mask contact-like strings and disclose tiny balanced subsets. Public messages can still contain personal content.

## Acquisition and offline replay

Original archives, named original members, provenance.json, and ATTRIBUTION.txt remain under runs/datasets/name. New archives must match the reviewed digest; cached member hashes are verified. Source changes require review rather than bypassing the check.

Separate attributed caches are available for [wine](https://ntious.github.io/ml_ai_it/downloads/wine-cache.zip "site-download:wine-cache.zip"), [SMS](https://ntious.github.io/ml_ai_it/downloads/sms-cache.zip "site-download:sms-cache.zip"), and [Adult](https://ntious.github.io/ml_ai_it/downloads/adult-cache.zip "site-download:adult-cache.zip"). Extract each into its named runs/datasets directory, preserving all files. External records stay outside the original-source ZIP. Worked reports can be read without executing a dataset or model.

## Pretrained model

[HuggingFaceTB/SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) has an Apache-2.0 card/license. Reviewed revision: 12fd25f77366fa6b3b4b768ec3050bf629380bac. It runs locally on CPU with safetensors and remote code disabled. The course does not claim to reproduce or audit every pretraining source. Our fine-tuning illustrations use real human SMS labels, not generated records.

First use downloads several hundred MB; retain runs/models for replay. Base weights remain separate from the original-source archive. Consult the official card and [SmolLM2 technical report](https://arxiv.org/abs/2502.02737). A pinned revision is reproducible, not a quality guarantee.

## Use limits

Data rights and model licenses are distinct. Preserve credits and disclose transformations. Public access does not prove representative sampling, privacy, causal validity, consent for every new purpose, or operational suitability. The reports retain weak-model and format failures.

## Authentic IT extension: website phishing

[UCI Phishing Websites](https://archive.ics.uci.edu/dataset/327/phishing+websites), Mohammad & McCluskey (2012), DOI 10.24432/C51W2X; UCI lists CC BY 4.0. The selected Training Dataset.arff contains 11,055 records and 30 encoded attributes. Archive SHA-256: 514f582cb44cba17251baf1d59f64cddff16efa2b644d091ce8d2a1e8d492940. Raw files remain unchanged; the case documents label recoding, ambiguous-profile exclusions and grouped splits. No live URLs are visited. [Case workflow and limits](cases/phishing.md).

## Authored agent controls

`data/samples/agent-requests.csv` is original teaching material: labelled demonstration, validation and test requests. It contains no real user interactions and is not an external dataset. Module 14 returns statistics from the attributed UCI wine records; keep that evidence separate from the authored routing controls.
