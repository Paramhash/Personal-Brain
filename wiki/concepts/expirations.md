---
tags: ["Options", "Expiration Date", "Contracts"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Expirations

In the context of [Option Data](../concepts/option-data.md), an "expiration" refers to the specific date on which an options contract ceases to be valid. After this date, the option can no longer be exercised.

## Key Characteristics:
*   **Format**: Expiration dates are typically provided in `YYYY-MM-DD` or `YYYYMMDD` format in the [Theta Data v3](../../entities/theta-data-v3.md) API.
*   **Wildcard Support**: Many options endpoints allow specifying `*` for the `expiration` [API Parameter](../concepts/api-parameters.md#expiration) to retrieve data for all available expiration dates for a given underlying symbol.
*   **Impact on Greeks**: The time remaining until expiration (Days to Expiration or DTE) is a critical factor in the calculation of [Option Greeks](../concepts/option-greeks.md).

## Usage in Theta Data v3:
*   **Listing Expirations**: The [Option List Expirations Endpoint](../concepts/option-list-expirations-endpoint.md) allows users to discover all available expiration dates for a specific underlying.
*   **Filtering Data**: The `expiration` parameter is used across various options snapshot and historical endpoints (e.g., [Option Snapshot OHLC Endpoint](../concepts/option-snapshot-ohlc-endpoint.md), [Option History Greeks All Endpoint](../concepts/option-history-greeks-all-endpoint.md)) to filter data for contracts expiring on a particular date.
*   **`max_dte` Parameter**: The `max_dte` [API Parameter](../concepts/api-parameters.md#max-dte) can be used to filter contracts based on their days to expiration.

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Strike Prices](../concepts/strike-prices.md)
*   [Option Greeks](../concepts/option-greeks.md)
*   [API Parameters](../concepts/api-parameters.md)

---