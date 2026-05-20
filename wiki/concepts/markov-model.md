---
tags: [statistics, probability, sequential data]
created: 2023-10-27
reviewed: false
source_origin: "hidden markov model.md"
---
A **Markov model** describes a system that transitions between different states over time, where these transitions are governed by probabilities. The defining characteristic of a Markov model is the **Markov property**: the probability of transitioning to any future state depends *only* on the current state, and not on the sequence of events that preceded it. In simpler terms, the future is independent of the past, given the present.

In a standard Markov model, all states are directly observable. For example, in a weather model, you might have states like "Sunny" and "Rainy." If it's "Rainy" today, there's a certain probability it will be "Rainy" tomorrow and a certain probability it will be "Sunny" tomorrow. You can directly observe whether it is raining or sunny.

Markov models are foundational to understanding more complex probabilistic models, such as the [[../concepts/hidden-markov-model.md|Hidden Markov Model (HMM)]], where the underlying states are not directly visible.