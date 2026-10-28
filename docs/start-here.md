# Start here: choose your learning route

You can begin without programming or ML experience. Start with the readiness check below. It chooses support, not admission or a grade. All routes work toward the same selected module outcomes. Canvas remains the authority for assessed work and deadlines.

## New to Python? Start with Python Foundation

Begin with [Introduction to Python: A Guided Beginner Course](https://ntious.github.io/python_foundation/). Use its getting-started notebook, then Modules 1–10 and the guided mini project as needed. The author estimates about 12 guided hours plus independent practice; budget this preparation explicitly rather than hiding it inside a short ML exercise. Students with existing skills can demonstrate readiness and skip familiar sections.

That course teaches notebook use, values, decisions, loops, lists, functions and debugging. Dictionaries/libraries are a preview and file reading is outside its core. Complete our [Python-to-ML bridge](setup/python-bridge.md) afterward for dictionaries, imports, paths, CSV/JSON and dataframes. Python Foundation's Binder is a separate environment: it does not install this course or its ML frameworks.

## Readiness check: attempt before opening the answers

1. Find a downloaded folder and identify its README. Explain what folder a relative path starts from.
2. In Python, predict `int("12") + 3` and explain why `"12" + "3"` differs.
3. Trace `total = 0` followed by a `for` loop that adds each value from `[2, 4, 6]` to `total`.
4. Write a function that returns twice an input; call it on 5. Explain return versus print.
5. Retrieve the minutes from `{"minutes": 15}` and explain how a list of these records differs from one dictionary.
6. Calculate the mean and median of `[2, 3, 10]`. Does a missing observation equal zero?
7. Of 20 actual positive cases, a system finds 15. Of 25 flagged cases, 15 are positive. State both fractions in words.
8. Explain why tomorrow's measured outcome cannot be an input to today's forecast.

## Answers and routing

1. Relative paths start from the current working folder. Review [acquisition and navigation](setup/student-workspace.md) if uncertain.
2. 15 versus the text 123. Review Foundation Modules 2–4.
3. 12. Review Foundation Modules 7–8.
4. `def double(x): return 2*x`; `double(5)` returns 10. Printing displays a value rather than returning it to the caller. Review Foundation Module 9.
5. `record["minutes"]`; a list contains multiple items, a dictionary maps keys to values. Use our bridge after the Foundation preview.
6. Mean 5; median 3. Missing means unavailable. Review Module 4's foundation bridge and glossary.
7. Recall is 15/20; precision is 15/25. These are ML entry concepts, not prerequisites for Python.
8. It is unavailable when the decision is made; using it leaks future information. Module 5 develops this idea.

| Route | Choose when | Next action |
| --- | --- | --- |
| Preparation plus core | Any of checks 1–5 needs help | Complete relevant Python Foundation sections and our bridge, then Modules 1–5 |
| Standard core | Checks 1–5 are explainable independently | Begin Module 1; use arithmetic/statistics support where needed |
| Core plus depth | You can also explain evaluation boundaries | Complete core mastery artifacts, then the module's predeclared extension |

The diagnostic is a routing aid rather than a validated test. Recheck uncertain items by solving a changed example without the answer visible. A student who needs support should receive planned time and help, not a lower learning target.

## The learning cycle

Read the module outcomes; use its foundation bridge; work through its guided construction; run the notebook; make one purposeful change; complete the mastery check; compare feedback. Save code, readable results and your explanation. Restart and run all before submitting execution evidence.

Use the [glossary](glossary.md), [troubleshooting](setup/troubleshooting.md), [environment choices](setup/hosted.md), and [project companion](project.md). If studying alone, keep a question log and write the strongest counterargument to your recommendation. If enrolled, use the instructor's published private support route; never post student records or credentials in GitHub issues.
