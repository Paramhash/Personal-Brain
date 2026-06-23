---
tags: ["research-agenda", "maopm", "hmm", "options-trading", "backtesting", "art-digital-culture", "validation"]
created: 2026-06-03
reviewed: false
source_origin: "level1-analysis"
---
# Research Agenda — 2026-06-03

> This agenda supersedes the open sub-questions in [research-agenda-options-maopm](research-agenda-options-maopm.md) that remain unresolved as of June 3, 2026. It is generated against the current vault state: Tool 4 (Near-Expiry HMM) is the Phase 1 MVP and fully specified; Tool 2 (BKM) is structurally complete except the `bkm_integrate()` function; the art/digital culture cluster is ingested but unanalyzed. Questions are ranked by knowledge gain per unit of available evidence.

---

## Q1: How do you validate Tool 4 (Near-Expiry HMM) when there is no labelled ground truth for pinning, mean-reverting, and gamma-squeeze states?

**The precise question**: Tool 4's Gaussian HMM learns three states unsupervised. State labels (`pinning`, `mean_reverting`, `gamma_squeeze`) are assigned post-hoc by interpreting the learned emission means. What observable market behavior — in the feature space and in subsequent price action — constitutes evidence that a state assignment is correct? What is the minimum out-of-sample test that must pass before Tool 4 is trusted as a live inner-gate signal?

**Why tractable now**: The vault has the complete 7-feature emission vector specification ([tooling-requirements-maopm](tooling-requirements-maopm.md): `gex_concentration_at_expiry`, `spot_to_gamma_wall_distance`, `atm_gamma_velocity`, `oi_concentration_ratio`, `realized_vol_intraday`, `atm_iv_dte_slope`, `call_put_volume_ratio`), three well-defined theoretical state semantics ([near-expiry-hmm-options-dynamics](../concepts/near-expiry-hmm-options-dynamics.md)), and the known historical examples of each regime type. An empirical validation protocol can be specified from vault knowledge alone, before any code is run.

**Knowledge gain**: Without this, Tool 4 cannot be trusted as a production signal — a model with plausible-looking state labels could be fitting noise. This is the single most likely failure mode for a build that proceeds directly from specification to deployment. Answering this question defines the "done" criterion for Tool 4.

**Expected form of the answer**: Three validation criteria:
1. **Emission consistency**: In `pinning` state, mean `spot_to_gamma_wall_distance` < 0.3% and mean `realized_vol_intraday` is the lowest of the three states. In `gamma_squeeze`, mean `realized_vol_intraday` is the highest and `atm_gamma_velocity` is largest. Confirm by inspecting $\hat{\mu}_k$ post-fit.
2. **Predictive validity**: Next 30-minute realized vol should be meaningfully lower in `pinning` than `gamma_squeeze` states, computed on a hold-out set of expiration cycles not used in training.
3. **Known event correspondence**: The August 2024 VIX spike and the March 2020 crash should appear as sustained `gamma_squeeze` state runs in the Viterbi path when Tool 4 is run retrospectively on ThetaData historical data.

---

## Q2: What is the minimum viable implementation of Tool 4 that can reach paper-trading in 30 days?

**The precise question**: Given that the dxFeed data engine already provides 6 of 7 required feature inputs (all except `realized_vol_intraday`), hmmlearn is installed, and the full build specification exists in [tooling-requirements-maopm](tooling-requirements-maopm.md), what is the shortest implementation path? Specifically: which features can be simplified or proxied for iteration 1 without materially degrading regime classification accuracy? What is the minimum training data window before the first state assignment is valid?

**Why tractable now**: The dependency graph is fully resolved. Tool 4 has no upstream tool dependencies — it reads directly from the dxFeed data engine and ThetaData 1-minute OHLC. The only missing piece is a `realized_vol_intraday` data fetch from ThetaData VALUE tier (1-minute bars → Parkinson estimator rolling 30 minutes). The training procedure (`hmmlearn.GaussianHMM.fit()` on DTE-aligned sequences) is straightforward. The 30-day minimum data requirement means data collection must start before training begins.

**Knowledge gain**: This question forces a concrete build plan with hard decisions: whether VIX stratification should be deferred to iteration 2 (simplifies initial training), whether `atm_gamma_velocity` (which requires three-strike options chain lookups) can be proxied by ATM gamma alone, and whether the Viterbi decoder should run every 5 minutes or only on new bar events. These decisions are currently implicit in the spec. Making them explicit reduces build time and eliminates the risk of over-engineering.

