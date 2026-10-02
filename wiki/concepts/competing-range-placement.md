---
domain: cl-market-making
tags:
- game-theory
- cl-market-making
- liquidity-concentration
- strategy
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-02-nash-equilibrium-cl-provider-strategies.md
ingest_hashes:
- cde8eede313a6553
---
# Competing Range Placement
**In one line:** A game-theoretic scenario where multiple concentrated liquidity providers (CLPs) independently choose their price ranges, leading to competition for trading volume and fee share.
## Intuition
When multiple LPs provide liquidity in the same pool, their decisions about where to place their liquidity ranges are interdependent. If all LPs choose the same narrow, high-fee range, they effectively dilute each other's fee earnings. This creates an incentive for LPs to differentiate their range placement or strategically react to competitors to maximize their individual returns.
## Mechanism / math
Each LP chooses a range ($R_i$) around the current price.
*   **Narrow range:** Offers high fee density when active but carries greater risk of being out-of-range and higher [[loss-versus-rebalancing|LVR]] exposure.
*   **Wide range:** Provides lower fee density but offers longer "survival" (time in range) and reduced redeployment frequency.
*   **Overlapping ranges:** LPs directly compete for the same trading volume.

A provider's fee share ($F_i$) can be approximated as:
$$
F_i = V \cdot f \cdot \frac{D_i(P_t)}{\sum_j D_j(P_t)}
$$
Where:
*   $V$: Total trading volume in the pool.
*   $f$: The pool's fee rate.
*   $D_i(P_t)$: Provider $i$'s active liquidity at the current price $P_t$.
*   $\sum_j D_j(P_t)$: Total active liquidity from all providers at price $P_t$.

The "best response" for an LP is not simply to choose the narrowest possible range, as this can lead to excessive crowding and diminished individual fee shares.

## Likely Equilibrium
A plausible equilibrium in this game involves differentiated ranges:
*   Some LPs concentrate liquidity near the active price (narrow ranges).
*   Others provide wider, less fee-dense liquidity.
*   LPs with lower hedging costs or gas costs may choose narrower ranges.
*   Risk-averse LPs may opt for wider ranges.
This suggests a mixed-strategy equilibrium where LPs randomize or differentiate slightly to avoid direct competition in exactly the same bins.
## Where it matters
This concept is vital for informing [[cl-entry-strategy|LP entry strategies]] and [[capital-allocation-rule-cl|capital allocation]] decisions. It highlights that a naive "narrowest range" approach is often suboptimal in a competitive environment. Understanding competitor behavior is key to optimizing [[liquidity-concentration|liquidity placement]] for sustainable fee generation.
## Evidence and limits
The source presents this as a theoretical model for understanding LP interactions. The exact nature of the equilibrium (e.g., pure vs. mixed strategies) can be complex and may require simulation.
## Related
[[nash-equilibrium-cl-strategies]], [[cl-provider-strategy]], [[liquidity-concentration]], [[fee-economics]], [[loss-versus-rebalancing]], [[range-planning]], [[dlmm-2026-nash-equilibrium-cl-provider-strategies]]