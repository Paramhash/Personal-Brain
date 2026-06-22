---
tags: ["research-agenda", "maopm", "hmm", "backtesting", "dual-engine", "regime-detection"]
created: 2026-06-23
reviewed: false
source_origin: "level1-analysis"
---
# Research Agenda — 2026-06-23

> Replaces the open items in [research-agenda-options-maopm.md](research-agenda-options-maopm.md) for questions not yet answered. That agenda tracked Q1–Q10 against MAOPM design; this agenda shifts focus to the empirical and implementation questions that become tractable now that the architecture is substantially specified. Maximum 10 questions, ranked ruthlessly.

**Status of prior agenda**: Q2 (~85% answered), Q3 (answered), Q5 (~45% open), Q7 (~50% open), Q9 (~45% open), Q10 (~25% open). Q1, Q4, Q6, Q8 remain substantially open. The questions below address the new highest-value open questions given the post-May-20 vault additions.

---

## Q1: How do the Near-Expiry HMM and the MAOPM Macro HMM divide authority over regime-driven decisions?

**The question precisely**: When the near-expiry HMM outputs `gamma_squeeze` for the current 3DTE position and the macro HMM outputs `low_vol_coherent`, which signal governs: (a) the fast-path management decision (should the position be closed now?), and (b) the next-cycle strategy initiation decision (should new short premium be opened)?

**Why it is tractable now**: Both HMMs are fully specified — feature vectors, training procedures, output classes, and data sources are documented. The Dual-Engine Temporal Risk Architecture defines the 0DTE/7DTE temporal boundary. The [RegimeRiskScaler](../entities/regimeriskscaler-class.md) implements the scaling engine. What is missing is an integration note (Gap A in [gap-analysis-2026-06-23](gap-analysis-2026-06-23.md)) that maps each HMM's output to a specific decision layer.

**Knowledge gain if answered**: Resolves the single largest architectural ambiguity in the MAOPM implementation path. Enables the GEX/Regime Analyst agent prompt to be written. Closes Gap A.

**Recommended approach**: Write `wiki/concepts/hmm-dual-layer-integration.md` specifying: (1) near-expiry HMM → fast-path management agent (DTE ≤ 7 positions); (2) macro HMM → strategy initiation debate prior (new positions); (3) conflict rule: near-expiry `gamma_squeeze` triggers fast-path close regardless of macro state (position management supersedes strategy initiation); (4) near-expiry `pinning` reinforces macro `low_vol` but neither activates without agreement.

---

## Q2: What does a K=3 Near-Expiry HMM actually learn from 2019–2024 SPX data, and does `gamma_squeeze` map cleanly to observable historical events?

**The question precisely**: Train the near-expiry HMM on 2019–2024 SPX 1-minute OHLC + ThetaData end-of-day options chains. Do the three emission clusters correspond to interpretable regime semantics? Specifically: does the high-realized-vol state (state assigned label `gamma_squeeze`) show elevated density around known squeeze events (Feb 2018 vol-spike, Oct 2018, Aug 2024 VIX spike)? Does the `pinning` state show elevated density on SPX OpEx Fridays?

**Why it is tractable now**: The Near-Expiry HMM repo structure is fully specified. `scripts/pull_historical.py` defines the data fetch. `hmm/train.py` defines the training procedure using Baum-Welch. The calibration events (Aug 2024 VIX spike as a near-term test; COVID-19 Dec 2019 as a longer-term test) are documented.

**Knowledge gain if answered**: First empirical result in the vault. Confirms or challenges the K=3 assumption. If states are not interpretable, the structural triad's regime semantics need revision before any strategy backtest. If states are interpretable, the validated HMM becomes the primary regime gate for all 1DTE-7DTE strategy backtests.

**Estimated data cost**: ThetaData VALUE tier sufficient for end-of-day options chain (no intraday options needed for the historical training pull). Estimated $25–60/month.

---

## Q3: What are the weighting and conflict resolution rules for the Structural Triad (HMM × GEX Profile × IV-HV Skew)?

**The question precisely**: The [Structural Triad](../concepts/structural-triad-systematic-options-trading.md) note is a stub. Given three signal inputs, define: (a) the conditions under which all three agree (confirmed entry), (b) the conditions under which exactly two agree (conditional entry — which two pairs override the third?), and (c) the conditions under which they conflict three-ways (no entry / wait).

**Why it is tractable now**: The vault has the full strategy matrix (HMM state × IVR tier → strategy type), the GEX regime classification (coherent/divergent), and the VRP sign (IV > HV → favorable short-vol). These three signals are independently computed in the pre-trade state matrix. The interaction rules are the only missing piece.

**Knowledge gain if answered**: Converts the pre-trade state matrix from a data join to a decision engine. Closes Gap C. Enables the first strategy backtest to be run (Q4 of prior agenda, now unblocked).

