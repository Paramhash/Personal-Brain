---
tags: [entity, library, python, machine-learning, hidden-markov-model]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# hmmlearn Library

`hmmlearn` is a Python library that implements [[../concepts/hidden-markov-model.md|Hidden Markov Models (HMMs)]] and their associated algorithms. It provides a scikit-learn compatible API for training, inference, and sampling from HMMs.

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] project, `hmmlearn` (specifically version `0.3.x`) is the core library used for the HMM implementation. The model chosen is the [[../concepts/gaussian-hmm.md|GaussianHMM]], which leverages `hmmlearn`'s capabilities for:
*   **Training:** Using the [[../concepts/baum-welch-algorithm.md|Baum-Welch algorithm]] to fit model parameters.
*   **Inference:** Employing the [[../concepts/forward-algorithm.md|Forward algorithm]] for posterior probabilities (`predict_proba`) and the [[../concepts/viterbi-algorithm.md|Viterbi algorithm]] for the most likely state sequence (`predict`).

---