# Interpret network records: from synthetic events to genuine flows

This bridge activity supports the course outcome on interpreting data from network sources. Modules 3 and 4 use small original synthetic event records. They teach the interpretation steps, but synthetic rows do not show that you can read genuine network data. Complete this activity after Module 4 to practice the same steps on documented real flow records.

It is optional, adds no required assessment, and does not replace any adopting course's own tasks. Budget about 90 minutes plus setup and the first download; this is an estimate awaiting a learner pilot.

## Learning outcomes

- **B1:** Describe what one record represents, when it was observed, and what it leaves out.
- **B2:** Read recorded fields with their units and decide which are available when a decision must be made.
- **B3:** Explain a rejected, missing, or unusual record without turning it into a claim about an attack.
- **B4:** Write a short analyst note that separates observation, interpretation, and action.

## Part 1: Read the synthetic events

Use `data/samples/network-events/events.csv` from [Module 3](../lessons/03-data-processing/index.md). Its fields are `event_id`, `timestamp`, `source`, `latency_ms`, and `bytes_sent`. Answer from the file, not from memory:

1. Which source produced each event, and what does a repeated `event_id` imply?
2. One timestamp has a `+01:00` offset. How should it be compared with the `Z` timestamps?
3. One `latency_ms` value is empty. What does the missing value mean, and what would a replacement hide?

## Part 2: Read genuine flow records

Use the data dictionary in the [RT-IoT triage project](../../projects/rt-iot-triage/README.md). Use its documented core environment with the regression extra. You do **not** need to train its classifier for this interpretation exercise. From the repository root, run:

```python
import runpy
from pathlib import Path

study = runpy.run_path("projects/rt-iot-triage/scripts/run.py")
load_frame = study["load_frame"]
frame = load_frame("runs/datasets/rt-iot2022/original.zip")
# source_row is the zero-based position in the checksum-verified source file.
records = frame[study["FEATURES"] + ["Attack_type"]].copy()
records.insert(0, "source_row", range(len(records)))
folder = Path("runs/network-interpretation")
folder.mkdir(parents=True, exist_ok=True)
output = folder / "three-flows.csv"
with output.open("x", encoding="utf-8", newline="") as handle:
    records.iloc[:3].to_csv(handle, index=False)
print(records.iloc[:3].to_string(index=False))
```

The downloader verifies the pinned archive. `three-flows.csv` contains three illustrative source records, not a representative sample. The exclusive write preserves an existing exercise: choose a fresh folder for another attempt.

If you already ran the full classifier, `predictions.csv` contains decisions and `source_row` identifiers, **not** the input fields. Retrieve those fields with `records.iloc[predictions["source_row"].astype(int)]` after loading `predictions` with pandas. `validation.csv` contains policy scores, not flow records. Inspecting these examples does not authorize retuning a frozen model on test results.

For each of the three exported flows, write one paragraph:

1. **Observation:** the protocol, service, duration, and forward and backward packet counts, with units where the source states them.
2. **Interpretation:** what the pattern could mean, and a second explanation that fits equally well.
3. **Availability:** whether each field exists at connection start or only after the flow ends.
4. **Action:** human review, or no action, with a reason. Do not propose automatic blocking.

## Part 3: Compare the two sources

Complete this table in your own words.

| Question | Synthetic events | Genuine flows |
| --- | --- | --- |
| What does one row represent? | | |
| Who or what produced the labels? | | |
| What is missing or ambiguous? | | |
| What could you not conclude from this alone? | | |

## What good evidence looks like

- Fields are described with their source definitions rather than guessed names or units.
- An unusual value is called a reason to investigate, not an incident.
- The note names at least one limit of the capture, such as a staged experimental environment or the absence of device identity and timestamps.
- Any statement about attacks cites a source label and says where it came from.

## Boundaries

The RT-IoT archive is a captured experiment, not a representative production fleet. This activity does not demonstrate packet-level analysis, live monitoring, or operational detection performance. For a second genuine security case, see the [phishing case](phishing.md); its records are URL and content attributes, not network traffic.
