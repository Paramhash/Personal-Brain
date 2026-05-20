---
tags: ["hmm", "markov-chains", "statistics", "modeling"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Transition Matrix

In the context of [Hidden Markov Models (HMMs)](../concepts/hidden-markov-model.md) and Markov chains, a transition matrix (also known as a stochastic matrix or probability matrix) is a square matrix used to describe the probabilities of transitioning from one state to another in a system.

For a system with $N$ states, the transition matrix $\mathbf{P}$ is an $N \times N$ matrix where each element $p_{ij}$ represents the probability of moving from state $i$ to state $j$ in a single time step.

Key properties of a transition matrix:
*   Each element $p_{ij}$ must be between 0 and 1 (inclusive).
*   The sum of probabilities in each row must equal 1 (i.e., $\sum_{j=1}^{N} p_{ij} = 1$ for all $i$), as the system must transition to *some* state.

Transition matrices are fundamental to modeling systems that switch between discrete states, such as market regimes. In [Regime-Switching Option Pricing Models](../concepts/regime-switching-option-pricing-model.md), as discussed in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), the transition matrix $\mathbf{P}$ defines the risk-neutral probabilities of switching between different volatility regimes, and its elements are often parameters to be calibrated from market data.