**Proposed resolution**:
- Confirmed entry (all three agree): HMM state compatible with strategy type + GEX sign consistent + VRP positive for short-vol (or negative for long-vol)
- GEX + HMM agree, VRP neutral: conditional entry at reduced size (50%)
- HMM alone signals `gamma_squeeze` while GEX and VRP say short-vol: block new premium selling; trigger fast-path review of existing near-expiry positions
- Three-way conflict: no new position initiation; escalate to LLM debate agent

---

## Q4: Does the Dual-Engine Gamma Multiplier ($M_\Gamma = M(\text{RDR}_T) \times M(\text{RDR}_S)$) interact correctly with the HMM posterior probability scaler?

**The question precisely**: The [Dual-Engine Temporal Risk Architecture](../concepts/dual-engine-temporal-risk-architecture.md) defines $M_\Gamma$ as the product of two RDR-based sigmoid outputs. The [dynamic-portfolio-greek-limits.md](../concepts/dynamic-portfolio-greek-limits.md) defines $M(x)$ as a bi-symmetric sigmoid over a composite RDR. Are these the same function applied twice, or are they additive layers? When the near-expiry HMM posterior probability for `gamma_squeeze` reaches 0.85, should it reduce $M_\Gamma$ further (a third multiplicative term), or does the `gamma_squeeze` state map to the `DIVERGENCE_STRATEGY_MODE` override in the [RegimeRiskScaler](../entities/regimeriskscaler-class.md)?

**Why it is tractable now**: All three scaling mechanisms are now documented. The question is not whether to use them — it's how they compose. The answer determines whether the RegimeRiskScaler needs a third input channel (HMM posterior prob) or whether the existing two-engine structure is sufficient when calibrated correctly.

**Knowledge gain if answered**: Finalizes the dynamic Greek limits architecture. Closes the last open sub-question in Q2 of the prior agenda (horizon spread integration into Layer 2/3). Required before any live paper-trading deployment.

---

## Q5: What is the minimum ThetaData subscription configuration needed to run the near-expiry HMM and horizon spread pipeline simultaneously?

**The question precisely**: The near-expiry HMM requires: (1) 1-minute OHLC for SPX/SPY intraday → ThetaData stock subscription; (2) end-of-day options chain for the 7DTE-1DTE window → ThetaData options subscription. The Horizon Spread (Tool 2) requires: (3) real-time option quote snapshots for the two bracketing expirations near 30 DTE and 180 DTE → ThetaData VALUE tier minimum. Does a single ThetaData subscription tier cover all three requirements simultaneously, or does running both pipelines require PRO tier?

**Why it is tractable now**: ThetaData tier documentation is in the vault and Tool 2 pipeline specification explicitly documents the endpoint requirements (`option_snapshot_quote` unlocks at VALUE tier; PRO tier adds pre-computed IV). Q9 of the prior agenda partially answered this for Tool 2 alone. The near-expiry HMM adds 1-minute intraday OHLC as a new requirement.

**Knowledge gain if answered**: Determines the minimum monthly data cost for Phase 1 paper-trading. Eliminates the cost ambiguity that makes Phase 1 infrastructure scoping uncertain. Directly unblocks the Tool 2 and near-expiry HMM build start.

---

## Q6: Can the Horizon Spread lead the near-expiry HMM's `gamma_squeeze` state by 2–8 weeks, enabling early position adjustment?

**The question precisely**: [Lai (2022)](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md) shows the horizon spread detected COVID-19 in December 2019 — twelve weeks before the near-expiry HMM would classify `gamma_squeeze` in March 2020. Is this lead-time relationship consistent across multiple regime transitions (Feb 2018, Oct 2018, Aug 2024)? If horizon spread inversions reliably precede near-expiry HMM `gamma_squeeze` states by a measurable lag, the macro HMM and the horizon spread can be used together as a two-stage early warning: HS < 0 → reduce short premium sizing; near-expiry HMM `gamma_squeeze` → close all short gamma.

**Why it is tractable now**: Both the horizon spread pipeline (Tool 2) and the near-expiry HMM are specified. Historical backtesting requires ThetaData EOD options chains from 2018 onward. The backtesting pipeline for sequential signal testing is defined.

**Knowledge gain if answered**: If the lead-lag relationship holds, MAOPM can adopt a two-stage defense posture against volatility regime breaks — a material improvement over a single-signal defensive trigger. The [MAOPM fusion blueprint](../concepts/maopm-architecture-horizon-spread-gex-fusion.md) describes this conceptually ("December 2019 condition") but provides no empirical evidence of consistent lag structure across multiple events.

---

## Q7: Which options-native baselines should be used to measure MAOPM alpha?

