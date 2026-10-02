---
domain: cl-market-making
tags:
- decision-making
- risk-management
- strategy
- dlmm
- decision-rule
- cost-model
- lvr
- hedging
- cost-accounting
- deployment-strategy
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- f7c0b952395e5ec2
- c2e2733d54ebecd9
- ad664e0ecbe2b439
updated: '2026-10-02'
sources:
- dlmm-ev-gate-calibration-2026-10-01.md
- dlmm-ev-gate-vs-simulator-2026-10-01.md
- dlmm-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are.md
---
# EV gate
**In one line:** A decision-making component within a [[cl-market-making]] bot that evaluates the expected value (EV) of a proposed liquidity deployment or rebalancing action against a predefined hurdle rate.
## Intuition
The EV gate acts as a filter or a "go/no-go" switch for strategic actions. Before a bot commits capital or adjusts an existing position, the EV gate calculates the expected profitability and costs associated with that action. If the expected value exceeds a certain threshold (the hurdle rate), the action is approved; otherwise, it is rejected. This prevents the bot from making unprofitable or excessively risky moves.
## Mechanism / math
The EV gate typically calculates the expected value by considering various factors, including:
*   **Expected Fees:** Projected fee generation from the new or adjusted position.
*   **[[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]]:** The expected cost incurred due to arbitrageurs rebalancing the pool.
*   **[[hedge-drag|Hedge Drag]]:** The costs associated with hedging the inventory exposure of the liquidity position.
*   **[[risk-premium|Risk Premium]]:** Any additional premium required for taking on specific risks.
*   **[[transaction-costs|Transaction Costs]]:** Costs associated with deploying or withdrawing liquidity.
*   **[[sol-rent-reserve|Deployment Rent]]:** Costs associated with maintaining the position on-chain.

The decision rule is often:
$$ \text{Expected Value} \ge \text{Hurdle Rate} $$
The hurdle rate itself can be dynamic, reflecting the [[economic-hurdle-rate-cl|cost of capital]] or desired minimum return.
## Where it matters
The [[ev-gate]] is central to the autonomous operation of a [[cl-market-making]] bot. It ensures that all liquidity management decisions are economically rational and align with the bot's profitability and risk objectives. It acts as a safeguard against deploying capital into unfavorable market conditions or configurations.
## Evidence and limits
The design and calibration of the [[ev-gate]] are critical. As detailed in [[dlmm-2026-ev-gate-calibration]], initial formulations of the EV gate model can suffer from inaccuracies, such as:
*   **Shape dependence:** The model's cost estimates (e.g., LVR, hedge drag) may vary systematically depending on the shape of the liquidity distribution (e.g., "Spot", "Curve", "BidAsk"). This was observed with the [[rho-0]] density measure.
*   **Overstatement of costs:** The model might systematically overestimate costs like [[hedge-drag]] if it doesn't accurately account for specific pool dynamics, such as lower [[realized-volatility]] compared to spot markets or [[burst-factor|bursty price movements]].
*   **[[sigma-forecast-error]]**: The accuracy of the EV gate is highly sensitive to the quality of its [[volatility-forecasting]]. Errors in predicting future volatility can lead to significant discrepancies between expected and realized outcomes.

Calibration efforts, such as those described in [[dlmm-2026-ev-gate-calibration]], are necessary to refine the EV gate's components (e.g., adopting [[rho-bar]]) and ensure its estimates align with simulated or real-world performance. The [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] outlines the pricing of range-dependent LVR and hedge costs within the EV gate.
## Related
[[cl-market-making]]
[[decision-gate-cl-bot]]
[[economic-hurdle-rate-cl]]
[[loss-versus-rebalancing]]
[[hedge-drag]]
[[rho-0]]
[[rho-bar]]
[[burst-factor]]
[[sigma-forecast-error]]
[[realized-volatility]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]
[[adr-046-real-time-hurdle-rate-restates-the-ev-gate]]
[[dlmm-2026-ev-gate-calibration]]

## Update from dlmm-ev-gate-vs-simulator-2026-10-01.md (2026-10-02)

# EV gate
**In one line:** A decision gate within the DLMM system that evaluates the expected value (EV) of a [[cl-position|concentrated liquidity position]] to determine if it should be deployed or maintained.
## Intuition
The EV gate acts as a primary [[risk-guardrails|risk guardrail]] for [[dlmm-hedge-bot|DLMM bots]], ensuring that only positions with a positive expected value, exceeding a defined [[economic-hurdle-rate-cl|hurdle rate]], are allowed. It aims to prevent the deployment of unprofitable liquidity.
## Mechanism / math
The EV gate calculates `net_ev = fees − LVR − funding − rent`.
Historically, the LVR term in the EV gate (`evCalculator.ts`) was calculated as:
$$ LVR_{gate} = \left(\frac{\sigma_s^2 \cdot 3600}{8}\right) \cdot 1.8 \cdot 24 \text{ h} = 0.225 \cdot \sigma_d^2 $$
where $\sigma_s$ is the per-second volatility, $\sigma_d$ is the daily volatility, and $1.8$ is the `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER`. This formula effectively treats the position as nearly full-range, similar to [[uniswap-v2|Uniswap v2]]'s LVR, scaled by a fixed concentration multiplier.

A significant limitation identified in 2026 was the absence of a dedicated [[hedge-drag|hedge-cost]] term in the `net_ev` calculation, meaning the cost of maintaining a [[delta_hedging|delta-neutral]] position was not factored in.
## Where it matters
The [[ev-gate]] is critical for:
*   **Deployment decisions:** It determines whether a new [[cl-position]] is economically viable.
*   **Position management:** It can inform decisions to adjust or exit existing positions if their expected value falls below the hurdle.
*   **Risk control:** It serves as a fundamental layer of [[risk-management-team-agent|risk management]] by filtering out potentially loss-making deployments.

