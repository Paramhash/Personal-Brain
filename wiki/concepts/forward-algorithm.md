---
tags: [hidden-markov-model, machine-learning, algorithms, inference]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Forward Algorithm

The Forward Algorithm is a dynamic programming algorithm used in [[../concepts/hidden-markov-model.md|Hidden Markov Models (HMMs)]] to calculate the probability of an observed sequence of events, given the model parameters. More specifically, it computes the probability of being in a particular hidden state at a given time, having observed the sequence of events up to that time.

This algorithm is crucial for:
*   **Evaluating the likelihood of an observation sequence:** This is used during the E-step of the [[../concepts/baum-welch-algorithm.md|Baum-Welch algorithm]] for training and for model validation (e.g., log-likelihood on holdout sets).
*   **Calculating posterior state probabilities:** Determining `P(State_t = k | O_1...O_t)`, which represents the probability of the HMM being in state `k` at time `t`, given the observations up to time `t`.

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], the Forward Algorithm is utilized in `hmm/inference.py` via `model.predict_proba()` to determine the `posterior_probs` for each potential market regime in live intraday inference.

---