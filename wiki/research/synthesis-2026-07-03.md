---
tags: ["synthesis", "maopm", "hmm", "regime-detection", "option-pricing", "architecture", "gap-status", "wonham-filter", "neural-networks", "mmjd"]
created: 2026-07-03
reviewed: false
source_origin: "level1-analysis"
---
# Vault Synthesis — 2026-07-03

> Incremental update to [synthesis-2026-06-23](synthesis-2026-06-23.md). That note declared the vault had crossed from conceptual design to implementation-ready. **This note was revised after four new ingestions on 2026-07-03T07:10–07:23** that closed one architectural gap, introduced a continuous-time regime inference framework with direct MAOPM relevance, and added a new isolated deep learning cluster. Read the June synthesis for cluster foundations; this note focuses on what changed and three newly identified non-obvious cross-cluster connections.

---

## What Changed Since 2026-06-23

### 0. Four New Ingestions — 2026-07-03

| File | Timestamp | New wiki notes |
|---|---|---|
| `1712.09913v3.pdf` (Li et al. 2018) | 07:10:29 | `Filter_Normalization`, `Neural_Network_Loss_Landscapes`, research note `Neural_Network_Trainability_and_Generalization` |
| `090770552.pdf` (Dai-Zhang-Zhu 2010) | 07:10:42 | `wonham-filter`, `optimal-stopping-time-finance`, `double-obstacle-problem-finance`, `trend-following-trading`, `regime-switching-model-financial`, research note `optimal-trend-following-strategy-regime-switching` |
| `Detecting stock market regimes from option prices.md` (Lai 2022 re-ingest) | 07:23:32 | `stock-market-regimes`, `horizon-spread-option-implied-erp`, entity `wan-ni-lai` |
| `appropriate HMM architectures...md` | 07:23:35 | `hidden-markov-models-in-option-pricing`, `markov-modulated-geometric-brownian-motion`, `markov-modulated-jump-diffusion`, `markov-switching-stochastic-volatility`, `volatility-clustering`, `gap-risk`, `volatility-smile`, `fast-fourier-transform-option-pricing` |

**Net result**: 19 new wiki notes, 2 new research outputs, 1 architectural gap closed (Gap D), 3 new non-obvious cross-cluster connections identified, 1 new naming conflict introduced.

---

### 1. Gap 1.D (AIC/BIC) — CLOSED (pre-ingestion)

`aic_bic_information_criteria.md` now exists and is substantive. It covers:
- $AIC = 2k - 2\ln\hat{L}$ and $BIC = k\ln n - 2\ln\hat{L}$ with correct sign convention
- Asymptotic consistency of BIC vs. prediction efficiency of AIC
- Application to Lai (2022) regime-switching model comparison

**Residual issue**: The note links to `[[../concepts/model_selection.md]]` and `[[../concepts/maximum_likelihood_estimation.md]]` — both likely non-existent. These are wikilink dead-ends but do not impair the note's usability. See [gap-analysis-2026-07-03](gap-analysis-2026-07-03.md) Gap 1.E.

**MAOPM impact**: The monthly K-selection recalibration procedure now has a documented mechanism. The Dai-Zhang-Zhu (2010) paper (ingested today) provides indirect evidence that K=2 suffices for trend-following on historical indices — but MAOPM's transitional state (K=3) remains the canonical assumption pending empirical K-selection.

### 2. Gap D — MMJD/MMGBM/MS-SV Option-Pricing Architectures: CLOSED

The raw source document was ingested at 07:23:35. The [hidden-markov-models-in-option-pricing](../concepts/hidden-markov-models-in-option-pricing.md) umbrella note confirms that the `fast-fourier-transform-option-pricing` approach uses matrix Riccati ODEs for the characteristic function — connecting directly to the [carr-madan-spanning-theorem](../concepts/carr-madan-spanning-theorem.md) already in the vault. Cross-cluster connection 10 (identified in June synthesis as hypothetical) now has explicit concept notes to anchor it. **Residual gap**: No bridge note connecting the Near-Expiry HMM posterior probability vector to MMJD state-conditional option prices.

### 3. Dai-Zhang-Zhu (2010) — Wonham Filter: NEW, HIGH RELEVANCE