**Expected form of the answer**: A prioritized simplification list: (a) defer VIX stratification — train a single model, add stratification in iteration 2; (b) proxy `atm_gamma_velocity` as `(gamma_atm_plus1 − gamma_atm_minus1) / (2 × strike_step)` — requires only three strikes, not a full chain; (c) run forward pass every 5 minutes on new bar event (not streaming); (d) minimum training window is 30 expiration cycles (~150 trading days) before first deployment, starting data collection immediately.

---

## Q3: What is the smallest BKM integration that remains numerically valid over a sparse far-dated options chain?

**The precise question**: The [Tool 2 BKM pipeline](tooling-requirements-maopm.md) integrates OTM option prices across the strike domain using trapezoidal approximation: $V_Q(T) = 2 \sum_i \frac{C(K_i) \text{ or } P(K_i)}{K_i^2} \cdot \Delta K_i \cdot e^{rT}$. For SPY at 30 DTE, the strike grid is typically dense (hundreds of strikes, $1 intervals). At 180 DTE, OTM options thin out substantially beyond 10–15% away from spot: liquidity drops, bid-ask spreads widen, and mid-prices become unreliable. What is the minimum number of valid OTM strikes needed on each side before the integrated variance is reliable? How should missing or illiquid far-OTM strikes be handled?

**Why tractable now**: The [Bakshi-Kapadia-Madan formulation](../concepts/bakshi-kapadia-madan-formulation.md) is documented in the vault. The [Breeden-Litzenberger theorem](../concepts/breeden-litzenberger-theorem.md) provides the theoretical constraint (integrated variance must be finite and positive). The dxFeed data engine already returns bid/ask per contract and flags zero-bid contracts. The question reduces to: at what bid-ask spread threshold should a strike be excluded, and what interpolation method (linear, cubic spline, flat extrapolation) preserves variance estimate quality? This is answerable by specifying validation criteria against a dense chain (30 DTE) used as ground truth.

**Knowledge gain**: Without this, Tool 2's `bkm_integrate()` function has undefined behavior on sparse chains — it either silently underestimates far-wing variance (missing crisis premium) or crashes on zero-bid strikes. Answering this produces the input validation logic and edge-case handling for the single missing function in Tool 2.

**Expected form of the answer**: (a) Exclude strikes where `bid == 0 or bid/ask < 0.3`; (b) require minimum 5 valid OTM puts and 5 valid OTM calls per side before integration; (c) extrapolate the last valid OTM strike using flat (constant) extrapolation — not linear — to avoid artificially inflating far-wing variance; (d) flag the horizon spread output with `chain_quality: "sparse"` when fewer than 10 total valid strikes are available per expiration, and suppress from agent input.

---

## Q4: Does horizon spread provide actionable lead time over GEX signals, and what threshold triggers a regime pre-position?

**The precise question**: Lai (2022) reports that horizon spread detected the COVID-19 market regime shift in December 2019 — approximately three months before equity returns or historical volatility signaled it. But "detected" requires a threshold crossing. What threshold? Was there a sustained false-positive period between December 2019 and the February 2020 market break during which HS was negative but GEX remained positive (dealers stabilizing)? If so, how long was the false-positive window, and what would a MAOPM have done in that window — entered premature long-vol that decayed for weeks before paying off?

**Why tractable now**: The vault has the [Lai 2022 source](../sources/detecting_stock_market_regimes_lai_2022.md), the [horizon spread concept](../concepts/option-implied-horizon-spread.md), and the [MAOPM architecture for signal conflict resolution](../concepts/maopm-architecture-horizon-spread-gex-fusion.md). Historical SPY options data for December 2019–February 2020 is accessible via ThetaData. This is the vault's most cited empirical claim — it drives the entire Tool 2 rationale — and it has never been verified against the raw data or cross-examined for its false positive behavior.

**Knowledge gain**: If the COVID-19 signal had a multi-week false-positive period with costs (theta decay on premature long-vol), then horizon spread is a useful risk indicator but not a direct position-entry signal. This changes Tool 2's role in the MAOPM: it would feed the Vol Analyst's macro context (suppressing short-vol debate) rather than triggering a hard strategy shift. If the signal was clean (HS crossed negative and stayed negative), it is a primary signal and warrants a hard strategy override rule. The distinction fundamentally determines how Tool 2 is weighted in the agent architecture.

---

## Q5: What ablation design isolates the three separable alpha sources in MAOPM — Tool 4 HMM, GEX, and LLM debate?

