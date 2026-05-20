---
tags: [hidden-markov-model, machine-learning, statistics, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Gaussian Hidden Markov Model (GaussianHMM)

A [[../concepts/hidden-markov-model.md|Hidden Markov Model (HMM)]] where the emission probabilities (the probability of observing a particular feature vector given a hidden state) are modeled by a Gaussian distribution. This means that for each hidden state, the observed features are assumed to follow a multivariate Gaussian distribution with a specific mean vector (μ) and covariance matrix (Σ).

In the context of the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], the `hmmlearn` library's `GaussianHMM` is used. It is configured with:
*   `n_components=3`: Indicating three distinct hidden market regimes.
*   `covariance_type="full"`: Allowing each state to have its own full, unconstrained covariance matrix, capturing complex correlations between features within that state.
*   `n_iter=200`: The maximum number of iterations for the [[../concepts/baum-welch-algorithm.md|Baum-Welch algorithm]] during training.

The choice of `GaussianHMM` is suitable when the observable features are continuous and can be reasonably approximated by a Gaussian distribution within each latent state.

---