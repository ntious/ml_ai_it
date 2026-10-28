"""Descriptive exploration with paired tables, figures, and text explanations.

No model is trained. The read/summary path needs NumPy/pandas; plotting is an
optional dependency installed with the visualization extra. Input data stay raw.
"""
import argparse
from html import escape
import json
from pathlib import Path

import numpy as np
import pandas as pd

FIELDS = ["date", "service", "requests", "p95_latency_ms"]
SERVICES = ["authentication_gateway", "network_monitor"]
CHARTS = ["latency_distribution", "service_comparison", "daily_requests", "request_latency", "axis_comparison"]
OUTPUTS = ["observations.csv", "summary.json", "summary.txt", "chart_descriptions.md", "index.html", *[name + ".csv" for name in CHARTS], *[name + ".png" for name in CHARTS]]


def read_workload(path: str | Path) -> tuple[pd.DataFrame, dict]:
    """Normalize known labels, retain missing latency, reject ambiguous records."""
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if not set(FIELDS).issubset(frame.columns):
        raise ValueError("Workload CSV needs date, service, requests, and p95_latency_ms columns.")
    frame = frame[FIELDS].copy()
    if frame.empty:
        raise ValueError("Workload CSV needs at least one observation.")
    raw_count = len(frame)
    original_labels = frame["service"].copy()
    frame["service"] = frame["service"].str.strip().str.lower()
    normalized_labels = int((original_labels != frame["service"]).sum())
    if not frame["service"].isin(SERVICES).all():
        raise ValueError("Service must normalize to authentication_gateway or network_monitor.")
    if not frame["date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
        raise ValueError("Dates must use YYYY-MM-DD.")
    try:
        frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="raise")
    except (ValueError, OverflowError) as error:
        raise ValueError("Dates must be valid YYYY-MM-DD calendar dates.") from error
    request_text = frame["requests"].str.strip()
    if not request_text.str.fullmatch(r"[0-9]+").all():
        raise ValueError("Requests must be nonnegative whole-number text.")
    requests = request_text.map(int)
    if any(value > np.iinfo(np.int64).max for value in requests):
        raise ValueError("Requests exceed the signed int64 range.")
    frame["requests"] = requests.astype("int64")
    latency_text = frame["p95_latency_ms"].str.strip()
    try:
        latency = pd.to_numeric(latency_text.mask(latency_text == "", np.nan), errors="raise").astype(float)
    except (ValueError, TypeError) as error:
        raise ValueError("Latency must be numeric or blank when unavailable.") from error
    observed = latency_text != ""
    if not (np.isfinite(latency[observed]) & (latency[observed] >= 0)).all():
        raise ValueError("Observed latency must be finite and nonnegative.")
    frame["p95_latency_ms"] = latency
    frame = frame.drop_duplicates()
    duplicates = raw_count - len(frame)
    if frame.duplicated(["date", "service"], keep=False).any():
        raise ValueError("Conflicting observations share a date/service key; investigate the input.")
    if sum(int(value) for value in frame["requests"]) > np.iinfo(np.int64).max:
        raise ValueError("Combined requests exceed the signed int64 range for exact grouped totals.")
    frame = frame.sort_values(["date", "service"]).reset_index(drop=True)
    return frame, {"input_rows": raw_count, "observations": len(frame), "exact_duplicates_removed": duplicates, "labels_normalized": normalized_labels}


def summarize_workload(frame: pd.DataFrame, quality: dict) -> tuple[dict, dict[str, pd.DataFrame]]:
    """Produce descriptive numbers and exactly the tables used by each chart."""
    latency = frame["p95_latency_ms"].dropna()
    q1 = float(latency.quantile(0.25)) if len(latency) else None
    q3 = float(latency.quantile(0.75)) if len(latency) else None
    lower = q1 - 1.5 * (q3 - q1) if q1 is not None else None
    upper = q3 + 1.5 * (q3 - q1) if q3 is not None else None
    flagged = frame.loc[(frame["p95_latency_ms"] < lower) | (frame["p95_latency_ms"] > upper)].copy() if len(latency) else frame.iloc[:0].copy()
    comparison = frame.groupby("service", as_index=False)["requests"].sum()
    daily = frame.groupby("date", as_index=False).agg(requests=("requests", "sum"), services_observed=("service", "nunique"))
    # np.histogram's final bin includes its right edge; others are left-closed.
    edges = np.linspace(0, max(200.0, float(latency.max()) if len(latency) else 200.0), 6)
    counts, edges = np.histogram(latency.to_numpy(), bins=edges)
    distribution = pd.DataFrame({"lower_ms": edges[:-1], "upper_ms": edges[1:], "count": counts})
    scatter = frame.dropna(subset=["p95_latency_ms"])[FIELDS].copy()
    summary = {
        **quality, "dates_observed": int(frame["date"].nunique()),
        "date_service_coverage": "Only supplied dates/services; absent rows are not assumed to be zero.",
        "total_requests": int(sum(int(value) for value in frame["requests"])),
        "missing_latency": int(frame["p95_latency_ms"].isna().sum()), "observed_latency": len(latency),
        "mean_daily_service_p95_ms": float(latency.mean()) if len(latency) else None,
        "median_daily_service_p95_ms": float(latency.median()) if len(latency) else None,
        "q1_ms": q1, "q3_ms": q3, "iqr_lower_fence_ms": lower, "iqr_upper_fence_ms": upper,
        "flagged_observations": [{"date": row.date.strftime("%Y-%m-%d"), "service": row.service, "p95_latency_ms": float(row.p95_latency_ms)} for row in flagged.itertuples()],
        "policies": ["Keep the first exact duplicate after normalization; reject conflicting date/service keys.", "Retain missing-latency rows for request totals; omit them only from latency-specific views.", "Keep flagged values; IQR fences are investigation prompts, not proof of errors.", "These daily service p95 summaries are not an overall request-level p95."],
    }
    return summary, {"latency_distribution": distribution, "service_comparison": comparison, "daily_requests": daily, "request_latency": scatter, "axis_comparison": comparison.copy()}


