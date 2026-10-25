# Module 8 practice and reflection

This independently authored companion activity is usable with or without an instructor. It is not an original Canvas task or an official grading policy. Allow roughly 45–75 minutes after the walkthrough.

## Core task P08

Explain each layer and tensor shape. Use the learning-history table to identify the best validation epoch and any divergence. Compare confusion counts with the logistic baseline, then verify that reloaded predictions agree on actual held-out rows.

Save the source/citation, environment versions, split/protocol manifest, commands, output tables, and your interpretation. Verify at least one numerical claim by hand from the actual evidence. Explain one failure/limitation and one next investigation. Screenshots are not required. If you use only the worked report, identify your evidence as interpretation rather than claiming that you executed training.

## Discussion or solo equivalent

A colleague argues that successful execution makes the method ready for use. Respond with a concrete missing piece of evidence from this module. In class, compare reasoning with a peer; independently, write and answer the strongest counterargument. Distinguish a design judgment from a fact measured in the data.

## Work with GenAI

Optional prompt: “Critique my reasoning against these tables and the declared protocol. Identify an unsupported generalization, availability error, metric confusion, or missing limitation.” Verify suggestions against code and actual values; record what you accepted/rejected. Without an assistant, apply that same checklist using the public feedback. Follow your instructor's disclosure policy and do not upload secrets/personal records.

## Optional extension

Declare another width, epoch budget, or class-weight policy as a development experiment. Explain parameter count and resource effects; do not require a GPU or treat the extension as necessary for core completion.

## Self-check and adaptable criteria

| Outcome | Evidence to check |
| --- | --- |
| M08.1 | Explain input, hidden activation, output probability, loss, and gradient updates. |
| M08.2 | Fit training-only numeric preprocessing and a TensorFlow network. |
| M08.3 | Select a checkpoint using validation loss without fitting to final labels. |
| M08.4 | Compare held-out errors with a logistic baseline. |
| M08.5 | Save/reload a trained model and document compute and limitations. |

Use correct denominators/units, preserve evaluation boundaries, explain changes, and state limitations. Adopting instructors set weights and submission rules. Public [feedback](feedback.md) supports independent study.

## Required independent construction

In a separate development cell construct the 11-input/16-hidden/1-output TensorFlow model. Print and explain every shape and parameter count; make one declared width change before final evaluation.

Use the [guided construction](guided.md) for a worked example, then reconstruct its central step without copying it. Retain changed code, expected/observed evidence and an explanation. This clarifies companion practice; Canvas remains the authority for assessed submissions.
