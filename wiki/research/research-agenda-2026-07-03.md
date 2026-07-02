---
tags: ["research-agenda", "maopm", "hmm", "option-pricing", "backtesting", "implementation", "wonham-filter", "mmjd", "double-obstacle"]
created: 2026-07-03
reviewed: false
source_origin: "level1-analysis"
---
# Research Agenda — 2026-07-03

> Updates [research-agenda-2026-06-23](research-agenda-2026-06-23.md). **Revised after four new ingestions on 2026-07-03** that closed one gap (MMJD/MMGBM/MS-SV now in vault) and introduced two new high-value questions (Wonham filter integration, double obstacle → structural triad). June agenda Q3 (ingest MMJD) is now complete. June Q6 (horizon spread lead time) and Q9 (AIC/BIC K-selection) are unchanged. Ranked ruthlessly by MAOPM build-blocking impact. Maximum 10 questions.

---

## Q1: Write `wiki/concepts/hmm-dual-layer-integration.md`

**The question precisely**: The vault contains two operational HMM specifications — the Near-Expiry HMM (4-feature, 7DTE-1DTE, `NearExpiryHMMState`) and the MAOPM Macro HMM (Tool 3, 6-feature, multi-week `hmm_state`). Define: (a) which HMM governs fast-path position management (DTE ≤ 7 positions currently held); (b) which HMM governs strategy initiation debate; (c) the conflict resolution rule when they disagree; (d) whether `NearExpiryHMMState` feeds as a sub-input to the macro HMM feature vector or runs in a parallel inference lane.

**Why tractable now**: Both HMMs are fully specified — feature vectors, training windows, output schemas, data sources. The [Dual-Engine Temporal Risk Architecture](../concepts/dual-engine-temporal-risk-architecture.md) defines the 0DTE/7DTE temporal boundary. The [MAOPM fusion blueprint](../concepts/maopm-architecture-horizon-spread-gex-fusion.md) defines the macro gating structure. The integration note requires architecture reasoning, not new research.

**Proposed resolution** (from June agenda Q1):
- Near-Expiry HMM → fast-path management agent (DTE ≤ 7 positions)
- Macro HMM → strategy initiation debate prior
- Conflict rule: near-expiry `gamma_squeeze` triggers fast-path close regardless of macro state (position management supersedes strategy initiation)
- Parallel inference lanes, not nested; `NearExpiryHMMState` is not a macro HMM feature

**Knowledge gain**: Unblocks the GEX/Regime Analyst agent prompt. Resolves Gap A (highest MAOPM build-impact open gap). Closes the 10-day stall since June 23.

---

## Q2: Define the Structural Triad Decision Matrix

**The question precisely**: The [Structural Triad](../concepts/structural-triad-systematic-options-trading.md) note is a stub. Define the complete 3×2×2 decision surface: HMM state ∈ {`low_vol`, `transitional`, `high_vol`} × GEX regime ∈ {`coherent`, `divergent`} × VRP sign ∈ {`positive`, `negative`}. For each of the 12 cells: (a) strategy type (iron condor, calendar spread, long straddle, no-trade); (b) size multiplier (full/half/zero); (c) overrides (near-expiry `gamma_squeeze` ∈ 12th-hour column; VVIX panic flag).

**Why tractable now**: All three signal dimensions are independently computed in the pre-trade state matrix. The strategy matrix (HMM × IVR tier → strategy type) and GEX regime classification (coherent/divergent) are both documented. The three components are documented; the decision rules are not. This is an authoring task with well-constrained inputs.

**Knowledge gain**: Converts the pre-trade state matrix from a data join to a decision engine. Enables the first strategy backtest to run. Closes Gap C.

---

## Q3: Can the Double Obstacle Problem Define the Structural Triad's Entry/Exit Thresholds?

**The question precisely** (new — from Dai-Zhang-Zhu 2010 ingestion): The [double-obstacle-problem-finance](../concepts/double-obstacle-problem-finance.md) defines two time-dependent threshold curves over a composite regime probability: upper (enter) and lower (exit). Map the structural triad's three inputs (HMM state posterior, GEX regime score, VRP sign) to a single composite probability `p*`. Apply the double-obstacle threshold framework to derive the confirmed-entry / hold / forced-exit decision zones. Does the resulting decision surface resolve the structural triad stub (Gap C) without requiring ad-hoc weighting choices?

