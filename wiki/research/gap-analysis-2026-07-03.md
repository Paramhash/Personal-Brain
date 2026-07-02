---
tags: ["gap-analysis", "maopm", "hmm", "option-pricing", "architecture", "wikilinks"]
created: 2026-07-03
reviewed: false
source_origin: "level1-analysis"
---
# Gap Analysis — 2026-07-03

> Updates [gap-analysis-2026-06-23](gap-analysis-2026-06-23.md). One gap closed (AIC/BIC note exists). All other gaps from June 23 remain open. Two new gaps identified: uningested raw source and missing option-pricing architecture notes. Ranked by MAOPM build impact.

---

## Section 1: Gaps CLOSED Since 2026-06-23

### Gap 1.D — AIC/BIC Concept Note: CLOSED

`wiki/concepts/aic_bic_information_criteria.md` exists and is substantive. Covers both criteria with correct formulas, asymptotic properties, and the application context of Lai (2022) regime model selection. **Status: functional; revision-optional.**

### Gap D — MMJD/MMGBM/MS-SV Uningested Source: CLOSED

Ingested at 2026-07-03T07:23:35. Eight concept notes created: [hidden-markov-models-in-option-pricing](../concepts/hidden-markov-models-in-option-pricing.md), [markov-modulated-geometric-brownian-motion](../concepts/markov-modulated-geometric-brownian-motion.md), [markov-modulated-jump-diffusion](../concepts/markov-modulated-jump-diffusion.md), [markov-switching-stochastic-volatility](../concepts/markov-switching-stochastic-volatility.md), [volatility-clustering](../concepts/volatility-clustering.md), [gap-risk](../concepts/gap-risk.md), [volatility-smile](../concepts/volatility-smile.md), [fast-fourier-transform-option-pricing](../concepts/fast-fourier-transform-option-pricing.md). **Residual gap**: No bridge note connecting Near-Expiry HMM posteriors to MMJD state-conditional option prices. See Gap G below.

---

## Section 2: Prior Gaps STILL OPEN (carried from 2026-06-23)

---

### Gap 1.C — Tool 3 Build Specification Missing from `tooling-requirements-maopm.md`

**Status**: Unchanged. `tooling-requirements-maopm.md` documents Tool 1 (GEX Regime Divergence Engine) and Tool 2 (Horizon Spread Pipeline) with full build specifications. The MAOPM macro HMM (Tool 3) — the Layer 3 Greek limit scaler that takes the 6-feature vector `[log_return, parkinson_vol, vrp_trend, gex_z_score, iv_hv_skew, horizon_spread_delta]` — has no entry.

**What must be added to `tooling-requirements-maopm.md`**:
- Feature sources: Tool 1 → GEX Z-score; Tool 2 → ΔIHS; ThetaData → log returns + Parkinson OHLC; local compute → VRP, IV/HV skew differential
- Training: rolling 252-day anchored window, nightly Baum-Welch (hmmlearn), Ray worker
- Inference: forward algorithm only intraday; state persistence across cycles
- Output: `hmm_state` JSON block with state label + posterior probability vector
- Validation events: COVID-19 December 2019 inversion; August 2024 VIX spike
- K-selection: AIC/BIC monthly on 6-month held-out window (mechanism now documented in `aic_bic_information_criteria.md`)
- Minimum burn-in: 60 trading days

**MAOPM impact**: Without this, Tool 3 cannot be scoped, assigned, or built. Tool 3 is the signal that drives dynamic Greek limits Layer 3 — every position sizing decision depends on it.

---

### Gap 2.C — Broken Wikilinks in `usefulness-of-hidden-markov-models-for-short-dated-options-trading.md`

**Status**: Unchanged. The note still contains two dead wikilinks:
- `[[../concepts/options-trading.md]]` — file does not exist
- `[[../concepts/hidden-markov-models.md]]` — file does not exist

Correct targets are `../concepts/hidden-markov-model-hmm-in-finance.md` and `../concepts/hidden-markov-models-for-options-trading.md`.

**Fix**: Two wikilink replacements in the source file. Five-minute task. Unblocks graph traversal through the HMM research cluster.

---

### Gap 3 — Naming Convention Violations (Unchanged)

