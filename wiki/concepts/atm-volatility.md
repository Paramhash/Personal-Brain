---
tags: ["options", "volatility", "market-metrics"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# ATM Volatility

ATM Volatility, or At-The-Money Volatility, refers to the implied volatility of an option whose strike price is very close to the current price of the underlying asset. It is typically derived from the implied volatility of an at-the-money straddle (a combination of an ATM call and an ATM put with the same strike and expiration).

ATM Volatility is a key metric on the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md) and serves as a general indicator of overall market fear or expected price movement. Higher ATM volatility suggests greater expected price fluctuations, while lower ATM volatility indicates a calmer market outlook.

In the context of [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), ATM Volatility is one of the primary features extracted from the option chain to characterize market regimes.