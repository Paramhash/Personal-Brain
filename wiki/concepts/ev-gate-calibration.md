---
domain: cl-market-making
tags:
- ev-gate
- calibration
- lvr
- hedge-drag
- dlmm
- volatility-forecasting
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- 2ad443febab32531
---
# EV gate calibration
**In one line:** The process of evaluating and adjusting the parameters and form of the [[ev-gate]] model to ensure its expected value (EV) cost estimates accurately reflect simulated or realized performance.
## Intuition
An [[ev-gate]] serves as a critical decision point for deploying or rebalancing liquidity in a [[cl-market-making]] strategy. If its cost estimates (such as [[loss-versus-rebalancing|LVR]] and [[hedge-drag]]) are systematically biased, the gate will make suboptimal decisions, potentially leading to reduced profitability or increased risk. Calibration ensures that the model's internal logic aligns with observed market behavior and the specific mechanics of the liquidity pool.
## Mechanism / math
The calibration process typically involves:
1.  **Comparison to a high-fidelity simulator:** Model-predicted costs (e.g., LVR, hedge drag) are compared against results from a detailed simulator that mimics real-world market and protocol dynamics.
2.  **Testing alternative inputs and formulations:** Different parameters or mathematical forms for key model components are tested. For instance, comparing [[rho-0]] (instantaneous density) against [[rho-bar]] (life-averaged density) to assess shape dependence.
3.  **Identifying sources of discrepancy:** Analyzing the differences between model and simulator to pinpoint specific biases. This can include:
    *   **Shape dependence:** How the model's accuracy varies with the shape of the liquidity distribution.
    *   **[[sigma-forecast-error]]**: The impact of inaccurate [[volatility-forecasting]] on cost estimates.
    *   **Pool-specific characteristics**: Deviations from idealized market assumptions, such as the pool's [[realized-volatility]] differing from external spot markets, or the presence of a [[burst-factor]] in price movements.
4.  **Model refinement:** Adjusting model components, introducing new parameters (like [[rho-bar]]), or applying scaling factors based on the identified biases.
## Where it matters
Accurate [[ev-gate-calibration]] directly informs the reliability of the [[ev-gate]]'s decision-making. It ensures that the gate's hurdle rate for deploying or rebalancing liquidity is realistic, thereby optimizing the profitability and risk management of [[cl-market-making]] strategies. Without proper calibration, the bot might deploy liquidity when it shouldn't, or fail to deploy when it should, leading to suboptimal capital allocation.
## Evidence and limits
The source details a calibration effort for a DLMM [[ev-gate]] model. Initially, the model failed against its D2 criteria (defined in [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]) due to the shape dependence of [[rho-0]] and an overstatement of costs. Subsequent analysis revealed that the pool's [[realized-volatility]] was lower than the external spot market's, and its price movements exhibited a [[burst-factor]]. Incorporating these pool-specific properties, along with adopting [[rho-bar]], brought the model's LVR and hedge drag estimates into close agreement with simulator results (within 2-3%). The process is iterative, requiring re-validation with more data and careful consideration of how to handle [[sigma-forecast-error]].
## Related
[[ev-gate]]
[[loss-versus-rebalancing]]
[[hedge-drag]]
[[rho-0]]
[[rho-bar]]
[[burst-factor]]
[[sigma-forecast-error]]
[[realized-volatility]]
[[cl-market-making]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]
[[adr-047-provisional-sigma-estimator]]