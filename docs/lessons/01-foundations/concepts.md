# Module 1: From a task to an accountable decision

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## A prediction is not the whole decision

A help desk predicts whether a ticket needs escalation. The prediction is an estimate; the action also depends on staff capacity, error costs and the option to ask a person. Start by naming the unit (one ticket at arrival), target (eventual escalation) and decision time. A field written after escalation cannot be an input at arrival. A rule is a useful baseline because you can trace every branch; machine learning estimates a rule from examples, but still needs a human-defined target.

## Trace before you train

For an authored rule that escalates priority at least 3, priorities 2, 3 and 4 produce False, True and True. The boundary matters. Against labels False, False, True, the middle case is a false alert. Correct execution of the rule does not establish that its threshold is useful. Change the threshold and predict which cases change before running code.

## Separate development from the final question

Training fits parameters; validation supports choices; a final test estimates the locked procedure on held-out examples. Once you use the final answer to select a threshold, that answer has become development evidence. A new random seed does not erase that reuse. Save the original question, the decision and the evidence needed to contradict it.

## Trace a small case

The first operation is **route**: Return a bool: priority >= threshold. On authored arguments `route(2)`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/first-run/scripts/first_run.py`. Compare the practice priority rule (`>= 3`) with the complete script’s storage rule (`> 80`). They use different inputs and intentionally different boundaries; do not search for the priority rule inside the storage script. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Further reading: foundations](https://developers.google.com/machine-learning/crash-course/framing/ml-terminology) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).

## Three names to recognize

Training examples teach the model; validation examples help choose between candidate settings; test examples check the chosen procedure afterward. Module 5 develops this distinction in a full experiment. For the first human-written rule, no model training or data split is performed. See the [glossary](../../glossary.md) when these terms recur.
