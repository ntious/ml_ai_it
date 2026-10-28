"""Evaluated retrieval over original fictional IT runbooks.

Retrieval-augmented generation (RAG) first retrieves passages, then answers
from them. This exercise evaluates the retrieval step and an abstention rule,
which decide what any answer can be grounded in. Settings and the abstention
threshold are chosen on validation questions; the locked choice is evaluated
once on test questions, including questions the corpus cannot answer.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data/samples/runbooks/runbooks.json"
QUESTIONS = ROOT / "data/samples/runbooks/questions.json"
SETTINGS = [{"ngram_range": [1, 1], "sublinear_tf": False}, {"ngram_range": [1, 1], "sublinear_tf": True},
            {"ngram_range": [1, 2], "sublinear_tf": False}, {"ngram_range": [1, 2], "sublinear_tf": True}]
THRESHOLDS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
K = 3


def load(corpus=CORPUS, questions=QUESTIONS):
    passages = json.loads(Path(corpus).read_text(encoding="utf-8"))["passages"]
    asked = json.loads(Path(questions).read_text(encoding="utf-8"))["questions"]
    return passages, asked


def rank(passages, questions, settings):
    """Return passage IDs ordered by similarity and the top similarity for each question."""
    # The index is fitted on the corpus only; questions are transformed, never fitted.
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=tuple(settings["ngram_range"]), sublinear_tf=settings["sublinear_tf"])
    index = vectorizer.fit_transform([p["title"] + ". " + p["text"] for p in passages])
    similarity = cosine_similarity(vectorizer.transform([q["question"] for q in questions]), index)
    ids = np.array([p["id"] for p in passages])
    order = np.argsort(-similarity, axis=1, kind="stable")
    return [list(ids[row]) for row in order], similarity.max(axis=1)


def evaluate(questions, ranked, top, threshold):
    """Recall@K and MRR on answerable questions; decision accuracy including abstention."""
    rows = []
    for question, order, score in zip(questions, ranked, top):
        relevant = set(question["relevant"])
        answer = order[0] if score >= threshold else None
        position = next((i + 1 for i, pid in enumerate(order) if pid in relevant), None)
        rows.append({"id": question["id"], "answerable": bool(relevant), "top_passage": order[0], "top_similarity": float(score),
                     "answered_with": answer, "relevant_rank": position,
                     "decision_correct": (answer in relevant) if relevant else answer is None})
    table = pd.DataFrame(rows)
    answerable = table[table.answerable]
    metrics = {"questions": len(table), "answerable": len(answerable), "unanswerable": int((~table.answerable).sum()),
               f"recall_at_{K}": float((answerable.relevant_rank <= K).mean()),
               "mrr": float((1 / answerable.relevant_rank).mean()),
               "decision_accuracy": float(table.decision_correct.mean()),
               "unanswerable_abstained": int(((~table.answerable) & table.answered_with.isna()).sum()),
               "answerable_wrongly_abstained": int((table.answerable & table.answered_with.isna()).sum())}
    return table, metrics


def choose(passages, questions):
    validation = [q for q in questions if q["split"] == "validation"]
    trials = []
    for settings in SETTINGS:
        ranked, top = rank(passages, validation, settings)
        for threshold in THRESHOLDS:
            _, metrics = evaluate(validation, ranked, top, threshold)
            trials.append({"settings": json.dumps(settings, sort_keys=True), "threshold": threshold, **metrics})
    table = pd.DataFrame(trials)
    # Highest decision accuracy, then MRR; ties prefer the earlier settings and the lower threshold.
    best = table.sort_values(["decision_accuracy", "mrr"], ascending=False, kind="stable").iloc[0]
    return table, json.loads(best.settings), float(best.threshold)


def run(passages, questions):
    trials, settings, threshold = choose(passages, questions)
    test = [q for q in questions if q["split"] == "test"]
    ranked, top = rank(passages, test, settings)
    table, metrics = evaluate(test, ranked, top, threshold)
    return trials, table, {"chosen_settings": settings, "chosen_threshold": threshold, "test": metrics}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", required=True, help="A new directory for this exercise's evidence.")
    parser.add_argument("--track", help="Optional JSON-lines experiment log to append this run to.")
    args = parser.parse_args(argv)
    output = Path(args.output)
    if output.exists():
        raise SystemExit(f"Choose a new output directory: {output}")
    passages, questions = load()
    trials, table, summary = run(passages, questions)
    output.mkdir(parents=True)
    trials.to_csv(output / "validation_trials.csv", index=False)
    table.to_csv(output / "test_decisions.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    test = summary["test"]
    lines = ["Runbook retrieval exercise (original fictional corpus)",
             f"Chosen on validation: {json.dumps(summary['chosen_settings'], sort_keys=True)}, abstain below similarity {summary['chosen_threshold']}",
             f"Test: recall@{K} {test[f'recall_at_{K}']:.3f} and MRR {test['mrr']:.3f} on {test['answerable']} answerable questions",
             f"Test decisions correct: {test['decision_accuracy']:.3f} of {test['questions']}; abstained on {test['unanswerable_abstained']} of {test['unanswerable']} unanswerable; wrongly abstained on {test['answerable_wrongly_abstained']} answerable"]
    (output / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if args.track:
        from .tracking import record
        record(args.track, "runbook-retrieval", {**summary["chosen_settings"], "threshold": summary["chosen_threshold"]},
               {key: value for key, value in test.items() if isinstance(value, float)}, inputs=[CORPUS, QUESTIONS])


if __name__ == "__main__":
    main()
