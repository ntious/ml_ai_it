"""Retrieval, API and tracking extensions keep their evaluation and contract boundaries."""
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from practical_ml_ai import api, retrieval, tracking


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.passages, self.questions = retrieval.load()

    def test_corpus_and_questions_are_consistent(self):
        ids = {p["id"] for p in self.passages}
        for question in self.questions:
            self.assertTrue(set(question["relevant"]) <= ids, question["id"])
            self.assertIn(question["split"], {"validation", "test"})
        for split in ["validation", "test"]:
            part = [q for q in self.questions if q["split"] == split]
            self.assertTrue(any(q["relevant"] for q in part) and any(not q["relevant"] for q in part))

    def test_test_questions_cannot_change_the_locked_choice(self):
        _, settings, threshold = retrieval.choose(self.passages, self.questions)
        altered = [dict(q, relevant=[] if q["split"] == "test" else q["relevant"]) for q in self.questions]
        self.assertEqual(retrieval.choose(self.passages, altered)[1:], (settings, threshold))

    def test_abstention_counts_unanswerable_questions(self):
        questions = [{"id": "a", "question": "q", "relevant": ["x"]}, {"id": "b", "question": "q", "relevant": []}]
        table, metrics = retrieval.evaluate(questions, [["x", "y"], ["x", "y"]], np.array([.5, .05]), .1)
        self.assertEqual((metrics["decision_accuracy"], metrics["unanswerable_abstained"], metrics["mrr"]), (1.0, 1, 1.0))
        table, metrics = retrieval.evaluate(questions, [["y", "x"], ["x", "y"]], np.array([.05, .5]), .1)
        self.assertEqual((metrics["decision_accuracy"], metrics["answerable_wrongly_abstained"], metrics["mrr"]), (0.0, 1, .5))

    def test_recorded_run(self):
        _, _, summary = retrieval.run(self.passages, self.questions)
        self.assertEqual(summary["chosen_threshold"], 0.15)
        self.assertEqual((summary["test"]["recall_at_3"], summary["test"]["unanswerable_abstained"]), (1.0, 2))


def fake_bundle():
    rng = np.random.default_rng(1)
    train = pd.DataFrame({"a": rng.normal(size=80), "b": rng.normal(size=80)})
    model = LogisticRegression().fit(train, (train.a > 0).astype(int))
    return {"features": ["a", "b"], "split": {"train": train}, "model": model, "selection": {"model": "logistic", "threshold": .5}}


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = api.create_server(fake_bundle(), port=0)
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close()

    def call(self, path, body=None):
        data = None if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode())
        request = urllib.request.Request(self.url + path, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_health_and_valid_prediction(self):
        self.assertEqual(self.call("/health")[0], 200)
        status, body = self.call("/predict", {"a": 2.0, "b": 0.0})
        self.assertEqual((status, body["predicted"]), (200, 1))
        self.assertTrue(0 <= body["probability"] <= 1)

    def test_contract_violations_are_rejected_with_reasons(self):
        for record in [{"a": 1.0}, {"a": 1.0, "b": 0.0, "label": 1}, {"a": True, "b": 0.0}, {"a": "1", "b": 0.0}]:
            status, body = self.call("/predict", record)
            self.assertEqual(status, 422, record)
            self.assertTrue(body["error"])
        self.assertEqual(self.call("/predict", b"{not json")[0], 400)
        self.assertEqual(self.call("/other")[0], 404)


class TrackingTests(unittest.TestCase):
    def test_records_settings_metrics_environment_and_input_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.txt"; source.write_bytes(b"data\n")
            log = Path(folder) / "runs/log.jsonl"
            tracking.record(log, "demo", {"k": 3}, {"score": .5}, inputs=[source])
            tracking.record(log, "demo", {"k": 5}, {"score": .6})
            entries = tracking.read(log)
        self.assertEqual([e["settings"]["k"] for e in entries], [3, 5])
        self.assertEqual(entries[0]["inputs"][str(source)], "6667b2d1aab6a00caa5aee5af8ad9f1465e567abf1c209d15727d57b3e8f6e5f")
        self.assertIn("python", entries[0]["environment"])


if __name__ == "__main__":
    unittest.main()
