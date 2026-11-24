# Worked feedback for the connected case

Attempt the relevant reading question first. These are formative examples, not secret assessment answers or submissions to copy.

## Module 1

Data meaning and a protected evaluation boundary remain necessary before fitting; error analysis and communication remain necessary after fitting. A replacement algorithm changes the model construction, not the need to know what a row and an error mean.

## Module 2

The controller specifies operation order; configuration supplies values such as the split seed and paths. Keeping behavior in functions lets a reader test or replace one stage without copying its implementation into every notebook.

## Module 3

X contains selected numeric predictors; y stores the defined label. Unknown text labels can become missing values in the reviewed mapping, so an explicit check is needed. A feature-order mismatch can send an otherwise valid number to the wrong learned coefficient or input unit.

## Module 4

Three records labeled malignant were predicted benign in the committed matrix. This is a label-conditioned count, not a claim about present-day clinical risk. A stakeholder would still need a defined population, decision, denominator, uncertainty, and consequences of both kinds of error.

## Module 5

The outer test set is separated before preparation/resampling, but the controller creates its internal validation slice later. Rows or generated neighbors can inform fitted preparation before becoming validation evidence. Reserve real validation first, then fit learned preparation and resampling only on the remaining training rows.

## Module 6

The tree selects inputs; the hybrid network predicts the outcome. Recall for label 1 uses all 42 actual positives: 39 found and three missed. Precision uses the 40 predicted positives. Neither denominator may silently replace the other.

## Module 7

Without labels, clustering could explore measurement profiles. The resulting cluster IDs would not establish benign/malignant diagnoses, and a label-dependent classification metric would not be the same unsupervised fitting criterion.

## Module 8

Keep the question/label meaning, split/selection protocol, and feature transformation/ordering contract. Replace network construction and its N by 1 by F reshape with the linear estimator's required matrix input. Re-evaluate a fair comparison rather than assuming either model wins.

## Module 12

A fitted scaler and selected feature order must accompany model state and the threshold/schema. A replay check should compare the frozen pipeline's predictions before and after save/load on actual permitted records, plus reject a changed or missing input field.

## Module 13

An attribution can help scrutinize which represented inputs influence a model under an explainer's assumptions. It does not prove causation, fairness, clinical benefit, or a valid feature mapping. Missing independent data provenance/validation or unclear error consequences can justify withholding a deployment recommendation.

## Extensions

A task may need no generated output. If a summary is useful, require source-grounded claims and separately evaluate the summarizer. If a retrieval assistant chooses tools, also check the allowlist, budget, evidence trace, and failure behavior. None of these additions automatically improves classifier accuracy or makes an agent safe for arbitrary tasks.

## Transfer

A satisfactory explanation connects inputs, fitted state, outputs, evidence, and a decision. It names files or actual observations, identifies at least one check, and distinguishes executed evidence from proposed work. Complexity, terminology, and reproducing an upstream score alone do not establish that reasoning.

[Case overview](index.md) · [All-module map](../../connections.md) · [Project transfer](transfer.md)
