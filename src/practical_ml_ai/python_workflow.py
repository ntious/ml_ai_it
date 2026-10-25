"""Small CSV/JSON workflow using Python's standard library.

Beginners can trace the loops, dictionaries, functions, and file boundaries.
No learned model or data-cleaning algorithm is hidden behind this example.
"""
import argparse
import csv
import json
from pathlib import Path

TICKET_FIELDS = ("ticket_id", "category", "minutes")
EVENT_FIELDS = ("event_id", "source", "severity")
SEVERITIES = ("info", "warning", "critical")


def read_tickets(path: str | Path) -> list[dict]:
    tickets = []
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(TICKET_FIELDS).issubset(reader.fieldnames):
            raise ValueError("Ticket CSV needs ticket_id, category, and minutes columns.")
        seen = set()
        for line_number, row in enumerate(reader, start=2):
            if any(row.get(field) is None or not row[field].strip() for field in TICKET_FIELDS):
                raise ValueError(f"Ticket CSV line {line_number}: required values are missing.")
            ticket_id, category = row["ticket_id"].strip(), row["category"].strip()
            if ticket_id in seen:
                raise ValueError(f"Ticket CSV line {line_number}: duplicate ticket_id {ticket_id}.")
            try:
                minutes = int(row["minutes"])
            except ValueError as error:
                raise ValueError(f"Ticket CSV line {line_number}: minutes must be a nonnegative whole number.") from error
            if minutes < 0:
                raise ValueError(f"Ticket CSV line {line_number}: minutes must be nonnegative.")
            seen.add(ticket_id)
            tickets.append({"ticket_id": ticket_id, "category": category, "minutes": minutes})
    return tickets


def summarize_tickets(tickets: list[dict]) -> dict:
    by_category = {}
    total_minutes = 0
    for ticket in tickets:
        category = ticket["category"]
        if category not in by_category:
            by_category[category] = {"ticket_count": 0, "total_minutes": 0}
        by_category[category]["ticket_count"] += 1
        by_category[category]["total_minutes"] += ticket["minutes"]
        total_minutes += ticket["minutes"]
    count = len(tickets)
    return {
        "count": count,
        "total_minutes": total_minutes,
        "average_minutes": total_minutes / count if count else None,
        "by_category": dict(sorted(by_category.items())),
    }


def read_events(path: str | Path) -> list[dict]:
    events = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(events, list):
        raise ValueError("Event JSON must contain a list of objects.")
    seen = set()
    for position, event in enumerate(events, start=1):
        if not isinstance(event, dict) or any(
            not isinstance(event.get(field), str) or not event[field].strip() for field in EVENT_FIELDS
        ):
            raise ValueError(f"Event JSON item {position}: event_id, source, and severity must be nonempty text.")
        event = {field: event[field].strip() for field in EVENT_FIELDS}
        if event["event_id"] in seen:
            raise ValueError(f"Event JSON item {position}: duplicate event_id.")
        if event["severity"] not in SEVERITIES:
            raise ValueError(f"Event JSON item {position}: severity must be info, warning, or critical.")
        seen.add(event["event_id"])
        events[position - 1] = event
    return events


def summarize_events(events: list[dict]) -> dict:
    by_source = {}
    by_severity = {severity: 0 for severity in SEVERITIES}
    for event in events:
        source = event["source"]
        by_source[source] = by_source.get(source, 0) + 1
        by_severity[event["severity"]] += 1
    return {"count": len(events), "by_source": dict(sorted(by_source.items())), "by_severity": by_severity}


def describe_workflow(report: dict) -> str:
    tickets, events = report["tickets"], report["events"]
    average = tickets["average_minutes"]
    lines = [
        "Synthetic service-file summary",
        f"Tickets: {tickets['count']}",
        f"Total handling minutes: {tickets['total_minutes']}",
        f"Average handling minutes: {average if average is not None else 'not available (no tickets)'}",
    ]
    for category, values in tickets["by_category"].items():
        lines.append(f"Category {category}: {values['ticket_count']} tickets; {values['total_minutes']} minutes")
    lines.append(f"Events: {events['count']}")
    for severity, count in events["by_severity"].items():
        lines.append(f"Severity {severity}: {count}")
    lines.append("These are descriptive summaries of fictional records, not predictions.")
    return "\n".join(lines) + "\n"


def run_workflow(ticket_path: str | Path, event_path: str | Path, output_dir: str | Path) -> dict:
    ticket_path, event_path, output_dir = Path(ticket_path), Path(event_path), Path(output_dir)
    output_paths = [output_dir / name for name in ["report.json", "category_summary.csv", "summary.txt"]]
    if any(source.resolve() == target.resolve() for source in [ticket_path, event_path] for target in output_paths):
        raise ValueError("Keep input files separate from generated output files.")
    report = {"tickets": summarize_tickets(read_tickets(ticket_path)), "events": summarize_events(read_events(event_path))}
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths[0].write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with output_paths[1].open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["category", "ticket_count", "total_minutes"])
        writer.writeheader()
        for category, values in report["tickets"]["by_category"].items():
            writer.writerow({"category": category, **values})
    output_paths[2].write_text(describe_workflow(report), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize synthetic CSV tickets and JSON events with ordinary Python.")
    parser.add_argument("--tickets", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run_workflow(args.tickets, args.events, args.output)
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"File workflow failed: {error}\n")
    print(describe_workflow(report), end="")


if __name__ == "__main__":
    main()
