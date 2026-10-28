# Module 2 worked feedback

Compare this with your [practice](practice.md) evidence. A matching number without an explanation is incomplete.

## Changed ticket

Adding `T005,network,5` produces 5 tickets, 65 total minutes, and average 13 minutes: `65 / 5`. Network becomes 3 tickets totaling 30 minutes. The event counts do not change because the event file did not change. A new identifier matters: copying an existing ID is rejected, rather than counted twice.

CSV values enter as text. `int` converts minutes for arithmetic. A ticket is represented by a dictionary; the returned collection of tickets is a list. The category accumulator is a dictionary of dictionaries. Its count and total increase inside the loop; its first-category conditional creates an entry before adding to it.

## Empty tickets

A header-only CSV is a valid zero-record file. Ticket count and total minutes are zero. Average is `null` in JSON and “not available” in the text report. Reporting zero as the average would imply an observed average rather than absence of observations. The separate event file still has 3 records, with info 2, warning 1, and critical 0.

## Invalid minutes and debugging

`unknown` cannot become an integer. The CLI exits with an error identifying the CSV line and minutes requirement. No new report is written after this validation failure. A report already present in the output directory may be from an earlier successful run; use separate output directories and retain the command/error for each experiment. Correct the input copy and rerun before interpreting a result.

A direct call to `read_tickets` in Python can show a full traceback; the CLI deliberately prints a shorter message. Neither is a reason to remove validation. Replacing unknown minutes with zero would lower the total and usually lower the average, hiding uncertainty. Depending on the task, quarantine or imputation might be reasonable later, but they need an explicit policy and evidence.

## Shared implementation

Both entry routes call `run_workflow`, which invokes the same readers and summary functions. Matching inputs should produce matching reports. Merely giving two different implementations the same name would not ensure agreement. Notebook cells can also be run out of order, so restart-and-run-all remains an important check.

## Example reflection

“I checked an assistant's claim that an empty ticket file should have average zero. The function uses `None` when the count is zero. The output says the average is unavailable. I retained that behavior because a fabricated numerical average would miscommunicate the evidence.”

Continue to [Module 3: Data processing and trustworthy inputs](../03-data-processing/index.md), or return to [Module 2](index.md).

## Construction check and misconception feedback

Question: Why does replacing unknown with zero change the question?

It treats unobserved work as measured absence, changing both meaning and summary.

Judge your answer with the [study workflow criteria](../../study-workflow.md#how-explanations-are-judged). If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.

## Continue the learning route

For feedback on your own functions, use [construction solutions](solutions.md). The results here describe the separate complete reference.