**Why tractable now**: The [double-obstacle-problem-finance](../concepts/double-obstacle-problem-finance.md) note documents the variational inequality formulation and the penalization method for numerical solution. The three triad inputs are all independently computed in the pre-trade state matrix. The HMM state posterior from the Near-Expiry HMM provides a direct `p*` candidate (no composite mapping needed if the triad uses only the HMM signal for zone determination and treats GEX + VRP as filters within each zone).

**Knowledge gain**: Closes Gap C with mathematical grounding rather than practitioner intuition. The double-obstacle thresholds also explicitly handle transaction cost friction — directly mapping to MAOPM's bid-ask spread and commission terms. Enables the first strategy backtest to run.

---

## Q4: Should the Near-Expiry HMM Use the Wonham Filter for Real-Time Inference Between Hourly Updates?

**The question precisely** (new — from Dai-Zhang-Zhu 2010 ingestion): The [wonham-filter](../concepts/wonham-filter.md) computes the conditional regime probability in continuous time via an SDE driven by observable price data — functionally identical to the MAOPM Near-Expiry HMM's forward-pass posterior, but at tick frequency rather than hourly. In the 1DTE-0DTE window, where a 60-minute HMM inference lag represents 10% of the trading day: (a) is the Wonham filter's SDE computationally tractable on 1-minute OHLC bars from the existing Parkinson vol pipeline?; (b) does it add material accuracy over the hourly HMM forward-pass for `gamma_squeeze` state detection?; (c) what is the implementation cost (one additional SDE integrator vs. the full Baum-Welch/Viterbi stack)?

**Why tractable now**: The Wonham filter's SDE is documented in [wonham-filter](../concepts/wonham-filter.md). The 1-minute OHLC stream is already the primary input to the [parkinson-volatility-estimator](../concepts/parkinson-volatility-estimator.md). The [forward-algorithm](../concepts/forward-algorithm.md) (already in vault) is the discrete-time counterpart — a comparison between discrete and continuous inference is architecturally well-defined.

**Knowledge gain**: If the Wonham filter adds accuracy in the 1DTE window at low computational cost, it closes the 60-minute inference gap in the most time-critical regime management zone. If it adds no accuracy (because 1-minute bars are close enough to continuous-time), it rules out an additional implementation layer and simplifies the architecture.

---

## Q4: Should LSTM-GARCH Replace or Augment the GaussianHMM for Regime Detection?

**The question precisely**: The current MAOPM Near-Expiry HMM uses a GaussianHMM with first-order Markov transitions — it cannot remember regime context from more than one time step back. An LSTM-GARCH hybrid would: (a) use an LSTM to encode long-range temporal dependencies in the feature sequence `[log_return, parkinson_vol, vrp_trend, gex_z_score]`; (b) use a GARCH(1,1) or EGARCH component to model conditional variance explicitly rather than leaving it implicit in HMM emission covariances. Specifically: does LSTM-GARCH produce more stable regime labels than the GaussianHMM on 2019–2024 SPX 1-minute data, measured by label-switching frequency and posterior probability sharpness? And does it produce interpretable regime clusters that map to `{pinning, mean_reverting, gamma_squeeze}` semantics — or does it require a supervised labeling step?

**Why tractable now**: The vault has [olorunnimbe_viktor_2022_deep_learning_in_stock_market](../sources/olorunnimbe_viktor_2022_deep_learning_in_stock_market.md) covering LSTM architectures on financial time series and their primary failure mode (overfitting — mitigated by dropout, walk-forward validation). The Li et al. (2018) loss landscape work in [Neural_Network_Trainability_and_Generalization](Neural_Network_Trainability_and_Generalization.md) shows that skip connections (ResNet-style) promote flat minima and prevent chaotic landscapes in deep networks — directly applicable to a deep LSTM architecture. The [garch_model](../concepts/garch_model.md) baseline is now documented. Both approaches can be tested on the same ThetaData 1-minute OHLC pipeline specified in the Near-Expiry HMM repo structure.