**The precise question**: The MAOPM generates alpha from three structurally separable components: (1) the HMM inner gate (Tool 4 `state_label == "pinning"` as entry condition); (2) the GEX-driven strategy selection (IVR × GEX regime → strategy type from the 2D matrix); (3) the LLM debate (Long-Vol vs. Short-Vol researcher debate that can override or confirm the mechanical strategy). Paper trading with all three active cannot distinguish which is adding alpha. What is the minimal set of controlled conditions needed to measure each component's independent contribution?

**Why tractable now**: The three components are architecturally modular — they can be replaced by baseline equivalents without changing the execution pipeline. The baseline for (1) is a rule-based DTE countdown gate (enter any short-gamma position when DTE ≤ 7 and GEX positive). The baseline for (2) is a mechanical IV-regime → strategy mapping (no GEX signal, just IVR buckets). The baseline for (3) is the mechanical strategy selection output, bypassing the LLM debate entirely. The vault has the [algorithmic trading strategies baselines](../concepts/algorithmic-trading-strategies-baselines.md) framework and all three module definitions.

**Knowledge gain**: Without this ablation design, 12 months of paper trading produces one data point about the composite system. With it, parallel paper-trading tracks produce attribution evidence by month 6. This is the evaluation design question that determines whether the research program produces a publishable result or just an engineering artifact.

**Expected form of the answer**: Three concurrent paper-trading tracks: (A) full MAOPM (HMM + GEX + LLM), (B) mechanical analog (rule-based DTE gate + IVR-only strategy + no debate), (C) GEX-only analog (rule-based DTE gate + GEX × IVR strategy + no debate). Monthly Sharpe, PoP vs. realized rate, and theta-adjusted return compared across all three. Attribution = A − C (LLM contribution) + C − B (GEX contribution) + B (baseline).

---

## Q6: How should MAOPM handle a VIX tier transition during an open position?

**The precise question**: Tool 4 uses VIX stratification — Tier A (VIX < 20) and Tier B (VIX ≥ 20) — and selects model parameters at inference time based on the current VIX. If a short-gamma position is opened at VIX = 18 (Tier A model, `state_label == "pinning"`, entry condition met) and VIX rises to 22 intraday before expiration, the Tier B model activates and may classify the same feature vector as `gamma_squeeze`, triggering an exit signal. What is the correct position management rule in this case: (a) exit immediately on state-label change driven by tier switch, (b) hold until the Tier B model has been active for a minimum number of bars, (c) treat mid-position tier transitions as a hard-exit event regardless of state label?

**Why tractable now**: The stratification design is fully specified in [tooling-requirements-maopm](tooling-requirements-maopm.md). The three management states (`pinning`, `mean_reverting`, `gamma_squeeze`) have defined action implications (enter / hold / exit-tighten). The VIX transition scenario is the highest-probability edge case for a 1DTE short-gamma position: VIX commonly crosses the 20 threshold intraday during moderate-stress events, which is precisely when 1DTE short-gamma positions are most at risk.

**Knowledge gain**: This question defines the `position management interrupt handler` for the Tool 4 state machine — a concrete code decision. Getting it wrong means the tool has undefined behavior at the exact moment it matters most (rising VIX during an open short-gamma position).

**Expected form of the answer**: Rule (c) is the correct answer for a 1DTE position where theta-decay is complete within hours: a VIX tier transition from A → B during an open 1DTE short-gamma position is a hard-exit event, executed at market. Rationale: the Tier B model was trained on high-VIX microstructure which is structurally different from low-VIX pinning dynamics; continuing under Tier A model parameters in a Tier B environment is equivalent to using the wrong model. For 7DTE positions, rule (b) applies with a 30-minute confirmation window to avoid noise triggers.

---

## Q7: Is the Decision Ledger schema complete enough to attribute P&L correctly when a position is rolled?

**The precise question**: The [Decision Ledger](../concepts/decision-ledger.md) and the Performance Observer track every position via `position_id`. But when a 45-DTE iron condor is rolled to new strikes and a new expiration at 21 DTE, is this one continuous position (economic continuity: same directional bet, adjusted strikes) or two positions (old one closed, new one opened)? The current schema does not specify. If it's two positions, then P&L from the roll debit is attributed to the old position (a loss) and the new position starts from zero — making rolled positions look like a series of small losses followed by a winning final position. This misrepresents how options professionals measure roll performance.

**Why tractable now**: The [Decision Ledger](../concepts/decision-ledger.md) schema exists. The [expiration management](../concepts/expiration-management.md) note defines roll events as a first-class management action triggered at 21 DTE. The accounting question (economic continuity vs. two separate positions) is standard in options portfolio reporting and has a well-established answer in institutional options management. The vault has enough to specify the correct schema extension.

