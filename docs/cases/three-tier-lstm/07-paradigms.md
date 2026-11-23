# Module 7 Compare learning paradigms

**Brief contrast. Target:** distinguish the learning signal. Allow about two minutes.

The continuing tumor case uses known labels and is supervised classification. Clustering searches for structure without using that target to fit the groups. Reinforcement learning requires a policy, actions, and feedback/rewards; repeatedly running a classifier is not reinforcement learning.

The shared lifecycle still asks about data, meaningful evaluation, and responsible use, but the evidence changes with the question. Do not append KMeans to this case and treat cluster IDs as diagnoses.

For implementation, use the existing [clustering module](../../lessons/07-clustering/index.md), which keeps quality labels out of fitting and model selection. No clustering or reinforcement-learning experiment is claimed for the upstream LSTM code.

## Complete one small explanation

If labels were unavailable, what question could clustering explore, and which claim about a diagnosis could it not establish? Compare [feedback](feedback.md#module-7), then continue to the [Module 8 integration checkpoint](08-integration.md).

[Case overview](index.md) · [All-module map](../../connections.md)