Paper ingested at 07:10:42. Core contribution: models unobservable bull/bear regimes; applies the [wonham-filter](../concepts/wonham-filter.md) to compute the conditional bull probability given observed prices (satisfying a specific SDE); derives optimal buy/sell thresholds via the [double-obstacle-problem-finance](../concepts/double-obstacle-problem-finance.md). Validates on NASDAQ, S&P 500, DJIA.

**Why highly significant for MAOPM** (see Connections 11 and 12 below):
1. The Wonham filter is the continuous-time counterpart to the discrete Baum-Welch/Viterbi HMM. Both answer the same question: probability of being in each hidden regime given observable data. A Wonham-filter-based continuous inference mechanism applied to the 1-minute OHLC stream could provide real-time regime probability updates between the near-expiry HMM's hourly forward passes — reducing the inference lag from 60 minutes to near-zero.
2. The double-obstacle problem's optimal threshold structure (upper band = buy; lower band = sell; between = hold) is the mathematical formalization that the [structural-triad-systematic-options-trading](../concepts/structural-triad-systematic-options-trading.md) stub needs. The three-zone structure directly maps to the triad's currently-undefined entry/exit rules.

### 4. Neural Network Loss Landscapes: NEW, ISOLATED

Paper ingested at 07:10:29. Li et al. (2018) on filter normalization, loss landscape visualization, skip connections, and flat minima as correlates of generalization. Research note [Neural_Network_Trainability_and_Generalization](Neural_Network_Trainability_and_Generalization.md) covers the key findings. **Currently isolated** — no wikilinks to any other vault cluster. Thin MAOPM connection: Baum-Welch solves a non-convex optimization; "flat minima generalize better" may apply to HMM parameter sensitivity. Recommend treating as standalone until a stronger connection is established.

### 5. Lai 2022 Re-Ingestion — New Notes and Naming Conflict

New concept [horizon-spread-option-implied-erp](../concepts/horizon-spread-option-implied-erp.md) is a complement (not duplicate) to [option-implied-horizon-spread](../concepts/option-implied-horizon-spread.md) — the former covers the theoretical definition and Lai (2022) empirical properties; the latter covers the MAOPM Tool 2 implementation. They need cross-links. **Naming conflict**: `stock-market-regimes.md` (new, kebab-case) duplicates `Stock Market Regimes.md` (existing, Title Case). See Gap F in [gap-analysis-2026-07-03](gap-analysis-2026-07-03.md).

| Architecture | Dynamics | Short-DTE Relevance |
|---|---|---|
| **Markov-Modulated GBM (MMGBM)** | $dS_t/S_t = \mu(Z_t)dt + \sigma(Z_t)dW_t$ | Captures volatility clustering; underprices overnight gap risk |
| **Markov-Modulated Jump-Diffusion (MMJD)** | Adds state-dependent Poisson jump process $dN_t(Z_t)$ with $J(Z_t)$ magnitude | Generates pronounced vol smile and OTM skew matching real 1DTE chains |
| **Markov-Switching Stochastic Volatility (MS-SV)** | CIR-style variance process $dV_t$ with $(\kappa, \theta, \xi)$ governed by $Z_t$ | Dynamic term structure; near-term IV explodes in "Crash" state |

These three architectures address a distinct problem from the Gaussian HMM in [hmm-estimates-of-probability-from-option-prices](hmm-estimates-of-probability-from-option-prices.md): they are for *pricing* options under regime uncertainty, not for *classifying* market regimes. The existing wiki conflates these two applications under a single HMM umbrella. The MMJD is the most directly relevant for 1DTE short-premium strategies because it structurally prices tail-risk in the regime where gap risk dominates theta capture.

---

## Cluster Status — No Material Changes

All six clusters from the June 23 synthesis are structurally unchanged. Confirming current status:

- **Cluster 1 (Infrastructure)**: Unchanged. Threadripper 3990X, ThetaData, Ray cluster remain documented but undeployed.
- **Cluster 2 (Market Mechanics)**: Unchanged. Dual-Engine Temporal Architecture is fully specified. The 7DTE-1DTE boundary zone between the two engines still has no explicit cross-reference to the Near-Expiry HMM.
- **Cluster 3 (Strategy Selection)**: Unchanged. [Structural Triad](../concepts/structural-triad-systematic-options-trading.md) remains a stub — three components named, zero weighting rules.
- **Cluster 4 (Agent Architecture)**: Unchanged. [RegimeRiskScaler](../entities/regimeriskscaler-class.md) remains the only concrete code artifact. No new agent prompts written.
- **Cluster 5 (Performance & Evaluation)**: Unchanged. Options-native baselines (mechanical iron condors, VIX-switching) proposed in the June research agenda but not documented.
- **Cluster 6 (Near-Expiry Microstructure Engine)**: Unchanged. Fully specified but not built. No new validation evidence.

