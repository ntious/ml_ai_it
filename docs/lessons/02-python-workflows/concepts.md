# Module 2: Make a small workflow inspectable

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Data in, evidence out

A reusable function takes explicit inputs and returns a value. Reading a file, computing a result and writing it are distinct responsibilities. If a function secretly reads a previous notebook variable, restarting the kernel may change its behavior. Pass records as an argument, inspect the return value and record the source path in the outer workflow.

## Count missingness rather than hiding it

Consider durations [10, None, 20]. The total observed duration is 30, the observed count is 2 and the missing count is 1. Dividing by all three rows invents a zero-duration observation. Report both counts. A record can be valid yet incomplete; invalid syntax, absent data and a genuine zero are different states.

## Debug the boundary

A relative path starts at the process working directory, not automatically at the notebook location. Locate the repository once, keep outputs under a named run folder and use pathlib instead of string concatenation. When debugging, inspect the smallest failing input and the exception message. Restart and run all cells to test whether hidden state was involved.

## Trace a small case

Predict `status_counts([{'status': 'open'}, {'status': 'closed'}, {'status': 'open'}])` and `status_counts([])` before running. The empty file must return an empty dictionary, not raise an error. Then predict `observed_mean([0, None])`: zero is an observed value, so the mean is 0. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/service-files/scripts/summarize.py`. Its `category_summary.csv` counts tickets per category the way `status_counts` counts statuses, and `summary.txt` reports the average handling minutes (15.0 for the fixture). It writes into the `--output` folder you choose, which is the job `output_path` does in miniature. Compare one count in `category_summary.csv` with a count you make by hand from `tickets.csv`. Success on an authored fixture does not establish performance on a real service.

## Optional reading

[Python tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) explains tracebacks, `try`/`except` and raising errors: the tools for diagnosing the path and type errors in outcome M02.4. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
