---
tags: ["gap-analysis", "maopm", "hmm", "backtesting", "dual-engine", "architecture"]
created: 2026-06-23
reviewed: false
source_origin: "level1-analysis"
---
# Gap Analysis — 2026-06-23

> Surgical identification of specific named gaps as of 2026-06-23. Covers: (1) gaps closed since [gap-analysis-2026-05-20](gap-analysis-2026-05-20.md), (2) prior gaps still open, (3) new gaps introduced by post-May-20 additions (near-expiry HMM, dual-engine architecture, backtesting pipeline, regime risk scaling engine). Ranked by MAOPM build impact within each section.

---

## Section 1: Gaps CLOSED Since 2026-05-20

**Gap 1.A (Baum-Welch Algorithm)**: CLOSED. `baum-welch-algorithm.md` exists. Covers E-step/M-step in HMM terms and links to `forward-algorithm.md`. Content is minimal but functional — the nightly refit mechanism is documented.

**Gap 1.B (Parkinson Volatility Estimator)**: CLOSED. `parkinson-volatility-estimator.md` exists. Formula is documented ($\hat{\sigma}_\text{park} = \sqrt{\frac{1}{4 \ln 2}(\ln H_t - \ln L_t)^2}$); annualization to `sqrt(252 × 6.5 × 60)` using 1-minute bars is specified. Links to `near-expiry-hmm-options-dynamics.md` as primary use case.

---

## Section 2: Prior Gaps STILL OPEN (from 2026-05-20 analysis)

---

### Gap 1.C — Tool 3 Build Specification Not in Tooling Requirements

**Referenced in**: [gap-analysis-2026-05-20](gap-analysis-2026-05-20.md) (Gap 1.C); [tooling-requirements-maopm.md](tooling-requirements-maopm.md) (Tools 1 and 2 documented, Tool 3 absent)

**Status as of 2026-06-23**: Still missing. `tooling-requirements-maopm.md` documents Tool 1 (GEX Regime Divergence Engine, deferred to Phase 2) and Tool 2 (Horizon Spread Pipeline) in full build specification. The MAOPM macro HMM Latent Regime Engine — now confirmed as the Layer 3 Greek limit scaler $M(x)$ — has no build spec in this document. The Near-Expiry HMM has its own repo structure (`near-expiry-hmm-options-dynamics.md`) but is not the same tool. Tool 3 is the *macro* HMM using the 6-feature vector `[log_return, parkinson_vol, vrp_trend, gex_z_score, iv_hv_skew, horizon_spread_delta]` with nightly Baum-Welch and intraday forward-pass.

**What is missing**: Tool 3 requires in `tooling-requirements-maopm.md`:
- Input feature sources: Tool 1 → GEX Z-score; Tool 2 → ΔIHS; ThetaData → log returns + Parkinson OHLC; local compute → VRP and IV/HV skew differential
- Training: rolling 252-day window, nightly Baum-Welch, Ray worker
- Inference: forward algorithm only intraday; state persistence between cycles
- Output: `hmm_state` JSON block in GEX Regime Report schema
- Validation targets: COVID-19 (Dec 2019 inversion) and Aug 2024 VIX spike as known calibration events
- K-selection: AIC/BIC monthly on 6-month held-out window (see Gap 1.D)
- Minimum data burn-in: 60 trading days before first live signal

**MAOPM impact**: Without this, Tool 3 cannot be scoped or built. Tool 3 drives the Layer 3 signal fusion that the entire dynamic Greek limits architecture depends on.

---

### Gap 1.D — `aic-bic-model-selection.md` Does Not Exist

**Referenced in**: [HMM research note](hmm-estimates-of-probability-from-option-prices.md); [hidden-markov-model-hmm-in-finance.md](../concepts/hidden-markov-model-hmm-in-finance.md)

**Status as of 2026-06-23**: Still missing. No concept note for AIC/BIC exists anywhere in the vault.

