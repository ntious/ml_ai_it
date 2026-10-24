# Module 1 worked feedback

Use this after trying the [practice](practice.md). Compare your reasoning as well as the final value.

## Boundary behavior

At 85, review is requested. At exactly 80, review is not requested because `80 > 80` is false. At 81, `81 > 80` is true. If you expected review at 80, you may have interpreted the requirement as “at least 80”; that would require `>=`, a different rule. Test the requirement rather than silently changing the operator.

Example explanation: “This program follows a threshold chosen by a person. It never fits parameters from observations, so its successful output does not demonstrate ML training.” AI is the broader field; ML learns from data; deep learning uses multilayer neural networks; generative AI produces content. Output fluency alone does not establish factual correctness.

## Example problem brief

An IT operator needs to review storage before it becomes unavailable. The input is fictional percentage usage, and the output is a review message. An explicit threshold is an understandable starting point for this demonstration. A missing or invalid measurement could give misleading evidence, so the function rejects values outside 0–100 and nonfinite values. A real operational policy would require further context and testing; this teaching rule does not establish a safe production threshold.

A workload predictor could help when anticipating future demand matters and suitable historical data exist. Its evaluation must compare predictions with held-out outcomes. A generated response could help draft language, but cannot replace the measurement or supply trustworthy facts without checks.

## Saved work and interfaces

The command's `--output` argument names the text file to create. Reusing the path replaces that generated file. A notebook stores cells and optionally outputs; its kernel holds the live variables. Restarting the kernel and running all cells exposes reliance on an old variable. Passing a Python-cell check does not establish that a particular notebook interface is accessible.

## Example discussion response

A simple storage alert has an explicit, inspectable condition. An LLM adds expense and uncertainty without a clear benefit for this comparison. For drafting a support reply, language generation may help if approved facts are provided and a person checks the draft. I would compare errors, operational effort, and the stakeholder's actual need before replacing an existing method.

If an assistant called the threshold a “trained model,” reject that claim: there is no training step. Your verification is stronger when it cites the function and the two boundary runs.

Return to [Module 1](index.md), or continue to [Module 2](../02-python-workflows/index.md).