---

## New Cross-Cluster Connections (Updated)

### 10. Regime-Detection HMMs ↔ Option-Pricing HMMs (Now Anchored)

Previously identified as a hypothetical connection. Now anchored: [markov-modulated-jump-diffusion](../concepts/markov-modulated-jump-diffusion.md) exists and explicitly states it generates the OTM skew and vol smile of real 1DTE chains. [fast-fourier-transform-option-pricing](../concepts/fast-fourier-transform-option-pricing.md) connects to [carr-madan-spanning-theorem](../concepts/carr-madan-spanning-theorem.md). **Still missing**: bridge note connecting Near-Expiry HMM posterior probabilities to MMJD state-conditional option prices for mark-to-model P&L.

### 11. Wonham Filter ↔ MAOPM Near-Expiry HMM (Continuous vs. Discrete Inference)

The [wonham-filter](../concepts/wonham-filter.md) and the MAOPM Near-Expiry HMM both answer: *what is the current regime probability given observable market data?* The Wonham filter runs in continuous time (SDE-based, updated on every price tick); the HMM uses discrete hourly bars. In the 0DTE-1DTE window, the HMM's 60-minute update lag is a material operational risk. A Wonham filter applied to the 1-minute OHLC stream already feeding the [parkinson-volatility-estimator](../concepts/parkinson-volatility-estimator.md) could provide real-time regime probability updates between hourly HMM forward passes. The two are complementary: Baum-Welch trains transition parameters; the Wonham filter runs real-time inference using those parameters. No vault note currently makes this connection — the Wonham filter links only to the Dai-Zhang-Zhu research output.

### 12. Double Obstacle Problem ↔ Structural Triad Decision Matrix

The [double-obstacle-problem-finance](../concepts/double-obstacle-problem-finance.md) defines two time-dependent threshold curves: upper (enter) and lower (exit) over a composite regime probability. This three-zone structure — confirm/hold/exit — is exactly what the [structural-triad-systematic-options-trading](../concepts/structural-triad-systematic-options-trading.md) stub needs. The triad's three signal inputs (HMM state, GEX regime, VRP sign) could be mapped to a composite probability, with the double-obstacle thresholds defining the decision zones. The double-obstacle formalism also handles transaction costs explicitly — directly applicable to MAOPM's bid-ask spread and commission friction. No vault note connects these two frameworks.

### 13. Orphaned HMM Research Note ↔ New Content

[usefulness-of-hidden-markov-models-for-short-dated-options-trading](usefulness-of-hidden-markov-models-for-short-dated-options-trading.md) is still broken (Gap 2.C). The Dai-Zhang-Zhu paper and MMJD architecture now provide the substantive answers the note was asking for. Fixing the two broken wikilinks and adding links to [wonham-filter](../concepts/wonham-filter.md) and [markov-modulated-jump-diffusion](../concepts/markov-modulated-jump-diffusion.md) would transform this orphaned stub into a hub connecting three distinct HMM lines.

---

## The Vault's State as of 2026-07-03 (Final)

**What is complete:**
- MAOPM architecture: macro HMM, near-expiry HMM, dual-engine risk, signal fusion
- Backtesting pipeline specification (event-driven, nanosecond alignment, slippage modeling)
- Infrastructure specification (Threadripper, Ray, ThetaData, dxFeed)
- Data models: GEX Regime Report JSON, Greek Exposure Report JSON, Vol Surface Summary JSON
- Option-pricing HMM architectures: MMGBM, MMJD, MS-SV (Gap D closed today)
- Continuous-time regime inference framework: Wonham filter, optimal stopping, double-obstacle

**What is blocking implementation start:**

