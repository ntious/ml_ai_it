# Module 4: Use exploration to ask a better question

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Begin with the denominator

Three errors among ten requests is 30%; three errors among one hundred is 3%. A count can rise while its rate falls. Preserve the count, denominator and time window together. A day with no requests has an undefined error rate, not evidence of perfect reliability. This distinction changes both tables and alerting decisions.

## The shape matters

For durations [1, 2, 3, 100], the median is 2.5 while the mean is 26.5. Neither is a mistake: the long request strongly affects the mean. Inspect the distribution and the actual extreme record before removing it. A boxplot identifies unusual values relative to a rule; it does not establish corrupted data. Tables provide exact values; charts help reveal shape and sequence.

## Exploration creates hypotheses

A weekday pattern might reflect traffic volume, maintenance or data collection. It is not proof of a causal weekday effect. Keep exploratory choices on development data; predeclare the comparison you will evaluate later. For a chart, state the unit, population, period and missingness rule. Choose a line for ordered dates and a bar for distinct categories; avoid an axis that exaggerates a small change.

## Trace a small case

The first operation is **error_rate**: Return errors/requests; None when requests is zero. On authored arguments `[3, 10]`, first predict the answer on paper. Change one boundary value, explain what should change, then use the practice notebook to test your reasoning. The [separate solutions](solutions.md) explain common errors after your attempt.

## Connect this to the full experiment

The complete module still uses `examples/service-workload/scripts/explore.py`. Identify the step that performs your small operation and trace its output into one actual table or decision. Explain the difference in scale and assumptions. The [practice](practice.md) includes an IT transfer case; success on an authored fixture does not establish performance on that service.

## Optional reading

[Primary explanation](https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm) offers additional detail on this module’s mechanism. Read the named topic after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