**What is missing**: AIC ($-2\ln\hat{L} + 2k$) and BIC ($-2\ln\hat{L} + k\ln n$) as applied to HMM K-selection: which criterion favors parsimony (BIC), how to structure a time-series held-out validation set without look-ahead bias, and the specific consequence for MAOPM (K=2 misses the transitional state that drives regime-transition calendar spread positioning; K=5+ overfits quarterly structural changes).

**MAOPM impact**: Monthly K-selection recalibration is documented as a required step in the MAOPM nightly maintenance schedule. Without this concept note, the recalibration procedure is an instruction without a mechanism.

---

### Gap 2.C — `usefulness-of-hidden-markov-models-for-short-dated-options-trading.md` Has Two Broken Links

**Status as of 2026-06-23**: Still broken. Links to `[[../concepts/options-trading.md]]` and `[[../concepts/hidden-markov-models.md]]` — neither file exists. This note is the only research-layer HMM entry that predates the MAOPM architecture work; it should link to `hidden-markov-model-hmm-in-finance.md` and `hidden-markov-models-for-options-trading.md` instead.

**Fix required**: Update the two broken wikilinks.

---

### Gap 3 — Naming Convention Violations (Partial Improvement)

Most naming duplication from the May analysis persists. New notes added since May-20 have mixed compliance:
- `intraday_gex_schedule.md` uses snake_case (violates kebab-case convention)
- `gamma_exposure_gex.md` still coexists with `gamma-exposure-gex.md` (no merge)
- `realized_volatility.md` still coexists with `realized-volatility.md` (no merge)
- `volatility_risk_premium.md` still coexists with `volatility-risk-premium-vrp.md` and `volatility-risk-premium.md` (three entries)

**Priority action**: `gamma_exposure_gex.md` duplicates the most-referenced file in the vault. Any backlink from the snake_case version is a dead end for graph traversal.

---

## Section 3: NEW Gaps (Introduced by Post-May-20 Additions)

---

### Gap A — No Integration Note for the Two HMMs

**Location**: Between `near-expiry-hmm-options-dynamics.md` (Cluster 6) and `hidden-markov-model-hmm-in-finance.md` (MAOPM macro HMM)

**What is missing**: The vault now contains two distinct, operational HMM specifications:
- **Near-Expiry HMM** (7DTE-1DTE): 4-feature vector, microstructure regime semantics (`pinning`, `mean_reverting`, `gamma_squeeze`), `NearExpiryHMMState` output, repo-deployed
- **MAOPM Macro HMM** (Tool 3): 6-feature vector including horizon spread delta and IV/HV skew, macro regime semantics (`low_vol`, `transitional`, `high_vol`), `hmm_state` block in GEX Regime Report JSON

No bridge note exists that answers:
1. Do these two HMMs feed different agents or the same agent?
2. When they produce conflicting state classifications (near-expiry says `gamma_squeeze`; macro says `low_vol`), which governs?
3. Is the near-expiry HMM's `NearExpiryHMMState` a sub-input to the macro HMM's feature vector, or are they parallel?
4. Does the MAOPM state machine have different transition rules for near-expiry vs. macro HMM signals?

**MAOPM impact**: Without this, an engineer implementing the GEX/Regime Analyst cannot determine which HMM output drives which decision layer. The two HMMs are both described as "regime classifiers" with no integration point.

**Recommended fix**: Create `wiki/concepts/hmm-dual-layer-integration.md` documenting the temporal scope separation, signal routing to agent roles, and conflict resolution rules.

---

### Gap B — Dual-Engine Temporal Architecture Does Not Reference Near-Expiry HMM

**Location**: `dual-engine-temporal-risk-architecture.md` ↔ `near-expiry-hmm-options-dynamics.md`

