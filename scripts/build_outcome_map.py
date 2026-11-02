"""Generate the course-outcome map page and per-module evidence blocks.

curriculum/outcomes.json is the single source. Run without arguments to write
docs/outcome-map.md and the marked block in each lesson entry page; run with
--check to fail when generated text is stale or the data is inconsistent.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
START, END = "<!-- OUTCOME_EVIDENCE_START -->", "<!-- OUTCOME_EVIDENCE_END -->"
HEADING = "## Course outcomes and evidence\n\n"
ANCHORS = ("## Learning route", "## Learning sequence for this module")


def load():
    data = json.loads((ROOT / "curriculum/outcomes.json").read_text(encoding="utf-8"))
    modules = json.loads((ROOT / "curriculum/modules.json").read_text(encoding="utf-8"))["modules"]
    return data, modules


def validate(data, modules):
    problems = []
    if data.get("schema_version") != 1:
        problems.append("unsupported schema_version")
    for collection in ("outcomes", "extensions", "modules", "additional_activities"):
        ids = [item["id"] for item in data[collection]]
        if len(ids) != len(set(ids)):
            problems.append(f"duplicate IDs in {collection}")
    outcomes = {item["id"] for item in data["outcomes"]}
    extensions = {item["id"] for item in data["extensions"]}
    activities = {item["id"]: item for item in data["additional_activities"]}
    for activity in activities.values():
        if not (ROOT / "docs" / activity["path"]).is_file():
            problems.append(f"{activity['id']}: activity page missing")
        if not activity["outcomes"] or any(x not in outcomes for x in activity["outcomes"]):
            problems.append(f"{activity['id']}: unknown or missing outcomes")
    labels = set(data["data_labels"])
    by_id = {item["id"]: item for item in data["modules"]}
    if sorted(by_id) != sorted(module["id"] for module in modules):
        problems.append("outcomes.json modules do not match curriculum/modules.json")
    for item in data["modules"]:
        name = f"module {item['id']}"
        for activity in item["additional_direct"]:
            if activity not in activities:
                problems.append(f"{name}: unknown additional activity {activity}")
        for key in ("direct", "support"):
            problems += [f"{name}: unknown outcome {x}" for x in item[key] if x not in outcomes]
        if set(item["direct"]) & set(item["support"]):
            problems.append(f"{name}: an outcome is both direct and support")
        if not (item["direct"] or item["support"]):
            problems.append(f"{name}: no outcome mapped")
        if item.get("extension") and item["extension"] not in extensions:
            problems.append(f"{name}: unknown extension")
        problems += [f"{name}: unknown label {x}" for x in item["labels"] if x not in labels]
        for key in ("evidence", "boundary", "responsible"):
            if not item.get(key):
                problems.append(f"{name}: missing {key}")
    for outcome in data["outcomes"]:
        if not outcome.get("coverage_note"):
            problems.append(f"{outcome['id']}: missing coverage_note")
        if not (ROOT / "docs" / outcome["bridge"]).exists():
            problems.append(f"{outcome['id']}: bridge page missing: {outcome['bridge']}")
    return problems


def summary(data):
    return {item["id"]: item["summary"] for item in data["outcomes"]}


def badges(labels):
    return " ".join(f'<span class="data-label">{label}</span>' for label in labels)


def module_block(data, item, module):
    names = summary(data)
    label = lambda ids: ", ".join(f"{x} ({names[x]})" for x in ids) or "none"
    lines = [START, "",
             f"- **Direct evidence:** {label(item['direct'])}",
             f"- **Supporting practice:** {label(item['support'])}"]
    if item["additional_direct"]:
        activities = {a["id"]: a for a in data["additional_activities"]}
        links = [f"[{aid} ({', '.join(activities[aid]['outcomes'])})](../../{activities[aid]['path']})" for aid in item["additional_direct"]]
        lines.append("- **Additional direct-evidence route (complete separately):** " + "; ".join(links))
    if item.get("extension"):
        extension = next(x for x in data["extensions"] if x["id"] == item["extension"])
        lines.append(f"- **Curriculum extension:** {extension['summary']}")
    lines += [    f"- **Data and tools:** {badges(item['labels'])}",
              f"- **Evidence you produce:** {item['evidence']} See [practice and evidence tasks](practice.md) and the [assessment criteria](../../study-workflow.md#how-explanations-are-judged).",
              f"- **Boundary:** {item['boundary']}",
              f"- **Responsible-AI check:** {item['responsible']}", "",
              "See the [outcome map](../../outcome-map.md) for all modules and the label definitions. "
              "These are proposed evidence links to working course-outcome summaries; they do not establish complete outcome coverage.", END]
    return "\n".join(lines)


PRACTICE_START, PRACTICE_END = "<!-- RESPONSIBLE_AI_START -->", "<!-- RESPONSIBLE_AI_END -->"


def practice_block(item):
    return "\n".join([
        "## Responsible-AI check", "", PRACTICE_START, "",
        f"{item['responsible']}", "",
        "Answer in two or three sentences about your own work. Cite one specific result or record, state what you do not know, and name who would review or act on it. "
        "This is a reasoning prompt, not an extra graded task.", "", PRACTICE_END])


def replace_marked(text, block, start, end):
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError(f"Expected one ordered marker pair: {start} / {end}")
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    return head + block + tail


def with_practice(text, block):
    if PRACTICE_START in text or PRACTICE_END in text:
        marked = block[block.index(PRACTICE_START):]
        return replace_marked(text, marked, PRACTICE_START, PRACTICE_END)
    return text.rstrip("\n") + "\n\n" + block + "\n"


def map_page(data, modules):
    names = summary(data)
    titles = {m["id"]: m["title"] for m in modules}
    link = {m["id"]: m["lesson"].replace("docs/", "") for m in modules}
    out = ["# Course outcome map", "",
           "<!-- Generated by scripts/build_outcome_map.py from curriculum/outcomes.json. Do not edit by hand. -->", "",
           "The institutional course outcomes are the fixed framework this resource supports. The lessons, code and examples are original teaching materials written to build toward them. "
           "An adopting course keeps its own outcomes and assessments; use the [adoption guide](instructor/adopt-outcomes.md) to map these modules to yours.", "",
           "**Direct** means the module offers an assessable artifact for a stated part of the working outcome summary, in the indicated context. **Support** means it builds a transferable skill without demonstrating that application. Optional bridges are separate activities, not completed core evidence. "
           "Neither claims student attainment, a rubric, or accreditation evidence.", "",
           "## Modules and outcomes", "",
           "| Module | Direct evidence | Supporting practice | Data and tools |", "| --- | --- | --- | --- |"]
    for item in data["modules"]:
        direct = ", ".join(item["direct"]) or "—"
        support = ", ".join(item["support"]) or "—"
        if item.get("extension"):
            support += f"; {item['extension']} extension"
        out.append(f"| [{item['id']}. {titles[item['id']]}]({link[item['id']]}) | {direct} | {support} | {badges(item['labels'])} |")
    out += ["", "## Outcomes and what the evidence shows", "",
            "| Outcome | Direct modules | Supporting modules | Evidence status and boundary | Bridge |", "| --- | --- | --- | --- | --- |"]
    for outcome in data["outcomes"]:
        pick = lambda key: ", ".join(str(m["id"]) for m in data["modules"] if outcome["id"] in m[key]) or "—"
        out.append(f"| {outcome['id']} {outcome['summary']} | {pick('direct')} | {pick('support')} | {outcome['evidence_status']} {outcome['coverage_note']} | [Related resource / optional bridge]({outcome['bridge']}) |")
    out += ["", "## Additional direct-evidence activities", "",
            "These links offer additional evidence only when the named activity and its assessment artifact are completed. They do not relabel the original datasets or add new official outcomes. Reusing one artifact across modules is not independent evidence from each module.", "",
            "| Activity | Outcome | Used with modules | Required evidence |", "| --- | --- | --- | --- |"]
    for activity in data["additional_activities"]:
        users = ", ".join(str(m["id"]) for m in data["modules"] if activity["id"] in m["additional_direct"])
        out.append(f"| [{activity['id']}]({activity['path']}) | {', '.join(activity['outcomes'])} | {users} | {activity['summary']} |")
    out += ["", "## Data and tool labels", "", "| Label | Meaning |", "| --- | --- |"]
    out += [f"| {badges([key])} | {value} |" for key, value in data["data_labels"].items()]
    out += ["", "## Evidence by module", "", "| Module | Evidence you produce | Boundary |", "| --- | --- | --- |"]
    out += [f"| {item['id']} | {item['evidence']} | {item['boundary']} |" for item in data["modules"]]
    out += ["", "## Responsible-AI extension", "",
            "Privacy, fairness and limits are practiced across the sequence and treated explicitly in [Module 13](lessons/13-ethics-fairness/index.md). "
            "This extension is not one of the fixed course outcomes. Each module asks one short question:", ""]
    out += [f"- **Module {item['id']}:** {item['responsible']}" for item in data["modules"]]
    return "\n".join(out) + "\n"


def with_block(text, block, path):
    if START in text or END in text:
        return replace_marked(text, block, START, END)
    anchor = next((a for a in ANCHORS if a in text), None)
    if anchor is None:
        raise SystemExit(f"{path}: none of {ANCHORS} found to anchor the block")
    head, tail = text.split(anchor, 1)
    return head + HEADING + block + "\n\n" + anchor + tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    check = parser.parse_args().check
    data, modules = load()
    problems = validate(data, modules)
    if problems:
        sys.exit("\n".join(problems))
    wanted = {ROOT / "docs/outcome-map.md": map_page(data, modules)}
    items = {item["id"]: item for item in data["modules"]}
    for module in modules:
        page = ROOT / module["lesson"]
        original = page.read_bytes().decode("utf-8")
        crlf = "\r\n" in original
        text = with_block(original.replace("\r\n", "\n"), module_block(data, items[module["id"]], module), page)
        wanted[page] = text.replace("\n", "\r\n") if crlf else text
        practice = page.with_name("practice.md")
        original = practice.read_bytes().decode("utf-8")
        text = with_practice(original.replace("\r\n", "\n"), practice_block(items[module["id"]]))
        wanted[practice] = text.replace("\n", "\r\n") if "\r\n" in original else text
    stale = []
    for path, text in wanted.items():
        current = path.read_bytes().decode("utf-8") if path.exists() else None
        # Git may check out Markdown with CRLF on Windows. Compare content,
        # not checkout line endings; real wording changes must still fail.
        if current is None or current.replace("\r\n", "\n") != text.replace("\r\n", "\n"):
            stale.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_bytes(text.encode("utf-8"))
    if check and stale:
        sys.exit("Stale generated outcome text; run python scripts/build_outcome_map.py: " + ", ".join(stale))
    print(("Stale: " if stale and not check else "Up to date: ") + (", ".join(stale) if stale else f"{len(wanted)} files"))


if __name__ == "__main__":
    main()
