---
tags: ["Options", "Greeks", "Derivatives", "Risk Management", "Pricing Models"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Greeks

Option Greeks are a set of measures that quantify the sensitivity of an option's price to changes in underlying factors such as asset price, time, volatility, and interest rates. They are crucial tools for options traders and risk managers to understand and manage the risks associated with options portfolios.

The [Theta Data v3](../../entities/theta-data-v3.md) API provides various endpoints to retrieve calculated Greeks, often using the Black-Scholes model or similar pricing models. Theta Data's methodology for calculating Greeks is detailed in their [Option Greeks Article](/Articles/Data-And-Requests/Option-Greeks.html).

## Key Greeks and Their Definitions:

*   **Delta**: Measures the sensitivity of an option's price to a $1 change in the underlying asset's price.
*   **Theta**: Measures the sensitivity of an option's price to the passage of time (time decay).
*   **Vega**: Measures the sensitivity of an option's price to a 1% change in the underlying asset's implied volatility.
*   **Rho**: Measures the sensitivity of an option's price to a 1% change in the risk-free interest rate.
*   **Epsilon**: Measures the sensitivity of an option's price to a 1% change in the dividend yield of the underlying asset.
*   **Lambda**: Measures the percentage change in an option's price for a 1% change in the underlying asset's price.
*   **Gamma**: Measures the rate of change of an option's Delta with respect to a change in the underlying asset's price. It's a second-order derivative.
*   **Vanna**: Measures the rate of change of an option's Delta with respect to a change in implied volatility, or the rate of change of Vega with respect to a change in the underlying asset's price.
*   **Charm**: Measures the rate of change of an option's Delta with respect to the passage of time.
*   **Vomma**: Measures the rate of change of an option's Vega with respect to a change in implied volatility. It's a second-order derivative of the option's value with respect to volatility.
*   **Veta**: Measures the rate of change of an option's Vega with respect to the passage of time.
*   **Vera**: Measures the rate of change of an option's Rho with respect to a change in implied volatility.
*   **Speed**: Measures the rate of change of an option's Gamma with respect to a change in the underlying asset's price. It's a third-order derivative.
*   **Zomma**: Measures the rate of change of an option's Gamma with respect to a change in implied volatility.
*   **Color**: Measures the rate of change of an option's Gamma with respect to the passage of time.
*   **Ultima**: Measures the sensitivity of Vomma to a change in implied volatility.
*   **D1 / D2**: Intermediate values used in the Black-Scholes formula.
*   **Dual Delta**: Measures the sensitivity of an option's price to a change in the strike price.
*   **Dual Gamma**: Measures the rate of change of Dual Delta with respect to a change in the strike price.
*   **Implied Volatility (IV)**: The market's expectation of future volatility of the underlying asset, derived from the option's market price.
*   **IV Error**: The difference between the option's theoretical value (calculated using implied volatility) and its actual market value, normalized.

## Greeks Endpoints in Theta Data v3:

The API provides various endpoints for retrieving Greeks, categorized by snapshot and historical data, and by the order of the Greek (first, second, third, or all).

### Snapshot Greeks:
*   **[Option Snapshot Greeks Implied Volatility Endpoint](../concepts/option-snapshot-greeks-implied-volatility-endpoint.md)**
*   **[Option Snapshot Greeks All Endpoint](../concepts/option-snapshot-greeks-all-endpoint.md)**
*   **[Option Snapshot Greeks First Order Endpoint](../concepts/option-snapshot-greeks-first-order-endpoint.md)**
*   **[Option Snapshot Greeks Second Order Endpoint](../concepts/option-snapshot-greeks-second-order-endpoint.md)**
*   **[Option Snapshot Greeks Third Order Endpoint](../concepts/option-snapshot-greeks-third-order-endpoint.md)**

### Historical Greeks:
*   **[Option History Greeks EOD Endpoint](../concepts/option-history-greeks-eod-endpoint.md)**
*   **[Option History Greeks All Endpoint](../concepts/option-history-greeks-all-endpoint.md)**
*   **[Option History Greeks First Order Endpoint](../concepts/option-history-greeks-first-order-endpoint.md)**
*   **[Option History Greeks Second Order Endpoint](../concepts/option-history-greeks-second-order-endpoint.md)**
*   **[Option History Greeks Third Order Endpoint](../concepts/option-history-greeks-third-order-endpoint.md)**
*   **[Option History Trade Greeks All Endpoint](../concepts/option-history-trade-greeks-all-endpoint.md)**
*   **[Option History Trade Greeks First Order Endpoint](../concepts/option-history-trade-greeks-first-order-endpoint.md)**
*   **[Option History Trade Greeks Second Order Endpoint](../concepts/option-history-trade-greeks-second-order-endpoint.md)**
*   **[Option History Trade Greeks Third Order Endpoint](../concepts/option-history-trade-greeks-third-order-endpoint.md)**
*   **[Option History Greeks Implied Volatility Endpoint](../concepts/option-history-greeks-implied-volatility-endpoint.md)**
*   **[Option History Trade Greeks Implied Volatility Endpoint](../concepts/option-history-trade-greeks-implied-volatility-endpoint.md)**

## Calculation Parameters:
Several [API Parameters](../concepts/api-parameters.md) can influence Greeks calculations:
*   `annual_dividend`
*   `rate_type`
*   `rate_value`
*   `stock_price`
*   `greeks_version`
*   `underlyer_use_nbbo`
*   `use_market_value`

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [API Parameters](../concepts/api-parameters.md)
*   [Implied Volatility](../concepts/implied-volatility.md) (often a key output or input for Greeks)

---