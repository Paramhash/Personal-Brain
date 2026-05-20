yaml
---
tags: ["finance", "quantitative-finance", "hidden-markov-models", "options", "probability-estimation", "market-microstructure", "maopm", "regime-detection"]
created: 2023-10-27
reviewed: 2026-05-20
source_origin: "level1-analysis"
---
# HMM Approaches in Options Pricing and Agent Architecture

This note synthesizes HMM architecture choices for modeling underlying asset price dynamics and extracting probability estimates from option prices, with direct integration mappings into the [MAOPM agent architecture](../research/current%20research%20initiatives.md).

---

## 1. Appropriate HMM Architectures for Asset Price Dynamics

Raw price series are non-stationary and must never be fed directly into an HMM. Three architectures are relevant, ordered by complexity:

### 1a. Gaussian HMM on Returns (Baseline)
The standard approach: model log-returns $r_t = \log(S_t / S_{t-1})$ as emissions from $K$ hidden states, each with a Gaussian emission distribution $\mathcal{N}(\mu_k, \sigma_k^2)$.

- **States**: Typically $K = 3$ in practice: low-vol mean-reverting, moderate-vol transitional, high-vol trending/crisis.
- **Parameters**: Transition matrix $A_{ij}$, emission means $\mu_k$ and variances $\sigma_k^2$, initial state distribution $\pi$.
- **Estimation**: Baum-Welch (EM) on in-sample training window; Viterbi decoding for current state $S_t$.
- **Limitation**: Single emission feature captures only return magnitude, not vol regime or microstructure.

See: [[../concepts/gaussian-hmm.md|Gaussian HMM]]

### 1b. Multivariate Gaussian HMM (MAOPM Target Architecture)
Extends 1a with a multivariate emission vector per time step. This is the architecture relevant to MAOPM:

```python
# Feature vector per bar (stationary, computed from raw data)
X_t = [
    daily_log_return,        # return dynamics
    intraday_parkinson_vol,  # realized vol proxy (stationary)
    vrp_trend,               # IV − HV spread direction
    gex_z_score,             # GEX normalized to 30-day rolling window
    iv_hv_skew,              # implied vs. historical skew differential
    horizon_spread_delta     # ΔIHS = ERP_180 − ERP_30 (from Vol Analyst)
]
```

- **Emission**: $\mathcal{N}(\mu_k, \Sigma_k)$ where $\Sigma_k$ is a full covariance matrix per state.
- **State semantics**: State labels are assigned post-hoc by inspecting $\mu_k$ — e.g., state with low $\sigma_k$, positive GEX Z-score → "dealer-stabilized"; state with high $\sigma_k$, negative GEX Z-score → "gamma-accelerating."
- **Key advantage**: The transition matrix $A_{ij}$ gives the probability of moving from state $i$ to state $j$ — directly answering how many bars a horizon spread inversion typically leads a GEX regime flip (Q9 sub-question 4).

### 1c. Regime-Switching Option Pricing Model (Hamilton-style)
For pricing: each hidden state $k$ drives a separate GBM with parameters $(\mu_k, \sigma_k)$. Option prices are expectations over all state paths weighted by the stationary distribution $\pi$.

$$C = \sum_k \pi_k \cdot C_{\text{BS}}(S, K, T, r, \sigma_k)$$

This is the bridge from regime detection to option *pricing* — distinct from the regime detection problem solved by 1a and 1b.

See: [[../concepts/geometric-brownian-motion.md|GBM]], [[../concepts/black-scholes-model.md|Black-Scholes Model]]

---

## 2. Integrating Option Prices into the HMM Framework

Option prices encode the market's risk-neutral distribution over future returns. Two integration strategies:

### 2a. Option-derived features as HMM emissions (indirect)
Extract stationary scalar features from the options surface and include them in $X_t$:
- **VRP (Variance Risk Premium)**: $\text{IV}^2 - \text{RV}^2$ — captures the spread between option-implied and realized vol. Positive in calm regimes; collapses or inverts ahead of stress.
- **IV/HV skew**: Direction of term structure slope.
- **Horizon spread ΔIHS**: $\text{ERP}_{180} - \text{ERP}_{30}$ from the [Lai 2022](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md) framework. Leading macro indicator — detected COVID-19 regime shift December 2019 vs. GEX/returns only in March 2020.

This is the approach used in MAOPM Tool 2 and is the practical path forward given ThetaData's per-contract data structure.

### 2b. BKM-implied variance as emission (direct)
Apply the [Breeden-Litzenberger theorem](../concepts/breeden-litzenberger-theorem.md) and [Bakshi-Kapadia-Madan](../concepts/bakshi-kapadia-madan-formulation.md) integration to extract model-free variance $V_Q(T)$ directly from the full options chain at each snapshot. Use $V_Q(30)$ and $V_Q(180)$ as emission dimensions alongside GEX and returns.

- **Advantage**: Model-free — no IV-solver, no Black-Scholes assumption.
- **Constraint**: Requires full strike chain snapshot at two expirations per observation; increases data requirements substantially. See Q9 in the [Research Agenda](research-agenda-options-maopm.md) for ThetaData polling architecture.

---

## 3. Challenges and Limitations

