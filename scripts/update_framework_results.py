"""Refresh Phase B teaching evidence from executed reports, never invented scores.

Run after fresh-kernel verification, then inspect and commit the source changes.
The normal site build deliberately does not edit teaching source.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = {8: "08-neural-networks", 9: "09-neural-nlp", 10: "10-llm-workflows",
         11: "11-fine-tuning", 14: "14-agents"}


def refresh(runs):
    results = {n: json.loads((runs / f"module{n:02d}/summary.json").read_text()) for n in NAMES}
    for n, result in results.items():
        if result["module"] != n:
            raise ValueError(f"Wrong report for Module {n}.")
    eight, nine, ten, eleven, agent = (results[n] for n in NAMES)
    rows = []
    diagnoses = {}
    for n in [8, 9]:
        result = results[n]
        neural, baseline = result["test"], result["linear_baseline"]
        positives = neural["tp"] + neural["fn"]
        rows.append(f'| {n} | {result["sample_rows"]:,} source rows; {neural["n"]:,} final | '
                    f'Neural recall {neural["tp"]}/{positives} = {neural["recall"]:.3f}; precision {neural["precision"]:.3f}; '
                    f'balanced accuracy {neural["balanced_accuracy"]:.3f} | Lexical/logistic recall {baseline["recall"]:.3f}; '
                    f'balanced accuracy {baseline["balanced_accuracy"]:.3f} |')
        diagnoses[n] = (
            f'**Recorded evidence.** Of {positives} actual positives among {neural["n"]} final records, the network finds '
            f'{neural["tp"]} and misses {neural["fn"]}, with {neural["fp"]} false alarms. Its recall is '
            f'{neural["recall"]:.3f}, precision {neural["precision"]:.3f} and balanced accuracy {neural["balanced_accuracy"]:.3f}. '
            f'The simpler baseline has recall {baseline["recall"]:.3f}, precision {baseline["precision"]:.3f} and '
            f'balanced accuracy {baseline["balanced_accuracy"]:.3f}.\n\n'
            f'**Explain the decision.** Validation loss selected checkpoint {result["best_validation_epoch"]} within a '
            f'{result["epochs_requested"]}-epoch maximum. Validation balanced accuracy selected thresholds '
            f'{result["threshold"]:.2f} (neural) and {result["baseline_threshold"]:.2f} (baseline). '
            'Recall alone hides the false-alarm cost; compare both confusion tables and the threshold-free ranking metrics. '
            'Neither the baseline nor the neural model is required to win.\n\n'
            '**Try a validation-only investigation.** Read validation_predictions.csv and validation_thresholds.csv. '
            'Explain one threshold tradeoff without changing a setting in response to final-test scores. '
            'For an imbalanced dataset, why would accuracy alone be misleading?'
        )
    rows.append(f'| 10 | {ten["real_examples"]} stratified final SMS | Likelihood accuracy {ten["label_likelihood_accuracy"]:.2f}; '
                f'free-generation validity {ten["strict_schema_rate"]:.2f}, accuracy '
                f'{ten["exact_label_accuracy_including_invalid_as_wrong"]:.2f} | Lexical accuracy '
                f'{ten["matched_baseline_accuracy"]:.2f}; training-majority accuracy {ten["majority_accuracy"]:.2f} |')
    diagnoses[10] = (
        f'**Recorded evidence.** On {ten["real_examples"]} matched final messages, free generation produces valid JSON '
        f'{ten["strict_schema_rate"]:.0%} of the time but correct labels only '
        f'{ten["exact_label_accuracy_including_invalid_as_wrong"]:.0%} of the time. Candidate likelihood with a '
        f'validation-selected threshold of {ten["likelihood_threshold"]:.2f} has accuracy {ten["label_likelihood_accuracy"]:.0%}. '
        f'The lexical baseline reaches {ten["matched_baseline_accuracy"]:.0%}, while always predicting the training-majority '
        f'label reaches {ten["majority_accuracy"]:.0%}.\n\n'
        '**Explain the difference.** Few-shot examples can improve output format without fixing semantic classification. '
        'Candidate scoring returns a legal label by construction; that is not evidence of learned JSON compliance. '
        'Read confusion_counts.csv before declaring an accuracy improvement useful: a classifier can recover spam while '
        'scoring below majority accuracy. The selected relative likelihood score is not calibrated confidence.\n\n'
        '**Check uncertainty.** Read the successes, observations and Wilson intervals in rate_intervals.csv. '
        'These are intervals for individual rates, not a paired significance test of method differences. '
        'Use llm_validation_predictions.csv to investigate errors; do not choose a prompt from final-test outcomes.'
    )
    rows.append(f'| 11 | {eleven["test_examples"]} balanced final SMS | JSON validity '
                f'{eleven["base_schema_rate"]:.2f} → {eleven["adapted_schema_rate"]:.2f}; label accuracy '
                f'{eleven["base_generation_accuracy"]:.2f} → {eleven["adapted_generation_accuracy"]:.2f} | '
                f'Validation loss {eleven["validation_loss_before"]:.4f} → {eleven["validation_loss_after"]:.4f}; '
                f'selected step {eleven["selected_step"]}/{eleven["steps"]} |')
    diagnoses[11] = (
        f'**Recorded evidence.** The selected all-layer adapter has {eleven["trainable_parameters"]:,} trainable parameters. '
        f'Validation completion loss moves from {eleven["validation_loss_before"]:.4f} to '
        f'{eleven["validation_loss_after"]:.4f}; validation loss selects step {eleven["selected_step"]} '
        f'within the {eleven["steps"]}-step maximum. On {eleven["test_examples"]} balanced final messages, '
        f'JSON validity changes from {eleven["base_schema_rate"]:.0%} to {eleven["adapted_schema_rate"]:.0%}, '
        f'and label accuracy from {eleven["base_generation_accuracy"]:.0%} to {eleven["adapted_generation_accuracy"]:.0%}.\n\n'
        '**Explain the improvement.** This study updates rank-8 adapters in every query/value layer, rather than '
        'eight updates to a single rank-2 projection. More training capacity and examples can change completion behavior. '
        'The checkpoint uses validation loss only; the final comparison cannot choose steps. '
        'The rank-2 hand construction remains useful for understanding the matrix operation.\n\n'
        '**Check what each output establishes.** validation_generation.csv provides development format/label checks; '
        'generation_comparison.csv provides the frozen final comparison. Safetensors replay checks serialization, '
        'not quality. Valid JSON can still be wrong, the balanced sample changes prevalence, and the interval '
        'does not correct historical sampling bias. If the last checkpoint wins, later training behavior is unknown.'
    )
    rows.append(f'| 14 | {agent["requests"]} authored final controls | Routing '
                f'{agent["routing_interval"]["successes"]}/{agent["requests"]} = {agent["routing_accuracy"]:.3f} | '
                f'Correct refusals {agent["unsupported_correctly_refused"]}/{agent["unsupported_requests"]}; '
                'no destructive tools available |')
    diagnoses[14] = (
        f'**Recorded evidence.** Routing is correct for {agent["routing_interval"]["successes"]} of '
        f'{agent["requests"]} authored final requests ({agent["routing_accuracy"]:.1%}). The model correctly refuses '
        f'{agent["unsupported_correctly_refused"]} of {agent["unsupported_requests"]} unsupported requests. '
        f'The validation-selected scoring rule is `{agent["routing_rule"]}`.\n\n'
        '**Inspect actual mistakes.** request_trace.csv includes expected_tool, chosen_tool and correct; '
        'routing_confusion.csv exposes which intents are confused. Read a wrong refusal and a wrong permitted '
        'operation if present. A one-call limit does not make an irrelevant answer correct.\n\n'
        '**Separate control from understanding.** The workflow plans, observes one allowlisted tool result and '
        'answers using that evidence. The model cannot add a write/shell/export capability. This permission '
        'boundary is enforced independently of whether a destructive request is correctly refused; '
        'there is no keyword denylist credited as model intelligence. Test the smaller max_steps budgets '
        'and explain why an incomplete workflow must not claim an evidence-backed answer. '
        'The authored controls and six validation examples are small; their interval does not estimate real-user reliability.'
    )
    for n, name in NAMES.items():
        path = ROOT / 'docs/lessons' / name / 'feedback.md'
        source = path.read_text()
        start = source.index('## Diagnose the verified run\n') + len('## Diagnose the verified run\n')
        end = source.index('\n## Transfer cautiously', start)
        source = source[:start] + '\n' + diagnoses[n] + '\n' + source[end:]
        if n in [9, 10]:
            start = source.index('## A reasoned interpretation\n') + len('## A reasoned interpretation\n')
            end = source.index('\n## What a good explanation contains', start)
            source = source[:start] + '\nCompare the current run below with the [archived under-trained/failed baseline](../../maintenance/reviews/framework-baseline-0.7.0.md). The archive records earlier settings; it is not the current protocol. A working mechanism and a useful task model require different evidence.\n' + source[end:]
        path.write_text(source)
    heading = '# Recorded Phase B framework results\n\n'
    context = ('Generated from actual `runs/verified/moduleNN/summary.json` files using '
               '`python scripts/update_framework_results.py`. Regenerate after changing the protocol; '
               'the site builder does not fabricate results or silently update source.\n\n'
               'These historical benchmarks and authored controls have been inspected during development. '
               'Repeated evaluation is a teaching/reproduction exercise, not a new prospective holdout claim. '
               'The Module 10 prevalence-preserving subset and Module 11 balanced subset differ; '
               'their accuracy values are not a matched cross-module comparison.\n\n')
    table = '| Module | Evaluation sample | Recorded result | Comparison / qualification |\n| --- | --- | --- | --- |\n' + '\n'.join(rows) + '\n'
    links = '\n## Reproduce and inspect\n\n'
    for n, name in NAMES.items():
        links += f'- [Module {n} workflow](lessons/{name}/index.md) and [feedback](lessons/{name}/feedback.md).\n'
    links += '\nThe [historical baseline](maintenance/reviews/framework-baseline-0.7.0.md) retains the earlier failure cases. Consult each report’s rate_intervals.csv where provided. Remaining repository-wide uncertainty work belongs to Phase C.\n'
    (ROOT / 'docs/framework-results.md').write_text(heading + context + table + links)
    path = ROOT / 'docs/status.md'
    source = path.read_text()
    source = source.replace('These are the actual results of the verified runs used to build edition 0.7.0.', 'The table below preserves the earlier edition 0.7.0 snapshot. **For the revised framework protocols and current measured results, use [Phase B results](framework-results.md).**')
    source = source.replace('Several framework results are weak or failed; each module\'s feedback page explains why in **Diagnose the verified run**.', 'Earlier weak framework runs are archived for diagnosis; current module feedback discusses the revised runs.')
    path.write_text(source)
    print('Updated five feedback pages and the source-backed framework-results page.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runs', type=Path, default=ROOT / 'runs/verified')
    refresh(parser.parse_args().runs)