def describe_charts(summary: dict, tables: dict[str, pd.DataFrame]) -> dict[str, tuple[str, str]]:
    """Return short alternatives and detailed numerical interpretation per figure."""
    mean = summary["mean_daily_service_p95_ms"]
    median = summary["median_daily_service_p95_ms"]
    distribution = (f"Observed daily service p95 values: {summary['observed_latency']}; unavailable values: {summary['missing_latency']}. "
                    f"Mean: {mean:.2f} ms; median: {median:.2f} ms. " if mean is not None else "No observed latency values; all latency bins are empty. ")
    distribution += "The companion bin table gives every count. Bins include their lower edge; only the final bin includes its upper edge. Daily service percentiles cannot be pooled into an overall request-level p95."
    totals = "; ".join(f"{row.service}: {int(row.requests)} requests" for row in tables["service_comparison"].itertuples())
    daily = tables["daily_requests"]
    peak = daily.loc[daily["requests"].idxmax()]
    coverage = int((daily["services_observed"] < len(SERVICES)).sum())
    trend = (f"Across {len(daily)} supplied dates, total requests are {summary['total_requests']}. "
             f"The first date has {int(daily.iloc[0].requests)} requests and the last has {int(daily.iloc[-1].requests)}. "
             f"The largest daily total is {int(peak.requests)} on {peak.date:%Y-%m-%d}. "
             f"Dates with fewer than two service observations: {coverage}. Gaps between dates break the plotted line; absent dates are not zero. "
             "Use the daily table to inspect changes rather than infer a stable trend from a tiny fictional sample.")
    scatter = (f"The relationship plot uses {len(tables['request_latency'])} complete request/latency pairs; {summary['missing_latency']} unavailable latency values are omitted only here and in the distribution. "
               f"IQR investigation flags: {len(summary['flagged_observations'])}; values remain included. "
               "Marker shapes and colors both identify services. Some marks may overlap; the paired table preserves every observation and gives exact values. The constructed association does not establish that request volume causes latency.")
    minimum = float(tables["service_comparison"]["requests"].min())
    maximum = float(tables["service_comparison"]["requests"].max())
    floor = minimum * .95
    axis_detail = (f"The cropped baseline is {floor:g} requests. Visible heights for the smallest/largest totals become {minimum-floor:g} and {maximum-floor:g}, "
                   f"a ratio of {(maximum-floor)/(minimum-floor):.2f}, while the actual total ratio is {maximum/minimum:.2f}. "
                   if floor > 0 else "The smallest total is zero, so no positive baseline crop is applied in this dataset. ")
    return {
        "latency_distribution": ("Histogram of observed per-service daily p95 latency in milliseconds; counts and interpretation follow.", distribution),
        "service_comparison": ("Bar comparison of total requests by service, starting at zero; exact totals follow.", totals + ". These are totals over supplied observations, not request rates or production estimates."),
        "daily_requests": ("Line plot of daily combined requests, with missing dates left as gaps; exact date totals follow.", trend),
        "request_latency": ("Scatter plot of requests and daily p95 latency by service; complete pairs and interpretation follow.", scatter),
        "axis_comparison": ("Two bar plots of the same service totals: a zero baseline and an explicitly truncated-axis teaching example.", totals + ". The left panel starts at zero. " + axis_detail + "Cropping a bar baseline exaggerates apparent height differences and is deliberately misleading for comparing lengths. The underlying values and their ratios do not change. Use the zero-baseline panel for the comparison."),
    }


