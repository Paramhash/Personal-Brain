---
domain: cl-market-making
tags:
- dlmm
- lvr
- cost-model
- placeholder
- concentrated-liquidity
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-vs-simulator-2026-10-01.md
ingest_hashes:
- 54180f920bea6b7d
---
# DLMM Concentration Multiplier
**In one line:** A fixed placeholder constant (1.8) used in the DLMM [[ev-gate]]'s [[loss-versus-rebalancing|LVR]] calculation to approximate the effect of [[liquidity-concentration|concentrated liquidity]].
## Intuition
In [[constant-function-market-maker|CFMMs]] like [[uniswap-v2]], [[loss-versus-rebalancing|LVR]] is often approximated by a formula that doesn't explicitly account for the concentration of liquidity. For [[dlmm-bins|concentrated liquidity]] protocols, the LVR is significantly higher for narrow ranges. The `DLMM_CONCENTRATION_MULTIPLIER` was introduced as a simple scaling factor to adjust the basic LVR formula to reflect this increased cost, without needing to dynamically calculate the actual [[rho-bar|value density]] of the position.
## Mechanism / math
The [[ev-gate]]'s LVR calculation historically used the following formula:
$$ LVR_{gate} = \left(\frac{\sigma_s^2 \cdot 3600}{8}\right) \cdot \text{PLACEHOLDER\_DLMM\_CONCENTRATION\_MULTIPLIER} \cdot 24 \text{ h} $$
where `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER` was set to 1.8. This is equivalent to taking [[uniswap-v2]]'s full-range LVR ($\frac{1}{8}\sigma_d^2$) and multiplying it by 1.8.
This implies an effective [[rho-bar]] of 0.45 in the gate's calculation, as a more accurate model for concentrated LVR is $\frac{1}{2}\sigma_d^2 \rho$.
## Where it matters
*   **Cost Estimation:** This multiplier directly influences the [[loss-versus-rebalancing|LVR]] component of the [[ev-gate]]'s total cost calculation.
*   **Decision Accuracy:** The accuracy of this placeholder is critical for the [[ev-gate]] to correctly assess the profitability of [[cl-position|concentrated liquidity positions]].
## Evidence and limits
A 2026 analysis comparing the [[ev-gate]]'s cost model to a [[dlmm-simulator]] and a more detailed model revealed that the fixed `DLMM_CONCENTRATION_MULTIPLIER` of 1.8 led to a severe underestimation of [[loss-versus-rebalancing|LVR]]. For a typical 202-bin concentrated liquidity position, the actual [[rho-bar|value density]] was approximately 21.7, meaning the gate's LVR calculation was about **48 times lower** than what a more accurate model would yield.

The documentation for the constant itself noted that "a constant does not vary with the range the planner actually chose, which is the term's whole point," acknowledging its limitation. This finding underscored the necessity of replacing the fixed multiplier with a dynamic calculation of [[rho-bar]] based on the planned range to ensure accurate cost estimation and prevent the approval of unprofitable positions. [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] was proposed to address this.
## Related
[[ev-gate]], [[loss-versus-rebalancing]], [[rho-bar]], [[dlmm-bins]], [[liquidity-concentration]], [[dlmm-simulator]], [[uniswap-v2]], [[constant-function-market-maker]], [[dlmm-2026-ev-gate-vs-simulator]], [[adr-046-real-time-hurdle-rate-restates-the-ev-gate]], [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]