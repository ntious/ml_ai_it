# Phase B implementation: independent-review handoff

Review the exact commit named in the pull request and its matching CI run. This
handoff covers the framework work requested after the critical edition 0.7.0
review. It does not claim completion of Phases C–E or authorize public release.

## Implemented findings

| Finding | Change | Evidence to inspect |
| --- | --- | --- |
| ML-1: collapsed neural NLP | Full 5,159-message deduplicated corpus; 25-epoch maximum, patience 5; validation-selected neural/lexical thresholds; balanced lexical baseline | Module 9 split manifest, vocabulary, learning history, validation thresholds, comparison and predictions |
| ML-2: unusable free generation and tiny evaluation | Four real training demonstrations; two-candidate likelihood scoring with a validation-selected threshold; 100 matched final messages; strict generation, lexical and majority comparisons; Wilson intervals | Module 10 demonstration IDs, validation predictions/thresholds, matched comparison, confusion counts and rate intervals |
| ML-3: negligible adaptation | Rank-8 PEFT LoRA in every query/value layer; 256 real training messages, batches of 8, 200-step maximum; best validation-loss checkpoint; validation and final format/label checks | Module 11 study config, training history, disjoint subset IDs, validation generation, final comparison, PEFT configuration and adapter safetensors |
| ML-4: unmeasured agent misrouting | 6 demonstrations, 6 validation controls and 26 final authored requests; explicit action labels; validation-selected score offsets; plan–observe–answer loop; one read-only call, three-step ceiling | Authored request CSV, validation routing scores/offsets, labelled request trace, confusion table and full state traces |
| Supporting neural comparison | Module 8 now uses validation loss with patience, a 40-epoch maximum, separate validation-selected thresholds and ranking metrics | Module 8 learning history, validation thresholds, saved-model replay and comparison |
| Evidence and instruction | Five updated walkthroughs; current generated feedback and results; old failures archived with historical labels | [Current results](../../framework-results.md), [baseline archive](framework-baseline-0.7.0.md), source notebooks and executed copies |

## Recorded outcomes

The [results page](../../framework-results.md) is generated from actual fresh-kernel
reports. It records neural NLP recall 118/128 versus lexical recall 116/128;
Module 10 likelihood accuracy 85/100, generation schema validity 99/100 and
generation accuracy 39/100; LoRA schema validity 0/100 → 100/100 and label accuracy
0/100 → 94/100; agent routing 22/26 and unsupported-request refusals 9/10.

Do not read these as universal wins. Module 9's lexical baseline has fewer false
alarms. Module 10's majority accuracy is 88/100 and lexical accuracy is 97/100;
the likelihood classifier's balanced accuracy, recall and false alarms explain
what its lower accuracy conceals. Module 11 uses a balanced final subset, unlike
Module 10. Module 8 recovers all 29 positives but makes 90 false alarms and loses
to logistic regression on balanced accuracy.

The router refuses three answerable requests and routes one terminal-command
request to a dataset summary. This is an intent error, not permission to execute
a command: the executor has no such capability. All five destructive-labelled
controls are refused, but these few prompts do not establish general safety.

## Reproduce

Use the separate core/framework environments in [the framework guide](../../setup/frameworks.md).
The language profile pins PEFT 0.14.0 alongside Transformers 4.46.3 and the exact
SmolLM2-135M revision. The adapter configuration and study config retain that revision.
The [PEFT versioned guide](https://huggingface.co/docs/peft/v0.14.0/tutorial/peft_model_config)
documents the configuration, wrapping and serialization APIs used here.

```sh
python scripts/preflight.py --profile frameworks
python examples/sms-neural-nlp/scripts/run.py --output runs/review09
python examples/sms-llm/scripts/run.py --output runs/review10 --examples 100
python examples/sms-fine-tuning/scripts/run.py --output runs/review11 --steps 200
python examples/bounded-assistant/scripts/run.py --output runs/review14
```

Use new output directories. Default-budget integration tests and fresh notebooks
execute actual models; the second CLI test uses explicitly smaller budgets to
check its interface without repeating every default experiment. These smaller
CLI runs are not credited with the default study scores.

```sh
ML_AI_HEAVY=1 USE_TF=0 HF_HUB_DISABLE_XET=1 python -m unittest discover -s tests -p test_continuation_heavy.py -v
python scripts/check_notebook.py --group frameworks --kernel ml-ai-frameworks
python scripts/update_framework_results.py
```

Run core tests/notebooks in their own profile before assembling the full site.
The source archive contains code and authored controls; external caches and
executed reports remain separate attributed downloads. No model weight is added
to tracked source. CI artifacts provide the complete review site before publication.

## Questions for independent review

Local verification completed: all 15 module/case notebooks executed in fresh
kernels; the full framework suite passed all 11 tests, including default training,
public CLIs and app checks. The core suite and eight lightweight Phase B contract
tests cover the split, selection, uncertainty and execution-boundary behavior.
The complete site, served routes, source/data archives, browser checks and
isolated installed-wheel inference were also exercised. Use the pull request's
matching CI run for the final Windows/Linux integration result.

Automated review additionally identified four edge cases, now covered: standard
user-data install prefixes; SMS caps too small for both stratified split stages;
a near-full evaluation subset with a one-row remainder; and long prompts losing
their assistant-turn boundary. Prompt packing now keeps the complete formatted
prompt. The declared LoRA study's longest train/validation/final prompts contain
129/120/137 tokens respectively, so that correction changes none of its recorded
inputs or scores. The long-prompt regression separately exercises 300 prompt
tokens and verifies that only completion tokens receive loss labels.

1. Confirm the final labels never select checkpoints, thresholds, demonstrations
   or routing offsets. Mutate final labels and inspect whether selections change.
2. Reconcile every reported success/rate with the raw CSV counts and denominators.
   In particular, keep invalid generation failures in the accuracy denominator.
3. Check padding/prompt masking and verify base-model parameters remain frozen
   and uncontaminated after the PEFT study. Reload only the selected adapter and
   verify its logits, configuration and base revision.
4. Inspect the original Module 14 count request and all four remaining routing
   errors. Try unsupported plans and smaller step budgets; distinguish the
   executor's capability boundary from model understanding.
5. Read a walkthrough as a novice. Check that current default descriptions and
   feedback agree with actual outputs, and that historical failures are clearly
   separated from current evidence.

## Limits and remaining work

All results use historical public benchmarks or authored controls. Development
included inspecting failed runs and changing configurations; this is transparent
benchmark development and teaching rehearsal, not an untouched prospective
evaluation. Candidate choices use validation data, but repeated public final
results should not be presented as new independent evidence.

Six validation requests provide weak evidence for class-score offsets. The
likelihood score and offsets are not calibrated confidence. Wilson intervals
cover individual binomial rates, not dataset shift, paired method differences or
multiple-comparison effects. No test score was forced to match a target; the
neural NLP recall guard is a broad collapse check on this fixed benchmark.

Phases C–E remain open: repository-wide uncertainty, regression changes, broader
instructional rewriting/exercise notebooks, lint/report refactoring and tested
hosted routes. No human assistive-technology session or learner pilot was
performed. Site deployment stays behind the owner's publication switch.