def render_charts(frame: pd.DataFrame, tables: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Write headless Matplotlib/Seaborn PNGs; evidence tables are written separately."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as error:
        raise ValueError('Install the visualization extra: python -m pip install -e ".[visualization]" -c environments/constraints-tested.txt') from error
    colors = ["#245080", "#895124"]
    with plt.rc_context({"font.size": 12, "axes.titlesize": 13, "axes.labelsize": 12, "xtick.labelsize": 10, "ytick.labelsize": 10, "figure.facecolor": "white", "axes.facecolor": "white"}):
        def save(fig, name):
            fig.savefig(output_dir / (name + ".png"), dpi=150, facecolor="white")
            plt.close(fig)
        fig, ax = plt.subplots(figsize=(7.6, 4.8), layout="constrained")
        dist = tables["latency_distribution"]
        edges = np.r_[dist["lower_ms"].to_numpy(), dist["upper_ms"].iloc[-1]]
        ax.hist(frame["p95_latency_ms"].dropna(), bins=edges, color=colors[0], edgecolor="black")
        ax.set(title="Distribution of observed daily service p95", xlabel="Per-service daily p95 latency (ms)", ylabel="Service-day observations")
        ax.set_ylim(bottom=0); ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
        save(fig, "latency_distribution")
        fig, ax = plt.subplots(figsize=(7.6, 4.8), layout="constrained")
        comparison = tables["service_comparison"].set_index("service")["requests"]
        comparison.plot.bar(ax=ax, color=colors, edgecolor="black", rot=0)
        ax.set(title="Total requests in the supplied observations", xlabel="Service", ylabel="Requests (count)", ylim=(0, None))
        ax.set_xticklabels([name.replace("_", "\n", 1) for name in comparison.index])
        for bar in ax.patches:
            ax.annotate(f"{int(bar.get_height())}", (bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 5), textcoords="offset points", ha="center")
        ax.margins(y=.15); save(fig, "service_comparison")
        fig, ax = plt.subplots(figsize=(7.6, 4.8), layout="constrained")
        daily = tables["daily_requests"].set_index("date")["requests"]
        calendar = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
        series = daily.reindex(calendar)  # NaN breaks the line across missing dates.
        ax.plot(series.index, series.values, marker="o", color=colors[0])
        ax.set(title="Daily requests across supplied services", xlabel="UTC calendar date", ylabel="Requests (count)", ylim=(0, None))
        ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=4, maxticks=6))
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %d"))
        save(fig, "daily_requests")
        fig, ax = plt.subplots(figsize=(7.6, 4.8), layout="constrained")
        scatter = tables["request_latency"]
        if not scatter.empty:
            sns.scatterplot(data=scatter, x="requests", y="p95_latency_ms", hue="service", style="service", hue_order=SERVICES, style_order=SERVICES, markers=["o", "X"], palette=colors, s=75, edgecolor="black", ax=ax)
            ax.legend(title="Service", loc="upper left", fontsize=9)
        else:
            ax.text(.5, .5, "No observed latency values", transform=ax.transAxes, ha="center")
        ax.set(title="Requests and observed daily service p95", xlabel="Requests per service-day (count)", ylabel="Per-service daily p95 latency (ms)", xlim=(0, None), ylim=(0, None))
        save(fig, "request_latency")
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.8), layout="constrained")
        floor = float(comparison.min()) * .95
        for ax, truncated in zip(axes, [False, True]):
            ax.bar(range(len(comparison)), comparison.to_numpy(), color=colors, edgecolor="black")
            ax.set_xticks(range(len(comparison)), [name.replace("_", "\n", 1) for name in comparison.index])
            ax.tick_params(axis="x", labelsize=8)
            ax.set_ylim(bottom=floor if truncated else 0)
            ax.set_title("Misleading: cropped baseline" if truncated and floor > 0 else "Comparison: zero baseline", fontsize=11)
            ax.set_ylabel("Requests (count)")
        save(fig, "axis_comparison")


def _one_decimal(value):
    # Text summaries round for reading; summary.json keeps full precision.
    return "unavailable" if value is None else f"{value:.1f}"


def describe_summary(summary: dict) -> str:
    lines = ["Synthetic workload exploration", f"Input rows: {summary['input_rows']}", f"Distinct observations: {summary['observations']}", f"Exact duplicates removed: {summary['exact_duplicates_removed']}", f"Labels normalized: {summary['labels_normalized']}", f"Total requests: {summary['total_requests']}", f"Observed latency values: {summary['observed_latency']}", f"Unavailable latency values: {summary['missing_latency']}", f"Mean daily service p95 (ms): {_one_decimal(summary['mean_daily_service_p95_ms'])}", f"Median daily service p95 (ms): {_one_decimal(summary['median_daily_service_p95_ms'])}", f"IQR investigation flags retained: {len(summary['flagged_observations'])}", "Descriptive synthetic evidence; no causal, production, or model-performance claim."]
    return "\n".join(lines) + "\n"