**Knowledge gain**: Without this, the Performance Observer — the single mechanism for closing the feedback loop between strategy decisions and outcomes — produces systematically misleading attribution data. Roll-heavy strategies (the vault's 21–45 DTE premium-selling core) will appear to perform worse than buy-hold strategies because roll debits are attributed as losses. Answering this question defines a schema extension to the Decision Ledger that is both technically simple and analytically essential.

**Expected form of the answer**: A `roll_chain_id` field linking parent and child positions across rolls. P&L attribution accumulates across all positions in the same `roll_chain_id`. A roll is not a close + open; it is a position state transition (`status: "active" → "rolled"`) with a debit logged as a roll cost against the chain's cumulative P&L.

---

## Q8: Does Singapore's state-driven IT policy constitute a distinctive enabling condition for digital art, and how does it differ from Western patronage models?

**The precise question**: The vault's art cluster documents three Singapore state digital infrastructure programs — [IT2000 Masterplan](../concepts/it2000-masterplan.md), [Singapore ONE](../concepts/singapore-one.md), and [Smart Nation](../concepts/smart-nation.md) — alongside the [CyberArts Exhibition](../entities/cyberarts-exhibition-2001.md), [Lin Hsin Hsin Art Museum](../entities/lin-hsin-hsin-art-museum.md), and a cohort of digital art practitioners ([Lin Hsin Hsin](../entities/lin-hsin-hsin.md), [Gunalan Nadarajan](../entities/gunalan-nadarajan.md), [Johann Yamin](../entities/johann-yamin.md), [Charles Lim](../entities/charles-lim-yi-yong.md)). The enabling condition for digital art in Singapore appears to be state infrastructure investment (broadband, digital public spaces, national digitization campaigns) rather than the art-institution patronage chain (museum commissions, art school grants, gallery representation) that defines the Western model. Is this reading accurate? What did state infrastructure provide that institutional patronage did not — and what did it foreclose?

**Why tractable now**: The vault now has both sides of this comparison: Singapore state policy (IT2000, CyberArts, the concept notes on [intelligent-island](../concepts/intelligent-island.md) and [strategic-amnesia-digital-culture](../concepts/strategic-amnesia-digital-culture.md)) and the art-practice network ([antoinette-2014-reworlding-art-history](../sources/antoinette-2014-reworlding-art-history.md), [yamin-mitchell-excavating-amnesia-2023](../sources/yamin-mitchell-excavating-amnesia-2023.md), [southeast-of-now-journal](../sources/southeast-of-now-journal.md)). The Yamin-Mitchell source specifically interrogates how state-sponsored digitization shaped and constrained local cultural memory — directly relevant to this question.

**Knowledge gain**: This is the synthesis question that would give the art cluster its conceptual spine. Without it, the cluster is a collection of entity notes and source stubs with no unifying argument. Answering it produces the art-cluster synthesis note that the gap analysis (Gap 3.A in [gap-analysis-2026-06-03](gap-analysis-2026-06-03.md)) identifies as missing, and does so with a specific, arguable thesis rather than a descriptive summary.

---

## Q9: What does the Antoinette "reworlding" methodology imply for how to organize non-Western art knowledge in the vault?

**The precise question**: Antoinette's [reworlding framework](../concepts/reworlding-art-history.md) argues that Southeast Asian art history should be constituted from local conditions, relational networks, and situated practices — not by measuring Southeast Asian work against a Western canonical baseline. This is a methodological claim with a direct implication for knowledge organization: the vault's current `contemporary-art-singapore.md` and `contemporary-southeast-asian-art-after-1990.md` notes define their subjects relationally to Western modernity. Should the art cluster be reorganized around practitioner networks and exhibition histories rather than canonical concept notes? Or is the vault's current structure (concept → entity → source) already compatible with Antoinette's approach if the concept notes are rewritten from local frames?

**Why tractable now**: The vault has Antoinette's argument in `antoinette-2014-reworlding-art-history.md`, the critical reception in [veal-2017-michelle-antoinette-reworlding-art-history-review](../sources/veal-2017-michelle-antoinette-reworlding-art-history-review.md), and the contrast with Piyadasa/Sulaiman's earlier "rethinking" project visible across the art entity notes. This is not a question about a missing external source — it is answerable from material already in the vault.

**Knowledge gain**: This question addresses the vault's meta-structure for the art cluster. A wrongly organized knowledge base produces insights that are artifacts of its organization. If the concept-first structure imposes a Western categorical frame, the research agenda built on it will reproduce that frame's blind spots. This question cannot be deferred: every new art-cluster note that is written before this is answered will need to be revised if the answer changes the organizational logic.

---

## Q10: When GEX and horizon spread conflict, which signal governs strategy selection and by what mechanism?

**The precise question**: The Q9 sub-questions from [research-agenda-options-maopm](research-agenda-options-maopm.md) identified but did not answer the conflict case: GEX is positive (dealer stabilized, short-vol strategies permissible) but horizon spread is negative (macro crisis regime incoming, long-vol is the correct structural position). In the current MAOPM architecture, GEX drives the inner gate (Tool 4 `state_label`) and horizon spread drives the Vol Analyst's narrative input to the debate. There is no hard rule specifying which prevails. This is not an edge case — Lai (2022) showed that for several weeks before the COVID-19 break, exactly this conflict would have obtained: positive GEX (market still stabilized by dealer hedging) and negative horizon spread (market pricing catastrophic short-term risk premium). MAOPM agents debating this conflict with no tie-breaking rule will produce inconsistent outcomes cycle to cycle.

**Why tractable now**: The [MAOPM architecture horizon spread / GEX fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md) documents the hierarchical gating structure. The 3-layer Greek limit trigger hierarchy in [dynamic-portfolio-greek-limits](../concepts/dynamic-portfolio-greek-limits.md) specifies Layer 1 (index GEX sign — binary), Layer 2 (VVIX spike — hard suspend), Layer 3 (RDR sigmoid — continuous). Horizon spread is not currently in this hierarchy. The question is whether it belongs as Layer 0 (a macro override that suspends all short-vol when HS < 0), or as a soft modifier fed only to the Vol Analyst's structured report for LLM debate. The vault has the architecture; it lacks the decision.

**Knowledge gain**: This is the last major unresolved architectural question before the MAOPM agent loop can be designed end-to-end. The answer determines whether horizon spread modifies the Greek limit system (deterministic code) or only influences agent debate (probabilistic LLM). These are fundamentally different implementation paths. A wrong answer at this stage — horizon spread in the debate only, no hard override — would mean the system continues selling volatility into a COVID-like event because the LLM debate is noisy and the inner gate (GEX still positive) remains open.

**Expected form of the answer**: Horizon spread belongs as a soft Layer 0 modifier, not a hard override: when HS < −1σ from its 12-month mean, reduce $L_{\text{base}}$ capacity for short-vega positions by 50% at the Portfolio Manager's position-sizing step, before the Greek limit sigmoid is applied. This is softer than Layer 2 (full suspend) but harder than debate input (no mechanical effect). The 50% reduction is parametric and calibrated by the August 2024 VIX spike as a recent near-miss test case. It does not block the LLM from approving a short-vol trade; it reduces the maximum size, making the conflict case a debate with mechanical stakes rather than an unconstrained LLM call.

---

## Priority Ranking Summary

| Rank | Question | Knowledge Type | Blocks |
|---|---|---|---|
| 1 | Q1: Tool 4 validation protocol | Methodology | Live deployment of Tool 4 |
| 2 | Q2: Tool 4 minimum viable implementation | Engineering | 30-day build timeline |
| 3 | Q3: BKM numerical stability (sparse chains) | Numerical methods | Tool 2 completion |
| 4 | Q10: GEX vs. horizon spread conflict resolution | Architecture | End-to-end agent loop design |
| 5 | Q7: Decision Ledger roll-chain attribution | Schema design | Performance Observer accuracy |
| 6 | Q5: Alpha ablation design (Tool 4 vs. GEX vs. LLM) | Evaluation design | Paper trading results interpretation |
| 7 | Q4: Horizon spread lead time and false positive rate | Empirical | Tool 2 role in agent debate |
| 8 | Q6: VIX tier transition during open position | Implementation rule | Tool 4 position management |
| 9 | Q8: Singapore state infrastructure as digital art enabler | Historical synthesis | Art cluster synthesis note |
| 10 | Q9: Antoinette reworlding and vault organization | Methodological | Art cluster structure |

---

*Next actions: Q1 and Q2 can be addressed immediately using vault knowledge alone (no new data required). Q3 requires running ThetaData chain queries for a 180 DTE SPY expiration to inspect strike density. Q8 and Q9 require reading the Antoinette and Yamin-Mitchell sources in the vault. All others require architectural decisions first.*

*Related: [tooling-requirements-maopm](tooling-requirements-maopm.md) · [research-agenda-options-maopm](research-agenda-options-maopm.md) · [gap-analysis-2026-06-03](gap-analysis-2026-06-03.md) · [synthesis-2026-05-17](synthesis-2026-05-17.md)*
