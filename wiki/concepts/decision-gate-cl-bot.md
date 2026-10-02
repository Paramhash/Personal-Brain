---
domain: cl-market-making
tags:
- market-making-strategy
- risk-management
- deployment-policy
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-00-dual-inventory-growth-policy.md
ingest_hashes:
- c83319a6e1f15622
---
# Decision Gate (CL Bot)
**In one line:** A set of conditions that must be met before a concentrated liquidity (CL) position is deployed or closed, specifically ensuring expected positive growth in both base and quote assets with a minimum probability.
## Intuition
To prevent unprofitable or strategically misaligned deployments, a CL market-making bot requires a rigorous filter. This "decision gate" acts as a pre-condition, ensuring that any action (like deploying new liquidity) is expected to contribute positively to the bot's specific objectives, which, under a `[[dual-inventory-growth-policy]]`, means growing both base and quote assets. It also ensures that the strategy outperforms the `[[zero-growth-baseline]]` after all costs and risks.
## Mechanism / math
The `[[decision-gate-cl-bot]]` for a `[[dual-inventory-growth-policy]]` requires that the expected change in both assets is positive:
$$
\mathbb{E}[\Delta SOL] > 0
$$
$$
\mathbb{E}[\Delta USDC] > 0
$$
Additionally, a safety requirement can be imposed, such as a minimum probability of achieving positive growth:
$$
P(\Delta SOL > 0) \geq p_{min}
$$
$$
P(\Delta USDC > 0) \geq p_{min}
$$
This gate is applied to both entry and exit decisions. For entry, it ensures that the projected terminal inventory satisfies these growth constraints. For exit, it ensures that closing the position will not violate these constraints or that remaining in the position would lead to a violation.
## Where it matters
The `[[decision-gate-cl-bot]]` is a critical component of the bot's `[[risk-management-team-agent|risk management]]` and `[[market-making-strategy|strategy execution]]`. It directly impacts:
*   **Deployment timing:** When to enter or adjust a liquidity position.
*   **Capital allocation:** Prevents capital from being deployed into positions that are unlikely to meet the dual-inventory growth targets.
*   **Profitability:** Filters out deployments where expected fees do not sufficiently cover LVR, hedging costs, gas, rent, and slippage.
*   **Operational integrity:** Ensures the bot's asset base remains healthy and growing in both tokens.
## Evidence and limits
This is a policy-driven mechanism for automated trading. Its effectiveness relies on the accuracy of the models used to estimate expected asset changes ($\mathbb{E}[\Delta SOL]$, $\mathbb{E}[\Delta USDC]$) and their associated probabilities. Inaccurate estimations could lead to suboptimal decisions, even with a well-defined gate.
## Related
[[dual-inventory-growth-policy]], [[zero-growth-baseline]], [[inventory-accounting]], [[m07-inventory-and-market-making-theory|market making theory]], [[dlmm-dual-inventory-growth-policy]]