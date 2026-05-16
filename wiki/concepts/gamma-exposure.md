---
tags: ["options", "greeks", "market-analysis", "quantitative-finance", "risk-management"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# Gamma Exposure (GEX)

Gamma Exposure (GEX) is an aggregated measure of the total [Gamma](../concepts/options-greeks.md) held by market makers and other participants across all outstanding options contracts for a given underlying asset or the entire market. It provides insight into potential future market movements.

## Key Concepts

*   **GEX Profiles:** Visualizations or data sets that show the distribution of Gamma across different strike prices and expirations.
*   **Net GEX:** The total aggregated Gamma exposure, often indicating whether market makers are net long or net short Gamma.
*   **Gamma Flip:** A specific price level where the market's overall Gamma exposure shifts from positive to negative, or vice-versa. This can indicate a change in market maker hedging behavior and potentially lead to increased volatility or trend acceleration.
*   **GEX Divergence:** A situation where the GEX profile or net GEX value diverges from the underlying asset's price action, potentially signaling an impending market shift.

## Interpretation

*   **Positive GEX:** When market makers are net long Gamma, they tend to buy into dips and sell into rallies to maintain a delta-neutral position. This can lead to reduced volatility and mean-reversion in the underlying asset.
*   **Negative GEX:** When market makers are net short Gamma, they tend to sell into dips and buy into rallies. This can amplify price movements, leading to increased volatility and trend-following behavior.

## Data Sources

Some [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md) like [FlashAlpha](../entities/flashalpha.md) offer pre-calculated GEX values and related metrics. Other providers like [ThetaData](../entities/thetadata.md) or [Polygon.io](../entities/polygon-io.md) provide raw [Options Greeks](../concepts/options-greeks.md) and options chain data, allowing users to calculate and aggregate GEX profiles locally.

Building custom "GEX Divergence dashboards" is a common application for powerful workstations like the [AMD Ryzen Threadripper 3990X](../entities/amd-ryzen-threadripper-3990x.md).

---