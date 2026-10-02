---
domain: cl-market-making
tags:
- strategy
- decision-making
- risk-management
- capital-allocation
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- b35f47a1d7993f1a
---
# CL Entry Strategy
**In one line:** The set of stringent conditions that must be satisfied before a concentrated liquidity position is deployed, ensuring operational safety, valid market conditions, and economic justification.
## Intuition
Entering a [[cl-position]] exposes the bot to risk and incurs costs. A robust entry strategy acts as a gatekeeper, preventing premature or ill-advised deployments. It ensures that the bot only commits capital when the expected returns outweigh the comprehensive costs and risks, and when its core operational reserves are secure.
## Mechanism / math
The [[cl-entry-strategy]] requires all of the following conditions to hold:
1.  [[sol-rent-reserve]] and [[sol-execution-reserve]] remain untouched.
2.  Both [[market-boundaries-cl]] (lower and upper) are valid.
3.  The active bin lies inside the [[buffered-policy-envelope]].
4.  The planned range satisfies minimum and maximum bin constraints.
5.  [[expected-fees-cl]] exceed the full [[economic-hurdle-rate-cl]]:
    $$
    \text{Expected fees} > \text{LVR} + \text{hedge funding} + \text{rent} + \text{gas} + \text{slippage} + \text{risk premium}
    $$
Capital deployment is further constrained by the [[capital-allocation-rule-cl]].
## Where it matters
This strategy is fundamental to the bot's overall risk management and profitability. By enforcing strict entry criteria, it minimizes the likelihood of deploying capital into unfavorable market conditions or jeopardizing operational continuity. It acts as a primary [[decision-gate-cl-bot]] for the market-making process.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] dedicates a section to "Entry Strategy," detailing these five conditions and the economic hurdle. This highlights its importance as a core policy. The effectiveness depends on the accuracy of the "Expected fees" and the comprehensive calculation of the "economic hurdle."
## Related
[[economic-hurdle-rate-cl]]
[[capital-allocation-rule-cl]]
[[market-boundaries-cl]]
[[buffered-policy-envelope]]
[[sol-rent-reserve]]
[[sol-execution-reserve]]
[[cl-position]]
[[blueprint-ev-policy]]
[[m11-strategic-lps-and-the-decision-rule]]