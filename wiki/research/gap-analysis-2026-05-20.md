---
tags: ["gap-analysis", "multi-agent-systems", "options-trading", "hmm", "knowledge-graph"]
created: 2026-05-20
reviewed: false
source_origin: "level1-analysis"
---
# Gap Analysis: Personal Brain Vault — 2026-05-20

> Surgical identification of specific named gaps introduced or made critical by the HMM integration work completed 2026-05-20. This supersedes the HMM-related portions of [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md); all non-HMM gaps from that note remain open. Each gap is named, located, and ranked by MAOPM impact.

---

## Section 1: New Missing Concept Notes (surfaced by HMM integration)

---

### Gap 1.A — `baum-welch-algorithm.md`

**Referenced in**: [HMM Approaches research note](hmm-estimates-of-probability-from-option-prices.md) (§3 challenges table, §5D refit schedule); [hidden-markov-model-hmm-in-finance.md](../concepts/hidden-markov-model-hmm-in-finance.md) (refit schedule); [hmmlearn entity](../entities/hmmlearn.md) ("implements the Baum-Welch algorithm"); [viterbi-algorithm.md](../concepts/viterbi-algorithm.md) (implicitly paired with Viterbi as the other core HMM algorithm)

**What is missing**: The Baum-Welch EM algorithm — the training method for all HMMs in the vault. `viterbi-algorithm.md` is a well-developed concept note; its pair for training does not exist. Required: the E-step / M-step interpretation in HMM terms, convergence properties, sensitivity to initialization, and the specific implication for MAOPM (nightly refit on 252-day rolling window, $O(K^2 T)$ complexity acceptable on a Ray worker at daily granularity, not suitable for intraday refit).

**MAOPM impact**: Anyone implementing the nightly HMM refit will immediately encounter `model.fit(X)` in hmmlearn and need to understand what it is doing. Without this note, the refit schedule in `hidden-markov-model-hmm-in-finance.md` is an instruction without a mechanism.

---

### Gap 1.B — `parkinson-volatility-estimator.md`

**Referenced in**: [HMM Approaches research note](hmm-estimates-of-probability-from-option-prices.md) (§1b feature vector: `intraday_parkinson_vol`); [hidden-markov-model-hmm-in-finance.md](../concepts/hidden-markov-model-hmm-in-finance.md) (MAOPM feature vector); both list it as a required HMM emission dimension

**What is missing**: The Parkinson (1980) high-low range estimator: $\hat{\sigma}^2 = \frac{1}{4 \ln 2} (\ln H_t - \ln L_t)^2$, with bias and efficiency properties relative to close-to-close realized variance. The vault has `realized-volatility.md` and `realized_volatility.md` (duplicates — see Section 3) but neither explains range-based estimators. Parkinson vol requires intraday high/low data; this means Tool 1 or Tool 2 must source intraday OHLC for the index — a data dependency not currently in `tooling-requirements-maopm.md`.

**MAOPM impact**: The HMM feature vector cannot be computed without this. Parkinson vol is the single emission dimension most sensitive to the intraday GEX flip mechanism — positive GEX dampens the high-low range; negative GEX amplifies it. This is why it is more informative than close-to-close returns for the regime engine.

---

### Gap 1.C — `hmm-latent-regime-engine-implementation.md` (Tool 3)

**Referenced in**: [HMM Approaches research note](hmm-estimates-of-probability-from-option-prices.md) (§5A-D implementation); [hidden-markov-model-hmm-in-finance.md](../concepts/hidden-markov-model-hmm-in-finance.md) (refit schedule); [gex-regime-report-json-schema.md](../entities/gex-regime-report-json-schema.md) (Step 4 pseudocode, `hmm_state` block)

**What is missing**: `tooling-requirements-maopm.md` documents Tool 1 (GEX Regime Divergence Engine) and Tool 2 (Horizon Spread Pipeline) in full build specification. The HMM Latent Regime Engine is a third custom tool with its own requirements: (1) nightly Baum-Welch refit on 252-day rolling feature matrix; (2) intraday forward-pass producing `posterior_probs` from streaming feature vector; (3) feature ingestion from both Tool 1 (GEX Z-score) and Tool 2 (ΔIHS); (4) state persistence between cycle for sequential forward algorithm; (5) monthly AIC/BIC K-selection. None of this appears in `tooling-requirements-maopm.md`. The `hmm_state` JSON block is now in the schema but the compute pipeline to populate it is undocumented.

**MAOPM impact**: Without this, Tool 3 cannot be scoped or built. The HMM is now architecturally load-bearing — it drives the Layer 3 Greek limit scaler $M(x)$ — but has no implementation note.

---

### Gap 1.D — `aic-bic-model-selection.md`