The accuracy of the EV gate's cost model directly impacts the profitability of [[cl-market-making]] strategies. Inaccurate cost estimations can lead to the deployment of positions that are unprofitable in reality, despite passing the gate.
## Evidence and limits
A 2026 analysis comparing the [[ev-gate]] to a [[dlmm-simulator]] and a more detailed model ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]) revealed significant limitations:
*   **LVR Underestimation:** The gate's LVR calculation was found to be approximately 48 times lower than a more accurate model for a typical 202-bin concentrated range. This is because the fixed [[dlmm-concentration-multiplier]] (1.8) does not adequately capture the actual [[rho-bar|value density]] of a concentrated position, which can be much higher.
*   **Missing Hedge Cost:** The gate completely lacked a term for [[hedge-drag|hedge costs]], which can be substantial (e.g., 110–190 bps/day for narrow ranges with high gamma).
*   **Consequence:** With these flaws, the [[ev-gate]] could approve positions that the simulator estimates would lose 150–240 bps/day, especially if measured [[fee-yield]] (e.g., 80–141 bps/day) were ratified without correcting the cost side.

[[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] acknowledged the LVR gap but intentionally kept the gate unchanged, pending further evidence and a more comprehensive fix. [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] was proposed to address these issues by incorporating range-dependent LVR and hedge costs.
## Related
[[economic-hurdle-rate-cl]], [[loss-versus-rebalancing]], [[hedge-drag]], [[dlmm-simulator]], [[dlmm-concentration-multiplier]], [[rho-bar]], [[cl-position]], [[risk-guardrails]], [[adr-046-real-time-hurdle-rate-restates-the-ev-gate]], [[adr-050-fee-yield-from-on-chain-bin-fee-counters]], [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]], [[blueprint-ev-policy]], [[blueprint-risk-guardrails]], [[dlmm-2026-ev-gate-vs-simulator]]

## Update from dlmm-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are.md (2026-10-02)

# EV Gate
**In one line:** A decision mechanism within the DLMM bot that evaluates the expected value (EV) of a potential liquidity deployment against its costs, authorizing or refusing capital allocation based on an economic hurdle rate.
## Intuition
The EV gate acts as a financial bouncer for capital deployments. Before the bot puts money into a liquidity pool, the gate checks if the expected returns from that deployment are high enough to cover all the associated costs and still provide a positive economic value. If the costs outweigh the expected benefits, the gate refuses the deployment.
## Mechanism / math
The [[ev-gate]], implemented in `src/decision/ev/evCalculator.ts`, takes various cost estimators and expected returns into account to determine the net expected value of a deployment. It compares this `net_ev` against an [[economic-hurdle-rate-cl]].

Initially, the EV gate's cost inputs included transaction and priority fees (represented by `gasFees` and a `PLACEHOLDER_DEPLOY_LAMPORTS`), but critically omitted a term for **sunk [[solana-rent]]**, specifically for bin-array initialization. This omission meant that the gate was blind to a significant, non-recoverable cost, especially for wider ranges.

The issue was addressed by [[adr-040-sunk-deployment-rent-is-an-ev-term]], which introduced `deploy_rent_sunk` into the EV inputs. This term is computed by `src/config/deployRentModel.ts` from the planned bin range and includes only the non-recoverable bin-array rent and associated fees, explicitly excluding recoverable position and ATA rent. The amortization policy for this sunk cost was set to charge the full amount against a single deployment (`deployRentAmortizationDeployments = 1`), a policy explicitly marked as UNRATIFIED.

The placeholder for transaction fees was also refined from `PLACEHOLDER_DEPLOY_LAMPORTS` to `PLACEHOLDER_DEPLOY_TX_LAMPORTS_PER_CHUNK` and made to scale with the number of transaction chunks required for a deployment. The `deploy_rent_sunk` term is subtracted directly from `net_ev` at a 1.0x multiplier, rather than being added to a friction budget with a safety margin, because it represents an exact arithmetic cost rather than an estimated variable cost.
## Where it matters
The EV gate is a core component of the [[cl-market-making]] strategy, informing critical decisions such as:
-   **Deployment Authorization**: Whether to proceed with a planned liquidity deployment.
-   **Range Width Selection**: Indirectly influences the perceived cost-effectiveness of different [[range-planning|range widths]].
-   **Capital Efficiency**: Ensures that capital is only deployed when it meets a minimum economic threshold.

Accurate cost accounting within the EV gate is paramount to prevent [[negative-economics-exit|deployments with negative expected value]] and to ensure the long-term profitability of the bot.
## Evidence and limits
The `[[dlmm-2026-ev-gate-no-rent-term]]` finding highlighted a significant flaw where the omission of sunk [[solana-rent]] caused wider ranges to appear 1,429x to 5,001x cheaper than their true cost. This bias could have led to economically unsound deployments if not for the fact that the EV estimators were uncalibrated placeholders at the time. The fix implemented via [[adr-040-sunk-deployment-rent-is-an-ev-term]] corrected this missing term, but the underlying EV estimators still require calibration before the gate can make fully informed economic judgments.
## Related
[[economic-hurdle-rate-cl]], [[solana-rent]], [[dlmm-bins]], [[range-planning]], [[adr-040-sunk-deployment-rent-is-an-ev-term]], [[adr-039-deploy-reserve-is-derived-from-the-plan]], [[cl-entry-strategy]], [[cl-provider-strategy]]
