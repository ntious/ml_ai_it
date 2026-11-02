# Optional live API route

This guide supports the course outcome on integrating generative AI and LLM-based systems into IT workflows. The required [Module 10](../lessons/10-llm-workflows/index.md) work runs a local model and needs no paid account. It does not show that you can call a hosted provider. This page describes an optional route for adopters who want that evidence. The repository does not make a live call for you, store credentials, or require any account.

## Decide first

Ask the course owner whether a live call is required. If it is, arrange approved access and a spending limit. Do not make a personal paid subscription a hidden prerequisite. If it is not required, the local route and the fixture practice below meet the module's own outcomes.

## Keep these three things apart

| Route | What it shows | What it does not show |
| --- | --- | --- |
| Offline fixture | Your validation, retry, and error-handling logic works on saved responses | That any provider accepted a request |
| Local model | Prompting, evaluation, and output-contract checks on your machine | Hosted-provider behavior, quotas, or latency |
| Live call | A real request and response, with cost and failure handling | Production readiness |

State which route produced each result in your report. A fixture result is never presented as a live result.

## Provider-neutral client pattern

Write the workflow so the provider call is one replaceable function. Tests then pass a fake function and exercise everything else offline. The same wrapper accepts a real provider function later.

```python
import json
import time


class OutputContractError(ValueError):
    pass


def check_output(text, allowed_labels):
    """Accept only the declared JSON shape; anything else is a contract failure."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise OutputContractError("not valid JSON") from error
    if set(data) != {"label", "reason"} or data["label"] not in allowed_labels:
        raise OutputContractError("unexpected fields or label")
    return data


def classify(send, prompt, allowed_labels, attempts=3, wait=0.0):
    """Call send(prompt), retry transient failures, and never accept unchecked output."""
    last = None
    for attempt in range(attempts):
        try:
            return check_output(send(prompt), allowed_labels)
        except (TimeoutError, ConnectionError, OutputContractError) as error:
            last = error
            time.sleep(wait * (2 ** attempt))
    raise RuntimeError(f"gave up after {attempts} attempts: {last}")
```

Practice offline with fakes that fail in each way: a timeout, malformed JSON, an extra field, and an unlisted label. Count how many calls each case consumed.

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
