---
tags: [research, maopm, tooling, infrastructure, gex, horizon-spread, data-pipeline]
created: 2026-05-19
reviewed: 2026-05-19
source_origin: "session-2026-05-19"
---
# MAOPM Tooling Requirements

Four custom computational tools are defined for MAOPM. Build order is determined by dependency structure and evidence quality — Tool 1 (constituent GEX/RDR) is deferred pending empirical validation. An [existing dxFeed/Tastytrade data engine](../entities/tastytrade-dxfeed-data-engine.md) provides partial live-data implementations of Tool 1 and Tool 2. All other signal sources are either vendor subscriptions or off-the-shelf libraries.

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

> ⚠️ **Status: Deferred to Phase 2** — Constituent GEX / RDR has no published predictive track record; only contemporaneous practitioner evidence exists for index-level GEX. The 500-stock bulk fetch, Ray parallelization, and ThetaData STANDARD tier subscription are deferred until empirical validation justifies the build cost. Index-level GEX (gamma flip, GEX sign, gamma wall) remains in scope via the existing dxFeed engine at no additional build cost.

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

## Tool 3: HMM Latent Regime Engine

**Purpose**: Fuse the outputs of Tool 1 (GEX Z-score) and Tool 2 (ΔIHS) with realized vol and return features into a single Viterbi-decoded latent market regime state. Replaces the hard RDR-threshold → sigmoid lookup for the Layer 3 Greek limit scaler with a continuous, probability-weighted signal $M(x) = P(S_t = \text{dealer\_stabilized} | O_{1:t}) \times M_{\max}$.

**Output**: Populates the `hmm_state` block in the [GEX Regime Report JSON Schema](../entities/gex-regime-report-json-schema.md): `state_label`, `state_semantics`, `posterior_probs`, `transition_row`, `regime_persistence_expected_bars`, `model_fit_date`.

**Feature vector** (6 dimensions, all stationary):

| Feature | Source | Requires |
|---|---|---|
| `daily_log_return` | Closing price history | Polygon.io or ThetaData |
| `intraday_parkinson_vol` | Intraday high/low: `(ln H − ln L)² / 4 ln 2` | Intraday OHLC data |
| `vrp_trend` | IV² − HV² direction | `vendor_iv` / `solved_iv` + historical HV |
| `near_expiry_state` | Near-Expiry HMM (Tool 4): 0=`pinning`, 1=`mean_reverting`, 2=`gamma_squeeze` | Tool 4 output |
| `iv_hv_skew` | IV skew − HV skew | `vol_surface.py` + historical HV |
| `horizon_spread_delta` | ΔIHS = ERP₁₈₀ − ERP₃₀ | Tool 2 output |

