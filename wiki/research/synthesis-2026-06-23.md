---
tags: ["synthesis", "maopm", "hmm", "regime-detection", "backtesting", "dual-engine", "infrastructure"]
created: 2026-06-23
reviewed: false
source_origin: "level1-analysis"
---
# Vault Synthesis — 2026-06-23

> This note updates the vault compass established in [synthesis-2026-05-17](synthesis-2026-05-17.md). That note identified five clusters and six non-obvious cross-cluster connections. This update focuses on what has materially changed since then: the vault has made a decisive shift from *conceptual design* to *operational specification*. Read the May synthesis first for cluster foundations; this note focuses on structural evolutions and a new sixth cluster.

---

## What Changed Since 2026-05-17

The May synthesis identified its most important unresolved issue as the gap between Signal Family A (GEX/microstructure) and Signal Family B (vol surface/option-implied macro), with no bridge note or agent role specifying how they fuse before reaching the Strategy Research Team. Since then, the vault has added:

1. **A concrete signal fusion blueprint** — [MAOPM Architecture: Horizon Spread & GEX Fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md): a hierarchical gating network where the Macro Regime Agent (Horizon Spread) sets parametric constraints for Microstructure Execution Agents (GEX/RDR). The fusion is not symmetric averaging — macro context gates micro execution parameters.

2. **A split of the single RDR into two temporal engines** — [Dual-Engine Temporal Risk Architecture](../concepts/dual-engine-temporal-risk-architecture.md): `RDR_Tactical` (0DTE GEX only) governs intraday Delta buffers; `RDR_Strategic` (>7DTE duration-weighted GEX) governs baseline Vega limits and capital capacity. Gamma uses both via $M_\Gamma = M(\text{RDR}_\text{Tactical}) \times M(\text{RDR}_\text{Strategic})$. This resolves the documented contamination of structural signals by 0DTE volume.

3. **An operational near-expiry HMM** — [Near-Expiry HMM for SPX/SPY 7DTE-1DTE](../concepts/near-expiry-hmm-options-dynamics.md): a standalone, deployable regime classifier with a defined repo structure (`hmm/`, `data/`, `scripts/`), ThetaData/dxFeed data sources, and `NearExpiryHMMState` output class. This is distinct from the macro 6-feature MAOPM HMM — they target different time horizons and feature vectors.

4. **A complete backtesting pipeline** — [Systematic Options Backtesting Pipeline](../concepts/systematic-options-backtesting-pipeline.md) and [Backtesting Best Practices](../research/backtesting-best-practices-for-short-duration-options.md): an end-to-end specification covering data ingestion, feature engineering, HMM regime tagging, pre-trade state matrix construction, and event-driven strategy execution. This closes the largest structural gap in Q4 of the [Research Agenda](research-agenda-options-maopm.md).

5. **A concrete implementation of the risk scaling engine** — [Regime Risk Scaling Engine](../concepts/regime-risk-scaling-engine.md) with the corresponding [RegimeRiskScaler class](../entities/regimeriskscaler-class.md), implementing the bi-symmetric sigmoid, absolute GEX filter, and VVIX panic override as executable code.

---

## Cluster 1–5: Status Updates

**Cluster 1 (Infrastructure)**: Unchanged in design; reinforced by the backtesting pipeline noting nanosecond-timestamped data alignment as a hard requirement. ThetaData remains the primary data source for historical Greeks. The Near-Expiry HMM repo structure (`scripts/pull_historical.py`) is the first concrete artifact that operationalizes the data fetch.

**Cluster 2 (Market Mechanics)**: The Dual-Engine Temporal Risk Architecture *supersedes* the single-RDR framework. The two-signal-family gap is *partially* closed: the MAOPM fusion blueprint describes the gating network, but the Near-Expiry HMM introduces a *third* temporal signal layer (near-expiry microstructure regime) that is not yet placed in the fusion hierarchy. See Cross-Cluster Connection 7 (below).

**Cluster 3 (Strategy Selection)**: The [Structural Triad](../concepts/structural-triad-systematic-options-trading.md) formalizes the pre-trade decision surface as HMM state × GEX Profile × IV-HV Skew. However, the triad note is currently a stub ("Further research is needed on weighting and interaction"). The strategy matrix and triad are both documented but their interaction rules remain undefined.

**Cluster 4 (Agent Architecture)**: [RegimeRiskScaler](../entities/regimeriskscaler-class.md) is the first concrete software entity that bridges agent architecture to code. The `DIVERGENCE_STRATEGY_MODE` and `NEGATIVE_GEX_RISK_REDUCTION` states in the engine map directly to the MAOPM state machine interrupt paths.

**Cluster 5 (Performance & Evaluation)**: Partially addressed. Backtesting pipeline specifies P&L logging and equity curve generation. Options-native baselines and theta-adjusted performance metrics remain undocumented (Q8 in research agenda still open).

---

## Cluster 6: Near-Expiry Microstructure Engine (New)

**Core files**: [Near-Expiry HMM](../concepts/near-expiry-hmm-options-dynamics.md), [Intraday GEX Schedule](../concepts/intraday_gex_schedule.md), [Parkinson Volatility Estimator](../concepts/parkinson-volatility-estimator.md), [Baum-Welch Algorithm](../concepts/baum-welch-algorithm.md), [Systematic Options Trading Pipeline 1DTE-7DTE](../concepts/systematic-options-trading-pipeline-1dte-7dte.md)

