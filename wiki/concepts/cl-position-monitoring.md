---
domain: cl-market-making
tags:
- real-time-data
- risk-management
- decision-making
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 1ff83a4cb5cd72be
---
# CL Position Monitoring
**In one line:** The continuous tracking of various market metrics and internal bot states while a [[cl-position]] is active, providing essential data for risk management and operational decisions.
## Intuition
An active [[cl-position]] is dynamic and exposed to constant market fluctuations. Continuous monitoring is like the bot's "eyes and ears," providing real-time awareness of its exposure, profitability, and proximity to critical thresholds. This information is vital for making timely decisions about rebalancing, hedging, or exiting the position.
## Mechanism / math
While a [[cl-position]] is open, the bot continuously tracks:
*   Active bin and pool price.
*   Distance to both [[market-boundaries-cl]].
*   [[volatility]].
*   [[gex-regime]] and [[zero-gamma-level]].
*   Fees earned.
*   Projected [[lvr-and-impermanent-loss|LVR]].
*   Hedge error (deviation from [[cl-hedge-target]]).
*   Remaining [[sol-inventory]] and [[usdc-inventory]] reserves.
*   Expected net equity.
## Where it matters
This monitoring process is fundamental for informing the [[cl-rebalancing-condition]] and the [[cl-exit-strategy]]. It enables the bot to react proactively to changing market conditions, maintain its desired risk profile, and optimize its performance. Without robust monitoring, the bot would operate blindly, increasing the risk of significant losses.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] dedicates a section to "While the Position Is Open," detailing the metrics the bot should continuously track. This underscores its importance for ongoing management. The effectiveness of monitoring depends on the reliability and timeliness of the data feeds and the accuracy of internal calculations.
## Related
[[cl-position]]
[[cl-rebalancing-condition]]
[[cl-exit-strategy]]
[[cl-hedge-target]]
[[gamma-exposure-gex]]
[[volatility]]
[[lvr-and-impermanent-loss]]
[[zero-gamma-level]]
[[blueprint-monitor]]
[[blueprint-observability-contract]]