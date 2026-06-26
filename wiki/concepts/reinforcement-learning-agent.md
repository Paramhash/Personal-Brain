---
tags: ["reinforcement-learning", "machine-learning", "artificial-intelligence", "trading-systems"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Reinforcement Learning Agent

A Reinforcement Learning (RL) Agent is an artificial intelligence entity that learns to make optimal decisions by interacting with an environment. It receives observations (states), performs actions, and receives rewards or penalties, iteratively improving its strategy over time.

## Role in Zero-Cost Feature Engineering
In the context of [[../concepts/zero-cost-feature-engineering.md]], the RL agent is the ultimate recipient of the engineered features. Specifically:
*   **Input**: Every month, the agent receives a (100, 5) cross-sectional array. This array contains the five carefully engineered features ([[../concepts/downside-semi-variance.md]], [[../concepts/chaikin-money-flow.md]], [[../concepts/cross-sectional-momentum.md]], [[../concepts/mean-reversion-stretch.md]], [[../concepts/stochastic-rsi.md]]) for each of the 100 stocks in the [[../entities/nasdaq-100.md]] index.
*   **Decision Making**: Based on these features, the agent is trained to make trading decisions, such as identifying a "Top 10" list of stocks to buy.
*   **Learning**: Through continuous interaction with market data and feedback on its trading outcomes, the agent learns to optimize its strategy for profitability and risk management.

The use of a Micro Agent implies a focused and potentially specialized RL model designed for this specific trading task.

---
### Related Concepts
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../concepts/feature-engineering.md]]
*   [[../entities/nasdaq-100.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].