---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-023
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/023-range-planner-devnet-scaling-and-containment.md
bot_commit: 93d497d
source_sha256: 4d4d7aa72472483db523f11045fe491a5086cfddafd0b04894d83f000e264786
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/023-range-planner-devnet-scaling-and-containment.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-023-range-planner-devnet-scaling-and-containment|ADR-023]] — Range Planner Devnet Scaling and Containment

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** Deribit GEX walls are USD-denominated, but the Devnet Meteora pool uses a quote token detached from USD: approximately 1 SOL = 6.9M pool-quote units. Directly mapping a `$105` USD wall to this pool produces bins thousands of steps away from the active market. Separately, the deployment adapter accepts range plans without checking whether the reconciled active bin is inside the requested interval, allowing an out-of-range deployment plan to proceed.
- **Decision 1 (Containment Safeguard):** The DLMM deploy adapter must verify that the reconciled `activeBinId` is contained in the requested range, using the inclusive condition `activeBinId >= lowerBinId && activeBinId <= upperBinId`, before building or simulating any transaction. If the condition fails, deployment is refused with a descriptive failure reason.
- **Decision 2 (Wall Scaling):** The range planner must scale the USD-denominated GEX walls into the pool's native quote space before calculating target bins. Given the pool active-bin price in pool quote units per SOL and the off-chain Deribit spot price in USD per SOL, multiply each wall strike by `poolActiveBinPrice / spotOffchain_t`, then pass the scaled walls through the existing decimal-aware price-to-bin conversion.
- **Consequences:** Devnet wall anchors and EV AMM pricing share one pool-native coordinate system, while the deploy adapter refuses plans that do not contain current market liquidity. The planner needs both pool and off-chain spot facts, and deployment tests must prove the containment check happens before transaction construction.
- **Alternatives rejected:** Map raw USD walls directly into pool bins — preserves the discovered numeraire error; let the adapter repair or clamp an out-of-range plan — silently changes approved intelligence; check containment only after building a transaction — too late to prevent an invalid simulation or submission; use a fixed Devnet conversion constant — fails on other pools and hides the required price relationship.
