# Module 4 foundation bridge: choosing and reading charts

Use this bridge before the [lesson](index.md) if dataframe summaries or chart choices are unfamiliar.

## Rows, groups, and units

One row is one service-day. Adding `requests` across rows gives request counts for those supplied observations. Grouping by `service` gives a total per service; grouping by `date` gives a total per date. A count is not a rate: a rate needs a denominator such as observation time.

The shared functions can be explored in Python or the guided notebook:

```python
frame, quality = read_workload(input_path)
summary, tables = summarize_workload(frame, quality)
print(tables["service_comparison"].to_string(index=False))
print(tables["daily_requests"].to_string(index=False))
```

The complete notebook supplies imports and paths. `dropna(subset=["p95_latency_ms"])` selects rows with observed latency for a latency question. It should not silently become the input for every unrelated summary.

## Distribution and variability

A histogram groups numeric observations into intervals and counts each interval. Boundary definitions matter: in this example 40 belongs to `[40,80)`, and 160 belongs to the final `[160,200]` interval. Changing bin width changes appearance without changing the observations.

The mean uses the sum divided by the observed count and can move strongly with a large value. The median is the middle sorted value (or average of the two middle values for an even count). Quartiles help describe spread; IQR is Q3 minus Q1. In small samples, quantile interpolation conventions can matter. A skewed distribution has an uneven tail; describing a tail is more defensible here than assuming a population distribution.

## Comparison, time, and relationship

Use a bar chart for comparing category magnitudes, a line for ordered time observations, and a scatter plot for paired numeric observations. Include titles, axis names, units, and a legend or direct labels when groups differ. Markers and text support meaning when colors cannot be distinguished.

A scatter point is not a causal experiment. If request count and latency rise together, alternative explanations include a deployment change, measurement change, service mix, or a deliberately constructed fixture. Missing rows and overlapping marks can also change what a reader sees.

## Read a figure through its table

Identify the plotted unit, count, scale, grouping, and missing-value policy. Locate the relevant values in the companion table. Then describe the same relationship in words, including uncertainty. A short alt label identifies a figure; the longer description and table carry the analytical evidence. Practice uses these routes to support the same interpretation goal.

Return to [Module 4](index.md).

## Continue the learning route

Continue with [concepts and a small trace](concepts.md) before the full workflow.