**Key trade-offs vs. current HMM**:
- **HMM advantage**: Soft posteriors directly interpretable as `P(state | observations)`; no labeling step required; stable EM convergence; works on 60-day burn-in
- **LSTM-GARCH advantage**: Captures multi-day regime persistence (first-order Markov assumption in HMM is a structural limitation); GARCH explicitly models volatility clustering rather than approximating it via emission covariances; can incorporate exogenous features (GEX, VRP) more flexibly
- **LSTM-GARCH risk**: Olorunnimbe & Viktor (2022) identifies overfitting as the primary failure mode; requires 2–5 years of high-frequency data; output is a continuous score, not a discrete labeled state — requires a calibration layer to produce `posterior_probs` compatible with `NearExpiryHMMState`
- **Lai (2022) context**: Plain GARCH-based HMM achieves 34% indecisive-zone probability vs. 4.6% for the horizon spread HMM — LSTM could recover this gap, but the vault has no evidence either way

**Recommended test design**: Train both models on 2019–2022 SPX 1-minute data; evaluate on 2023–2024 held-out set; compare on: (1) label-switching frequency per day, (2) posterior sharpness (% of bars with max-state probability > 0.80), (3) density of high-vol state around known squeeze events (Aug 2024 VIX spike, Feb 2018).

**Knowledge gain**: If LSTM-GARCH produces sharper, more stable regime labels on the held-out period, it should replace the GaussianHMM as the Near-Expiry HMM's classification engine. If it matches but doesn't improve, the simpler HMM wins on operational grounds. Either outcome is high-information and settles the architecture question before Phase 2 build.

---

## Q5: Does the Horizon Spread Lead Near-Expiry HMM `gamma_squeeze` by 2–8 Weeks?

**The question precisely** (unchanged from June Q6): Lai (2022) shows the horizon spread detected COVID-19 in December 2019 — twelve weeks before the near-expiry HMM would classify `gamma_squeeze` in March 2020. Is this lead-lag relationship consistent across Feb 2018, Oct 2018, and Aug 2024 regime breaks? Test using the [backtesting pipeline](../concepts/systematic-options-backtesting-pipeline.md) with ThetaData EOD options chains from 2018 onward.

**Why tractable now**: Both pipelines are specified. Historical data access (ThetaData VALUE tier) is the only dependency. The test design is: for each known vol-regime break, measure the timestamp when the horizon spread first crossed −1σ vs. the timestamp when the near-expiry HMM first classified `gamma_squeeze` with posterior probability > 0.70.

**Knowledge gain**: If the lead-lag relationship is consistent (± 2 weeks across events), MAOPM can adopt a two-stage defense: HS inversion → reduce premium selling; near-expiry `gamma_squeeze` → close short gamma. This is a material improvement over a single-trigger defense and resolves the practical question of how early to react to macro regime breaks. Empirical result required — the vault currently documents this pattern as a hypothesis with one supporting data point (COVID-19).

---

## Q6: What Does a K=3 Near-Expiry HMM Actually Learn from 2019–2024 SPX Data?

**The question precisely** (unchanged from June Q2): Train the Near-Expiry HMM on 2019–2024 SPX 1-minute OHLC + ThetaData EOD options chains. Do the K=3 emission clusters map to interpretable regime semantics? Does the high-realized-vol state show elevated density around Feb 2018, Oct 2018, and Aug 2024 VIX spike? Does the `pinning` state show elevated density on SPX OpEx Fridays?

**Why tractable now**: The repo structure is fully specified (`hmm/train.py`, `hmm/inference.py`, `hmm/validate.py`). ThetaData VALUE tier provides the data. The calibration events are documented. This is the first empirical result available to the vault.

**Knowledge gain**: Validates or challenges K=3 assumption. If states are not interpretable, the structural triad's regime semantics need revision before any strategy backtest can be trusted. If validated, the HMM becomes the primary regime gate for all 1DTE-7DTE strategy backtests and Q2 (structural triad decision matrix) becomes immediately executable.

**Data cost estimate**: ThetaData VALUE tier, ~$25–60/month. Single-node run on Threadripper 3990X.

---

