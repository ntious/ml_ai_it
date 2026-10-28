# Module 4: Use exploration to ask a better question

Read this between the foundation and guided construction. Keep the same question through prediction, calculation and the complete reference.

## Begin with the denominator

Three errors among ten requests is 30%; three errors among one hundred is 3%. A count can rise while its rate falls. Preserve the count, denominator and time window together. A day with no requests has an undefined error rate, not evidence of perfect reliability. This distinction changes both tables and alerting decisions.

## The shape matters

For durations [1, 2, 3, 100], the median is 2.5 while the mean is 26.5. Neither is a mistake: the long request strongly affects the mean. Inspect the distribution and the actual extreme record before removing it. A boxplot identifies unusual values relative to a rule; it does not establish corrupted data. Tables provide exact values; charts help reveal shape and sequence.

## Exploration creates hypotheses

A weekday pattern might reflect traffic volume, maintenance or data collection. It is not proof of a causal weekday effect. Keep exploratory choices on development data; predeclare the comparison you will evaluate later. For a chart, state the unit, population, period and missingness rule. Choose a line for ordered dates and a bar for distinct categories; avoid an axis that exaggerates a small change.

## Trace a small case

Predict `error_rate(3, 10)` and `error_rate(0, 0)` before running. A zero denominator means no requests were observed, so the rate is unavailable (`None`), not 0%. Then predict `median([1, 2, 3, 100])`: with an even count, average the two middle values (2.5). The outlier 100 does not move it. Use the practice notebook to test your prediction, then the [separate solutions](solutions.md) after your attempt.

## Connect this to the full experiment

The complete module runs `examples/service-workload/scripts/explore.py`. `summary.txt` reports 24 distinct observations, 23 observed latencies and one unavailable latency, and a median daily service p95 of 34.0 ms: the same median rule as your `median`, applied to real columns. The workload fixture records requests and p95 latency but no error counts, so `error_rate` and `weighted_rate` have no direct counterpart in this study. Use them for the transfer task, and use `service_comparison.csv` (1,860 versus 2,320 requests) to see why unequal volumes matter before comparing any rate. Success on an authored fixture does not establish performance on a real service.

## Optional reading

[NIST/SEMATECH e-Handbook of Statistical Methods: What is EDA?](https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm) describes exploratory analysis as looking at data before assuming a model, which is the stance of this module's figures and tables. Read the named section after the worked case; external mathematics is optional unless your instructor explicitly adopts it. For deeper experiment reasoning, use the [research comparison guide](../../advanced/research-comparison.md).
