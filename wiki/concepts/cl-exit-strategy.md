---
domain: cl-market-making
tags:
- risk-management
- decision-making
- capital-preservation
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 92aac8fbe2802ebc
---
# CL Exit Strategy
**In one line:** A predefined set of conditions and procedures for safely withdrawing a [[cl-position]] before it incurs significant losses or becomes economically unviable.
## Intuition
Exiting a position is as critical as entering one. A robust exit strategy ensures that the bot can proactively de-risk, preserve capital, and avoid forced liquidations or prolonged periods of negative expected returns. It's about knowing when to cut losses or reallocate capital.
## Mechanism / math
Exit is triggered by three main conditions:
1.  **[[boundary-threat-exit]]:** When the projected price path can cross a [[market-boundaries-cl]] before a safe execution is possible.
2.  **[[negative-economics-exit]]:** When projected fees no longer cover projected [[lvr-and-impermanent-loss|LVR]], funding, and exit/redeployment costs.
3.  **[[regime-deterioration-exit]]:** When off-chain [[gamma-exposure-gex]] signals indicate a likely [[market-regime-transition]], especially near the [[zero-gamma-level]] or during sharp volatility increases.

The exit process is followed by a [[cl-closing-procedure]].
## Where it matters
This strategy is paramount for capital preservation and overall risk management. It prevents the bot from holding onto positions that are either too risky (e.g., approaching liquidation) or no longer economically justified. It allows for dynamic adaptation to changing market conditions and protects the bot's long-term profitability.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] dedicates a section to "Exit Strategy," detailing these three triggers and emphasizing that exit should occur *before* a dangerous boundary is reached. This highlights its proactive nature. The effectiveness relies on accurate projections and reliable market signals.
## Related
[[cl-position]]
[[boundary-threat-exit]]
[[negative-economics-exit]]
[[regime-deterioration-exit]]
[[cl-closing-procedure]]
[[blueprint-risk-guardrails]]
[[m11-strategic-lps-and-the-decision-rule]]