**Training**: `hmmlearn.GaussianHMM`, $K = 3$ states (canonical labels: `dealer_stabilized`, `transitional`, `gamma_accelerating`), Baum-Welch EM on 252-day rolling window. See [Baum-Welch algorithm gap](gap-analysis-2026-05-20.md#gap-1a--baum-welch-algorithmmd).

**Inference**: Forward algorithm intraday (no refit) → `posterior_probs[k]` per state. Viterbi decoding → `state_label`.

**Refit schedule**:
- Nightly EOD: Baum-Welch on rolling 252-day feature matrix; update $A$, $\mu_k$, $\Sigma_k$; re-label states by ascending realized vol of $\mu_k$
- Intraday: forward-pass only using that morning's fitted parameters
- Monthly: AIC/BIC K-selection on prior 6-month holdout

**Minimum data requirement**: 30 trading days before first valid signal (Baum-Welch estimation minimum). Tool 4 (Near-Expiry HMM) must be live and accumulating `near_expiry_state` observations before Tool 3 training can begin. No dependency on Tool 1.

**Existing partial implementation**: None. `hmmlearn` is available as a dependency ([hmmlearn entity](../entities/hmmlearn.md)). Tool 3 is a **Phase 1 dependency** on Tool 4 (Near-Expiry HMM provides `near_expiry_state`) and Tool 2 (BKM module provides `horizon_spread_delta`). No dependency on Tool 1.

**Parallelization**: Baum-Welch on 252 days × 6 features is fast (seconds on a single core). No Ray distribution needed for Tool 3 itself.

**Relevant vault docs**: [HMM Approaches in Options Pricing and Agent Architecture](hmm-estimates-of-probability-from-option-prices.md), [HMM in Finance — Latent Regime Engine](../concepts/hidden-markov-model-hmm-in-finance.md), [GEX Regime Report Schema](../entities/gex-regime-report-json-schema.md), [Dynamic Portfolio Greek Limits](../concepts/dynamic-portfolio-greek-limits.md), [hmmlearn](../entities/hmmlearn.md)

---

## Tool 4: Near-Expiry HMM (7DTE → 1DTE)

**Purpose**: Classify the intraday microstructure regime during the final week of each expiration cycle for SPX/SPY. Runs independently of Tool 1, 2, and 3. Serves two roles simultaneously: (1) standalone MVP signal for DTE selection and position management, and (2) upstream training feature (`near_expiry_state`) fed into Tool 3's macro HMM feature vector.

**Why custom**: No vendor provides a latent-state classifier keyed specifically to the 7DTE→1DTE gamma-dominated microstructure. Requires DTE-aligned per-expiration training sequences and VIX-stratified models not available in off-the-shelf HMM libraries without custom data assembly.

**Output schema** (`near_expiry_hmm_state` block in GEX Regime Report):

```json
"near_expiry_hmm_state": {
  "state_label": "pinning | mean_reverting | gamma_squeeze",
  "state_index": 0,
  "posterior_probs": [0.72, 0.18, 0.10],
  "vix_tier": "A",
  "dte_remaining": 2,
  "as_of": "2026-05-20T14:35:00Z"
}
```

**States**:

| State | Index | Microstructure Interpretation |
|---|---|---|
| `pinning` | 0 | Spot gravitating toward high-OI strike; dealer hedging suppresses realized vol |
| `mean_reverting` | 1 | Intraday mean reversion; GEX positive; no dominant pin |
| `gamma_squeeze` | 2 | Spot escaping gamma wall; realized vol expanding; dealer delta-hedge creates feedback loop |

**Feature vector** (7 dimensions):

| Feature | Source | Notes |
|---|---|---|
| `gex_concentration_at_expiry` | dxFeed (live chain) | GEX mass within 1% of spot from target expiry only |
| `spot_to_gamma_wall_distance` | dxFeed (live chain) | \|spot − gamma wall strike\| / spot |
| `atm_gamma_velocity` | dxFeed (live chain) | dΓ/dt of ATM strike; see [ATM Gamma Velocity](../concepts/atm-gamma-velocity.md) |
| `oi_concentration_ratio` | dxFeed (live chain) | Max-strike OI / total chain OI for target expiry |
| `realized_vol_intraday` | ThetaData VALUE (1-min bars) | Parkinson estimator on rolling 30-min OHLC |
| `atm_iv_dte_slope` | dxFeed (live chain) | dIV/dDTE at ATM; see [ATM IV DTE Slope](../concepts/atm-iv-dte-slope.md) |
| `call_put_volume_ratio` | dxFeed (live chain) | Rolling 30-min call volume / put volume; see [Call-Put Volume Ratio](../concepts/call-put-volume-ratio.md) |

**Training spec**:
- `hmmlearn.GaussianHMM`, $K = 3$ states
- Training sequences: DTE-aligned per-expiration slices (7DTE open → 1DTE close), each treated as one observation sequence
- **VIX stratification**: Tier A (VIX < 20), Tier B (VIX ≥ 20) — separate model parameters per tier; tier selected at inference time
- Baum-Welch EM on rolling 252-day (≈ 52 expiration cycles) history
- Nightly refit; intraday forward-pass only
- Minimum data: 30 trading days (≈ 6 expiration cycles) per VIX tier

**Data sources**: ThetaData VALUE (1-min OHLC for `realized_vol_intraday`) + dxFeed live options chain (all other features). No ThetaData STANDARD required. No dependency on Tool 1, 2, or 3.

**Update cadence**: Feature vector computed every 5 minutes during 7DTE→1DTE windows. Forward-pass inference → updated `near_expiry_hmm_state` block in GEX Regime Report.

**Dual role**:
- **Inner gate** (standalone MVP): DTE selection rule — enter short-gamma only when `state_label == "pinning"`; exit or tighten stops when `state_label == "gamma_squeeze"`. Actionable without Tool 3.
- **Tool 3 input feature**: `near_expiry_state` (integer index 0/1/2) replaces `gex_z_score` in Tool 3's feature vector. Eliminates Tool 3's dependency on deferred Tool 1.

**Build prompt**: Implementation specification at `plan-nearExpiryHmm7dteTo1dte.prompt.md` (Claude Code prompt).

**Relevant vault docs**: [HMM in Finance — Latent Regime Engine](../concepts/hidden-markov-model-hmm-in-finance.md), [HMM Approaches in Options Pricing and Agent Architecture](hmm-estimates-of-probability-from-option-prices.md), [GEX Regime Report Schema](../entities/gex-regime-report-json-schema.md), [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md), [ThetaData](../entities/thetadata.md), [ATM Gamma Velocity](../concepts/atm-gamma-velocity.md), [ATM IV DTE Slope](../concepts/atm-iv-dte-slope.md), [Call-Put Volume Ratio](../concepts/call-put-volume-ratio.md)

---

## Non-Custom Infrastructure (Subscriptions / Off-the-Shelf)

| Component | Type | Provider / Library | Used By | Tier / Cost |
|---|---|---|---|---|
| Options chain (live) | Existing tool + Subscription | [dxFeed Data Engine](../entities/tastytrade-dxfeed-data-engine.md) (live); [ThetaData](../entities/thetadata.md) (historical + constituents) | Tool 1, Tool 2, Tool 3, Greeks Analyst, Vol Analyst | dxFeed: Tastytrade account; ThetaData: VALUE min |
| Underlying price, volume | Subscription | [Polygon.io](../entities/polygon-io.md) | Technical Analyst, delta hedge triggers, Tool 3 log returns | Varies |
| News, earnings calendar | Subscription | Financial news APIs | News/Catalyst Analyst | Varies |
| Live positions, P&L, margin | Broker API | [Interactive Brokers TWS API](../entities/interactive-brokers-api.md) | Portfolio Manager, Risk Team, Execution Agent | Included with account |
| HMM training library | Open source | [hmmlearn](../entities/hmmlearn.md) | Tool 3, Tool 4 | Free |
| Distributed compute | Open source | [Ray](../entities/ray.md) | Tool 1 (GEX parallelization — deferred) | Free |
| Hardware | Owned | [AMD Threadripper 3990X](../entities/amd-ryzen-threadripper-3990x.md) | All local compute | Owned |

> **FlashAlpha removed**: Since Tool 1 computes GEX Z-scores, the Internal GEX Index, and the RDR from raw ThetaData options chain data, regime classification is a trivial rules-based output of the same pipeline — no black-box vendor labels needed. FlashAlpha’s only remaining value is cross-validation during Tool 1 development (one-time, not a permanent dependency).

---

## Build Sequencing

Build order is determined by dependency structure and evidence quality. Steps 1 and 2 are independent and can proceed in parallel.

| Step | Tool | Prerequisite Data / Tools | Unlocks |
|---|---|---|---|
| 1 | **Tool 4** — Near-Expiry HMM (7DTE→1DTE) | ThetaData VALUE + dxFeed (both already available) | MVP inner-gate signal; `near_expiry_state` observation stream for Tool 3 |
| 2 | **Tool 2** — Horizon Spread / BKM module | dxFeed Data Engine (exists); only BKM integration function missing | `horizon_spread_delta` for Tool 3 |
| 3 | **Tool 3** — Macro HMM Latent Regime Engine | Tool 4 (`near_expiry_state`) + Tool 2 (`horizon_spread_delta`) both live | Greek limit scaler M(x); outer risk gate for full agent loop |
| 4 | **Tool 1** — Constituent GEX / RDR Scanner | ThetaData STANDARD + Ray parallelization + empirical validation | Deferred to Phase 2 |

**Open research questions**:
- Q9 Sub-Qs 3–5: How horizon spread conflicts with GEX signals are resolved — affects how Tool 2 output is weighted in the agent debate
- Q6: Portfolio scope (SPY-only vs. constituent basket) — affects the constituent universe eventually fed into Tool 1

**Relevant research agenda questions**: [Q6](research-agenda-options-maopm.md#q6), [Q9](research-agenda-options-maopm.md#q9)
