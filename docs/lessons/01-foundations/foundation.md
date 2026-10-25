# Foundation bridge: decisions before models

You can start this course without calculus, prior AI experience, or a paid assistant. Use [first-run setup](../../../QUICKSTART.md), then return to the [module](index.md).

## Read a simple decision

A rule applies an instruction someone wrote. In this module, a value above 80 requests a review: 80 does not, 81 does. Changing the threshold changes the rule; it does not train a model.

A learned model estimates a relationship from examples. For instance, a model could estimate the probability that a service alert needs investigation. Before learning, define an observation, the information available at decision time, an outcome, and the consequence of an error.

A generative model produces content. A fluent explanation is not evidence that an incident occurred or that a recommendation is safe. Check its factual claims against an identified source.

## Four questions to write down

1. Who uses the result and who might be affected?
2. What is the input, including its unit and availability?
3. What output is needed: a number, label, grouping, or generated text?
4. How will you know the method is useful relative to a simple rule?

For an IT alert, a false alarm can waste investigation time; a missed incident can delay recovery. Different costs can justify different decisions. A high accuracy number alone does not settle the choice.

## Trace before running

Write the expected outputs for inputs 79, 80, and 81. Run the supplied script, compare named results, and explain any difference. Save the input and command with your explanation. If the command fails, retain the error text and consult setup; a screenshot is unnecessary.

## Check your understanding

Explain why replacing 80 with 90 is rule editing. Name information a trained alert model would need and one way that information could leak the answer. The module's prediction sketches are design comparisons, not trained services.

Read [practice](practice.md), attempt a response, then consult [feedback](feedback.md). Further mathematics is optional at this stage.