**Referenced in**: [HMM Approaches research note](hmm-estimates-of-probability-from-option-prices.md) (§3 table: "Re-evaluate K via AIC/BIC on prior 6-month holdout"); [hidden-markov-model-hmm-in-finance.md](../concepts/hidden-markov-model-hmm-in-finance.md) (monthly recalibration: "Re-evaluate K via AIC/BIC")

**What is missing**: Akaike Information Criterion and Bayesian Information Criterion as applied to HMM K-selection. The monthly recalibration step requires understanding which criterion favors parsimony (BIC) vs. goodness-of-fit (AIC) and how to structure a held-out validation set for a time series. This is the only hyperparameter in the regime engine and a wrong choice (K=2 missing the transitional state, or K=5 overfitting) directly degrades the posterior probabilities driving $M(x)$.

---

### Gap 1.E — `option-implied-erp-horizon-spread.md` (carried from Gap 1.3 in 2026-05-17 analysis)

**Status**: Still missing. Now more urgent. The MAOPM feature vector explicitly includes `horizon_spread_delta = ERP_180 − ERP_30`, and the HMM research note describes BKM-integrated variance as an alternative emission dimension. The vault has [q-measure-equity-risk-premium-isolation.md](../concepts/q-measure-equity-risk-premium-isolation.md) which documents the ERP derivation mathematically, but no concept note specifically capturing the Lai (2022) horizon spread: its formula, its regime detection superiority vs. GARCH and historical returns (4.6% vs. 34% indecisive-zone rate), its sign interpretation (HS < 0 → crisis), and its role as HMM emission input.

**Distinction from existing notes**: `q-measure-equity-risk-premium-isolation.md` covers ERP extraction; `option-implied-horizon-spread.md` covers the general concept. Neither documents the two-maturity differential structure, the regime detection performance statistics from Lai 2022, or the specific implementation as an HMM feature dimension.

---

## Section 2: HMM Concept Note Fragmentation (structural integrity issue)

The HMM conceptual space now has **7 separate notes** in the vault — more than any other topic — and they are not a coherent hierarchy. They are parallel, partially overlapping entries from different ingestion sessions, most linking to each other inconsistently.

| File | Location | Depth | Authority | MAOPM-linked? |
|---|---|---|---|---|
| `hidden-markov-model.md` | concepts/ | Good — core formal definition | General | Links to `how-to-obtain-hmm-estimates-from-option-prices.md` (concept) |
| `hidden-markov-model-hmm.md` | concepts/ | Shallow — structural triad only | Pre-MAOPM | No |
| `hidden-markov-models-in-finance.md` | concepts/ | Good — RND comparison, strategy gatekeeper | Pre-MAOPM | No |
| `hidden-markov-models-for-options-trading.md` | concepts/ | Good — 1DTE-7DTE strategy table, GEX emissions | Pre-MAOPM | No |
| `how-to-obtain-hmm-estimates-from-option-prices.md` | concepts/ | Excellent — IVS surface clustering (Method 1) + parametric (Method 2) | Pre-MAOPM | No |
| **`hidden-markov-model-hmm-in-finance.md`** | concepts/ | **Authoritative — MAOPM integration** | **MAOPM** | **Yes** |
| **`hmm-estimates-of-probability-from-option-prices.md`** | research/ | **Authoritative — architecture + method synthesis** | **MAOPM** | **Yes** |

### Specific connectivity failures

**Gap 2.A**: `how-to-obtain-hmm-estimates-from-option-prices.md` (concept) contains the most detailed methodology in the vault for Method 1 (IVS surface clustering) and Method 2 (parametric calibration). The new authoritative research note [hmm-estimates-of-probability-from-option-prices.md](hmm-estimates-of-probability-from-option-prices.md) does not link to it. The concept note therefore cannot be found by anyone navigating from the research note.

**Gap 2.B**: `hidden-markov-models-for-options-trading.md` contains the canonical 3-state regime strategy table (State 1: iron condors; State 2: wide credit spreads; State 3: long calendars) and the GEX-as-emission-input rationale. It does not link to the new research note or the updated `hidden-markov-model-hmm-in-finance.md`. The strategy-selection logic it documents should be the direct output of the MAOPM Latent Regime Engine but the connection is invisible.

**Gap 2.C**: `usefulness-of-hidden-markov-models-for-short-dated-options-trading.md` (research/) is a stub that references two broken links: `[[../concepts/options-trading.md]]` and `[[../concepts/hidden-markov-models.md]]` — neither file exists. It also does not link to any MAOPM architecture note.

**Gap 2.D**: `hidden-markov-model-hmm.md` duplicates the opening paragraph of `hidden-markov-model.md` verbatim and has no unique content beyond a shallow structural triad reference. It is a redundant file producing inbound link confusion.

---

## Section 3: Persistent Naming Convention Violations

