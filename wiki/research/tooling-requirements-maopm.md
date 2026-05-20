---
tags: [research, maopm, tooling, infrastructure, gex, horizon-spread, data-pipeline]
created: 2026-05-19
reviewed: 2026-05-19
source_origin: "session-2026-05-19"
---
# MAOPM Tooling Requirements

Three custom computational tools must be built before the MAOPM agent loop can receive the structured signals it requires. An [existing dxFeed/Tastytrade data engine](../entities/tastytrade-dxfeed-data-engine.md) provides partial live-data implementations of Tool 1 and Tool 2. All other signal sources are either vendor subscriptions or off-the-shelf libraries.

---

## Tool 1: GEX Regime Divergence Engine

**Purpose**: Compute the Regime Divergence Ratio (RDR) and the S&P 500 Internal GEX Index — metrics that are central to the 3-layer dynamic Greek limit trigger hierarchy but are not available from any vendor in the required form.

**Why custom**: [FlashAlpha](../entities/flashalpha.md) provides pre-computed `net_gex`, `gamma_flip`, and regime labels (~$239/month), but its regime labels are a black box — the MAOPM agent cannot interrogate classification confidence, extend the metric set, or compute the RDR (`|Index GEX| / Σ|Component GEX|`) which is a custom metric not exposed by FlashAlpha. Without the RDR, the 3-layer trigger hierarchy (Layer 1: index GEX sign; Layer 2: VVIX; Layer 3: RDR sigmoid) cannot operate as designed.

**Output**: Populates the [GEX Regime Report JSON Schema](../entities/gex-regime-report-json-schema.md) fields:
- `index_gex`, `index_gex_z_score`, `index_gex_sign`
- `internal_gex_index` (average GEX Z-score across all 500 S&P 500 constituents)
- `regime_divergence_ratio` = `|index_gex| / Σ|component_gex|`
- `gamma_flip_level`, `above_gamma_flip`, `gamma_flip_distance_pct`
- `top_weighted_stocks[]` (top 5–10 by index weight with per-stock `gex_z_score` and `gex_signal`)
- `regime.divergence_regime_classification`, `regime.microstructure_bias`, `regime.new_positions_permitted`

**Computation pipeline** (per [GEX Scanner Logic Flow](gex-scanner-logic-flow.md)):
1. For each of 500 S&P 500 constituents: fetch current options chain → compute per-contract GEX → sum → stock GEX
2. Normalize each stock GEX against its 30-day rolling mean and standard deviation → GEX Z-score
3. Average all 500 Z-scores → Internal GEX Index
4. Compute `RDR = |SPX/SPY index GEX| / Σ|stock GEX|`
5. Classify regime (coherent band 0.5–2.0; outside = divergence regime)
6. Emit `GEXRegimeReport` JSON to GEX/Regime Analyst agent via Seam A

**Parallelization**: 500 stocks × per-contract Greeks aggregation is CPU-bound. Distribute across 64 cores (128 threads) using [Ray](../entities/ray.md) per [Optimizing Greek Calculations with Ray](optimizing-greek-calculations-with-ray.md). Target latency: sub-second per cycle.

**Data source**: [ThetaData](../entities/thetadata.md) STANDARD tier minimum (real-time quote snapshots and historical per-contract Greeks). PRO tier adds pre-computed per-contract implied vol and 2nd-order Greeks.

**Burn-in requirement**: GEX Z-scores require a 30-day rolling window. Any backtest or paper-trading start needs 30 trading days of per-stock GEX history before the first signal is valid.

**Open design decision (resolved)**: Tool 1 produces regime labels as a rules-based output of the already-computed RDR, Z-scores, and `above_gamma_flip` flag. FlashAlpha is not needed. Its $239/month subscription is eliminated. Optional one-time use: cross-validate Tool 1 labels against FlashAlpha during development to catch Z-score pipeline bugs.