All snake_case / kebab-case conflicts from June 23 persist:
- `intraday_gex_schedule.md` vs. kebab-case convention (no kebab version exists)
- `gamma_exposure_gex.md` coexists with `gamma-exposure-gex.md` (duplicate; no merge)
- `realized_volatility.md` coexists with `realized-volatility.md` (duplicate; no merge)
- `volatility_risk_premium.md` coexists with `volatility-risk-premium-vrp.md` and `volatility-risk-premium.md` (three entries)

**Priority**: `gamma_exposure_gex.md` is the most-referenced duplicate in the vault. Any backlink to the snake_case version is a graph dead-end.

---

### Gap A — No Integration Note for the Two HMMs

**Status**: Unchanged. `wiki/concepts/hmm-dual-layer-integration.md` does not exist. The two operational HMMs remain undocked:
- Near-Expiry HMM (`near-expiry-hmm-options-dynamics.md`): 4-feature, `NearExpiryHMMState`, 7DTE-1DTE window
- MAOPM Macro HMM (Tool 3): 6-feature, `hmm_state` JSON block, multi-week macro regime

**Unanswered questions** (unchanged from June 23):
1. Which HMM governs fast-path position management (DTE ≤ 7)?
2. Which HMM governs strategy initiation?
3. Conflict rule: near-expiry `gamma_squeeze` + macro `low_vol` — which wins?
4. Does `NearExpiryHMMState` feed as a sub-input to the macro HMM feature vector or are they parallel?

**MAOPM impact**: The GEX/Regime Analyst agent cannot be prompted until this integration note exists. This is the single highest-impact open gap.

---

### Gap B — `dual-engine-temporal-risk-architecture.md` Does Not Reference Near-Expiry HMM

**Status**: Unchanged. Neither file references the other. The `gex_z_score` emission dimension of the Near-Expiry HMM is ambiguous: it should draw from `RDR_Tactical` (0DTE-filtered GEX) per the Dual-Engine architecture, but no note makes this explicit.

**Fix**: Add a cross-reference in `dual-engine-temporal-risk-architecture.md` under Section 2 (Strategic Engine) and in `near-expiry-hmm-options-dynamics.md` under the feature vector definition, stating that `gex_z_score` is sourced from `RDR_Tactical`.

---

### Gap C — `structural-triad-systematic-options-trading.md` Is a Stub

**Status**: Unchanged. The note explicitly states: *"Further research is needed to elaborate on the specific methodologies for combining these elements, the weighting or interaction between them."* The three components (HMM state, GEX profile, IV-HV skew) are named but no decision rules exist.

**What is needed**:
- A 3×N decision matrix: HMM state (3 rows) × GEX regime (coherent/divergent) × VRP sign (+/−)
- Priority rule when two of three signals agree vs. three-way conflict
- Specific strategy assignments per cell (iron condor, calendar, skip/wait)
- Size scaling: full/half/zero position by agreement level

**MAOPM impact**: Without this matrix, the pre-trade state matrix is a data join with no decision output. The backtesting pipeline cannot execute any strategy without it.

---

## Section 3: NEW Gaps

---

### Gap D — Uningested Raw Source: HMM Option-Pricing Architectures

**Location**: `raw/assets/appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md`

**Problem**: This file sits in `raw/assets/` rather than `raw/`. The ingest watcher (`ingest.py`) watches `raw/` only. The file has never been processed into the wiki.

**Content summary**: Covers three architectures — MMGBM (Markov-Modulated GBM), MMJD (Markov-Modulated Jump-Diffusion), and MS-SV (Markov-Switching Stochastic Volatility) — with full SDE dynamics, pricing impact, and short-DTE relevance notes. Also describes the FFT pricing advantage for regime-switching models (Carr-Madan FFT under MMJD). This is the only document in the vault that addresses option *pricing* under HMM regime uncertainty, as distinct from regime *classification*.

**Missing wiki notes** (none of these exist):
- `wiki/concepts/markov-modulated-geometric-brownian-motion.md` (MMGBM)
- `wiki/concepts/markov-modulated-jump-diffusion.md` (MMJD)
- `wiki/concepts/markov-switching-stochastic-volatility.md` (MS-SV)

**MAOPM impact**: The MMJD is the most appropriate pricing model for 1DTE short-premium strategies because it structurally assigns non-zero probability mass to overnight gap events — precisely the tail risk that kills short-gamma positions. If MAOPM ever generates mark-to-model P&L or computes implied fair value for strategy selection, MMJD is the correct architecture. Currently the vault has no bridge between the Near-Expiry HMM state posteriors and any option pricing model.

