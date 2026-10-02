---
domain: cl-market-making
tags:
- inventory-control
- stablecoin
- asset-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 8b2c73507a3b865e
---
# USDC Inventory
**In one line:** The amount of USDC (a stablecoin) held by a market-making bot, serving as stable operating capital and the primary accounting unit for its overall equity.
## Intuition
USDC provides a stable base for the bot's operations, insulating it from the volatility of assets like SOL. It is the preferred numeraire for measuring the bot's performance and equity, as its value is pegged to the US dollar.
## Mechanism / math
The [[usdc-inventory]] (`USDC_t`) is a component of the bot's total equity ($E_t$):
$$
E_t = SOL_t \cdot P_t + USDC_t
$$
where $SOL_t$ is the [[sol-inventory]] and $P_t$ is the price of SOL in USDC.
The strategy enforces a hard minimum constraint: `USDC_t >= USDC_min`.
## Where it matters
[[usdc-inventory]] is crucial for deploying liquidity into CL positions and for providing a stable reference point for profit and loss calculations. Maintaining sufficient USDC is a hard requirement for the bot's operational stability and its ability to participate in market-making activities. It acts as the primary capital for generating fees and is the benchmark against which the bot's performance is often measured.
## Evidence and limits
The source document, outlining the [[warehouse-manager-cl-inventory-strategy]], establishes [[usdc-inventory]] as the "primary accounting unit" and a "stable operating capital." It mandates minimum constraints to ensure the bot's ability to function. The strategy acknowledges that a CL position changes the composition of inventory, requiring reconciliation of USDC alongside SOL.
## Related
[[sol-inventory]]
[[cl-position]]
[[equity-accounting]]
[[inventory-accounting]]
[[cl-success-metrics]]