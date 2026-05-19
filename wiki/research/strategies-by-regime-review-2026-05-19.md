---
tags: ["regime-detection", "options-trading", "gex", "implied-volatility", "strategy-selection", "review"]
created: 2026-05-19
reviewed: false
source_origin: "vault-synthesis"
---
# Strategies by Regime: Research Review — 2026-05-19

> Full review of the vault's research on strategy selection across different market regimes. Synthesizes [Cluster 2](synthesis-2026-05-17.md) (Market Mechanics) and [Cluster 3](synthesis-2026-05-17.md) (Strategy Selection) from the vault synthesis. Gaps reference [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md).

---

## Regime Framework: Two Independent Signal Families

The vault identifies two distinct regime-detection mechanisms that must be read together:

| | Signal Family A — GEX / Microstructure | Signal Family B — Option-Implied Macro |
|---|---|---|
| **What it measures** | Current dealer hedging behavior and its price feedback | Aggregate market expectations embedded in option prices |
| **Time horizon** | Real-time / intraday | Forward-looking (days to months ahead) |
| **Key metrics** | GEX level, Gamma Flip Zone, Regime Divergence Ratio | IVR/IVP, vol surface skew, term structure, horizon spread |
| **Leading edge** | Identifies *current* stability vs. instability | Detected COVID-19 regime shift in Dec 2019, 3 months early (Lai 2022) |

**Critical gap** (Gap 1.3): these two families are never formally fused in the vault. No bridge note or agent role specifies *how* they are combined before strategy selection.

---

## Strategy Selection: The 2D Decision Matrix

Strategy selection operates on a two-dimensional surface of **IVR tier × GEX regime**:

| | Low IVR (< 30) | Moderate IVR (30–50) | High IVR (> 50) |
|---|---|---|---|
| **Coherent / Positive GEX** | Calendars, debit spreads, LEAPS | Defined-risk spreads, diagonals | Iron condors, credit spreads, CSPs |
| **Divergent GEX (Ratio > 2.0)** | Fragility Shorts on weak components | Dispersion trades | Dispersion trades, term structure catch-up |
| **Divergent GEX (Ratio < 0.5)** | Long vol on fragile index | Gamma Flip mean reversion | Gamma Flip mean reversion |

---

## Strategies by Regime

### 1. Positive GEX (Coherent / Stable) — Mean-Reversion Regime

Dealers are long gamma → they buy dips and sell rallies → price is stabilized. Preferred strategies are **premium-selling** (theta capture):

- Iron condors, credit spreads, cash-secured puts at High IVR
- Calendars and diagonals at Low–Moderate IVR (defined risk, long-vol lean)

**Source**: [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [Options Strategies](../concepts/options-strategies.md)

---

### 2. Negative GEX (Momentum / Volatile) — Trend Regime

Dealers are short gamma → they sell dips and buy rallies → moves accelerate. Premium selling is dangerous here.

- **Long vol** (buying options or straddles) on the index
- **[Gamma Flip Mean Reversion](../concepts/gamma-flip-mean-reversion-strategy.md)**: when individual stocks flip below their Gamma Flip Zone while the index stays positive-GEX, stocks often overshoot then snap back. Enter longs at the Gamma Wall (major put open interest concentration).

---

### 3. Divergent GEX — Index Stable, Components Fragile (Ratio > 2.0)

The surface is calm but foundations are cracking. Two strategies:

- **[Fragility Short](../concepts/fragility-short-strategy.md)**: Buy OTM put spreads on low/negative-GEX individual stocks (especially Mag-7), hold neutral/long the index. The fragile components "slip" faster in a sell-off while the index has GEX support.
- **[Dispersion Trade](../concepts/dispersion-trade-strategy.md)**: Sell index straddles (low index vol), buy straddles on the highest-divergence individual stocks (high component vol). Profits if index stays flat while components move wildly — arbitrages the implied correlation premium.

**Source**: [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)

---

### 4. Term Structure Divergence — 0DTE Positive, 45DTE Negative

Daily pinning masks structural weakness building in medium-term positioning.

- **[Term Structure Catch-Up (Calendar Spread)](../concepts/term-structure-catch-up-strategy.md)**: Sell 0DTE (overpriced by pinning effect, rapid theta decay), buy 45DTE (underpriced given structural negative GEX). Profits from short-dated premium collection while holding a cheap long-vol position for the eventual structural break.

This is the only vault concept that explicitly uses multi-expiration GEX signals together.

---

### 5. High-Vol / Crisis Regime (Signal Family B)

When IVR > 50 and the vol surface inverts (short-term IV > long-term IV), the market is pricing immediate stress:

- All short-vol (premium-selling) strategies are suspended
- Long-vol, defined-risk structures only
- The **Horizon Spread** ($HS = \text{ERP}_{180d} - \text{ERP}_{30d}$) going negative is the vault's highest-conviction leading indicator for entering this regime early — it detected COVID-19 three months before GARCH or return-based models

**Source**: [Option-Implied Regimes](../concepts/Option-Implied%20Regimes.md), [Detecting Stock Market Regimes from Option Prices](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md)

---

## Research Gaps Directly Affecting Strategy-Regime Coverage

| Gap | Impact |
|---|---|
| No `option-implied-erp-horizon-spread.md` note | Horizon spread is the best leading regime detector in the vault (Lai 2022) but is orphaned from agent design |
| No fusion mechanism for Signal Family A + B | Strategy selection matrix exists but no agent or note specifies *when* GEX overrides vol surface or vice versa |
| No `vol-crush-exploitation.md` | The event calendar is used for risk avoidance but the symmetric opportunity (sell into pre-event IV expansion) has no formal concept note |
| [`regime-detection.md`](../concepts/regime-detection.md) is thin | Only covers high/low vol and trending/ranging at a surface level; doesn't reference GEX, horizon spread, or the 2D matrix |
| No options-native baselines | Mechanical iron condors, XYLD, VIX-regime switching not in the vault — needed for fair MAOPM evaluation |

**Priority action**: Connect the Lai (2022) horizon spread (physically in the vault at [raw/assets/Detecting stock market regimes from option prices.md](../../raw/assets/Detecting%20stock%20market%20regimes%20from%20option%20prices.md)) into the Vol Analyst agent role and formally specify the fusion logic between Signal Family A (GEX/microstructure) and Signal Family B (option-implied macro).
