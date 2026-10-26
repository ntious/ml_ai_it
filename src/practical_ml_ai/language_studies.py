"""Matched SMS experiments: candidate scoring, generation and trained PEFT LoRA.

Templates and budgets are declared before final evaluation. Authored agent
requests are separate from these human-annotated external SMS records.
"""
import copy
import json
import time

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from .continuation_data import (
    balanced_real_subset, binary_metrics, new_run, publish_report, sms_splits, write_json,
)
from .learning import wilson_interval
from .language import (
    MODEL_ID, MODEL_REVISION, generate_label, local_model, packed_example,
    sms_content, sms_prompt,
)


def rate_record(method, metric, successes, observations):
    low, high = wilson_interval(int(successes), int(observations))
    return {"method": method, "metric": metric, "successes": int(successes),
            "observations": int(observations), "rate": successes / observations,
            "ci_low": low, "ci_high": high, "confidence": .95}


def completion_scores(model, tokenizer, prompt, candidates):
    """Sum conditional completion log probabilities; scores are not confidence."""
    import torch
    prefix = tokenizer.encode(prompt, add_special_tokens=False)
    scores = []
    model.eval()
    with torch.no_grad():
        for candidate in candidates:
            completion = tokenizer.encode(candidate, add_special_tokens=False)
            inputs = torch.tensor([prefix + completion])
            labels = torch.tensor([[-100] * len(prefix) + completion])
            # HF loss averages over non-masked labels; undo that normalization.
            loss = model(input_ids=inputs, labels=labels, use_cache=False).loss
            scores.append(-float(loss) * len(completion))
    return scores


def score_label(model, tokenizer, text, examples=None):
    candidates = ['{"label":"ham"}', '{"label":"spam"}']
    scores = completion_scores(model, tokenizer, sms_prompt(tokenizer, text, examples), candidates)
    return int(np.argmax(scores)), scores


def evaluation_subset(frame, count):
    if isinstance(count, bool) or not isinstance(count, int) or not 20 <= count <= len(frame):
        raise ValueError(f"Choose 20–{len(frame)} examples before evaluation.")
    if count == len(frame):
        return frame.copy().reset_index(drop=True)
    if len(frame) - count < frame.label.nunique():
        # A one-row remainder cannot itself be stratified. Drop one seeded row
        # from the majority class, retaining both labels in the near-full set.
        majority = frame.label.mode().iloc[0]
        drop = frame.loc[frame.label == majority].sample(n=len(frame) - count, random_state=45).index
        return frame.drop(index=drop).sort_values("text_id").reset_index(drop=True)
    chosen, _ = train_test_split(frame, train_size=count, stratify=frame.label, random_state=45)
    return chosen.sort_values("text_id").reset_index(drop=True)


