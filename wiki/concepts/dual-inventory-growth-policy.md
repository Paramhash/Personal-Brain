---
domain: cl-market-making
tags:
- dlmm
- inventory-control
- market-making-strategy
- fee-economics
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-00-dual-inventory-growth-policy.md
ingest_hashes:
- 834df410e0fa0461
---
# Dual-Inventory Growth Policy
**In one line:** A strategy for concentrated liquidity market-making bots that targets positive growth in both base and quote assets independently, rather than just overall equity.
## Intuition
While maximizing total portfolio equity is a common objective, a market-making bot often needs to maintain and grow its holdings in *both* the base and quote assets to ensure continued operation and strategic flexibility. Price movements or uneven fee accrual can lead to an increase in total equity but a depletion of one asset, which is undesirable if the bot needs both for future deployments or other operations. This policy ensures that the bot's capital base in each token is preserved and ideally grown.
## Mechanism / math
The policy's objective is defined by:
$$
SOL_{close} > SOL_{start}
$$
and
$$
USDC_{close} > USDC_{start}
$$
while also preserving any required rent reserves.

This objective is stricter than merely maximizing equity ($E_t = SOL_t \cdot P_t + USDC_t$), as positive $\Delta E$ does not guarantee positive $\Delta SOL$ and $\Delta USDC$.

The policy involves:
1.  Maintaining a non-deployable reserve for operational costs (e.g., SOL rent).
2.  Deploying only surplus assets.
3.  Entering positions only when expected fees exceed all associated costs (LVR, hedge, gas, rent, slippage).
4.  Periodically harvesting fees.
5.  Converting harvested fee surplus to rebalance and meet growth targets for the asset that is lagging.
6.  Exiting positions before market boundaries become unsafe.
7.  Closing positions only if projected terminal inventory satisfies both growth constraints.
## Where it matters
This policy is critical for the long-term sustainability and strategic operation of concentrated liquidity market-making bots. It directly informs:
*   **Deployment decisions:** Whether to open a new liquidity position.
*   **Range width and placement:** Indirectly, by influencing the risk/reward calculation for expected asset growth.
*   **Fee harvesting and rebalancing:** Dictates when and how to convert earned fees to ensure balanced growth.
*   **Exit strategies:** Defines conditions under which a position should be closed.
## Evidence and limits
This is a policy document outlining a strategic objective for a specific bot, rather than a research paper presenting empirical evidence. Its effectiveness is contingent on accurate forecasting of fees, LVR, and other costs, as well as the ability to execute rebalancing and hedging efficiently.
## Related
[[zero-growth-baseline]], [[inventory-accounting]], [[equity-accounting]], [[decision-gate-cl-bot]], [[m07-inventory-and-market-making-theory|inventory control]], [[m05-fee-economics|fee economics]], [[dlmm-dual-inventory-growth-policy]]