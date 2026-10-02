---
domain: cl-market-making
tags: []
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- d27d1f034ca70cd3
---
# Automated Market Making and Loss-Versus-Rebalancing (Milionis et al., 2026)
**Type:** paper
## Claim
This paper proposes a continuous-time model to decompose Automated Market Maker (AMM) Liquidity Provider (LP) returns into two components: a "beta-like" component reflecting market risk exposure (captured by a [[rebalancing-strategy]]), and an "alpha-like" component reflecting microstructural forces (accrued fees minus losses to arbitrageurs, quantified by [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]]). The empirical analysis of the [[uniswap-v2]] ETH-USDC pool shows that over 99.991% of LP return variance is driven by beta exposure, highlighting the critical need to hedge market risk for meaningful microstructural analysis.
## Method and data
The authors develop a continuous-time model where a risky asset's price follows a geometric Brownian motion, and an infinitely deep [[centralized-exchange|CEX]] exists alongside the AMM. Arbitrageurs frictionlessly trade between the AMM and CEX, while [[noise-traders-amm|noise traders]] contribute fees. LP returns are decomposed using a [[pool-value-function]] and a [[rebalancing-strategy]] that mimics AMM asset holdings at CEX prices.

Empirical analysis is conducted on the [[uniswap-v2]] WETH-USDC trading pair from August 1, 2021, to July 31, 2022. Data includes minute-level USDC-ETH prices from Binance API and Uniswap v2 pool data (holdings, mints, burns, trades) from Dune Analytics. Realized volatility is estimated from Binance prices.
## Key results
*   **LP P&L Decomposition:** LP P&L = Beta-like (market risk) + Alpha-like (microstructural forces: fees - arbitrage losses).
*   **Dominance of Market Risk:** For the [[uniswap-v2]] ETH-USDC pool, 99.991% of LP return variance is driven by the "beta-like" exposure to ETH prices. The "alpha-like" component (fees minus adverse selection costs) accounts for only 0.009% of the variance.
*   **Rebalancing Strategy:** This strategy effectively hedges market risk. Subtracting its profits from raw LP P&L reduces variance by four orders of magnitude. Higher rebalancing frequencies (e.g., 1 minute) lead to lower P&L volatility, converging to fees minus LVR.
*   **Critique of [[impermanent-loss|Impermanent Loss (IL)]]:** The common "one-interval" IL metric is problematic because it is non-additive, path-independent, and conflates market risk with microstructural effects. It fails to remove market risk effectively.
*   **Superiority of LVR:** [[loss-versus-rebalancing|LVR]] is additive, path-dependent (reflects volatility), and cleanly separates market risk from microstructural effects. The "many-interval" IL metric (with periodically updated holdings) is equivalent to LVR.
*   **Implications for Research:** Empirical studies of AMM LP returns must hedge out market risk (using [[rebalancing-strategy|rebalancing strategies]]) to avoid results predominantly reflecting market risk rather than microstructural effects. Failure to do so can lead to significantly larger standard errors and omitted-variable bias.
## Assumptions and limits
*   Continuous-time model with geometric Brownian motion for risky asset prices.
*   Infinitely deep [[centralized-exchange|CEX]] with zero fees.
*   Arbitrageurs pay no fees (relaxed in empirical section).
*   LPs are passive (no mint/burn in model, relaxed in empirical section).
*   Noise traders contribute fees in numéraire (relaxed in empirical section where fees are reinvested).
*   Ignores blockchain transaction fees ("gas" fees) and discrete-time nature of block updates.
*   The model is stylized to motivate decomposition, not an equilibrium model of AMM liquidity.
## Concepts introduced or used
[[automated-market-maker]], [[liquidity-provider]], [[loss-versus-rebalancing]], [[rebalancing-strategy]], [[alpha-like-component-lp-returns]], [[beta-like-component-lp-returns]], [[impermanent-loss]], [[constant-function-market-maker]], [[pool-value-function]], [[marginal-liquidity-amm]], [[rebalancing-arbitrage]], [[noise-traders-amm]], [[loss-versus-holding]], [[markouts]], [[uniswap-v2]], [[uniswap-v3]], [[centralized-exchange]], [[market-risk]], [[slippage]], [[delta_hedging]], [[hodl-benchmark]]