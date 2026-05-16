---
tags: ["options", "derivatives", "risk-management", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# Options Greeks

Options Greeks are a set of measures that quantify the sensitivity of an option's price to changes in underlying market parameters. They are crucial tools for options traders and portfolio managers for understanding and managing risk.

## Primary Greeks

*   **Delta (Δ):** Measures the sensitivity of an option's price to a $1 change in the underlying asset's price. It also represents the approximate probability of the option expiring in-the-money.
*   **Gamma (Γ):** Measures the rate of change of an option's Delta with respect to a change in the underlying asset's price. It indicates how quickly Delta will change as the underlying moves.
*   **Vega (ν):** Measures the sensitivity of an option's price to a 1% change in the underlying asset's implied volatility.
*   **Theta (Θ):** Measures the sensitivity of an option's price to the passage of time (time decay). It typically represents the amount an option's price will decrease each day, all else being equal.

## Importance

Greeks are fundamental for:
*   **Risk Management:** Identifying and hedging various types of market risk.
*   **Strategy Development:** Constructing and adjusting options strategies based on market expectations.
*   **Valuation:** Understanding the components that contribute to an option's premium.

## Data Providers

Access to real-time [Options Greeks](../concepts/options-greeks.md) is critical for active traders. Various [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md) offer these values, either directly or by providing raw data for local computation.

Related concepts include [Gamma Exposure (GEX)](../concepts/gamma-exposure.md), which aggregates Gamma across the market.

---