**Fix**: Move the file to `raw/` and run `ingest.py`, or manually create the three concept notes from the source document.

---

### Gap E — `aic_bic_information_criteria.md` Contains Two Dead Wikilinks

**Location**: `wiki/concepts/aic_bic_information_criteria.md` (Related Concepts section)

**Broken links**:
- `[[../concepts/model_selection.md]]` — file does not exist
- `[[../concepts/maximum_likelihood_estimation.md]]` — file does not exist

These are low-priority dead-ends (related concepts, not load-bearing). However, they follow the same pattern as Gap 2.C and contribute to wikilink graph fragmentation.

**Fix**: Remove or replace these links with existing notes (e.g., `[[../concepts/hidden-markov-model-hmm-in-finance.md]]` as the primary application context for MLE in this vault).

---

### Gap F — `stock-market-regimes.md` Duplicates `Stock Market Regimes.md` (NEW — from 2026-07-03 ingestion)

**Location**: Both in `wiki/concepts/`

**Problem**: The Lai 2022 re-ingestion at 07:23:32 produced `stock-market-regimes.md` (kebab-case). `Stock Market Regimes.md` (Title Case) already existed from the 2026-05-17 ingestion. Two nodes for the same concept — any wikilink using one case will be a dead link from the other, fragmenting the Lai 2022 cluster from the broader market regimes graph.

**Fix**: Read both files, merge content into `stock-market-regimes.md` (kebab-case is the convention), delete `Stock Market Regimes.md`, update any backlinks.

---

### Gap G — No Bridge: Near-Expiry HMM Posteriors → MMJD Pricing (NEW — from 2026-07-03 ingestion)

**Location**: Between `near-expiry-hmm-options-dynamics.md` and `markov-modulated-jump-diffusion.md`

**What is missing**: The Near-Expiry HMM outputs `NearExpiryHMMState` with a `posterior_probs` vector over K=3 states. The [markov-modulated-jump-diffusion](../concepts/markov-modulated-jump-diffusion.md) note defines MMJD but does not describe how to use HMM posteriors to weight state-conditional option prices. The bridge is: `C_MMJD = sum_k pi_k * C_k` where `C_k` is the Black-Scholes-MMJD price in state k and `pi_k` is the posterior. The [carr-madan-spanning-theorem](../concepts/carr-madan-spanning-theorem.md) and [fast-fourier-transform-option-pricing](../concepts/fast-fourier-transform-option-pricing.md) provide the pricing machinery; the HMM output provides the state weights. No note combines them.

**MAOPM impact**: Without this, MAOPM cannot compute mark-to-model P&L for 1DTE positions — it can only use exchange mid-prices. The MMJD pricing layer is required for the Performance & Evaluation cluster (Cluster 5) to generate meaningful mark-to-model attribution.

---

### Gap H — No Bridge: Wonham Filter ↔ MAOPM Near-Expiry HMM (NEW — from 2026-07-03 ingestion)

**Location**: Between `wonham-filter.md` and `near-expiry-hmm-options-dynamics.md`

**What is missing**: The [wonham-filter](../concepts/wonham-filter.md) note links only to the Dai-Zhang-Zhu source and regime-switching model concept. No link to `baum-welch-algorithm.md`, `forward-algorithm.md`, or `near-expiry-hmm-options-dynamics.md`. The key unasked question: could the Wonham filter (continuous-time, SDE-driven regime probability) replace or supplement the near-expiry HMM's hourly forward-pass for real-time inference in the 1DTE window where 60-minute lags are material?

**Recommended fix**: Add a note `wiki/concepts/wonham-filter-vs-hmm-discrete-continuous.md` comparing the two inference mechanisms and specifying which MAOPM sub-system should use each.

---

### Gap I — No Bridge: Double Obstacle Problem ↔ Structural Triad Decision Matrix (NEW — from 2026-07-03 ingestion)

**Location**: Between `double-obstacle-problem-finance.md` and `structural-triad-systematic-options-trading.md`

