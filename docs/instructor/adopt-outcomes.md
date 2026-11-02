# Adopt the modules with your own outcomes

This resource was written to support a fixed set of institutional course and module outcomes. The lessons, code, examples and feedback are original teaching materials built toward them. You do not need that course to use the resource. This guide shows how to connect the modules to your own outcomes and assessments.

The [outcome map](../outcome-map.md) shows the existing connections. Its data lives in `curriculum/outcomes.json`. Treat the map as a starting point you check against your own course, not as a statement of equivalence.

## Steps

1. **List your outcomes.** Write each one in the verb-and-evidence form your course uses. Keep your institution's wording in your private register. Do not copy it into the public repository.
2. **Pick modules by evidence.** Read each candidate module's "Course outcomes and evidence" section. Choose a module when the artifact it produces is the evidence you need.
3. **Check the label.** A module labeled *Synthetic* or *Offline fixture* builds technique but does not show work on genuine operational data or a live service. Add a bridge activity when your outcome requires that. The [network record interpretation](../cases/network-record-interpretation.md), [monitoring decision record](../advanced/monitoring-decision-record.md) and [live API route](../advanced/live-api-route.md) pages are bridges.
4. **Name the artifact and rubric.** Use the criteria in [adaptable assessment](assessment.md). State what a learner produces, what the support allowed, and how you will judge it.
5. **Record the mapping.** Keep it in a private register. Mark each link as direct evidence, supporting practice or no mapping.
6. **Pilot before grading.** Run the task from a clean setup and check workload and access. Use the [pilot protocol](teaching-prototype-pilot.md).

## Mapping register template

Copy this table into your own register. Leave anything you have not verified marked as unverified.

| Your outcome (private wording) | Module(s) | Link type | Artifact you assess | Bridge needed | Assessor | Reviewed | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | Direct / Support / None | | Yes / No | | | Unverified |

## Adoption checklist

- Each outcome you assess has at least one direct artifact, not only supporting practice.
- Data and tool labels match your claims. Do not describe a fixture as a live call or a synthetic record as network traffic.
- Allowed AI assistance, disclosure and an equivalent no-assistant route are published before grading.
- Accessible alternatives still demonstrate the same outcome.
- Weights, deadlines and submission rules come from your course, not from this repository.
- No institutional text, student work or restricted assessments are added to the public repository.

## Limits

The map records planned alignment. It does not show that learners attained an outcome, that a rubric measures it, or that any accreditation requirement is met. The advisory computing labels in the instructor notes are planning shorthand, not official outcome numbers.
