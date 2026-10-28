# Module 9: From text to an imbalanced decision

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## A vocabulary is a fitted transformation

Tokenization turns text into units; a vocabulary maps units to IDs. Fit the vocabulary on training only. Reserve an unknown token for a later word and a separate padding ID for missing positions. If validation text creates the vocabulary, you have let future text shape the representation. Lowercasing and splitting on whitespace are a deliberately limited teaching tokenizer, not universal language processing.

## Sequence choices change the information

A fixed-length model truncates long messages and pads short ones. State whether it keeps the start or end: a warning or suspicious URL may occur in the discarded portion. Embeddings learn numerical representations from the training objective. A recurrent or pooled network can exploit patterns, but a simpler lexical classifier may generalize better with limited data. Compare under the same split and validation decision rule.

## Accuracy can hide the relevant failure

If only 10 of 100 messages are spam, predicting ham every time has 90% accuracy and zero spam recall. Count TP, FP and FN at a declared threshold. Precision answers what fraction of alerts were spam; recall answers what fraction of spam was found. Changing the threshold trades workload against misses. Validation can select it; final-test errors must not then tune the vocabulary or threshold.

## Trace a small case

Predict `vocabulary(['FREE offer', 'offer now'])` before running: lowercase tokens in alphabetical order from ID 2 give `{'free': 2, 'now': 3, 'offer': 4}`, with 0 reserved for padding and 1 for unknown words. Then predict `encode('NEW offer', {'offer': 2}, 4)`: `new` is unknown (1), `offer` is 2, and two padding zeros fill the length, giving `[1, 2, 0, 0]`. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/sms-neural-nlp/scripts/run.py`. Its Keras `TextVectorization` layer adapts on training messages only, with at most 6,000 tokens and length 96. It reserves the same two IDs (0 padding, 1 unknown), but orders words by training frequency rather than alphabetically. `vocabulary.json` and `vocabulary_preview.csv` record the result. Recall in `comparison.csv` uses actual positives as its denominator, exactly like your `recall` function. Success on an authored fixture does not establish performance on a real service.

## Check yourself

Answer each question before opening its explanation.

<details>
<summary>1. If 10 of 100 messages are spam and a model predicts ham every time, what are its accuracy and spam recall?</summary>

Accuracy is 90% and recall is 0: it finds no spam.

</details>

<details>
<summary>2. Why must the vocabulary be fitted on training messages only?</summary>

Building it from validation or test text lets future messages shape the representation, which leaks information into evaluation.

</details>

<details>
<summary>3. A suspicious link appears at word 120 of a message, and the model keeps the first 96 tokens. Can the model use it?</summary>

No: it is truncated. State the truncation rule and check on validation data how often long messages lose information.

</details>

## Optional reading

[TensorFlow guide: Word embeddings](https://www.tensorflow.org/text/guide/word_embeddings) shows how integer token IDs become learned vectors and how `TextVectorization` pads and truncates sequences. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
