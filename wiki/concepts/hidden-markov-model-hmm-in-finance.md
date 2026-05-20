---
tags: ["machine learning", "quantitative finance", "HMM", "regime detection", "time series analysis", "maopm"]
created: 2023-10-27
reviewed: 2026-05-20
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Hidden Markov Model (HMM) in Finance

A Hidden Markov Model (HMM) is a statistical Markov model in which the system being modeled is assumed to be a Markov process with unobserved (hidden) states. In quantitative finance, HMMs are powerful tools for identifying and classifying latent market regimes, such as "low-volatility mean-reverting," "high-volatility trending," or "bear market" states.

## Application in Systematic Trading Pipelines

Within a [[../concepts/systematic-options-trading-pipeline-1dte-7dte.md|systematic options trading pipeline]], the HMM functions as a "Latent Regime Engine." It is crucial that the HMM does *not* process raw prices directly, as price series are often non-stationary. Instead, it ingests a clean, stationary feature array derived from raw data.

### Conceptual Input Matrix for HMM

```python
# Conceptual input matrix shape for the HMM
X = [
    [Daily_Log_Returns, Intraday_Parkinson_Vol, VRP_Trend, GEX_ZScore]
]
```

### Training Window Constraints

To ensure the model accurately reflects real-world conditions and avoids [[../concepts/look-ahead-bias-in-backtesting.md|look-ahead bias]], the HMM is fit using an **Anchored or Rolling Walk-Forward Window**. This means that for any given backtest date, the model can only train on data that occurred strictly *before* that date. For example, if backtesting a trade in June 2025, the HMM would only be trained on data up to May 2025.

### Viterbi Decoding

After training, the HMM uses the Viterbi algorithm to decode the observed features into the most probable sequence of hidden states. The current day's final decoded state label (e.g., $S_t \in \{0, 1, 2\}$) is then passed to the pre-trade state matrix, informing subsequent strategy logic.

The HMM's ability to classify market regimes is a critical component of the "structural triad," allowing strategies to adapt to prevailing market conditions.

---

## MAOPM Integration: Latent Regime Engine

In the [[../research/current research initiatives.md|MAOPM architecture]], the HMM serves as the **signal fusion layer** inside the GEX/Regime Analyst — replacing the need for a separate debate between the GEX and Vol Analysts over conflicting signals.

### Extended Feature Vector (MAOPM)

The MAOPM feature vector extends the baseline with horizon spread and IV/HV skew:

```python
X_t = [
    daily_log_return,        # return dynamics (stationary)
    intraday_parkinson_vol,  # realized vol proxy
    vrp_trend,               # IV² − HV² direction
    gex_z_score,             # GEX normalized to 30-day rolling window (Tool 1)
    iv_hv_skew,              # implied vs. historical skew differential
    horizon_spread_delta     # ΔIHS = ERP_180 − ERP_30 (Tool 2, Lai 2022)
]
```

### State Semantics (K=3 canonical labels)

Post-fit state labels are assigned by sorting emission means $\mu_k$ on the realized vol dimension:

| State | Canonical Label | Typical Characteristics |
|---|---|---|
| $S=0$ | `dealer_stabilized` | Low Parkinson vol, positive GEX Z-score, positive ΔIHS |
| $S=1$ | `transitional` | Moderate vol, mixed GEX, ΔIHS approaching zero |
| $S=2$ | `gamma_accelerating` | High Parkinson vol, negative GEX Z-score, negative ΔIHS |

### Output: `hmm_state` block in GEX Regime Report

The HMM forward pass produces the `hmm_state` JSON block appended to the [[../entities/gex-regime-report-json-schema.md|GEX Regime Report]]:

```json
{
  "hmm_state": {
    "state_label": 0,
    "state_semantics": "dealer_stabilized",
    "posterior_probs": [0.87, 0.10, 0.03],
    "transition_row": [0.94, 0.05, 0.01],
    "regime_persistence_expected_bars": 16,
    "model_fit_date": "2026-05-19"
  }
}
```

### Greek Limit Scaler

The HMM posterior replaces the hard RDR-threshold → sigmoid lookup for the Layer 3 scaler:

$$M(x) = P(S_t = \text{dealer\_stabilized} \mid O_{1:t}) \cdot M_{\max}$$

This produces a continuous, probability-weighted limit that degrades gracefully as regime uncertainty grows — no cliff effects at RDR threshold boundaries.

### Early Management Trigger

When `transition_row[state_label][gamma_accelerating] > 0.15`, the Portfolio Manager tightens Greek limits proactively — before the rules-based GEX hard caps would activate. This gives MAOPM a probabilistic early-warning mechanism unavailable in the pure rules-based regime classification.

### Refit Schedule

| Trigger | Action |
|---|---|
| Nightly EOD | Baum-Welch refit on rolling 252-day window; update $A$, $\mu_k$, $\Sigma_k$; re-label states |
| Intraday cycle | Forward-pass only using current model parameters; no refit |
| Monthly expiry | Re-evaluate $K$ via AIC/BIC on prior 6-month holdout |

**Minimum training data**: 60 trading days (30 for GEX Z-score normalization + 30 for HMM estimation). This compounds the historical GEX availability blocker documented in [Research Agenda Q4](../research/research-agenda-options-maopm.md).

---

## Related

- [[../research/hmm-estimates-of-probability-from-option-prices.md|HMM Approaches in Options Pricing and Agent Architecture]] — full methodology note
- [[../entities/gex-regime-report-json-schema.md|GEX Regime Report JSON Schema]] — `hmm_state` block definition
- [[../concepts/gaussian-hmm.md|Gaussian HMM]] — single-feature baseline
- [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio]] — rules-based Layer 3 predecessor
- [[../concepts/dynamic-portfolio-greek-limits.md|Dynamic Portfolio Greek Limits]] — where $M(x)$ is used
- [[../sources/Detecting stock market regimes from option prices.md|Detecting Stock Market Regimes from Option Prices (Lai 2022)]] — horizon spread source