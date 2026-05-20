---
tags: ["hmm", "machine-learning", "statistics", "time-series"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Hidden Markov Model (HMM)

A Hidden Markov Model (HMM) is a statistical Markov model in which the system being modeled is assumed to be a Markov process with unobserved (hidden) states. An HMM consists of:

1.  **Hidden States:** A finite set of states that are not directly observable.
2.  **Observations:** A finite set of observable symbols or a continuous distribution of observable emissions.
3.  **Transition Probabilities:** Probabilities of moving from one hidden state to another, often represented by a [transition matrix](../concepts/transition-matrix.md).
4.  **Emission Probabilities:** Probabilities of observing a particular symbol or emission given a hidden state.
5.  **Initial State Probabilities:** Probabilities of starting in each hidden state.

HMMs are widely used in various fields, including speech recognition, bioinformatics, and quantitative finance. In finance, they can be used to model market regimes (e.g., bull, bear, volatile) that are not directly observable but influence observable market data like returns or implied volatilities.

For example, in the context of [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), HMMs are used to infer underlying market "moods" or regimes from features of the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md) or to calibrate [Regime-Switching Option Pricing Models](../concepts/regime-switching-option-pricing-model.md). A specific type, the [Gaussian HMM](../concepts/gaussian-hmm.md), is often employed when observations are continuous numerical vectors.