**Existing partial implementation**: The [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md) (`data_engine.py`) provides real-time per-contract `gamma` and `oi` via Tastytrade's OpenAPI websocket — sufficient to compute raw index GEX and `gamma_flip_level` for SPX/SPY. **Does not cover**: constituent-level GEX (500-stock bulk fetch is architecturally infeasible with a streaming websocket), GEX Z-scores (no historical data), or RDR. ThetaData remains required for the constituent chain data and 30-day rolling normalization window.

**Relevant vault docs**: [GEX Scanner Logic Flow](gex-scanner-logic-flow.md), [Optimizing Greek Calculations with Ray](optimizing-greek-calculations-with-ray.md), [GEX Regime Report Schema](../entities/gex-regime-report-json-schema.md), [Dynamic Portfolio Greek Limits](../concepts/dynamic-portfolio-greek-limits.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md), [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md)

---

## Tool 2: Horizon Spread Pipeline

**Purpose**: Compute the option-implied equity risk premium horizon spread ΔIHS = ERP₁₈₀ − ERP₃₀ — the macro leading indicator (Lai 2022) that detected COVID-19 in December 2019, three months before GEX or historical volatility methods signaled it.

**Why custom**: No vendor pre-computes this metric. ThetaData provides the raw options chain data (per-contract IV, bid, ask); the BKM integration, tenor interpolation, and ERP differential must all be built client-side.

**Output**: Populates the `term_structure.horizon_spread` field in the [Vol Surface Summary JSON Schema](../entities/vol-surface-summary-json-schema.md), delivered by the Volatility Analyst agent. Negative values signal a crisis regime (short-term risk premium exceeds long-term).

**Computation pipeline** (per [MAOPM Architecture: Horizon Spread & GEX Fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md)):
1. Snapshot the full SPY/SPX options chain for the two expirations bracketing 30 DTE and the two bracketing 180 DTE (`option_snapshot_quote` or `option_snapshot_greeks_implied_volatility`)
2. For each bracketing expiration: extract all OTM puts (K < F) and OTM calls (K > F), compute mid-price
3. Apply BKM integration over the strike domain → model-independent Q-measure variance V_Q(T) at each bracketing expiry
4. Time-interpolate between the two bracketing expiries to get V_Q(30) and V_Q(180) at constant maturity (see [Constant-Maturity Interpolation](../concepts/constant-maturity-interpolation.md))
5. Compute ERP₃₀ and ERP₁₈₀ using risk-free rate, dividend yield, and P-measure drift estimate
6. ΔIHS = ERP₁₈₀ − ERP₃₀; emit to Vol Surface Summary JSON

**Update cadence**: Poll ThetaData every 5–15 minutes. The horizon spread is a macro leading indicator — sub-minute resolution provides no additional signal value.

**Data source**: [ThetaData](../entities/thetadata.md):
- **Minimum viable tier: VALUE** — real-time `option_snapshot_quote` (bid/ask per contract). BKM formula operates directly on option prices; no IV solver required. Client must run BSM locally only if IV is needed for other purposes.
- **PRO tier advantage**: `option_snapshot_greeks_second_order` (PRO only) returns pre-computed `implied_vol` per contract, eliminating client-side BSM numerical solving across hundreds of strikes per expiration chain. Materially reduces pipeline latency.

**Key constraint (confirmed from ThetaData docs)**: ThetaData returns data keyed to actual YYYY-MM-DD expiration dates — NOT constant-maturity surfaces. The client must select the two expirations bracketing each target tenor and perform time-interpolation of the integrated variance. There is no constant-maturity endpoint.

**Existing partial implementation**: The [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md) (`data_engine.py` + `vol_solver.py` + `vol_surface.py`) provides all data inputs Tool 2 requires from the live market: per-contract `mid` prices, `vendor_iv`, and `solved_iv` across the full OTM strike chain, for any expiration, at 15-second collection cadence. Four calls to `fetch_chain_snapshot()` (two expirations bracketing 30 DTE + two bracketing 180 DTE) deliver the raw chain data. **The single missing module is the BKM integration function**:

