# Pilot the applied teaching prototype

Modules [5](../lessons/05-regression/index.md), [6](../lessons/06-classification/index.md) and [8](../lessons/08-neural-networks/index.md) prototype a fuller explanation → worked construction → independent code → diagnostic feedback → real-data sandbox → complete reference sequence. Their learning outcomes are unchanged. The other 11 modules have practice and solution notebooks with authored checks and a reasoning task, but no real-data sandbox; this protocol can be used for them too. Mathematical depth is optional open reading; the core remains applied.

## What is ready and what is not yet measured

The implementation supplies three original concept figures with equivalent tables, nine learner-written function contracts, visible local checks, six separate starter/solution notebooks, development sandboxes and task-specific feedback. Technical execution is checked separately from human learning.

**Human learner pilot: NOT RUN.** Do not infer effective learning, reliable workload estimates or accessible notebook operation from code tests or rendered-page checks. The first implementation review and an independent review can use this protocol; no learner session is claimed by its presence.

## Recruit contrasting preparation routes

Use a small formative sample with at least a learner new to programming, a programmer new to ML and a learner with prior ML experience when feasible. Let participants choose the appropriate readiness route. Record relevant preparation and chosen execution interface, not disability diagnoses or unnecessary personal details. These sessions diagnose barriers; they do not estimate a population success rate.

The preparation route must be practical. If a participant needs Python Foundation or the bridge, arrange that preparation before timing an ML task. Record preparation time separately instead of presenting it as a failure to finish the module.

## Run the same observable journey

1. Start at a direct module link. Ask the learner to identify the unchanged outcomes, prerequisites and next action.
2. Ask for a prediction from the concepts page before executing code. Observe whether the learner explains units, labels, shapes or timing in their own words.
3. Let the learner use the worked construction, then attempt the starter's three functions. Record which hint or check was needed and whether it explained the error.
4. Ask for a changed case without the solution visible. Passing remembered check examples is insufficient; observe a new explanation and code change.
5. Run the real-data development sandbox, reconcile one numerical result and identify the boundary between it and the complete reference study.
6. Use the complete reference to address outcomes outside the sandbox: final evaluation, tree-path explanation, baseline comparison or saved-model artifacts as applicable.
7. Attempt the IT transfer and short decision memo. Ask for one missing piece of operational evidence and the appropriate next action.
8. Save code and readable evidence, restart/run all, and ask the learner to explain a decision without assistant-generated text.

Use the [learner-pilot record](../../templates/learner-pilot.md) for observations. Participants can pause or stop; time is descriptive, not a pass/fail threshold. Separate setup failures, content misunderstandings, interface barriers and assessor assistance.

## Diagnostic prompts by module

| Module | Changed prompt | Evidence of understanding | Misconception to investigate |
| --- | --- | --- | --- |
| 5 | Explain a real zero versus a missing lag; change an actual count | Correct residual/MAE, issue-time reasoning and training-only fitting | Signed error cancellation, target-day persistence or full-data imputation |
| 6 | Change error costs and include a score exactly at the threshold | Recomputed counts/cost and a defensible validation choice | Accuracy substituted for cost, wrong denominator or final-test selection |
| 8 | Change width and give a different loss history | Correct dimensions/count and restored validation checkpoint | Batch size treated as parameters or training loss selecting the model |

## Keep access review explicit

Record keyboard navigation, headings/table/figure equivalents, code-entry and feedback reading in the actual chosen notebook/interface. Where appropriate testers and tools are available, observe relevant assistive-technology tasks. The static page's automated checks do not cover notebook editing or app operation. Use the existing [accessibility review log](../accessibility/review-log.md) for actual tested environments and barriers.

Offer an effective equivalent route for the same selected outcome when a format blocks participation. Reading a solution supports interpretation but does not substitute for the required independent implementation. Keep institutional accommodation processes with the course owner.

## Review, revise and decide before extending

Classify each observed barrier, identify its affected outcome, propose a repair and retest that task. Preserve unsuccessful attempts and assessor notes as private formative evidence under the adopting course's process; publish only a nonidentifying summary where appropriate.

Extend the pattern beyond the prototype after the owner and independent reviewer can see that learners locate the route, implement and explain a changed case, use the feedback to recover, preserve evaluation boundaries and save usable evidence. If those observations are absent or a core task remains blocked, record the unresolved issue and revise the prototype first. A small pilot is a design check, not proof that the course is better than another institution's course.

## Pattern to reuse after the pilot

Keep one applied question, a concrete hand example, a bounded code construction, a task with less support, meaningful diagnostic checks, separate public solutions, a development-data connection and outcome-specific evidence. Retain each module's independent entry and complete reference. Adopt useful teaching patterns rather than copying another course's text, assignments or prerequisite assumptions.
