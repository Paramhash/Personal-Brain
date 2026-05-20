---
tags: [hidden-markov-model, machine-learning, algorithms, inference]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Viterbi Algorithm

The Viterbi Algorithm is a dynamic programming algorithm for finding the most probable sequence of hidden states (the Viterbi path) that results in a given sequence of observed events, within a [[../concepts/hidden-markov-model.md|Hidden Markov Model (HMM)]].

While the [[../concepts/forward-algorithm.md|Forward Algorithm]] calculates the probability of being in a state at a given time, the Viterbi Algorithm finds the single best path of states that explains the entire observed sequence.

In the context of the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], the Viterbi Algorithm is implicitly used when `model.predict()` is called in `hmm/inference.py` to determine the most likely `state_label` (e.g., [[../concepts/market-regime-pinning.md|pinning]], [[../concepts/market-regime-mean-reverting.md|mean-reverting]], [[../concepts/market-regime-gamma-squeeze.md|gamma-squeeze]]) for a given feature vector.

---