| Blocker | Required For | Status |
|---|---|---|
| `hmm-dual-layer-integration.md` | GEX/Regime Analyst agent prompt; fast-path vs. strategy-initiation routing | Not written |
| Structural Triad weighting rules | Pre-trade state matrix resolves signals; double-obstacle formalism now provides theoretical grounding | Stub only |
| Tool 3 build spec in `tooling-requirements-maopm.md` | Macro HMM scoping and build task assignment | Not written |
| Near-expiry HMM ↔ Dual-Engine cross-reference | `gex_z_score` source ambiguity (0DTE-filtered vs. full-chain) | Not written |

**What is newly identified as missing:**
- Bridge note: Near-Expiry HMM posteriors → MMJD state-conditional pricing (Connection 10)
- Bridge note: Wonham filter ↔ MAOPM near-expiry HMM real-time inference path (Connection 11)
- Bridge note: Double obstacle thresholds → structural triad decision zones (Connection 12)
- `stock-market-regimes.md` duplicates `Stock Market Regimes.md` (Gap F)
- `horizon-spread-option-implied-erp.md` and `option-implied-horizon-spread.md` need mutual cross-links
- Neural Network Loss Landscapes cluster is currently isolated (no connections to any other cluster)

The vault has two well-developed lines of HMM work:

**Line A — Regime Detection** (Clusters 2 & 6): Gaussian HMM / Multivariate Gaussian HMM used to classify market states (`low_vol`, `transitional`, `high_vol`, `pinning`, `mean_reverting`, `gamma_squeeze`). Output feeds the structural triad and dynamic Greek limits.

**Line B — Option Pricing** (uningested): MMGBM / MMJD / MS-SV used to price options under regime uncertainty. Output is a state-weighted option price that correctly prices the OTM skew and vol smile generated by regime switching.

No vault note connects these two lines. The connection matters because:

1. The Near-Expiry HMM (Line A) outputs a posterior probability vector $[\pi_1, \pi_2, \pi_3]$ over states. If the MAOPM is *also* pricing options (for mark-to-model P&L or implied fair value estimation), the same posterior can directly weight the MMJD state-conditional option prices: $C = \sum_k \pi_k \cdot C_k$ where $C_k$ is the option price in state $k$.

2. The [Breeden-Litzenberger theorem](../concepts/breeden-litzenberger-theorem.md) and [Carr-Madan spanning theorem](../concepts/carr-madan-spanning-theorem.md) are already in the vault — these are the risk-neutral density tools that connect option prices back to state probabilities. They form one half of the bridge; the MMJD pricing model is the other half.

3. The [how-to-obtain-hmm-estimates-from-option-prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md) concept note addresses this partially from the option-implied direction, but no note documents the forward direction (given HMM state priors, how to price options under that distribution).

**Resolution**: Ingest the raw architectures document. Create separate concept notes for MMGBM, MMJD, and MS-SV. Add a bridge note connecting Line A posterior outputs to Line B pricing inputs.

---

## The Vault's State as of 2026-07-03

**What is complete:**
- Architecture specification for MAOPM (macro HMM, near-expiry HMM, dual-engine risk, signal fusion)
- Backtesting pipeline specification (event-driven, nanosecond alignment, slippage modeling)
- Infrastructure specification (Threadripper, Ray, ThetaData, dxFeed)
- Data models: GEX Regime Report JSON, Greek Exposure Report JSON, Vol Surface Summary JSON

**What is blocking implementation start:**

| Blocker | Required For | Status |
|---|---|---|
| `hmm-dual-layer-integration.md` | GEX/Regime Analyst agent prompt; fast-path vs. strategy-initiation routing | Not written |
| Structural Triad weighting rules | Pre-trade state matrix resolves signals rather than just joining them | Stub only |
| Tool 3 build spec in `tooling-requirements-maopm.md` | Macro HMM scoping and build task assignment | Not written |
| Near-expiry HMM ↔ Dual-Engine cross-reference | `gex_z_score` source ambiguity (0DTE-filtered vs. full-chain) | Not written |

**What is newly identified as missing:**
- Bridge note: Near-Expiry HMM posteriors → MMJD state-conditional pricing (Connection 10)
- Bridge note: Wonham filter → MAOPM near-expiry HMM real-time inference path (Connection 11)
- Bridge note: Double obstacle thresholds → structural triad decision zones (Connection 12)
- `stock-market-regimes.md` duplicates `Stock Market Regimes.md` (Gap F)
- Neural Network Loss Landscapes cluster is currently isolated
