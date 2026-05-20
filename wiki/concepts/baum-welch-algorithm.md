---
tags: [hidden-markov-model, machine-learning, algorithms, training]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Baum-Welch Algorithm

The Baum-Welch algorithm is a specific instance of the Expectation-Maximization (EM) algorithm used to find the unknown parameters (transition probabilities, emission probabilities, and initial state probabilities) of a [[../concepts/hidden-markov-model.md|Hidden Markov Model (HMM)]] given a set of observed sequences.

It is an iterative algorithm that consists of two main steps:
1.  **Expectation (E-step):** Calculates the expected number of times a particular transition or emission occurs, given the current model parameters and the observed data. This step typically uses the [[../concepts/forward-algorithm.md|Forward Algorithm]] and Backward Algorithm.
2.  **Maximization (M-step):** Updates the model parameters to maximize the likelihood of the observed data, based on the expectations calculated in the E-step.

The algorithm converges to a local maximum of the likelihood function. In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], the Baum-Welch algorithm is employed in `hmm/train.py` to fit the [[../concepts/gaussian-hmm.md|GaussianHMM]] on historical DTE-aligned options data.

---