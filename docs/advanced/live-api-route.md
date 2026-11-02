# Optional live API route

This guide supports the course outcome on integrating generative AI and LLM-based systems into IT workflows. The required [Module 10](../lessons/10-llm-workflows/index.md) work runs a local model and needs no paid account. It does not show that you can call a hosted provider. This page describes an optional route for adopters who want that evidence. The repository does not make a live call for you, store credentials, or require any account.

## Decide first

Ask the course owner whether a live call is required. If it is, arrange approved access and a spending limit. Do not make a personal paid subscription a hidden prerequisite. If it is not required, use the module's local-model activities for its learning outcomes; this fixture exercise supplies only additional contract-handling practice.

## Keep these three things apart

| Route | What it shows | What it does not show |
| --- | --- | --- |
| Offline fixture | Your validation, retry, and error-handling logic works on saved responses | That any provider accepted a request |
| Local model | Prompting, evaluation, and output-contract checks on your machine | Hosted-provider behavior, quotas, or latency |
| Live call | A real request and response, with cost and failure handling | Production readiness |

State which route produced each result in your report. A fixture result is never presented as a live result.

## Provider-neutral client pattern

The package provides `practical_ml_ai.llm_client`, with the provider call as one replaceable function. Tests pass a fake function and exercise everything else offline, and a real provider function can replace it later. `check_output` requires exactly a permitted string label and a nonempty string reason. A structurally valid reason may still be incorrect. `classify` retries timeouts and connection errors with a limit and returns the result with the number of calls used.

```python
from practical_ml_ai.llm_client import classify

def fake_send(prompt):
    return '{"label": "spam", "reason": "asks for a code"}'

result, calls = classify(fake_send, "Classify: win a prize", {"spam", "ham"})
print(result["label"], calls)  # spam 1
```

Practice offline with fakes that fail in each way: a timeout, malformed JSON, an extra field, and an unlisted label. [tests/test_bridge_tools.py](https://github.com/ntious/ml_ai_it/blob/main/tests/test_bridge_tools.py) shows each case. Count how many calls each one consumed. Invalid output raises `OutputContractError` immediately; it is not retried as a transient connection problem. Unexpected errors are not swallowed. Only `TimeoutError` and `ConnectionError` are retried, up to the declared attempt count. A provider adapter must translate its SDK exceptions deliberately, set a request timeout and handle refusals and rate limits. The wrapper itself does not enforce request timeouts or measure cost.

## If you add a live call

- Read credentials from an environment variable. Never place a key in code, a notebook, a prompt, or a saved log.
- Send only text that is approved for that provider. Mask contact details and personal content first.
- Set a timeout, a retry limit, and a maximum number of calls so a loop cannot run up cost.
- Save the model name, date, request count, and failures. Provider models change, so a result is tied to its date.
- Handle rate limits and refusals as normal outcomes, not surprises.

## Evidence to submit

1. The route used for each result: fixture, local, or live.
2. The failure cases you tested and what each one did.
3. A short paragraph on which checks would catch fluent but wrong output, and which would not.
4. For a live run, the call count, cost, and any content you chose not to send.

Fixtures supply the practice. A live run only adds the real provider step.
