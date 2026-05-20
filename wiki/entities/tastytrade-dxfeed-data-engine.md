---
tags: ["entity", "data-pipeline", "options-data", "tastytrade", "dxfeed", "gex", "implied-volatility", "maopm", "tooling"]
created: 2026-05-20
reviewed: 2026-05-20
source_origin: "code-review-2026-05-20"
---
# Tastytrade / dxFeed Data Engine

An existing Python toolchain (`data_engine.py`, `vol_solver.py`, `vol_surface.py`) built on Tastytrade's OpenAPI dxFeed websocket. It constitutes the **partial live-data implementation** of MAOPM Tool 2 (Horizon Spread Pipeline) and the index-level portion of Tool 1 (GEX Regime Divergence Engine).

**Repository**: `Tastytrade-API-GEX-Volatility-Surface-Dashboard`

---

## Architecture

```
DataEngine.fetch_chain_snapshot()       → ChainSnapshot
  └── enrich_contract_snapshot()        → + solved_iv, solved_delta, time_to_expiry_years
        └── aggregate_surface_data()    → OTM-blend surface (expiration × strike)
```

### Data source: dxFeed websocket

- **Endpoint**: `wss://tasty-openapi-ws.dxfeed.com/realtime`
- **Protocol**: Subscribe to `Quote`, `Trade`, `Greeks`, `Summary` events per contract symbol
- **Authentication**: Tastytrade OpenAPI quote token
- **Latency**: Streaming real-time; one `ChainSnapshot` takes `wait_seconds` (default 15s) to collect events
- **Historical data**: None. Live-only. No replay capability.

### `data_engine.py` — Chain Snapshot

Fetches and normalizes one options chain for one underlying × one expiration.

Per-contract fields produced:

| Field | Source event | Notes |
|---|---|---|
| `bid`, `ask`, `mid` | `Quote` | `mid = (bid + ask) / 2` |
| `last`, `volume` | `Trade` | `volume` = day volume |
| `gamma`, `delta` | `Greeks` | Pre-computed by dxFeed (BSM-derived) |
| `vendor_iv` | `Greeks` (`volatility`) | BSM IV from dxFeed; opaque model |
| `oi` | `Summary` (`openInterest`) | Open interest |
| `underlying_price` | `Trade`/`Quote` midpoint | Fetched separately via `fetch_underlying_price()` |

Strike range generation: `center_strike ± (strikes_up/down × increment)` around the current underlying price. Caller must set these wide enough to cover the full OTM wing for BKM integration.

### `vol_solver.py` — BSM IV Solver

Solves implied volatility per contract from market price. Primary: `py_vollib` (C-backed); fallback: `scipy.optimize.brentq`.

| Field added | Description |
|---|---|
| `solved_iv` | Own BSM solve from `mid` (or `last`) price |
| `solved_delta` | BSM delta at `solved_iv` |
| `time_to_expiry_years` | Seconds to midnight after expiry ÷ (365 × 86400) |
| `solver_status` | `ok:py_vollib` / `ok:scipy_fallback` / `error:*` |

**Two IVs per contract** after enrichment: `vendor_iv` (dxFeed) and `solved_iv` (own solve). Both are BSM-derived — neither is model-free variance. For BKM integration use raw `mid` prices, not either IV.

**Known precision issue**: `time_to_expiry_years` sets expiry at midnight the day after the expiration date. Correct for SPY (PM-settled). Slightly wrong for SPX (AM-settled, expires at open). Negligible at 30/180-day tenors; material for 0DTE Greek accuracy.

**Dividend yield**: Defaults to `0.0` if not passed. SPY carries ~1.3% yield — must be passed explicitly as `dividend_yield` parameter. Without it, `solved_iv` for SPY is systematically biased upward; `vendor_iv` will not share this bias.

### `vol_surface.py` — OTM-Blend Surface

Aggregates per-contract IV into an expiration × strike surface.

**Blending rule**: K < spot → put IV; K > spot → call IV; ATM → (call_iv + put_iv) / 2. Correct market convention — OTM legs are more liquid.

Output columns: `expiration`, `dte`, `strike`, `call_iv`, `put_iv`, `surface_iv`, `expiration_date`, `expiration_label`.

---

## MAOPM Integration Coverage

### Tool 1 (GEX Regime Divergence Engine)

| Requirement | Status |
|---|---|
| Per-contract `gamma` and `oi` | ✅ Available from `ChainSnapshot` |
| Index GEX (SPX/SPY): `Σ(gamma × oi × 100 × S²)` across expirations | ✅ Computable from `ChainSnapshot` |
| `gamma_flip_level`, `above_gamma_flip` | ✅ Computable from index GEX profile |
| GEX Z-score (30-day rolling normalization) | ❌ Requires historical GEX — live-only |
| Internal GEX Index (avg Z-score across 500 constituents) | ❌ 500-stock bulk fetch not architecturally feasible with streaming websocket |
| Regime Divergence Ratio (RDR) | ❌ Requires constituent GEX |

