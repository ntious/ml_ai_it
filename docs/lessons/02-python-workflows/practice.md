# Module 2 practice: change a file, explain a result

This independently authored practice complements the [workflow](index.md). Allow 35–60 minutes. Keep all experiments in `runs/module02-practice/` or another generated-work folder; preserve the checked-in samples.

## Core task P02

1. Run the original files and save the text/JSON outputs. Explain the difference between a list, dictionary, integer, and string using one actual input field.
2. Copy `tickets.csv` to your practice folder and append `T005,network,5` on a new line. Predict ticket count, total minutes, average, and network-category totals. Rerun using your copy and a new output directory. Explain the difference from the original.
3. Create a separate ticket CSV containing only the original header. Run with the unchanged event JSON. Explain why no ticket average is available while event counts remain valid.
4. Make another copy with `unknown` as one minutes value. Predict the outcome, run it, and save the error text. Identify the failing field and repair your copy. Explain why the original report should not be treated as the output of this failed run; the program validates inputs before writing a new report.
5. In `summarize_tickets`, identify the loop, first-category conditional, accumulator, and returned value. Explain why a function receiving explicit inputs is easier to reuse than code depending on a previous notebook cell's hidden variables.
6. Run the supplied notebook if that interface is usable for you. Compare its report with the script's report for the original input. If using the script route exclusively, explain the shared function and inspect its call sites; this is a conceptual comparison, not evidence that you operated a notebook interface.

Submit or save commands, small input copies, result/error text, and explanations under your instructor's rules. No screenshots or paid assistant are required.

## Discussion or solo reflection

A team member proposes replacing invalid minutes with zero to “keep the program running.” Explain how this could change the reported average and why a visible error may be preferable. In a group, compare two policies; alone, write one benefit and one risk for each. Module 3 develops traceable accepted/rejected reports as another policy.

## Work with GenAI

Optional prompt: “Review this small CSV summary function. Propose one edge case and predict the result. Do not rewrite it yet.” Verify the proposal on synthetic input and retain only changes you can explain. Record the suggested case, observed output, and your decision. Without an assistant, use the empty-file and invalid-value tasks above.

## Optional extension

Write a function that summarizes events from a new fictional source, without changing the severity vocabulary. Verify it with a two-record synthetic list, including one critical event. State its expected inputs and returned values. This skippable extension needs only the standard library.

## Self-check and adaptable criteria

| Criterion | Evidence of a satisfactory result |
| --- | --- |
| Structures and functions, M02.1–M02.2 | Correct field types and an explained loop/conditional/return |
| File processing, M02.3 | Correct labeled outputs for the original and changed input |
| Debugging, M02.4 | Preserved error, identified cause, repaired copy, and rerun |
| Reuse, M02.5 | Explained shared function; matched results if both interfaces were operated |
| Judgment | No fabricated average; explicit handling of invalid records |

These are adaptable criteria, not official university grading rules. Compare [worked feedback](feedback.md) after your attempt.

## Required independent construction

Write an explicit loop version independently. Add one record on a copy and reconcile both totals. Demonstrate one rejected value.

Use the [guided construction](guided.md) for a worked example, then reconstruct its central step without copying it. Retain changed code, expected/observed evidence and an explanation. This clarifies companion practice; Canvas remains the authority for assessed submissions.
