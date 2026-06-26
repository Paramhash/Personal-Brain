---
tags: ["machine-learning", "data-science", "data-preprocessing"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Feature Engineering

Feature Engineering is the process of using domain knowledge to extract or create features (variables) from raw data that make machine learning algorithms work more effectively. It involves transforming raw data into a format that is more suitable for modeling, often leading to improved model performance.

## Role in Zero-Cost Feature Engineering
In the context of [[../concepts/zero-cost-feature-engineering.md]], this process is crucial. It involves:
*   **Identification**: Pinpointing relevant financial indicators that can serve as proxies for more complex or expensive data.
*   **Transformation**: Applying mathematical and statistical operations to free End-of-Day (EOD) data (e.g., prices, volume) to derive these indicators.
*   **Selection**: Choosing a concise and impactful set of features (like [[../concepts/downside-semi-variance.md]], [[../concepts/chaikin-money-flow.md]], [[../concepts/cross-sectional-momentum.md]], [[../concepts/mean-reversion-stretch.md]], and [[../concepts/stochastic-rsi.md]]) that capture essential market dynamics for a [[../concepts/reinforcement-learning-agent.md]].

Effective feature engineering is key to building robust and performant quantitative models, especially when data resources are limited or costly.

---
### Related Concepts
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../concepts/reinforcement-learning-agent.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].