The vault has a mixed kebab-case / snake_case naming conflict that produces duplicate content nodes. These existed before today but are worsened by any new HMM notes inadvertently linking to one version over the other.

| Authoritative | Duplicate | Notes |
|---|---|---|
| `realized-volatility.md` | `realized_volatility.md` | Both exist; Parkinson estimator belongs in the authoritative one |
| `implied-volatility.md` | `implied_volatility.md` | Both exist |
| `volatility-risk-premium-vrp.md` | `volatility-risk-premium.md`, `volatility_risk_premium.md` | Three entries |
| `look-ahead-bias-in-backtesting.md` | `look-ahead-bias.md` | Both exist; HMM training window constraint belongs in the backtesting one |
| `zero-days-to-expiration-0dte.md` | `zero-days-to-expiration.md` | Both exist |
| `options-greeks.md` | `option-greeks.md` | Both exist |
| `gamma-exposure-gex.md` | `gamma-exposure.md`, `gamma_exposure_gex.md`, `gex.md` | Four GEX entries |
| `hidden-markov-model-hmm-in-finance.md` | `hidden-markov-model-hmm.md`, `hidden-markov-models-in-finance.md` | Three finance-application HMM notes |

**Gap 3.A — `realized-volatility.md` missing Parkinson content**: Specifically, `parkinson-volatility-estimator.md` (Gap 1.B above) content should be housed either as its own note or as a section in the authoritative `realized-volatility.md`. Currently neither file mentions range-based estimators.

---

## Section 4: Tooling Requirements Gap (carried urgency)

### Gap 4.A — Tool 3 not in tooling-requirements-maopm.md

`tooling-requirements-maopm.md` documents Tool 1 and Tool 2 in full implementation detail (data sources, endpoints, compute architecture, output schema fields). The HMM Latent Regime Engine is now architecturally equivalent in importance — it is the Layer 3 scaler and signal fusion layer — but is absent from the tooling document. The build specification needed:

- Input feature sources: Tool 1 → GEX Z-score; Tool 2 → ΔIHS; ThetaData/Polygon → log returns, Parkinson high-low range
- Training: `hmmlearn.GaussianHMM`, rolling 252-day window, nightly Baum-Welch via Ray worker
- Inference: forward algorithm intraday, forward-pass-only (no refit)
- Output: `hmm_state` JSON block → GEX Regime Report schema
- Validation: AIC/BIC K-selection monthly; calibration check against COVID-19 (Dec 2019) and Aug 2024 VIX spike as known regime transition events
- Minimum data requirement: 60 trading days before first live signal (30 GEX normalization + 30 HMM estimation)

---

## Prioritization

| Gap | Type | Blocks |
|---|---|---|
| **1.C — Tool 3 implementation note** | Missing research note | HMM Latent Regime Engine cannot be built |
| **2.A — Research note ↔ concept note link** | Missing link | `how-to-obtain-hmm-estimates-from-option-prices.md` invisible from authoritative research note |
| **2.B — Strategy table ↔ MAOPM link** | Missing link | 3-state strategy selection logic disconnected from MAOPM architecture |
| **1.A — `baum-welch-algorithm.md`** | Missing concept | HMM refit schedule has no mechanism documentation |
| **1.B — `parkinson-volatility-estimator.md`** | Missing concept | HMM feature vector incomplete; triggers Tool 3 data dependency |
| **1.E — `option-implied-erp-horizon-spread.md`** | Missing concept (carried) | HMM feature ΔIHS not formally documented as emission dimension |
| **2.C — `usefulness-of-hidden-markov-models` broken links** | Broken links | Dead stub; cannot be found in graph traversal |
| **1.D — `aic-bic-model-selection.md`** | Missing concept | Monthly K-recalibration step lacks prerequisite knowledge |
| **2.D — `hidden-markov-model-hmm.md` redundant** | Duplicate/redundant | Navigation confusion; contradicts authoritative note |
| **3.A — `realized-volatility.md` missing Parkinson** | Incomplete concept | Parkinson estimator referenced but not documented |

---

## Related

- [Gap Analysis 2026-05-17](gap-analysis-2026-05-17.md) — prior analysis; non-HMM gaps remain open
- [HMM Approaches in Options Pricing and Agent Architecture](hmm-estimates-of-probability-from-option-prices.md) — new authoritative research note (primary gap source)
- [Hidden Markov Model (HMM) in Finance](../concepts/hidden-markov-model-hmm-in-finance.md) — authoritative MAOPM concept note
- [GEX Regime Report JSON Schema](../entities/gex-regime-report-json-schema.md) — `hmm_state` block requiring Tool 3
- [Tooling Requirements MAOPM](tooling-requirements-maopm.md) — needs Tool 3 entry
- [Research Agenda Q5](research-agenda-options-maopm.md) — HMM resolves signal fusion; implementation gaps now the blocker
