---
tags: ["modeling", "statistics", "machine_learning", "finance", "time_series"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Hidden Markov Model (HMM)

## Definition
A [[../concepts/hidden_markov_model.md|Hidden Markov Model]] (HMM) is a statistical Markov model in which the system being modeled is assumed to be a Markov process with unobserved (hidden) states. The observed data is dependent on these hidden states, and the goal is often to infer the sequence of hidden states from the observed data, or to learn the parameters of the model.

## Components
An HMM is characterized by:
1.  **Hidden States ($S_t$):** A finite set of unobservable states (e.g., "expansion" or "contraction" in financial markets).
2.  **Observations ($Y_t$):** A sequence of observable data points, where each observation is dependent on the current hidden state.
3.  **Initial State Probabilities:** The probability distribution of starting in each hidden state.
4.  **Transition Probabilities ($a_{jk}$):** The probabilities of moving from one hidden state to another (e.g., from state $k$ to state $j$). These form a transition matrix.
5.  **Emission Probabilities ($f_k(Y_t)$):** The probability distribution of observing a particular data point $Y_t$ given that the system is in a specific hidden state $k$.

## Application in Finance
HMMs are widely used in finance to model [[../concepts/stock_market_regimes.md|stock market regimes]] because they can capture the idea that market dynamics (e.g., mean returns, volatility) switch between different unobservable states. For example, [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]] applies an HMM to detect shifts between an expansion and a contraction state in equity markets.

In this context:
*   **Hidden States:** Typically represent market regimes (e.g., "expansion" and "contraction").
*   **Observations:** Can be financial indicators like [[../concepts/horizon_spread_financial.md|horizon spread]], observed stock returns, or conditional volatility.
*   **Emission Distribution:** Often assumed to be Gaussian for simplicity, but can be other distributions depending on the data.

## Advantages
*   **Captures Non-linearities:** Effectively models complex financial phenomena like [[../concepts/volatility_clustering.md|volatility clustering]] and [[../concepts/excess_kurtosis.md|excess kurtosis]] by allowing different parameters for each regime.
*   **Forward-Looking Insights:** When combined with forward-looking indicators like the [[../concepts/horizon_spread_financial.md|horizon spread]] from [[../concepts/options.md|option prices]], HMMs can provide earlier and sharper detection of market shifts.

## Related Concepts
*   [[../concepts/regime_switching_models.md|Regime Switching Models]]
*   [[../concepts/stock_market_regimes.md|Stock Market Regimes]]
*   [[../concepts/markov_process.md|Markov Process]]
*   [[../concepts/horizon_spread_financial.md|Horizon Spread (Financial)]]
*   [[../concepts/garch_model.md|GARCH Model]]
*   [[../concepts/aic_bic_information_criteria.md|AIC and BIC Information Criteria]]

---