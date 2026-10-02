---
domain: cl-market-making
tags:
- market-making-strategy
- performance-evaluation
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-00-dual-inventory-growth-policy.md
ingest_hashes:
- a6c5508e18eaec3f
---
# Zero-Growth Baseline
**In one line:** A benchmark for evaluating concentrated liquidity strategies, where the "do-nothing" scenario results in zero nominal growth in both base and quote assets.
## Intuition
To justify the active management and associated risks of a concentrated liquidity (CL) market-making strategy, its expected performance must demonstrably outperform a passive alternative. The simplest passive alternative is to hold the initial inventory without deploying it, which by definition results in no change in the nominal quantity of each asset. This "do-nothing" scenario serves as a fundamental hurdle that any active strategy must clear after accounting for all costs and risks.
## Mechanism / math
The `[[zero-growth-baseline]]` is defined by:
$$
\Delta SOL = 0
$$
$$
\Delta USDC = 0
$$
This means that if the bot simply holds its initial SOL and USDC, their quantities remain unchanged. The CL strategy is only considered successful if its expected fee production, after deducting all costs (LVR, hedge, gas, rent, slippage), leads to a net positive change in both SOL and USDC.
## Where it matters
The `[[zero-growth-baseline]]` is crucial for:
*   **Performance evaluation:** It provides a clear, minimal standard against which the profitability and efficacy of a CL strategy can be measured.
*   **Decision-making:** It forms a core component of the `[[decision-gate-cl-bot]]`, ensuring that deployments are only made when there's a reasonable expectation of beating this baseline.
*   **Risk assessment:** By comparing against this baseline, the true value added by the active strategy, net of all risks and costs, becomes apparent.
## Evidence and limits
This concept is a foundational principle for evaluating active trading strategies, particularly in contexts where passive holding is a viable alternative. It is a theoretical baseline used for policy definition rather than an empirical finding. Its primary limit is that it doesn't account for potential opportunity costs of not deploying, but rather sets a floor for *nominal asset growth*.
## Related
[[dual-inventory-growth-policy]], [[decision-gate-cl-bot]], [[inventory-accounting]], [[dlmm-dual-inventory-growth-policy]]