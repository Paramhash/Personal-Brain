---
tags: ["volatility-modeling", "time-series", "econometrics", "regime-detection", "quantitative-finance"]
created: 2026-07-03
reviewed: false
source_origin: "level1-analysis"
---
# GARCH Model

## Definition

Generalized Autoregressive Conditional Heteroskedasticity (GARCH), introduced by Bollerslev (1986) as an extension of Engle's (1982) ARCH, models time-varying conditional variance in financial return series. The standard GARCH(p,q) specification:

$$r_t = \mu + \epsilon_t, \quad \epsilon_t = \sigma_t z_t, \quad z_t \sim \mathcal{N}(0,1)$$

$$\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2$$

where $\omega > 0$, $\alpha_i \geq 0$, $\beta_j \geq 0$, and $\sum \alpha_i + \sum \beta_j < 1$ for covariance stationarity.

The GARCH(1,1) is the workhorse in practice:

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

- $\alpha$ (ARCH term): sensitivity of current variance to the last squared shock
- $\beta$ (GARCH term): persistence — how long shocks remain elevated
- $\alpha + \beta$ close to 1 → high volatility persistence (typical in equity markets)

## Variants Relevant to MAOPM

### EGARCH (Exponential GARCH)
Models log-variance to allow asymmetric responses (negative returns raise volatility more than positive returns of equal magnitude — the leverage effect):

$$\ln \sigma_t^2 = \omega + \alpha \left(\frac{|\epsilon_{t-1}|}{\sigma_{t-1}} - \sqrt{\frac{2}{\pi}}\right) + \gamma \frac{\epsilon_{t-1}}{\sigma_{t-1}} + \beta \ln \sigma_{t-1}^2$$

The $\gamma < 0$ term captures the leverage effect, relevant for SPX where down moves amplify realized vol disproportionately.

### Markov-Switching GARCH (MS-GARCH)
Combines GARCH with a discrete hidden Markov chain governing GARCH parameters:

$$\sigma_t^2 = \omega(S_t) + \alpha(S_t)\epsilon_{t-1}^2 + \beta(S_t)\sigma_{t-1}^2$$

where $S_t \in \{1, 2, \ldots, K\}$ is the hidden regime state. This is the GARCH equivalent of the HMM-based regime detection in the MAOPM pipeline. Lai (2022) estimates MS-GARCH as the primary comparison baseline for the horizon spread HMM.

## Performance vs. Horizon Spread HMM (Lai 2022)

Lai (2022) ([detecting-stock-market-regimes-from-option-prices-lai-2022](../sources/detecting-stock-market-regimes-from-option-prices-lai-2022.md)) tests three regime detection inputs under the same two-state HMM framework:

| Detection Input | Indecisive-Zone Probability | Notes |
|---|---|---|
| **Horizon spread (option-implied ERP)** | **4.6%** | Forward-looking; detected COVID-19 in Dec 2019 |
| Historical returns | 16% | Backward-looking; lags structural breaks |
| **GARCH conditional volatility** | **34%** | Backward-looking; most indecision in crisis transitions |

GARCH-based regime detection has the highest indecisive-zone rate — meaning the model is frequently uncertain about the current regime precisely when regime clarity matters most (at transition boundaries). The horizon spread HMM used in MAOPM substantially outperforms it.

## LSTM-GARCH Hybrid

An LSTM-GARCH combines:
- **LSTM**: encodes long-range temporal dependencies in the feature sequence — addresses the first-order Markov limitation of the GaussianHMM
- **GARCH**: models conditional variance explicitly rather than approximating it via HMM emission covariances

Two common architectures:
1. **Sequential**: LSTM produces a latent state vector; GARCH(1,1) models the variance of the LSTM residuals
2. **Parameterized**: LSTM outputs the time-varying GARCH parameters $(\omega_t, \alpha_t, \beta_t)$ directly

For regime detection (vs. volatility forecasting), the LSTM-GARCH output is a continuous variance estimate that requires a calibration threshold layer to produce discrete state labels equivalent to the HMM's `posterior_probs`. See [research-agenda-2026-07-03](../research/research-agenda-2026-07-03.md) Q4 for the proposed comparison test against the current GaussianHMM.

## Key Limitations for MAOPM Context

1. **Backward-looking**: GARCH variance estimates lag forward-looking signals (options-implied volatility, horizon spread). Lai (2022) demonstrates this quantitatively.
2. **No discrete regime semantics**: Raw GARCH output is a continuous $\sigma_t^2$ — does not directly produce `{pinning, mean_reverting, gamma_squeeze}` labels without a supervised or clustering step.
3. **No GEX integration**: Standard GARCH treats all return variance as endogenous. MAOPM's GEX Z-score is an exogenous microstructure signal; GARCH cannot incorporate it without extension (GARCH-X with exogenous regressors).

## Related Concepts
- [[../concepts/hidden-markov-model-hmm-in-finance.md|HMM in Finance]]
- [[../concepts/regime_switching_models.md|Regime Switching Models]]
- [[../concepts/realized-volatility.md|Realized Volatility]]
- [[../concepts/implied-volatility.md|Implied Volatility]]
- [[../concepts/stochastic_volatility_models.md|Stochastic Volatility Models]]
- [[../concepts/hidden_markov_model.md|Hidden Markov Model]]
- [[../concepts/horizon-spread-option-implied-erp.md|Horizon Spread (Option-Implied ERP)]]
- [[../concepts/Neural_Network_Loss_Landscapes.md|Neural Network Loss Landscapes]]
