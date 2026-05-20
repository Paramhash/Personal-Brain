---
tags: ["hmm", "machine-learning", "statistics", "time-series"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Gaussian Hidden Markov Model (Gaussian HMM)

A Gaussian Hidden Markov Model (Gaussian HMM) is a specific type of [Hidden Markov Model (HMM)](../concepts/hidden-markov-model.md) where the observable emissions from each hidden state are assumed to follow a Gaussian (normal) distribution. This makes it suitable for modeling continuous, real-valued data.

In a Gaussian HMM:
*   The hidden states transition according to a [transition matrix](../concepts/transition-matrix.md).
*   For each hidden state, the observations are generated from a multivariate Gaussian distribution, characterized by a mean vector and a covariance matrix.

This model is particularly useful in quantitative finance when the observable features are continuous numerical values, such as the metrics extracted from the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md) (e.g., [ATM Volatility](../concepts/atm-volatility.md), [Skew (Options)](../concepts/options-skew.md), and [Smile Curvature](../concepts/smile-curvature.md)). As described in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), these features can be fed into a Gaussian HMM to identify underlying market regimes or "mood shifts" of option market makers. The [hmmlearn](../entities/hmmlearn.md) library in Python provides an implementation for Gaussian HMMs.