def _table_html(table: pd.DataFrame, caption: str) -> str:
    columns = list(table.columns)
    header = "".join(f'<th scope="col">{escape(name)}</th>' for name in columns)
    rows = []
    for row in table.itertuples(index=False, name=None):
        cells = "".join(f"<td>{escape(value.strftime('%Y-%m-%d') if isinstance(value, pd.Timestamp) else str(value))}</td>" for value in row)
        rows.append("<tr>" + cells + "</tr>")
    return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{escape(caption)}"><table><caption>{escape(caption)}</caption><thead><tr>{header}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def run_exploration(input_path: str | Path, output_dir: str | Path) -> dict:
    """Generate all five figures with paired CSV tables and an HTML/text report."""
    input_path, output_dir = Path(input_path), Path(output_dir)
    if any(input_path.resolve() == (output_dir / name).resolve() for name in OUTPUTS):
        raise ValueError("Keep input separate from generated output files.")
    frame, quality = read_workload(input_path)
    summary, tables = summarize_workload(frame, quality)
    descriptions = describe_charts(summary, tables)
    output_dir.mkdir(parents=True, exist_ok=True)
    render_charts(frame, tables, output_dir)
    frame.to_csv(output_dir / "observations.csv", index=False, date_format="%Y-%m-%d")
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (output_dir / "summary.txt").write_text(describe_summary(summary), encoding="utf-8")
    sections, text = [], ["# Workload chart descriptions", describe_summary(summary)]
    for name in CHARTS:
        tables[name].to_csv(output_dir / (name + ".csv"), index=False, date_format="%Y-%m-%d")
        short, detail = descriptions[name]
        text.extend(["## " + name.replace("_", " "), short, detail, "Underlying values: " + name + ".csv"])
        sections.append(f'<section aria-labelledby="{name}"><h2 id="{name}">{escape(name.replace("_", " ").title())}</h2><figure><img src="{name}.png" alt="{escape(short)}" aria-describedby="{name}-detail"><figcaption id="{name}-detail">{escape(detail)}</figcaption></figure><p><a href="{name}.csv">Download {escape(name.replace("_", " "))} table (CSV)</a></p>' + _table_html(tables[name], "Underlying values: " + name.replace("_", " ")) + '</section>')
    (output_dir / "chart_descriptions.md").write_text("\n\n".join(text) + "\n", encoding="utf-8")
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Module 4: synthetic workload evidence</title><style>'
            'body{font:1.1rem/1.65 system-ui,sans-serif;color:#18232d;background:white;max-width:76ch;margin:auto;padding:1rem}img{max-width:100%;height:auto}table{border-collapse:collapse}.table-wrap{max-width:100%;overflow-x:auto}th,td{border:1px solid #718096;padding:.4rem;text-align:left}a{color:#075985}a:focus-visible,pre:focus-visible,.table-wrap:focus-visible{outline:3px solid currentColor;outline-offset:3px}pre{white-space:pre-wrap}.skip{position:absolute;top:-6rem}.skip:focus{top:0;background:white;padding:1rem}'
            '</style></head><body><a class="skip" href="#main">Skip to main content</a><main id="main" tabindex="-1"><h1>Module 4: synthetic workload evidence</h1><p>Every figure has a description and its actual data table. This fixture contains deliberately constructed patterns; no trained model or real operational finding is represented.</p>'
            '<p><a href="summary.json">Structured summary (JSON)</a> · <a href="summary.txt">Plain-text summary</a> · <a href="observations.csv">Normalized observations (CSV)</a> · <a href="chart_descriptions.md">All chart descriptions (Markdown)</a></p>'
            '<pre tabindex="0" aria-label="Named summary values">' + escape(describe_summary(summary)) + '</pre>' + ''.join(sections) + '</main><footer><p>Original synthetic data and educational content: CC BY 4.0. Generated by shared MIT-licensed code. Results are available as text, tables and downloads; consult the course accessibility guide for interface test scope.</p></footer></body></html>')
    (output_dir / "index.html").write_text(html + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore synthetic workload with figures, tables, and text evidence.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        summary = run_exploration(args.input, args.output)
    except (ValueError, OSError, pd.errors.ParserError) as error:
        parser.exit(2, f"Exploration failed: {error}\n")
    print(describe_summary(summary), end="")
    print("Open the generated index.html or read summary.txt and the companion CSV tables.")


if __name__ == "__main__":
    main()