| Challenge | Detail | Mitigation in MAOPM |
|---|---|---|
| **Non-stationarity** | Raw prices violate HMM Markov assumption | Use log-returns + normalized features only |
| **Look-ahead bias** | HMM fitted on future data inflates backtest returns | Walk-forward anchored window — see [[../concepts/hidden-markov-model-hmm-in-finance.md|HMM in Finance]] |
| **State label instability** | State ordering can permute across re-fits | Post-fit canonical relabeling by $\mu_k[\text{vol}]$ ascending |
| **Training window length** | GEX Z-score requires 30-day rolling window before first valid observation; HMM needs additional history | Minimum 60 trading days (30 for GEX normalization + 30 for HMM estimation) before first live signal |
| **Number of states K** | $K$ is a hyperparameter; AIC/BIC selection on held-out data | Start with $K=3$; validate against known regime dates (COVID March 2020, Aug 2024 VIX spike) |
| **Computational cost** | Baum-Welch is $O(K^2 T)$ per fit; acceptable for daily bars | Nightly batch refit on Ray worker — see [[../research/optimizing-greek-calculations-with-ray.md|Ray architecture]] |

---

## 4. HMM vs. Other Regime Detection Methods

| Method | Leading / Lagging | IV-informed | Transition probabilities | MAOPM role |
|---|---|---|---|---|
| GEX Z-score + RDR rules | Lagging (microstructure) | No | No | Layer 1 hard caps; Layer 3 sigmoid scaler |
| Horizon spread ΔIHS (Lai 2022) | Leading (macro, weeks ahead) | Yes (BKM-integrated) | No | Vol Analyst emission; macro leading signal |
| **Multivariate Gaussian HMM** | Contemporaneous + transition probabilities | Yes (via features) | **Yes — $A_{ij}$** | **Latent Regime Engine fusing all signals** |
| Risk-neutral density (Breeden-Litzenberger) | Contemporaneous | Yes | No | Point-in-time distribution estimate; no regime dynamics |
| GARCH volatility | Lagging | No | No | Baseline; significantly worse than horizon spread per Lai 2022 |

**Key differentiator**: Only the HMM produces a transition probability matrix $A_{ij}$. This is what resolves Q9 sub-question 4 — the lag structure between horizon spread inversion and GEX regime transition is empirically readable from $A_{ij}$ after fitting on historical data.

---

## 5. Practical Applications in MAOPM

### A. HMM as the Latent Regime Engine (replaces/augments RDR rules)

The HMM Viterbi-decoded state $S_t \in \{0, 1, 2\}$ is added to the [GEX Regime Report JSON schema](../entities/gex-regime-report-json-schema.md) as an `hmm_state` block alongside the existing rules-based `regime` block. The rules engine retains hard-cap authority (Layer 1 / Layer 2); the HMM state is the continuous signal driving the Layer 3 sigmoid scaler $M(x)$.

```
hmm_state:
  state_label: 1                       # Viterbi decoded state
  state_semantics: "dealer_stabilized" # Post-fit canonical label
  posterior_probs: [0.08, 0.87, 0.05]  # P(S_t = k | O_1:t) per state
  transition_row: [0.03, 0.94, 0.03]   # A[state_label, :] — P(next state)
  regime_persistence_expected_bars: 16 # E[duration in current state] = 1/(1-A_ii)
```

### B. Posterior probabilities → Greek limit scaler

Instead of the hard RDR threshold → sigmoid lookup, use the HMM posterior directly:

$$M(x) = P(S_t = \text{stable} \mid O_{1:t}) \cdot M_{\max}$$

This is a continuous, probability-weighted scaler that degrades gracefully as the model becomes uncertain about the regime — no cliff effects at RDR threshold boundaries.

### C. Transition probabilities → early position management

If $A_{ij}$ shows that the current stable state transitions to crisis with probability > 15% per bar, the Portfolio Manager can preemptively tighten Greek limits before GEX rules would trigger — reducing drawdown at regime transitions.

### D. Walk-forward refit schedule

| Event | HMM Action |
|---|---|
| Nightly EOD (M0 milestone) | Refit HMM on rolling 252-day window; update $A$, $\mu_k$, $\Sigma_k$; re-label states |
| Gamma flip crossing (intraday) | Use existing $A_{ij}$ — no refit; read transition probability to accelerating state |
| Monthly expiry (baseline recal.) | Re-evaluate $K$ via AIC/BIC on prior 6-month holdout |

---

## Related

- [[../concepts/hidden-markov-model-hmm-in-finance.md|HMM in Finance — Latent Regime Engine]]
- [[../concepts/gaussian-hmm.md|Gaussian HMM]]
- [[../entities/gex-regime-report-json-schema.md|GEX Regime Report JSON Schema]]
- [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio]]
- [[../concepts/dynamic-portfolio-greek-limits.md|Dynamic Portfolio Greek Limits]]
- [[../sources/Detecting stock market regimes from option prices.md|Detecting Stock Market Regimes from Option Prices (Lai 2022)]]
- [[../concepts/bakshi-kapadia-madan-formulation.md|Bakshi-Kapadia-Madan Formulation]]
- [[../concepts/breeden-litzenberger-theorem.md|Breeden-Litzenberger Theorem]]
- [[research-agenda-options-maopm.md|Research Agenda Q5, Q9]]