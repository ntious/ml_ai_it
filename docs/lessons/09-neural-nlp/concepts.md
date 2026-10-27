# Module 9: From text to an imbalanced decision

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## A vocabulary is a fitted transformation

Tokenization turns text into units; a vocabulary maps units to IDs. Fit the vocabulary on training only. Reserve an unknown token for a later word and a separate padding ID for missing positions. If validation text creates the vocabulary, you have let future text shape the representation. Lowercasing and splitting on whitespace are a deliberately limited teaching tokenizer, not universal language processing.

## Sequence choices change the information

A fixed-length model truncates long messages and pads short ones. State whether it keeps the start or end: a warning or suspicious URL may occur in the discarded portion. Embeddings learn numerical representations from the training objective. A recurrent or pooled network can exploit patterns, but a simpler lexical classifier may generalize better with limited data. Compare under the same split and validation decision rule.

## Accuracy can hide the relevant failure

If only 10 of 100 messages are spam, predicting ham every time has 90% accuracy and zero spam recall. Count TP, FP and FN at a declared threshold. Precision answers what fraction of alerts were spam; recall answers what fraction of spam was found. Changing the threshold trades workload against misses. Validation can select it; final-test errors must not then tune the vocabulary or threshold.

## Trace a small case

The first operation is **vocabulary**: Return alphabetical lowercase whitespace tokens with IDs starting at 2; 0=padding,1=unknown. On authored arguments `[['FREE offer', 'offer now']]`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/sms-neural-nlp/scripts/run.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Primary explanation](https://www.tensorflow.org/text/guide/word_embeddings) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
