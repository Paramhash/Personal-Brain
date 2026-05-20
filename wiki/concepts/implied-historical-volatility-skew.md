---
tags: ["options trading", "volatility", "implied volatility", "historical volatility", "market sentiment"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Implied Volatility - Historical Volatility (IV-HV) Skew

The Implied Volatility (IV) - Historical Volatility (HV) skew refers to the difference or ratio between the implied volatility (derived from option prices) and the historical volatility (calculated from past price movements) of an underlying asset. This comparison is often analyzed across different strike prices or maturities.

## Understanding the Components:

*   **Implied Volatility (IV):** A forward-looking measure representing the market's expectation of future volatility for the underlying asset, derived from the current prices of options.
*   **Historical Volatility (HV):** A backward-looking measure representing the actual realized volatility of the underlying asset over a specific past period.

## Interpretation of the Skew:

The IV-HV skew provides crucial insights into market expectations about future volatility relative to past realized volatility:

*   **Positive Skew (IV > HV):** A significant positive skew might suggest that market participants are pricing in higher future uncertainty, potential downside risk, or an expectation of increased volatility compared to what has been observed historically. This often occurs during periods of market stress or anticipation of significant events.
*   **Negative Skew (IV < HV):** Conversely, a negative skew could imply market complacency, an expectation of lower future volatility, or that options are relatively cheap compared to recent realized movements. This can occur during periods of sustained calm or after a sharp volatility spike.

## Application in the Structural Triad:

As part of the [[../concepts/structural-triad-systematic-options-trading.md|Structural Triad for Advanced Systematic Options Trading]], the IV-HV skew provides a crucial input for assessing whether options are relatively cheap or expensive. It helps gauge market sentiment regarding future volatility, aiding in strategy selection (e.g., selling expensive volatility, buying cheap volatility) and risk management.

## Further Research:

Explore different methods for calculating IV-HV skew (e.g., using specific maturities, weighted averages) and its correlation with subsequent market movements, option pricing anomalies, and the profitability of various volatility-based trading strategies.

---