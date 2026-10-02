---
domain: cl-market-making
tags:
- impermanent-loss
- lp-returns
- adverse-selection
- slippage
- market-making-theory
- amm
- rebalancing
- arbitrage
- concentrated-liquidity
aliases:
- LVR
- loss-versus-rebalancing
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 1006c9cea827fd79
- e7e416a2408df14d
updated: '2026-10-02'
sources:
- dlmm-amm-and-loss-versus-rebalancing.pdf
- dlmm-ev-gate-vs-simulator-2026-10-01.md
---
# Loss-Versus-Rebalancing
**In one line:** A metric that quantifies the cumulative losses incurred by Automated Market Maker (AMM) [[liquidity-provider|LPs]] due to [[slippage]] from [[rebalancing-arbitrage|arbitrageurs]], representing the "alpha-like" microstructural component of LP returns after accounting for market risk.
## Intuition
When external market prices move, an AMM's quotes become "stale." [[rebalancing-arbitrage|Arbitrageurs]] exploit these stale quotes by trading with the AMM at worse-than-market prices and immediately rebalancing on a [[centralized-exchange|CEX]]. This systematic loss to arbitrageurs is what LVR measures. It is the cost of providing liquidity and passively rebalancing in response to price changes.
## Mechanism / math
LVR is formally defined as the difference between the value of the [[rebalancing-strategy]] ($R_t$) and the actual value of the AMM pool ($V_t$):
$$LVR_t \triangleq R_t - V_t$$
The instantaneous LVR, $l(\sigma, P)$, is given by:
$$l(\sigma, P) = \frac{\sigma^2 P^2}{2} |x^{*'}(P)| \ge 0$$
where $\sigma$ is the instantaneous volatility of the risky asset, $P$ is its price, and $|x^{*'}(P)|$ is the absolute value of the [[marginal-liquidity-amm|marginal liquidity]] (the second derivative of the [[pool-value-function|pool value function]] with respect to price).

LVR is always positive, non-negative, non-decreasing, and predictable. It represents the cumulative profits of rebalancing arbitrageurs.
## Where it matters
*   **LP Profitability Analysis:** LVR is a crucial metric for understanding the true microstructural costs of providing liquidity in AMMs, isolating these costs from general [[market-risk]].
*   **Superiority over [[impermanent-loss|Impermanent Loss (IL)]]:** Unlike traditional [[impermanent-loss|IL]] metrics, LVR is additive over time, path-dependent (reflecting volatility), and cleanly separates market risk from microstructural effects. This makes it a more robust and economically meaningful measure for empirical research.
*   **AMM Design:** LVR is directly influenced by the AMM's [[bonding-function|bonding function]] curvature (via [[marginal-liquidity-amm|marginal liquidity]]) and market volatility. This provides insights for designing AMMs that aim to reduce or eliminate adverse selection losses.
*   **Hedging Effectiveness:** The "alpha-like" component of LP returns is defined as accrued fees minus LVR ($FEE_t - LVR_t$), representing the net microstructural profit.
## Evidence and limits
*   **Empirical Relevance:** For [[uniswap-v2]] ETH-USDC, the "alpha-like" component (fees minus LVR) accounts for only 0.009% of the total variance in unhedged LP P&L, highlighting the dominance of market risk.
*   **General Applicability:** The LVR framework applies to any AMM with a locally-smooth demand curve, including [[constant-function-market-maker|CFMMs]] and concentrated liquidity AMMs like [[uniswap-v3]].
*   **Relationship to Options:** Expected LVR can be thought of as the value of European options given away by LPs, as AMM LP positions are analogous to short option positions.
## Related
[[rebalancing-strategy]], [[impermanent-loss]], [[alpha-like-component-lp-returns]], [[beta-like-component-lp-returns]], [[constant-function-market-maker]], [[pool-value-function]], [[marginal-liquidity-amm]], [[rebalancing-arbitrage]], [[slippage]], [[uniswap-v2]], [[uniswap-v3]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]

## Update from dlmm-ev-gate-vs-simulator-2026-10-01.md (2026-10-02)

# Loss-Versus-Rebalancing
**In one line:** The opportunity cost incurred by a liquidity provider (LP) due to arbitrageurs rebalancing their position in response to price movements, often considered a component of [[impermanent-loss]].
## Intuition
When the price of assets in an Automated Market Maker (AMM) changes, arbitrageurs step in to rebalance the pool to match the external market price. This rebalancing activity effectively "sells" the appreciating asset and "buys" the depreciating asset from the LP's position. The [[loss-versus-rebalancing|LVR]] quantifies the value extracted by these arbitrageurs, representing a cost to the LP. It's the difference between the value of holding the initial assets (HODL) and the value of the AMM position after rebalancing.
## Mechanism / math
For a [[constant-function-market-maker|CFMM]] like [[uniswap-v2]], the LVR over a period $T$ is often approximated by:
$$ LVR \approx \frac{1}{8} \sigma^2 T $$
where $\sigma$ is the volatility of the price.

For [[liquidity-concentration|concentrated liquidity]] AMMs like [[uniswap-v3]] or [[meteora]], the LVR becomes highly dependent on the specific price range chosen by the LP. The value density ($\rho$) of the position at the current price plays a crucial role. A more accurate model for concentrated liquidity LVR is given by:
$$ LVR = \frac{1}{2} \sigma_d^2 \rho $$
where $\sigma_d$ is the daily volatility and $\rho$ is the position's value density per unit log-price at the current price.

The [[ev-gate]] in the DLMM system initially used a simplified LVR calculation:
$$ LVR_{gate} = \left(\frac{\sigma_s^2 \cdot 3600}{8}\right) \cdot 1.8 \cdot 24 \text{ h} = 0.225 \cdot \sigma_d^2 $$
This formula applies [[uniswap-v2]]'s full-range LVR and multiplies it by a fixed [[dlmm-concentration-multiplier]] of 1.8, effectively assuming a constant value density. This simplification was found to significantly underestimate the actual LVR for narrow, concentrated ranges.
## Where it matters
*   **LP Profitability:** LVR is a direct cost that reduces an LP's net returns. Understanding and accurately estimating LVR is crucial for assessing the true profitability of providing liquidity.
*   **Range Selection:** The magnitude of LVR is highly sensitive to the chosen [[dlmm-bins|liquidity range]]. Narrower ranges, while offering higher [[fee-yield]] potential, also expose LPs to higher LVR due to increased [[rho-bar|value density]] and more frequent rebalancing.
*   **Strategy Design:** Effective [[cl-provider-strategy|LP strategies]] must account for LVR, either by seeking higher fees to offset it, or by dynamically adjusting ranges to minimize its impact.
*   **Risk Management:** Accurate LVR calculation is a core component of [[ev-gate|expected value]] models and [[economic-hurdle-rate-cl|hurdle rate]] calculations, informing decisions on when and where to deploy capital.
## Evidence and limits
A 2026 analysis comparing the DLMM [[ev-gate]]'s LVR calculation to a [[dlmm-simulator]] and a more detailed model revealed that the gate's fixed [[dlmm-concentration-multiplier]] led to an LVR estimate approximately **48 times lower** than the actual value density for a typical concentrated position. This significant underestimation meant the [[ev-gate]] was approving positions with much higher true LVR costs than it perceived.

The discrepancy highlights that simplified LVR models, especially those not accounting for the specific [[liquidity-concentration|concentration]] and [[rho-bar|value density]] of a position, can lead to severely flawed profitability assessments. The [[dlmm-simulator]] integrates LVR over the price path, providing a more realistic estimate by accounting for how value density changes as price drifts within and out of the LP's range.
## Related
[[impermanent-loss]], [[rebalancing-arbitrage]], [[fee-economics]], [[cl-position]], [[dlmm-bins]], [[rho-bar]], [[dlmm-concentration-multiplier]], [[ev-gate]], [[dlmm-simulator]], [[adr-046-real-time-hurdle-rate-restates-the-ev-gate]], [[dlmm-2026-ev-gate-vs-simulator]], [[m04-lvr-and-impermanent-loss]], [[m02-concentrated-liquidity-math]]