def run_llm(output, examples=100):
    directory = new_run(output)
    model, tokenizer, revision = local_model()
    split, manifest = sms_splits(limit=None)
    test = evaluation_subset(split["test"], examples)
    demonstrations = list(balanced_real_subset(split["train"], 4).itertuples())
    # Estimate a decision threshold on 100 validation messages. A softmax over
    # two candidate likelihoods is a relative score, not calibrated confidence.
    validation = evaluation_subset(split["validation"], 100)
    validation_scores = []
    for row in validation.itertuples():
        _, scores = score_label(model, tokenizer, row.text, demonstrations)
        relative = float(1 / (1 + np.exp(np.clip(scores[0] - scores[1], -700, 700))))
        validation_scores.append({"text_id": row.text_id, "actual": row.label, "relative_spam_score": relative})
    from .neural import select_threshold
    validation_table = pd.DataFrame(validation_scores)
    llm_threshold, llm_thresholds = select_threshold(validation_table.actual, validation_table.relative_spam_score)
    baseline = make_pipeline(TfidfVectorizer(min_df=2, ngram_range=(1, 2)),
                             LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
    baseline.fit(split["train"].text.map(sms_content), split["train"].label)
    # Threshold chosen on validation, not the matched final comparison.
    threshold, threshold_table = select_threshold(
        split["validation"].label,
        baseline.predict_proba(split["validation"].text.map(sms_content))[:, 1],
    )
    baseline_labels = baseline.predict_proba(test.text.map(sms_content))[:, 1] >= threshold
    records = []
    for index, row in enumerate(test.itertuples()):
        started = time.perf_counter()
        raw_scored, scores = score_label(model, tokenizer, row.text, demonstrations)
        relative = float(1 / (1 + np.exp(np.clip(scores[0] - scores[1], -700, 700))))
        scored = int(relative >= llm_threshold)
        scoring_seconds = time.perf_counter() - started
        label, raw, seconds = generate_label(model, tokenizer, row.text, demonstrations)
        records.append({"text_id": row.text_id, "actual": row.label, "predicted": label,
                        "schema_valid": label is not None, "correct": label == row.label,
                        "seconds": seconds, "response": raw, "scored_predicted": scored,
                        "raw_likelihood_predicted": raw_scored, "relative_spam_score": relative,
                        "scored_correct": scored == row.label, "ham_log_probability": scores[0],
                        "spam_log_probability": scores[1], "scoring_seconds": scoring_seconds,
                        "baseline_predicted": int(baseline_labels[index]),
                        "baseline_correct": bool(baseline_labels[index] == row.label)})
    table = pd.DataFrame(records)
    majority = int(split["train"].label.mode().iloc[0])
    majority_labels = np.full(len(test), majority)
    table["majority_correct"] = test.label.to_numpy() == majority
    intervals = [rate_record(method, metric, table[column].sum(), len(table))
                 for method, metric, column in [("free_generation", "schema_validity", "schema_valid"),
                                                ("free_generation", "accuracy", "correct"),
                                                ("label_likelihood", "accuracy", "scored_correct"),
                                                ("lexical", "accuracy", "baseline_correct"),
                                                ("training_majority", "accuracy", "majority_correct")]]
    confusion = [{"method": name, **binary_metrics(test.label, prediction)}
                 for name, prediction in [("label_likelihood", table.scored_predicted),
                                          ("lexical", table.baseline_predicted),
                                          ("training_majority", majority_labels)]]
    manifest["evaluation_text_ids"] = test.text_id.tolist()
    manifest["demonstration_text_ids"] = [row.text_id for row in demonstrations]
    write_json(directory / "split_manifest.json", manifest)
    summary = {"module": 10, "model": MODEL_ID, "revision": revision, "real_examples": len(test),
               "sampling": "Seeded label-stratified subset of the deduplicated final split; historical sample, not deployment prevalence",
               "strict_schema_rate": float(table.schema_valid.mean()),
               "exact_label_accuracy_including_invalid_as_wrong": float(table.correct.mean()),
               "label_likelihood_accuracy": float(table.scored_correct.mean()),
               "matched_baseline_accuracy": float(table.baseline_correct.mean()),
               "majority_accuracy": float(table.majority_correct.mean()),
               "baseline_threshold": threshold, "likelihood_threshold": llm_threshold, "rate_intervals": intervals,
               "mean_generation_seconds": float(table.seconds.mean()),
               "mean_scoring_seconds": float(table.scoring_seconds.mean()),
               "comparison_contract": "Same IDs and masked first 240 characters; four real training-only demonstrations for both LLM methods; baseline fits training and selects threshold on validation.",
               "decoding": "greedy free generation vs exhaustive conditional JSON-candidate likelihood",
               "contact_masking": "Regex masking reduces contact display; not a privacy guarantee"}
    return publish_report(directory, "Module 10: likelihood scoring versus free generation", summary,
                          {"generation_evaluation": table, "matched_comparison": table.drop(columns="response"),
                           "rate_intervals": pd.DataFrame(intervals), "confusion_counts": pd.DataFrame(confusion),
                           "llm_validation_predictions": validation_table, "llm_validation_thresholds": llm_thresholds,
                           "baseline_validation_thresholds": threshold_table},
                          ["Candidate scoring always returns a legal label by construction. It does not demonstrate that the model learned JSON generation or that its label is correct.",
                           "Invalid free-generated JSON is counted as wrong; no repair, retries or test-selected prompts.",
                           "Wilson 95% intervals describe binomial sampling uncertainty, not dataset shift, sampling bias or paired method differences.",
                           "Demonstrations are real training records; reports use hashes rather than raw SMS. Latencies exclude model loading and training."])


def completion_batch(tokenizer, rows):
    """Right padding; prompt and padding labels are masked independently."""
    import torch
    packed = [packed_example(tokenizer, row) for row in rows]
    length = max(item[0].shape[1] for item in packed)
    inputs = torch.full((len(packed), length), tokenizer.pad_token_id, dtype=torch.long)
    labels = torch.full_like(inputs, -100)
    attention = torch.zeros_like(inputs)
    for index, (tokens, targets) in enumerate(packed):
        width = tokens.shape[1]
        inputs[index, :width], labels[index, :width] = tokens[0], targets[0]
        attention[index, :width] = 1
    return {"input_ids": inputs, "labels": labels, "attention_mask": attention}


def frame_loss(model, tokenizer, frame):
    """Mean per-example completion loss, using the same boundary in every arm."""
    import torch
    values = []
    model.eval()
    with torch.no_grad():
        for row in frame.itertuples():
            values.append(float(model(**completion_batch(tokenizer, [row]), use_cache=False).loss))
    return float(np.mean(values))


def generated_comparison(model, tokenizer, frame, base_labels):
    adapted = [generate_label(model, tokenizer, row.text)[0] for row in frame.itertuples()]
    table = pd.DataFrame({"text_id": frame.text_id, "actual": frame.label,
                          "base_predicted": base_labels, "adapted_predicted": adapted})
    for prefix, labels in [("base", base_labels), ("adapted", adapted)]:
        table[prefix + "_schema_valid"] = [label is not None for label in labels]
        table[prefix + "_correct"] = [label == int(actual) for label, actual in zip(labels, frame.label)]
    return table


def run_finetuning(output, steps=200):
    """Train all-layer q/v LoRA; select checkpoint using validation loss only."""
    import torch
    from peft import LoraConfig, PeftModel, TaskType, get_peft_model
    from safetensors.torch import load_file
    if isinstance(steps, bool) or not isinstance(steps, int) or not 1 <= steps <= 300:
        raise ValueError("Choose 1–300 training steps before final evaluation.")
    directory = new_run(output)
    base, tokenizer, revision = local_model()
    # PEFT wraps modules in-place. Clone so the cached base and later studies stay untouched.
    model = copy.deepcopy(base)
    split, manifest = sms_splits(limit=None)
    training = balanced_real_subset(split["train"], 256)
    validation = balanced_real_subset(split["validation"], 40)
    test = balanced_real_subset(split["test"], 100)
    before_validation = frame_loss(base, tokenizer, validation)
    base_validation_labels = [generate_label(base, tokenizer, row.text)[0] for row in validation.itertuples()]
    torch.manual_seed(42)
    config = LoraConfig(task_type=TaskType.CAUSAL_LM, revision=revision, r=8, lora_alpha=16,
                        target_modules=["q_proj", "v_proj"], lora_dropout=0., bias="none")
    model = get_peft_model(model, config)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=.001)
    rng = np.random.default_rng(42)
    order, cursor = rng.permutation(len(training)), 0
    best_loss, best_step, history = before_validation, 0, []
    # A zero-step adapter is an eligible checkpoint if training fails to improve validation loss.
    model.save_pretrained(directory / "adapter", safe_serialization=True)
    for step in range(1, steps + 1):
        if cursor + 8 > len(order):
            order, cursor = rng.permutation(len(training)), 0
        rows = list(training.iloc[order[cursor:cursor + 8]].itertuples())
        cursor += 8
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = model(**completion_batch(tokenizer, rows), use_cache=False).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.)
        optimizer.step()
        measured = None
        if step % 25 == 0 or step == steps:
            measured = frame_loss(model, tokenizer, validation)
            if measured < best_loss:
                best_loss, best_step = measured, step
                model.save_pretrained(directory / "adapter", safe_serialization=True)
            print("LORA_VALIDATION", json.dumps({"step": step, "loss": measured, "selected_step": best_step}), flush=True)
        history.append({"step": step, "training_completion_loss": float(loss.detach()),
                        "validation_completion_loss": measured,
                        "training_text_ids": "|".join(row.text_id for row in rows)})
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    # Reload the selected checkpoint before validation generation and any final evaluation.
    del optimizer, model
    model = PeftModel.from_pretrained(copy.deepcopy(base), directory / "adapter", is_trainable=False)
    after_validation = frame_loss(model, tokenizer, validation)
    validation_table = generated_comparison(model, tokenizer, validation, base_validation_labels)
    # Final evaluation begins here. It cannot select a checkpoint or change training.
    base_test = frame_loss(base, tokenizer, test)
    adapted_test = frame_loss(model, tokenizer, test)
    base_labels = [generate_label(base, tokenizer, row.text)[0] for row in test.itertuples()]
    test_table = generated_comparison(model, tokenizer, test, base_labels)
    with torch.no_grad():
        probe = completion_batch(tokenizer, [next(test.itertuples())])
        expected_logits = model(**probe, use_cache=False).logits.detach().clone()
    del model
    reloaded = PeftModel.from_pretrained(copy.deepcopy(base), directory / "adapter", is_trainable=False)
    with torch.no_grad():
        replay = reloaded(**probe, use_cache=False).logits
    torch.testing.assert_close(replay, expected_logits, atol=1e-6, rtol=1e-5)
    weights = load_file(directory / "adapter/adapter_model.safetensors")
    update_norm = float(np.sqrt(sum(float(tensor.square().sum()) for name, tensor in weights.items() if "lora_B" in name)))
    del reloaded
    intervals = [rate_record(prefix, metric, test_table[column].sum(), len(test))
                 for prefix in ["base", "adapted"]
                 for metric, column in [("schema_validity", prefix + "_schema_valid"), ("accuracy", prefix + "_correct")]]
    manifest.update(training_subset=training.text_id.tolist(), validation_subset=validation.text_id.tolist(),
                    final_subset=test.text_id.tolist())
    write_json(directory / "split_manifest.json", manifest)
    write_json(directory / "study_config.json", {"base_model": MODEL_ID, "revision": MODEL_REVISION,
               "rank": 8, "target_modules": ["q_proj", "v_proj"], "layers": "all", "batch_size": 8,
               "learning_rate": .001, "maximum_steps": steps, "selected_step": best_step,
               "selection": "minimum validation completion loss, including step zero", "prompt_loss_mask": -100})
    summary = {"module": 11, "base_model": MODEL_ID, "revision": revision, "steps": steps,
               "selected_step": best_step, "trainable_parameters": trainable,
               "adapter_update_norm": update_norm, "adapter_replay_verified": True,
               "validation_loss_before": before_validation, "validation_loss_after": after_validation,
               "validation_base_schema_rate": float(validation_table.base_schema_valid.mean()),
               "validation_adapted_schema_rate": float(validation_table.adapted_schema_valid.mean()),
               "base_test_completion_loss": base_test, "adapted_test_completion_loss": adapted_test,
               "base_generation_accuracy": float(test_table.base_correct.mean()),
               "adapted_generation_accuracy": float(test_table.adapted_correct.mean()),
               "base_schema_rate": float(test_table.base_schema_valid.mean()),
               "adapted_schema_rate": float(test_table.adapted_schema_valid.mean()),
               "test_examples": len(test), "rate_intervals": intervals,
               "quality_claim": "Historical class-balanced sample; format compliance and label correctness are separate"}
    return publish_report(directory, "Module 11: trained all-layer LoRA and matched replay", summary,
                          {"training_history": pd.DataFrame(history), "generation_comparison": test_table,
                           "validation_generation": validation_table, "rate_intervals": pd.DataFrame(intervals)},
                          ["Only all-layer q/v LoRA parameters train. The cached base remains unchanged; the best validation-loss checkpoint is loaded before final evaluation.",
                           "Training/validation/final subsets contain disjoint real text IDs. Prompt and padding tokens carry label -100.",
                           "Schema-valid JSON can still have the wrong label. The balanced final subset changes prevalence; binomial intervals do not correct sampling bias.",
                           "Adapters are saved as safetensors with PEFT configuration and exact base revision; reloaded logits must match."])
