---
domain: cl-market-making
tags:
- hedging
- inventory-control
- risk-management
- delta-hedging
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 82cbe662946b5776
---
# CL Hedge Target
**In one line:** The desired amount of a hedging instrument (e.g., perpetual futures) to hold, aimed at offsetting the directional exposure of the [[sol-inventory]] within a [[cl-position]].
## Intuition
When a bot provides liquidity in a SOL/USDC pool, its [[cl-position]] will naturally accumulate more SOL as price falls and more USDC as price rises. This creates directional exposure to SOL. The [[cl-hedge-target]] aims to neutralize this exposure, protecting the bot's overall equity from large price swings in SOL that are not compensated by fees. It's a form of delta hedging for the inventory.
## Mechanism / math
The hedge target is defined as:
$$
q_t^* = -x_t
$$
where $q_t^*$ is the target quantity of the hedging instrument (e.g., short SOL perpetuals) and $x_t$ is the amount of SOL held by the [[cl-position]]. This implies a goal of maintaining a delta-neutral position with respect to the base asset inventory.
## Where it matters
This target is a core component of the bot's risk management strategy, specifically for mitigating [[inventory-risk]]. By actively hedging the [[sol-inventory]], the bot reduces its vulnerability to SOL price volatility, allowing it to focus on capturing fees from market-making. Deviations from this target trigger the [[cl-rebalancing-condition]].
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly states this formula for the hedge target, noting that it "protects the Bot's equity from excessive SOL directionality, but it does not remove LVR." This highlights its specific purpose and limitations. The strategy also specifies that during unwinding, the hedge must use the remaining inventory, not the original position inventory.
## Related
[[hedging-lp-exposure]]
[[perpetuals-and-funding]]
[[sol-inventory]]
[[cl-position]]
[[cl-rebalancing-condition]]
[[blueprint-hedge-engine]]
[[adr-051-inventory-objective-benchmark-hedge]]