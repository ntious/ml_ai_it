# Module 2: Make a small workflow inspectable

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Data in, evidence out

A reusable function takes explicit inputs and returns a value. Reading a file, computing a result and writing it are distinct responsibilities. If a function secretly reads a previous notebook variable, restarting the kernel may change its behavior. Pass records as an argument, inspect the return value and record the source path in the outer workflow.

## Count missingness rather than hiding it

Consider durations [10, None, 20]. The total observed duration is 30, the observed count is 2 and the missing count is 1. Dividing by all three rows invents a zero-duration observation. Report both counts. A record can be valid yet incomplete; invalid syntax, absent data and a genuine zero are different states.

## Debug the boundary

A relative path starts at the process working directory, not automatically at the notebook location. Locate the repository once, keep outputs under a named run folder and use pathlib instead of string concatenation. When debugging, inspect the smallest failing input and the exception message. Restart and run all cells to test whether hidden state was involved.

## Trace a small case

The first operation is **status_counts**: Return a dictionary counting the status string in each record. On authored arguments `[[{'status': 'open'}, {'status': 'closed'}, {'status': 'open'}]]`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/service-files/scripts/summarize.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Primary explanation](https://docs.python.org/3/tutorial/errors.html) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
