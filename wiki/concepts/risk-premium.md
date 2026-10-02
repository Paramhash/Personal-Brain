---
domain: cl-market-making
tags:
- finance-theory
- investment-returns
- cost-of-capital
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 0f8f5cdd9db22e03
---
# Risk Premium
**In one line:** The additional return an investor or a trading strategy expects to receive for taking on a higher level of risk compared to a risk-free asset.
## Intuition
In finance, risk and return are inherently linked. Investors demand extra compensation for bearing uncertainty. For a market-making bot, deploying capital into a [[cl-position]] involves various risks (e.g., [[impermanent-loss]], operational risks). The [[risk-premium]] ensures that the expected returns from these activities are sufficiently high to justify taking on those risks, above and beyond covering explicit costs.
## Mechanism / math
The [[risk-premium]] is a component of the [[economic-hurdle-rate-cl]]:
$$
\text{Expected fees} > \text{LVR} + \text{hedge funding} + \text{rent} + \text{gas} + \text{slippage} + \text{risk premium}
$$
It represents the minimum acceptable compensation for the inherent risks of the market-making strategy.
## Where it matters
The [[risk-premium]] is a fundamental concept in investment decision-making and is crucial for the [[cl-entry-strategy]]. By including it in the [[economic-hurdle-rate-cl]], the bot ensures that it only deploys capital into positions that offer an adequate return for the risk taken, contributing to long-term capital growth and sustainability.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] includes "risk premium" as a cost in the [[economic-hurdle-rate-cl]], signifying its importance in the bot's economic decision-making framework. The precise quantification of a risk premium can be subjective and depends on the specific risk appetite and market conditions.
## Related
[[economic-hurdle-rate-cl]]
[[equity-risk-premium]]
[[lvr-and-impermanent-loss]]
[[cl-entry-strategy]]
[[financial-trading-performance-metrics]]