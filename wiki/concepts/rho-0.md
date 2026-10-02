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
- 3ac82f1dcb331f77
---
# Rho(0)
**In one line:** An instantaneous density measure used in the initial formulation of the [[ev-gate]] model, calculated as the active-bin weight divided by the log step.
## Intuition
[[rho-0]] represents the immediate concentration of liquidity at the current price point within a [[dlmm-bins|DLMM pool]]. It's a localized measure of how much liquidity is available precisely where the price is trading, intended to inform the expected interaction with price movements.
## Mechanism / math
The calculation for [[rho-0]] is given by:
$$ \rho(0) = \frac{\text{active-bin weight}}{\text{log step}} $$
Where:
*   `active-bin weight` refers to the proportion of total liquidity concentrated in the currently active price bin.
*   `log step` is the logarithmic increment between price bins.
## Where it matters
[[rho-0]] was initially used within the [[ev-gate]] model to estimate components of [[loss-versus-rebalancing|LVR]] and [[hedge-drag]]. Its accuracy directly influenced the [[ev-gate]]'s assessment of the profitability and costs associated with deploying liquidity.
## Evidence and limits
The [[dlmm-2026-ev-gate-calibration|EV gate calibration]] effort confirmed that [[rho-0]] exhibits significant shape dependence. It was found to systematically overstate costs for "Curve" shaped liquidity profiles and understate them for "BidAsk" profiles. This inconsistency led to inaccurate [[ev-gate]] estimations, highlighting its limitation as a universal density measure for diverse liquidity shapes. Consequently, its replacement by [[rho-bar]] was recommended to achieve more robust and shape-independent cost estimations.
## Related
[[ev-gate]]
[[rho-bar]]
[[dlmm-bins]]
[[liquidity-concentration]]
[[ev-gate-calibration]]
[[loss-versus-rebalancing]]
[[hedge-drag]]