**What is missing**: The Dual-Engine Temporal Risk Architecture defines the Tactical Engine as monitoring 0DTE GEX and the Strategic Engine as monitoring >7DTE GEX. The Near-Expiry HMM operates on the 7DTE-1DTE window — the exact domain of the Tactical/Strategic boundary. Specifically:
- `RDR_Tactical` = `|Index GEX_≤1DTE| / Σ|Component GEX_≤1DTE|` — should be the `gex_z_score` emission source for the near-expiry HMM
- The near-expiry HMM's `gamma_squeeze` state is the HMM-learned signal equivalent of the Tactical Engine's `RDR_Tactical` spike

Neither file references the other. The Dual-Engine Architecture has no reference to HMM. The Near-Expiry HMM has no reference to Dual-Engine RDR source selection. The two documents describe the same 7DTE-1DTE regime dynamics from different angles without connecting.

**MAOPM impact**: An implementation engineer reading `dual-engine-temporal-risk-architecture.md` cannot discover the Near-Expiry HMM, and vice versa. The `gex_z_score` dimension of the near-expiry HMM is ambiguous — should it use full-chain GEX or 0DTE-filtered GEX?

---

### Gap C — `structural-triad-systematic-options-trading.md` Is a Stub

**Location**: `wiki/concepts/structural-triad-systematic-options-trading.md`

**What is missing**: The note states explicitly: *"The original payload content was empty. Further research is needed to elaborate on the specific methodologies for combining these elements, the weighting or interaction between them."* The structural triad (HMM + GEX Profile + IV-HV Skew) is the pre-trade decision gate in `systematic-options-trading-pipeline-1dte-7dte.md` — it is architectural load-bearing. The stub lists the three components but provides no:
- Weighting or priority rules when components agree vs. conflict
- Specific HMM state × GEX regime × VRP tier decision matrix
- Definition of what constitutes a "confirmed entry signal" vs. a "conditional" or "blocked" entry
- Link to the 2D strategy matrix in [synthesis-2026-05-17](synthesis-2026-05-17.md) or [strategies-by-regime-review-2026-05-19](strategies-by-regime-review-2026-05-19.md)

**MAOPM impact**: The pre-trade state matrix joins three signals by timestamp but the strategy execution engine has no logic for resolving what to do when GEX says "sell premium" (positive RDR, coherent) and HMM says "gamma squeeze" (near-expiry model). Without this, the triad is a data assembly step, not a decision framework.

---

### Gap D — No HMM Validation Framework Concept Note

**Location**: Referenced by `near-expiry-hmm-options-dynamics.md` (`hmm/validate.py`) but no vault concept note covers it

**What is missing**: The near-expiry HMM repo has a `validate.py` placeholder and the tooling note references two calibration events (COVID-19 Dec 2019, Aug 2024 VIX spike). No concept note explains:
- What constitutes a valid out-of-sample HMM regime classification test
- How to evaluate K-stability across rolling walk-forward windows
- Calibration protocol: how to confirm the model would have classified Dec 2019 as `transitional` or `high_vol` three months before the March 2020 crash
- The specific test structure: what held-out window, what performance metric (predictive accuracy? posterior probability in the decisive zone?), what comparison baseline (GARCH? IV rank?)

**Distinct from `aic-bic-model-selection.md`** (Gap 1.D): AIC/BIC covers K-selection during training. This gap covers regime classification accuracy during backtesting — they are different problems.

---

### Gap E — No Slippage / Transaction Cost Model Concept Note

**Location**: Referenced implicitly by both backtesting notes but no dedicated concept exists

**What is missing**: `backtesting-best-practices-for-short-duration-options.md` specifies selling at bid / buying at ask and including commission per contract, but names no specific slippage model. For 1DTE-7DTE short-premium strategies on SPX/SPY, the bid-ask spread is the dominant transaction cost (often $0.50–$2.00 per spread leg on SPX). A concept note is needed covering:
- Proportional bid-ask capture models (e.g., assume fill at bid + 25% of spread)
- Commission structure: per-contract flat ($0.65–$1.00) vs. per-leg with exchange fees
- Market-impact model for larger notional (relevant when GEX-based sizing produces large position counts)
- Which parameter sensitivity test is most informative (half-spread pessimism vs. full-spread pessimism)?