**The question precisely**: Q8 of the prior agenda flagged that `algorithmic-trading-strategies-baselines.md` covers only equity strategies. For options-native comparison, what are the mechanical baselines? Candidates: (a) weekly mechanical iron condors on SPY at 30 DTE, sold when IVR > 50 regardless of other signals; (b) systematic cash-secured puts on SPY at 30 DTE, always; (c) buy-and-hold plus covered call (XYLD replication); (d) VIX-regime switching: sell iron condors when VIX < 20, exit all positions when VIX > 30. Which of these is most appropriate as the primary comparison for MAOPM?

**Why it is tractable now**: The backtesting pipeline is specified. Running any of these baselines through it requires only strategy execution rules — no additional infrastructure. ThetaData historical data covers these expirations.

**Knowledge gain if answered**: Establishes the performance floor against which MAOPM must justify its complexity. Without an options-native baseline, any MAOPM paper-trading result has no valid comparison. This is a prerequisite for Q8 of the prior agenda.

**Proposed baseline ranking**: Primary baseline = mechanical weekly iron condors (IVR > 50 trigger, 30 DTE, no HMM/GEX filter). Secondary = VIX-regime switching (VIX < 20 → sell premium; VIX > 30 → exit). Rationale: these most directly isolate the value added by the HMM + GEX structural triad vs. a simple volatility filter.

---

## Q8: How should the unified alert queue merge the expiration management calendar, event-driven options risk calendar, and the near-expiry HMM monitoring schedule?

**The question precisely**: Q7 of the prior agenda (~50% answered) identified that the expiration management calendar (21 DTE forced-close rule, 3 PM ET pin risk) and the event-driven options risk calendar (earnings 2-day pre-event block, FOMC blackout) should merge into a single alert queue. The near-expiry HMM's inference loop adds a third monitoring schedule (hourly or triggered by GEX flip crossing). Define: (a) the unified data structure for this alert queue; (b) the priority ordering when multiple alerts are active simultaneously; (c) the routing logic: which alerts go to the fast-path management agent vs. the LLM debate loop.

**Why it is tractable now**: All three alert sources are fully documented. The RegimeRiskScaler `requires_fast_path` boolean in the Greek Exposure Report schema (from Q3 of prior agenda) already provides one routing flag. The question is the full queue schema and priority rules.

**Knowledge gain if answered**: Closes Gap 4.C (partial) in [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md) and the open sub-question in Q7 of the prior agenda. Required before Phase 2 implementation (fast-path management agent).

---

## Q9: What does AIC/BIC K-selection produce for the MAOPM macro HMM on 2018–2024 SPX data?

**The question precisely**: The MAOPM macro HMM documentation specifies K=3 as the canonical assumption based on practitioner convention. AIC/BIC on historical data may favor K=2 (bull/bear) or K=4+ (adding a trending/momentum state). Run the K-selection test on 2018–2024 data using BIC (favors parsimony) and AIC (favors fit) on a 6-month held-out window. What does each criterion select? Do they agree? If BIC selects K=2 and AIC selects K=4, what are the practical consequences for regime classification stability?

**Why it is tractable now**: The training procedure is documented (rolling 252-day window, GaussianHMM, hmmlearn). Once historical ThetaData options chains and SPX OHLC are available from Q2 (above), this test runs in the same pipeline with a loop over K values.

**Knowledge gain if answered**: Empirically validates or challenges the K=3 canonical assumption. If K=2 is optimal, the transitional state disappears and the term-structure catch-up strategy (which depends on detecting the boundary between regimes) loses its entry signal. If K=4 is optimal, the strategy matrix needs a fourth row. Either outcome is high-information.

---

## Q10: What is the minimum end-to-end backtest result needed to justify Phase 2 (paper trading) investment?

**The question precisely**: Phase 2 requires: ThetaData subscription (~$60/month), broker API integration (Tastytrade sandbox), Ray cluster deployment on the Threadripper 3990X, and logging infrastructure for the Recording Secretary / Decision Ledger. This is a non-trivial infrastructure investment. What backtest result is the minimum sufficient evidence to proceed? Define: (a) what strategy, (b) what time window, (c) what metric threshold, and (d) what comparison baseline constitutes "go/no-go" for Phase 2.

**Why it is tractable now**: The backtesting pipeline is specified. All required concept notes for evaluation metrics exist (Sharpe, Sortino, max drawdown in `financial-trading-evaluation-metrics.md`). Options-native baselines will be defined by Q7 (above).

**Knowledge gain if answered**: Creates a decision gate that prevents premature Phase 2 investment. The vault currently has no documented Phase 1 → Phase 2 success criteria. Without this, the project has no exit criteria for the backtest phase and risks infinite iteration.

**Proposed threshold (for debate)**: Backtest Sharpe ≥ 1.5 over 2020–2024 (including COVID-19 and Aug 2024 stress events), max drawdown ≤ 20%, PoP vs. realized profit rate within 10 percentage points, vs. mechanical iron condor baseline on same data. These criteria should be documented in a concept note or updated in `current research initiatives.md`.
