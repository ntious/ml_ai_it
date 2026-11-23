# Model-use summaries and limitations

These are educational model-use records for the implemented examples, not approvals for operational decisions. Full experimental configuration, splits, selected parameters, and measured outputs are saved with each run. Read [data provenance](data-sources.md) before adapting.

| Family and modules | Intended learning use | Evaluation boundary | Principal limitation |
| --- | --- | --- | --- |
| Rules, M1 | Trace explicit decisions | Hand-checked boundary inputs | No model was trained |
| Forecasting, M5 | Availability, baselines, frozen evaluation | Chronological train/validation/test; rolling one-day observations | Historical bike demand is not current IT demand |
| Wine classifiers, M6/M8/M12 | Compare classical/neural approaches and checked inference | Group identical chemistry profiles across splits; validation-only selection | Classroom quality >=7 label is not certification; record groups are not verified physical identities |
| Wine clustering, M7 | Unsupervised selection and profile interpretation | Training scaling; validation silhouette; quality excluded | Cluster IDs are arbitrary, not quality ranks |
| SMS neural classifier, M9 | Training-only vocabulary, imbalance, error analysis | Deduplicated normalized real text; disjoint split IDs | Recorded current run finds 118/128 positives but makes 30 false alerts; the lexical baseline has higher precision and slightly higher balanced accuracy on this split |
| Local LLM, M10/M12/M14 | Prompt/schema evaluation, checked interfaces, bounded tools | Fixed SmolLM2-135M-Instruct revision and bounded real examples | Recorded M10 generation is schema-valid on 99/100 messages but correct on 39/100; M14 uses authored controls, not a real-user reliability sample |
| LoRA, M11 | Real adapter gradients, save/reload, and prompt masking | Rank-8 query/value adapters across layers; validation selects a checkpoint within 200 steps; separate final text IDs | Recorded 94/100 correct labels on a balanced historical sample; this does not establish performance at operational prevalence |
| Adult classifier, M13 | Denominators, group audit, decision ethics | Provided benchmark boundaries with overlap removal; validation threshold | Historic income/category labels are limited and harmful if generalized to people; age remains an input |

The figures above summarize the [recorded framework results](framework-results.md). Earlier failure cases remain in the [historical baseline](maintenance/reviews/framework-baseline-0.7.0.md); they describe different configurations.

## Intended users and exclusions

Learners and instructors can inspect mechanics, change a bounded assumption, and explain measured results. These artifacts are not validated for grading individuals, employment, credit, medical use, incident response automation, quality certification, or unsupervised production actions.

The local Streamlit app has no production authentication, rate limiting, availability commitment, or durable operations process. Keep it local. Bounded agents use an outside-model allowlist, read-only tools, and a call budget; legal plans can still misunderstand intent. Never turn model text directly into a shell command.

## Model identity and rights

The language-model identity, exact revision, license links, dataset citations, and reviewed archive hashes are in [data sources](data-sources.md). Remote custom code is disabled and safetensors are requested. Pinning identity does not establish safety or eliminate dependency risk.

## Review before adaptation

Document the new population, decision, error costs, privacy requirements, available features, evaluation boundary, baselines, uncertainty, failure response, and accountable owner. Repeat relevant behavior and accessibility checks. Add a completed model card using the source template; do not copy this demonstration's performance into a new domain.