```python
def bkm_integrate(contracts_df, risk_free_rate, time_to_expiry_years):
    """Model-free Q-measure variance from OTM mid prices.
    Input: ChainSnapshot.contracts filtered to OTM strikes (K < F for puts, K > F for calls).
    Returns: scalar V_Q(T) for use in ERP computation.
    """
    # 1. Sort OTM contracts by strike
    # 2. Compute ΔK (trapezoidal weights) per strike
    # 3. V_Q = 2 × Σ [mid(K) / K² × ΔK × exp(r × T)]
```

Once implemented, constant-maturity interpolation and ERP differential complete Tool 2. Note: use `mid` prices as BKM input — do NOT use `solved_iv` or `vendor_iv` (both are BSM-derived, not model-free).

**Relevant vault docs**: [Option-Implied Horizon Spread](../concepts/option-implied-horizon-spread.md), [MAOPM Architecture: Horizon Spread & GEX Fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md), [Constant-Maturity Interpolation](../concepts/constant-maturity-interpolation.md), [Vol Surface Summary Schema](../entities/vol-surface-summary-json-schema.md), [ThetaData](../entities/thetadata.md), [Lai 2022 source](../sources/lai-2022-horizon-spread.md), [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md), [Bakshi-Kapadia-Madan Formulation](../concepts/bakshi-kapadia-madan-formulation.md)

---

---

## Tool 3: HMM Latent Regime Engine

**Purpose**: Fuse the outputs of Tool 1 (GEX Z-score) and Tool 2 (ΔIHS) with realized vol and return features into a single Viterbi-decoded latent market regime state. Replaces the hard RDR-threshold → sigmoid lookup for the Layer 3 Greek limit scaler with a continuous, probability-weighted signal $M(x) = P(S_t = \text{dealer\_stabilized} | O_{1:t}) \times M_{\max}$.

**Output**: Populates the `hmm_state` block in the [GEX Regime Report JSON Schema](../entities/gex-regime-report-json-schema.md): `state_label`, `state_semantics`, `posterior_probs`, `transition_row`, `regime_persistence_expected_bars`, `model_fit_date`.

**Feature vector** (6 dimensions, all stationary):

| Feature | Source | Requires |
|---|---|---|
| `daily_log_return` | Closing price history | Polygon.io or ThetaData |
| `intraday_parkinson_vol` | Intraday high/low: `(ln H − ln L)² / 4 ln 2` | Intraday OHLC data |
| `vrp_trend` | IV² − HV² direction | `vendor_iv` / `solved_iv` + historical HV |
| `gex_z_score` | Tool 1 output | 30-day rolling GEX history |
| `iv_hv_skew` | IV skew − HV skew | `vol_surface.py` + historical HV |
| `horizon_spread_delta` | ΔIHS = ERP₁₈₀ − ERP₃₀ | Tool 2 output |

