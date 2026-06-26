---
tags: ["feature-engineering", "mean-reversion", "technical-analysis", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Mean Reversion Stretch

Mean Reversion Stretch is a feature employed in [[../concepts/zero-cost-feature-engineering.md]] to identify when a stock is temporarily overextended and potentially due for a pullback. It serves as a proxy for options Term Structure data.

## Logic
The goal is to detect conditions where a stock's price has moved significantly away from its average, suggesting it might revert to its mean. This helps in timing entries or exits to optimize trading decisions.

## Calculation
This feature is calculated as the percentage distance between the current price and the 50-day moving average. A higher positive percentage indicates the stock is stretched above its average, while a negative percentage indicates it's below.

## Data Cost
This feature can be derived entirely from standard daily close price data, incurring $0.00 in data costs.

---
### Related Concepts
*   [[../concepts/feature-engineering.md]]
*   [[../concepts/zero-cost-feature-engineering.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].