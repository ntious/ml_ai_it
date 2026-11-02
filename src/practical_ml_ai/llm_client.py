"""Provider-neutral wrapper for a language-model call with checked output.

The provider is one replaceable function, so every failure path can be tested
offline with fakes. Nothing here contacts a service, reads credentials or
retries without a limit.
"""
import json
import math
import time


class OutputContractError(ValueError):
    """Model output did not match the declared JSON shape."""


def check_output(text, allowed_labels):
    """Accept exactly {"label", "reason"} with a listed label; reject everything else."""
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError) as error:
        raise OutputContractError("not valid JSON") from error
    if not isinstance(data, dict) or set(data) != {"label", "reason"} or not isinstance(data["label"], str) or not isinstance(data["reason"], str) or not data["reason"].strip() or data["label"] not in allowed_labels:
        raise OutputContractError("unexpected fields or label")
    return data


def classify(send, prompt, allowed_labels, attempts=3, wait=0.0):
    """Call send(prompt), retry transient failures with doubling waits, never accept unchecked output.

    Returns (result, calls_used). Raises RuntimeError after `attempts` transport failures.
    Invalid output raises OutputContractError immediately; retrying it needs a separate policy.
    """
    if isinstance(attempts, bool) or not isinstance(attempts, int) or attempts < 1:
        raise ValueError("attempts must be a positive integer")
    if isinstance(wait, bool) or not isinstance(wait, (int, float)) or not math.isfinite(wait) or wait < 0:
        raise ValueError("wait must be finite and nonnegative")
    last = None
    for attempt in range(attempts):
        try:
            return check_output(send(prompt), allowed_labels), attempt + 1
        except (TimeoutError, ConnectionError) as error:
            last = error
            if attempt + 1 < attempts:
                time.sleep(wait * (2 ** attempt))
    raise RuntimeError(f"gave up after {attempts} attempts: {last}")