**Training**: `hmmlearn.GaussianHMM`, $K = 3$ states (canonical labels: `dealer_stabilized`, `transitional`, `gamma_accelerating`), Baum-Welch EM on 252-day rolling window. See [Baum-Welch algorithm gap](gap-analysis-2026-05-20.md#gap-1a--baum-welch-algorithmmd).

**Inference**: Forward algorithm intraday (no refit) → `posterior_probs[k]` per state. Viterbi decoding → `state_label`.

**Refit schedule**:
- Nightly EOD: Baum-Welch on rolling 252-day feature matrix; update $A$, $\mu_k$, $\Sigma_k$; re-label states by ascending realized vol of $\mu_k$
- Intraday: forward-pass only using that morning's fitted parameters
- Monthly: AIC/BIC K-selection on prior 6-month holdout

**Minimum data requirement**: 60 trading days before first valid signal (30 for GEX Z-score rolling window + 30 for HMM estimation). Compounds the constituent GEX historical data dependency from Tool 1.

**Existing partial implementation**: None. `hmmlearn` is available as a dependency ([hmmlearn entity](../entities/hmmlearn.md)); the feature matrix assembly requires Tool 1 and Tool 2 to be operational first. Tool 3 is therefore a **Phase 1 dependency** on Tool 1 completion and **Phase 0.5** for Tool 2 (BKM module completion enables `horizon_spread_delta`).

**Parallelization**: Baum-Welch on 252 days × 6 features is fast (seconds on a single core). No Ray distribution needed for the HMM itself. Ray parallelization in Tool 1 produces the `gex_z_score` input; Tool 3 consumes it.

**Relevant vault docs**: [HMM Approaches in Options Pricing and Agent Architecture](hmm-estimates-of-probability-from-option-prices.md), [HMM in Finance — Latent Regime Engine](../concepts/hidden-markov-model-hmm-in-finance.md), [GEX Regime Report Schema](../entities/gex-regime-report-json-schema.md), [Dynamic Portfolio Greek Limits](../concepts/dynamic-portfolio-greek-limits.md), [hmmlearn](../entities/hmmlearn.md)

---

## Non-Custom Infrastructure (Subscriptions / Off-the-Shelf)

| Component | Type | Provider / Library | Used By | Tier / Cost |
|---|---|---|---|---|
| Options chain (live) | Existing tool + Subscription | [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md) (live); [ThetaData](../entities/thetadata.md) (historical + constituents) | Tool 1, Tool 2, Tool 3, Greeks Analyst, Vol Analyst | dxFeed: Tastytrade account; ThetaData: VALUE min |
| Underlying price, volume | Subscription | [Polygon.io](../entities/polygon-io.md) | Technical Analyst, delta hedge triggers, Tool 3 log returns | Varies |
| News, earnings calendar | Subscription | Financial news APIs | News/Catalyst Analyst | Varies |
| Live positions, P&L, margin | Broker API | [Interactive Brokers TWS API](../entities/interactive-brokers-api.md) | Portfolio Manager, Risk Team, Execution Agent | Included with account |
| HMM training library | Open source | [hmmlearn](../entities/hmmlearn.md) | Tool 3 | Free |
| Distributed compute | Open source | [Ray](../entities/ray.md) | Tool 1 (GEX parallelization) | Free |
| Hardware | Owned | [AMD Threadripper 3990X](../entities/amd-ryzen-threadripper-3990x.md) | All local compute | Owned |

> **FlashAlpha removed**: Since Tool 1 computes GEX Z-scores, the Internal GEX Index, and the RDR from raw ThetaData options chain data, regime classification is a trivial rules-based output of the same pipeline — no black-box vendor labels needed. FlashAlpha’s only remaining value is cross-validation during Tool 1 development (one-time, not a permanent dependency).

---

## Build Sequencing

All three tools are **Phase 0 prerequisites** — the MAOPM agent loop cannot produce reliable structured signals without them. Build order:

1. **Tool 2 first** (BKM module): The [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md) already provides all data inputs; only the BKM integration function is missing. Shortest path to a working signal.
2. **Tool 1**: Constituent GEX requires ThetaData access and Ray parallelization. The GEX Regime Divergence Engine is higher priority than Tool 3 because:
- The 3-layer dynamic Greek limit trigger hierarchy depends on the RDR (Layer 3)
- It feeds all four GEX divergence strategies (Dispersion, Fragility Short, Gamma Flip Mean Reversion, Term Structure Catch-Up)
- Regime classification is a rules-based output of the same pipeline at no additional cost — no interim vendor substitute required

The Horizon Spread Pipeline is independent and can be developed in parallel once ThetaData access is established.

**Open research questions blocking full specification**:
- Q9 Sub-Qs 3–5: How horizon spread conflicts with GEX signals are resolved — affects how Tool 2 output is weighted in the agent debate
- Q6: Portfolio scope (SPY-only vs. constituent basket) — affects the constituent universe fed into Tool 1

**Relevant research agenda questions**: [Q6](research-agenda-options-maopm.md#q6), [Q9](research-agenda-options-maopm.md#q9)
