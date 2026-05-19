---
tags: ["gex", "options", "derivatives", "market-making", "risk-management"]
created: 2023-10-27
reviewed: false
source_origin: "gex_compute_pipeline.md"
---
# Gamma Exposure (GEX)

Gamma Exposure (GEX) is a measure of the sensitivity of an options dealer's delta hedging position to changes in the underlying asset's price. It quantifies the potential impact of options trading on market movements, particularly around key price levels. A high positive GEX suggests dealers are long gamma, meaning they will buy into falling prices and sell into rising prices, potentially dampening volatility. Conversely, negative GEX suggests dealers are short gamma, leading them to sell into falling prices and buy into rising prices, which can exacerbate volatility.

## Calculation Context

GEX calculations are critical for understanding market dynamics, especially for:
*   **0DTE (Zero Days To Expiration) Options:** Highly sensitive to price movements and time decay, requiring frequent updates.
*   **21DTE / 45DTE Options:** Provide a broader view of market positioning over longer timeframes.

## Dollar GEX Formula

The Dollar GEX per contract is typically computed using the following formula, assuming the calculation measures the dollar impact per 1% move in the underlying:

$$	ext{GEX}_{	ext{contract}} = \Gamma 	imes 	ext{Open Interest} 	imes 	ext{Contract Size (100)} 	imes S^2 	imes 0.01$$

Where:
*   $\Gamma$ (Gamma) is the second derivative of the option price with respect to the underlying asset's price.
*   `Open Interest` is the number of outstanding contracts.
*   `Contract Size` is typically 100 shares per option contract.
*   $S$ is the Spot Price of the underlying asset.

## Optimization for GEX Calculation

Efficient GEX calculation, especially across many tickers and expiries, requires:
*   [[../concepts/vectorized_greek_calculation.md]] for rapid Gamma computation.
*   Robust [[../concepts/process_based_parallelism.md]] to handle the computational load.
*   Effective [[../concepts/local_cache_layer.md]] for data ingestion and memory management.
*   A well-defined [[../concepts/intraday_gex_schedule.md]] to capture market shifts.

## Determining GEX Sign

A critical aspect of GEX aggregation is determining the final sign (Positive/Negative GEX) for component summation. This often involves inspecting volume/Open Interest at the Bid vs. Ask or applying institutional heuristics. Further research into this area is explored in [[../research/gex_sign_determination.md]].

## Source

This concept is derived from the [[../sources/gex_compute_pipeline_blueprint.md]].

---
tags: ["options", "greeks", "gamma", "finance"]
created: 2023-10-27
reviewed: false
source_origin: "gex_compute_pipeline.md"
---