## Q7: What is the Minimum ThetaData Subscription Configuration for Both Pipelines Simultaneously?

**The question precisely** (unchanged from June Q5): Does a single ThetaData VALUE tier subscription cover all three simultaneous data requirements: (1) 1-minute OHLC for SPX/SPY intraday (near-expiry HMM); (2) EOD options chain for 7DTE-1DTE window (near-expiry HMM training); (3) real-time option quote snapshots for the two bracketing expirations near 30 DTE and 180 DTE (Horizon Spread pipeline, Tool 2)?

**Why tractable now**: ThetaData tier documentation is in the vault. The endpoint requirements for Tool 2 (`option_snapshot_quote` at VALUE tier minimum) are documented. The new requirement is the 1-minute intraday OHLC for the near-expiry HMM.

**Knowledge gain**: Determines minimum monthly infrastructure cost for Phase 1 paper-trading. Eliminates cost ambiguity blocking Phase 1 scoping.

---

## Q8: How Should the Unified Alert Queue Merge Three Monitoring Schedules?

**The question precisely** (from June Q8): Define the unified data structure, priority ordering, and routing logic that merges: (a) expiration management calendar (21 DTE forced-close rule, 3 PM ET pin risk); (b) event-driven options risk calendar (earnings 2-day pre-event block, FOMC blackout); (c) near-expiry HMM inference loop (hourly or triggered by GEX flip crossing). Which alerts route to the fast-path management agent vs. the LLM debate loop?

**Why tractable now**: All three alert sources are documented. The RegimeRiskScaler `requires_fast_path` boolean is already a JSON schema field. The question is the full queue schema and priority rules.

**Knowledge gain**: Required before Phase 2 implementation (fast-path management agent). Closes a partial gap in Q7 of the June research agenda.

---

## Q9: What Does AIC/BIC K-Selection Produce for the MAOPM Macro HMM on 2018–2024 SPX Data?

**Status update from June agenda**: The AIC/BIC mechanism is now documented (`aic_bic_information_criteria.md`). The K-selection procedure — rolling 252-day window, GaussianHMM, BIC on 6-month held-out window — is specified. What remains is the empirical execution.

**The question precisely**: Train the macro HMM on 2018–2024 SPX data. Sweep K ∈ {2, 3, 4, 5}. Apply BIC (favors parsimony) and AIC (favors fit) on 6-month held-out windows. What does each criterion select? Do they agree? If BIC selects K=2, the transitional state (which drives term-structure catch-up positioning) disappears. If AIC selects K=4, the strategy matrix needs a fourth row.

**Knowledge gain**: Empirically validates the K=3 canonical assumption embedded in all MAOPM architecture documentation. High-information regardless of outcome.

---

## Q10: Is MMJD the Correct Option-Pricing Architecture for 1DTE MAOPM Positions?

**Status update**: MMJD is now in the vault as [markov-modulated-jump-diffusion](../concepts/markov-modulated-jump-diffusion.md). The architecture question shifts from "does it exist?" to "should we implement it?"

**The question precisely**: For 1DTE iron condors: (a) does MMJD better explain observed OTM skew than MMGBM on historical ThetaData options chains?; (b) can the Near-Expiry HMM `posterior_probs` vector be used directly to weight MMJD state-conditional option prices for mark-to-model P&L?; (c) what is the pricing error of MMGBM vs. MMJD for 1DTE SPX options with 2-sigma OTM short strikes, measured against historical mid-prices?

**Why tractable now**: [markov-modulated-jump-diffusion](../concepts/markov-modulated-jump-diffusion.md) documents the SDE. [fast-fourier-transform-option-pricing](../concepts/fast-fourier-transform-option-pricing.md) documents the Carr-Madan FFT pricing approach. The Near-Expiry HMM output schema provides the posterior weights. ThetaData provides historical chains. This closes Gap G and builds the mark-to-model layer absent from the current MAOPM architecture.

**Knowledge gain**: Determines whether MAOPM needs a pricing layer beyond exchange mid-prices. If MMJD matches observed OTM skew better than MMGBM, it becomes the internal fair-value benchmark for all short-premium position monitoring — the completion of Cross-Cluster Connection 10.