**MAOPM impact**: Backtesting pipeline is complete in structure; without a concrete slippage model, the equity curve results are not comparable across providers or strategy sizes.

---

### Gap F — `option-implied-horizon-spread.md` vs Lai 2022 Performance Statistics

**Location**: `wiki/concepts/option-implied-horizon-spread.md`

**What may be missing**: The May gap analysis (Gap 1.E) called for a note capturing: the two-maturity differential structure, the regime detection superiority statistics (4.6% indecisive-zone probability vs. 34% for GARCH, 16% for historical returns), HS < 0 sign interpretation, and role as HMM emission input. The file now exists. **Need to verify** whether it contains the Lai 2022 performance statistics or only the formula. If the statistics are absent, this note is insufficient as a reference for the Vol Analyst agent's horizon spread narrative generation — the agent needs the benchmarked performance context to reason about signal confidence.

**Recommended action**: Read `option-implied-horizon-spread.md` and confirm it includes: (a) $HS = \text{ERP}_{180} - \text{ERP}_{30}$, (b) Lai 2022 performance statistics, (c) sign interpretation, (d) role as HMM feature dimension.

---

## Section 4: Orphaned and Weakly Connected Notes

### Gap 4.A — `hidden-markov-model-hmm.md` Is a Redundant Stub

Status unchanged from May-20 analysis (Gap 2.D). This note duplicates `hidden-markov-model.md`'s opening paragraph verbatim with no unique content. Every inbound link to it is a missed connection to the authoritative note. Recommend: redirect all wikilinks to `hidden-markov-model.md` and delete the stub.

### Gap 4.B — `structural-triad-systematic-options-trading.md` Links to Wrong HMM Note

The triad stub references `[[./hidden-markov-model-hmm.md|Hidden Markov Model (HMM)]]` — the redundant stub (Gap 4.A above). It should link to `hidden-markov-model-hmm-in-finance.md` (the MAOPM-authoritative note). The GEX Profile link goes to `gamma-exposure-gex-profile.md` — check whether this file exists or should go to `gamma-exposure-gex.md`.

### Gap 4.C — `systematic-options-backtesting-pipeline.md` and `systematic-options-trading-pipeline-1dte-7dte.md` Are Near-Duplicates

Both notes describe the same 4-stage pipeline (Raw Ingestion → Feature Engineering → Latent Regime Engine → Pre-Trade State Matrix → Strategy Execution). `systematic-options-backtesting-pipeline.md` emphasizes historical replay; `systematic-options-trading-pipeline-1dte-7dte.md` emphasizes live trading. The separation is valid architecturally — backtesting and live trading differ in data timestamping, fill simulation, and HMM training mode. However, neither note links to the other, creating apparent duplication without declared distinction.

**Recommended fix**: Add a disambiguation note at the top of each: one sentence stating that the other note covers the same pipeline in the complementary context (live vs. historical).

---

## Summary: Priority Ranking

| Gap | Description | Priority | Effort |
|---|---|---|---|
| **A** | No integration note for two HMMs | Critical | Medium |
| **1.C** | Tool 3 missing from tooling requirements | Critical | Medium |
| **C** | Structural triad stub — no weighting rules | High | Medium |
| **1.D** | AIC/BIC model selection note missing | High | Low |
| **B** | Dual-engine ↔ near-expiry HMM disconnect | High | Low |
| **D** | No HMM validation framework note | Medium | Medium |
| **E** | No slippage/transaction cost model note | Medium | Low |
| **4.A** | `hidden-markov-model-hmm.md` redundant stub | Medium | Low |
| **2.C** | Broken links in HMM usefulness research note | Low | Low |
| **F** | Verify Lai 2022 stats in horizon spread note | Low | Low |
