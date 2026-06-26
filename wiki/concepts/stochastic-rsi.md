---
tags: ["feature-engineering", "technical-analysis", "oscillators", "timing"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Stochastic RSI

Stochastic RSI (StochRSI) is a technical indicator used as a timing overlay feature in [[../concepts/zero-cost-feature-engineering.md]]. Its purpose is to identify short-term oversold or overbought conditions, thereby optimizing the monthly entry point for trading decisions.

## Logic
StochRSI is an oscillator that measures the RSI (Relative Strength Index) relative to its high/low range over a set period, rather than price. This provides a "volatility of volatility" measure, making it more sensitive and useful for short-term timing.

## Calculation
The feature uses the standard 14-day StochRSI calculation. This involves applying the Stochastic Oscillator formula to the RSI values instead of price.

## Data Cost
This feature can be derived entirely from standard daily close price data, incurring $0.00 in data costs.

---
### Related Concepts
*   [[../concepts/feature-engineering.md]]
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../entities/pandas-ta.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].