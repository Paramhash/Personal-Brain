---
tags: ["feature-engineering", "risk-management", "volatility", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Downside Semi-Variance

Downside Semi-Variance is a feature utilized in [[../concepts/zero-cost-feature-engineering.md]] as a proxy for Implied Volatility (IV) Skew, aiming to identify potential crash risk.

## Logic
The primary goal is to observe actual realized crash behavior rather than relying on options market pricing. If a stock consistently grinds upwards but experiences violent, high-volume red days, it can indicate that institutions are quietly exiting their positions.

## Calculation
The feature is calculated as the standard deviation of only the negative daily returns over the last 30 days. This focuses specifically on downside volatility, providing insight into the severity and frequency of negative price movements.

## Data Cost
This feature can be derived entirely from standard daily close price data, incurring $0.00 in data costs.

---
### Related Concepts
*   [[../concepts/feature-engineering.md]]
*   [[../concepts/zero-cost-feature-engineering.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].