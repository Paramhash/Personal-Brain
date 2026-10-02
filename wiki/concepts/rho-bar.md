---
domain: cl-market-making
tags:
- ev-gate
- liquidity-density
- dlmm
- lvr
- hedge-drag
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- 6a9c4c0fc9e6e082
---
# Rho-bar
**In one line:** A shape-independent, life-averaged density measure used in the refined [[ev-gate]] model, derived from the occupation density of driftless Brownian motion killed at the range edges.
## Intuition
Unlike [[rho-0]], which provides an instantaneous measure of liquidity density, [[rho-bar]] offers a more robust and representative measure over the entire expected lifetime of a liquidity position within its defined price range. It accounts for the probability of the price moving across the range, making its estimate of density less sensitive to the specific shape of the liquidity distribution at any given moment. This leads to more consistent cost estimations across different liquidity profiles.
## Mechanism / math
The density for [[rho-bar]] is modeled as a tent-shaped Green's function for driftless Brownian motion within a defined range:
$$ g(u) = \begin{cases} (u-a) \cdot b & \text{for } u \le 0 \\ (-a) \cdot (b-u) & \text{for } u \ge 0 \end{cases} $$
Where:
*   `u` represents the price.
*   `a` and `b` are parameters defining the range and the peak of the density function.
This formulation provides a closed-form, derived (not fitted) measure of average density.
## Where it matters
[[rho-bar]] is crucial for improving the accuracy and consistency of [[ev-gate]] cost estimations by effectively removing the shape dependence observed with [[rho-0]]. Its adoption is a key recommendation for the [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] update, enabling the [[ev-gate]] to make more reliable decisions regardless of the specific liquidity shape deployed.
## Evidence and limits
The [[dlmm-2026-ev-gate-calibration|EV gate calibration]] effort confirmed that adopting [[rho-bar]] successfully removes the shape dependence in [[loss-versus-rebalancing|LVR]] and [[hedge-drag]] cost estimations. This resulted in the model's output ratios for "Spot", "Curve", and "BidAsk" liquidity shapes converging to a common residual bias, demonstrating its effectiveness in providing a more reliable and consistent measure of liquidity density.
## Related
[[ev-gate]]
[[rho-0]]
[[dlmm-bins]]
[[liquidity-concentration]]
[[ev-gate-calibration]]
[[loss-versus-rebalancing]]
[[hedge-drag]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]