This cluster is a concrete, deployable subsystem targeting the 7DTE-1DTE window — the most structurally complex zone of an options position lifecycle, where gamma dominates, pin risk emerges, and delta management becomes intraday rather than periodic.

**Internal logic**:
1. 1-minute OHLC data (ThetaData/dxFeed) → Parkinson vol → feature vector `[log_return, parkinson_vol, vrp_trend, gex_z_score]`
2. Baum-Welch training on rolling anchored window → GaussianHMM with K=3 states
3. Viterbi decoding → `NearExpiryHMMState`: `{state_id, state_label, posterior_probs}`
4. State labels: {`pinning`, `mean_reverting`, `gamma_squeeze`} sorted by emission mean on realized vol dimension
5. Pre-trade state matrix joins GEX profile + HMM state + VRP matrix by timestamp
6. Intraday GEX schedule gates calculation timing (specific intervals tied to market open, auction, MOC window)

**What makes it different from the MAOPM macro HMM**:

| Dimension | Near-Expiry HMM (Cluster 6) | MAOPM Macro HMM |
|---|---|---|
| **Target horizon** | 7DTE to 1DTE expiry window | Multi-week macro regime |
| **Feature vector** | 4 features: returns, Parkinson vol, VRP, GEX Z-score | 6 features: + IV/HV skew, horizon spread delta |
| **Regime semantics** | Microstructure: pinning, mean-reversion, gamma-squeeze | Macro: low-vol, transitional, high-vol |
| **Update frequency** | Hourly or triggered by GEX flip crossing | Nightly Baum-Welch; intraday forward-pass |
| **Output class** | `NearExpiryHMMState` | `hmm_state` block in GEX Regime Report JSON |
| **Primary use** | Intraday execution gating, delta buffer sizing | Strategy selection, long/short-vol debate prior |

These are complementary, not competing. The near-expiry HMM provides the fine-grained expiry microstructure classification needed for execution; the macro HMM provides the multi-week context needed for position initiation. **No integration note exists** — this is the vault's primary open architectural gap (see gap-analysis-2026-06-23).

---

## Non-Obvious Cross-Cluster Connections (Updates)

The six connections in the May synthesis remain valid. Three new ones are now visible:

### 7. Dual-Engine Temporal Split ↔ Two-HMM Architecture

The Dual-Engine Temporal Risk Architecture defines its boundary at 0DTE (Tactical) vs. >7DTE (Strategic). The Near-Expiry HMM operates in the 7DTE-1DTE window — precisely the boundary zone between the two engines. The Tactical Engine's `RDR_Tactical` is the strongest GEX signal inside the near-expiry HMM's operating window. The implication: the near-expiry HMM's `gex_z_score` emission dimension should be sourced from `RDR_Tactical` (0DTE-filtered GEX), not the full-chain `RDR_Strategic`. No vault note makes this connection explicit.

### 8. Intraday GEX Schedule ↔ Near-Expiry HMM Update Cadence

The [Intraday GEX Schedule](../concepts/intraday_gex_schedule.md) defines calculation intervals aligned with market open, VWAP windows, MOC auction, and final 30-minute session. The near-expiry HMM's inference loop runs at hourly or triggered intervals but its feature vector depends on Parkinson vol computed from 1-minute OHLC bars from session open. These two cadences must synchronize: GEX recalculation must precede or coincide with HMM forward pass. The pre-trade state matrix timestamp alignment requirement (nanosecond UTC) propagates to this synchronization problem.

### 9. RegimeRiskScaler `DIVERGENCE_STRATEGY_MODE` ↔ Near-Expiry HMM `gamma_squeeze` State

When the [RegimeRiskScaler](../entities/regimeriskscaler-class.md) enters `DIVERGENCE_STRATEGY_MODE` (VVIX >3σ or RDR beyond band), it contracts Gamma/Vega by 95% and expands Delta buffers. The near-expiry HMM's `gamma_squeeze` state represents the intraday manifestation of the same underlying dynamic: dealers short gamma, price acceleration, expanding realized vol. These two risk signals should trigger the same fast-path management action (close or hedge short gamma positions), but they live in different sub-systems with no shared alert queue. Connecting them — either by making `gamma_squeeze` state an input to the RegimeRiskScaler, or by routing both to the same unified alert queue — would close the largest remaining management-path gap.

---

## The Vault's Current State: Where Design Ends and Building Begins

As of 2026-06-23, the vault has crossed a threshold. The architecture is sufficiently specified that the next phase of knowledge acquisition is empirical — validation against historical data — rather than conceptual design. Specifically:

1. The Near-Expiry HMM repo structure (`hmm/train.py`, `hmm/inference.py`, `hmm/validate.py`) is implementation-ready. The first knowledge gain is running the backtest.
2. Tool 3 (MAOPM macro HMM Latent Regime Engine) is architecturally described but has no build specification — this is the critical remaining design gap.
3. The [Structural Triad](../concepts/structural-triad-systematic-options-trading.md) is the last underdeveloped foundational concept. Without weighting rules and conflict resolution, the pre-trade state matrix joins data but doesn't resolve conflicting signals.
4. The backtesting pipeline spec is complete. Running it produces the first observable result: **does the structural triad (HMM × GEX × VRP) improve strategy selection vs. GEX-only or HMM-only rules?**