**What is missing**: The [double-obstacle-problem-finance](../concepts/double-obstacle-problem-finance.md) defines time-dependent threshold curves (upper = enter; lower = exit; between = hold) derived from the conditional regime probability. The [structural triad](../concepts/structural-triad-systematic-options-trading.md) needs exactly this structure — three decision zones over a composite signal — but defines none. The connection is: map the triad's three inputs to a composite probability, then apply the double-obstacle threshold framework to define the entry/exit rules. Transaction cost terms in the double-obstacle formulation directly model MAOPM's bid-ask spread friction.

**MAOPM impact**: Resolves Gap C's stub status without requiring arbitrary weighting choices — the optimal thresholds are derived from the model's cost function, not set ad hoc.

---

### Gap J — `horizon-spread-option-implied-erp.md` and `option-implied-horizon-spread.md` Missing Cross-Links (NEW)

**What is missing**: Both notes cover the Lai (2022) horizon spread but from different angles. [horizon-spread-option-implied-erp](../concepts/horizon-spread-option-implied-erp.md) covers the theoretical definition and regime behavior. [option-implied-horizon-spread](../concepts/option-implied-horizon-spread.md) covers the MAOPM Tool 2 implementation (constant maturity interpolation, data sources). Neither links to the other.

**Fix**: Add a `See Also` or backlink in each note pointing to the other. Two-line edit.

---

### Gap K — Neural Network Loss Landscapes Cluster Is Isolated (NEW)

**Location**: `Neural_Network_Loss_Landscapes.md`, `Filter_Normalization.md`, `Neural_Network_Trainability_and_Generalization.md`

**What is missing**: These three notes have no wikilinks to any other vault cluster. The closest content is `overfitting_in_quantitative_models.md` (quantitative ML overfitting). The connection is thin but real: HMM Baum-Welch maximizes a non-convex log-likelihood; "flat minima generalize better" from the loss landscape literature is relevant to HMM parameter sensitivity. The neural network research note also covers skip connections and generalization — relevant if the user pursues neural architecture design for regime detection.

**Recommended fix**: Add a wikilink from `Neural_Network_Trainability_and_Generalization.md` to `overfitting_in_quantitative_models.md` (and optionally to `hidden-markov-model-hmm-in-finance.md` with a note on non-convex optimization parallels). At minimum prevents permanent orphaning.

---

## Priority Ranking (MAOPM Build Impact)

| Priority | Gap | Impact | Effort |
|---|---|---|---|
| 1 | **Gap A** — Write `hmm-dual-layer-integration.md` | Unblocks GEX/Regime Analyst agent prompt | Medium (architecture reasoning) |
| 2 | **Gap C** — Fill structural triad decision matrix | Unblocks first strategy backtest; double-obstacle formalism now provides theoretical grounding | Medium |
| 3 | **Gap G** — Bridge note: HMM posteriors → MMJD pricing | Enables mark-to-model P&L for 1DTE positions | Medium |
| 4 | **Gap H** — Bridge note: Wonham filter ↔ MAOPM near-expiry HMM | Enables real-time regime inference between hourly HMM updates | Low-medium |
| 5 | **Gap I** — Bridge note: Double obstacle ↔ structural triad decision zones | Provides mathematical grounding for entry/exit thresholds | Low-medium |
| 6 | **Gap 2.C** — Fix broken wikilinks in HMM research note | Unblocks graph traversal; add links to Wonham + MMJD | Trivial |
| 7 | **Gap B** — Cross-reference Dual-Engine ↔ Near-Expiry HMM | Resolves `gex_z_score` source ambiguity | Low |
| 8 | **Gap 1.C** — Write Tool 3 spec in `tooling-requirements-maopm.md` | Unblocks Tool 3 build assignment | Medium-high |
| 9 | **Gap F** — Merge `stock-market-regimes.md` with `Stock Market Regimes.md` | Graph hygiene; prevent backlink fragmentation | Low |
| 10 | **Gap J** — Cross-link `horizon-spread-option-implied-erp.md` and `option-implied-horizon-spread.md` | Graph connectivity | Trivial |
| 11 | **Gap K** — Connect Neural Network Loss Landscapes cluster to rest of vault | Prevents permanent isolation | Low-medium |
| 12 | **Gap E** — Fix dead wikilinks in AIC/BIC note | Graph hygiene | Trivial |
| 13 | **Gap 3** — Merge snake_case duplicate files | Graph hygiene | Low-medium |
