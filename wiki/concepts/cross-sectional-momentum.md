---
tags: ["feature-engineering", "momentum-trading", "quantitative-finance", "relative-strength"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Cross-Sectional Momentum

Cross-Sectional Momentum is a core feature within the [[../concepts/zero-cost-feature-engineering.md]] framework, designed to identify and capitalize on trending technology stocks.

## Logic
The underlying principle is that tech stocks tend to trend, and a [[../concepts/reinforcement-learning-agent.md]] should be trained to "ride the strongest horses." By identifying stocks with superior momentum relative to their peers, the agent can learn to buy into the top decile of performers and avoid laggards.

## Calculation
This feature is calculated as the 90-day return of each stock. Crucially, this return is then [[../concepts/z-scoring.md]] against the other 99 stocks within the [[../entities/nasdaq-100.md]] index. This cross-sectional normalization allows for a direct comparison of relative strength among the index components.

## Data Cost
This feature can be derived entirely from standard daily close price data, incurring $0.00 in data costs.

---
### Related Concepts
*   [[../concepts/feature-engineering.md]]
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../concepts/z-scoring.md]]
*   [[../entities/nasdaq-100.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].