**Assessment**: Implements index-level raw GEX and gamma flip. The MAOPM-specific metrics (Z-score, RDR, Internal GEX Index) require [ThetaData](thetadata.md) for constituent chains and historical normalization.

### Tool 2 (Horizon Spread Pipeline)

| Requirement | Status |
|---|---|
| Per-contract `mid` prices (OTM chain) | ✅ Available from `ChainSnapshot` |
| Multiple expirations (two bracketing 30 DTE, two bracketing 180 DTE) | ✅ Call `fetch_chain_snapshot` four times per cycle |
| BKM integration: `V_Q(T) = 2 Σ [mid(K) / K² × ΔK × exp(r×T)]` | ❌ Not yet implemented — **this is the missing module** |
| Constant-maturity time interpolation | ❌ Not yet implemented |
| ΔIHS = ERP₁₈₀ − ERP₃₀ | ❌ Downstream of BKM |

**Assessment**: All data inputs for Tool 2 are available from the engine. A `bkm_integrate()` function operating on `ChainSnapshot.contracts` (filtered to OTM, using `mid` column) is the single missing piece. See [Horizon Spread Pipeline spec](../research/tooling-requirements-maopm.md#tool-2-horizon-spread-pipeline).

### Vol Surface Summary Schema fields

| Schema field | Status |
|---|---|
| `term_structure[].atm_iv` | ✅ Filter `surface_iv` at ATM strike per expiration |
| `vol_skew.put_wing_iv` / `call_wing_iv` | ✅ Filter by `solved_delta` ≈ ±0.25 |
| `vol_skew.skew_direction` | ✅ Derived from put_wing − call_wing |
| `smile_curvature` | ✅ OTM avg − ATM from `surface_iv` |
| `term_structure.horizon_spread` | ❌ Requires BKM module |
| `vrp` (IV² − HV²) | ⚠️ IV side ready; HV side requires historical data |

### HMM Feature Vector coverage

| Feature | Status |
|---|---|
| `daily_log_return` | ❌ Needs historical closing prices (Polygon.io or ThetaData) |
| `intraday_parkinson_vol` | ❌ Needs intraday high/low — not in dxFeed `Greeks`/`Quote` events |
| `vrp_trend` | ⚠️ IV side ready; HV baseline needs historical data |
| `gex_z_score` | ❌ Requires 30-day historical GEX rolling window |
| `iv_hv_skew` | ⚠️ IV skew ready from `vol_surface`; HV side needs history |
| `horizon_spread_delta` | ❌ Requires BKM module (data inputs present) |

---

## Data Boundary

| Data type | This engine | ThetaData required |
|---|---|---|
| Real-time per-contract Greeks (live trading / paper trading) | ✅ | Optional (redundant) |
| Real-time IV surface (live) | ✅ | Optional (redundant) |
| Historical options chains (HMM training, Z-score normalization) | ❌ | ✅ Required |
| Constituent-level GEX (500 stocks) | ❌ | ✅ Required |
| Realized volatility (close-to-close) | ❌ | ✅ or Polygon.io |

---

## Execution Broker Boundary

This engine is a **market data tool only**. It does not submit orders. The MAOPM architecture currently specifies [Interactive Brokers TWS API](interactive-brokers-api.md) for execution. If the user intends to execute on Tastytrade, the execution entity reference in the architecture must be updated accordingly — Tastytrade's order entry API is separate from the dxFeed data websocket documented here.

---

## Related

- [Tooling Requirements MAOPM](../research/tooling-requirements-maopm.md) — Tool 1, Tool 2, Tool 3 specs
- [GEX Regime Report JSON Schema](gex-regime-report-json-schema.md) — outputs Tool 1 populates
- [Vol Surface Summary JSON Schema](vol-surface-summary-json-schema.md) — outputs Tool 2 populates
- [HMM Approaches in Options Pricing and Agent Architecture](../research/hmm-estimates-of-probability-from-option-prices.md) — HMM feature vector context
- [Bakshi-Kapadia-Madan Formulation](../concepts/bakshi-kapadia-madan-formulation.md) — BKM integration needed for Tool 2 completion
- [Constant-Maturity Interpolation](../concepts/constant-maturity-interpolation.md) — tenor interpolation step
- [ThetaData](thetadata.md) — required for historical data and constituent GEX
</content>
</invoke>