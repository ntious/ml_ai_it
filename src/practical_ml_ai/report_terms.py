"""Plain-language definitions included with classification reports, also offline."""
from html import escape

TERMS = {
    "tp": "True positives: actual positive examples correctly flagged positive.",
    "fp": "False positives: actual negative examples incorrectly flagged positive.",
    "fn": "False negatives: actual positive examples missed by the classifier.",
    "tn": "True negatives: actual negative examples correctly classified negative.",
    "precision": "Of the examples flagged positive, the fraction actually positive: TP / (TP + FP).",
    "recall": "Of all actual positives, the fraction found: TP / (TP + FN).",
    "specificity": "Of all actual negatives, the fraction correctly rejected: TN / (TN + FP).",
    "f1": "Harmonic mean of precision and recall: 2TP / (2TP + FP + FN). It does not include true negatives.",
    "balanced_accuracy": "Mean of recall and specificity, giving each class equal weight regardless of its size.",
    "fpr": "False-positive rate: FP / (FP + TN), the fraction of actual negatives incorrectly flagged.",
    "selection_rate": "Fraction of all examples flagged positive; this describes workload, not correctness.",
    "split_group_overlap": "Whether a declared group occurs in more than one partition. False means no overlap under that grouping rule; it does not prove all leakage is absent.",
    "calibration": "Compare predicted probabilities with observed positive frequencies in score bins. Similar values support calibration on these observations, not guaranteed correctness for an individual prediction.",
}


def explain_terms(summary, tables):
    """Select definitions from the fields and table names actually shown."""
    keys = set()
    def collect(value):
        if isinstance(value, dict):
            keys.update(str(k) for k in value)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)
    collect(summary)
    for name, frame in tables.items():
        keys.update(str(c) for c in frame.columns)
        if "calibration" in name:
            keys.add("calibration")
    selected = [(k, v) for k, v in TERMS.items() if k in keys]
    if not selected:
        return "", ""
    caveat = "Positive means the study's declared target class. Undefined ratios are reported as null/None rather than evidence of zero performance."
    text = "Reading these results\n" + caveat + "\n" + "\n".join(f"{k}: {v}" for k, v in selected)
    html = '<section><h2>Reading these results</h2><p>' + escape(caveat) + '</p><dl>'
    html += ''.join('<dt><code>' + escape(k) + '</code></dt><dd>' + escape(v) + '</dd>' for k, v in selected)
    return text, html + '</dl></section>'
