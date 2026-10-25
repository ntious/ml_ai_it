# Module 4 worked feedback

Use this after attempting the [practice](practice.md). Different defensible memos are possible; compare their evidence and limitations.

## Numerical reconciliation

The raw file has 25 rows. Normalizing one label and retaining the first exact duplicate produces 24 service-day observations. Both services appear on all 12 dates. The gateway contributes 1,860 requests, the monitor 2,320, totaling 4,180. The monitor total exceeds the gateway by 460 requests, about 24.7% of the gateway total. Cropping the bar baseline changes perceived lengths; it cannot change that difference or ratio.

The missing-latency row is the gateway on January 4, with 130 requests. Dropping it entirely produces 23 normalized observations and 4,050 requests, with 1,730 gateway requests. There are still 23 observed latencies; their mean and median remain about 38.70 ms and 34 ms. Keeping the row for count-based questions avoids discarding known workload merely because another field is unavailable. The reduced daily table now reports only one observed service on January 4.

## Investigating the spike

The latency quartiles are 28 and 40 ms; IQR is 12 ms. The fences are `28 - 1.5 × 12 = 10` and `40 + 1.5 × 12 = 58` ms. The monitor's January 7 value of 160 ms is the only flagged observation. It remains in all relevant core summaries.

Excluding that observation in a clearly labeled sensitivity comparison leaves 22 observed latencies. Their mean is about 33.18 ms and median 33 ms. The original mean was about 38.70 ms and median 34 ms. Removing the observation reduces the mean much more, illustrating sensitivity to a large value. That change does not establish that deletion was appropriate; it removes the very observation the stakeholder may need to investigate.

The combined daily request total is highest on January 7 at 560: gateway 160 plus monitor 400. The same monitor row has p95 160 ms. These deliberately encoded values illustrate an association. They do not establish a causal traffic effect, a population trend, or a prediction about future reliability. Averaging daily percentiles also does not recover an overall p95.

## Example chart descriptions

Histogram short alternative: “Distribution of observed daily service p95 latency, with counts in the accompanying table.” Detailed account: “There are 23 observed values and one unavailable value. Sixteen lie in `[0,40)`, six in `[40,80)`, none in the next two intervals, and one in `[160,200]`. The mean is about 38.70 ms and the median 34 ms. The large upper value is retained for investigation.”

Comparison account: “Gateway total is 1,860 requests and monitor total 2,320 over the supplied observations. Both services cover 12 dates. Bars start at zero; the monitor total is 460 greater. These are counts in an invented fixture, not rates or production estimates.”

A time account should preserve the dates and totals, including the January 7 peak. A scatter account should state the 23 complete pairs, service grouping, overlapping marks, and absent causal evidence. Pair each explanation with its actual table rather than relying on a generic caption.

## Example operations memo

We explored the supplied fictional service-day records to compare request totals and identify observations worth investigating. After normalizing one service label and removing one exact duplicate, the data contain 24 observations across 12 dates. Gateway requests total 1,860 and monitor requests total 2,320. The combined total reaches 560 on January 7, including 400 monitor requests. That monitor observation also has daily p95 latency of 160 ms, above the exploratory IQR fence of 58 ms.

We retained the high latency because a statistical flag does not establish a recording error. We also retained the January 4 gateway row for request totals despite its unavailable latency, excluding it only from latency-specific analysis. The observed daily service p95 values have mean about 38.70 ms and median 34 ms; these are not an overall request-level p95.

These patterns were deliberately constructed in a small synthetic fixture. They cannot establish that traffic caused latency or predict operational reliability. For a real system, the next step would be to verify instrumentation and date/service coverage, then investigate deployment or workload changes around the flagged observation. The accompanying figures, tables, and descriptions expose the values supporting this interpretation.

## Feedback for an AI suggestion

If an assistant recommends dropping every outlier, ask what would be lost and what evidence establishes an error. If it says “the overall p95 is 38.70 ms,” correct the quantity: this is the mean of supplied daily service p95 values. If it calls 4,180 a request rate, ask for the denominator and units.

Return to [Module 4](index.md). Regression and reliable evaluation are the next planned module.

## Construction check and misconception feedback

Question: Does a rising scatter pattern establish causation?

No. Confounding, measurement changes and selection can produce association.

A satisfactory response includes the calculation or concrete counterexample, the fitting/decision boundary, your actual changed code and one limitation. Compare the [mastery criteria](guided.md) with your work. If you cannot reproduce the central operation, return to the worked step and try changed inputs before reading the answer again.
