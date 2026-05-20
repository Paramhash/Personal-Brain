---
tags: ["python", "library", "machine-learning", "hmm"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# hmmlearn

`hmmlearn` is an open-source Python library that implements [Hidden Markov Models (HMMs)](../concepts/hidden-markov-model.md) and other related models. It provides tools for fitting HMMs to observed sequences, predicting the most likely sequence of hidden states, and computing the probability of an observed sequence.

Key features of `hmmlearn`:
*   **Model Types:** Supports various HMM types, including [Gaussian HMMs](../concepts/gaussian-hmm.md), Multinomial HMMs, and GMM HMMs.
*   **Fitting:** Implements the expectation-maximization (EM) algorithm (specifically, the Baum-Welch algorithm) for learning model parameters from data.
*   **Decoding:** Provides the Viterbi algorithm for finding the most likely sequence of hidden states given an observation sequence.
*   **Forecasting:** Can be used to predict future observations or state probabilities.

As mentioned in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), `hmmlearn` is a practical tool for implementing the non-parametric surface clustering approach (Method 1), particularly for fitting [Gaussian HMMs](../concepts/gaussian-hmm.md) to continuous features extracted from the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md).