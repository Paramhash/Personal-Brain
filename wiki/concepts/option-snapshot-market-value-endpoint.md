---
tags: ["Option", "Snapshot", "Market Value", "Real-time Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Market Value Endpoint

The `/option/snapshot/market_value` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API retrieves a real-time market value derived from the last National Best Bid and Offer (NBBO) quote of an options contract.

## Endpoint Details:
*   **Path**: `/option/snapshot/market_value`
*   **Method**: `GET`
*   **Summary**: Market Value
*   **Operation ID**: `option_snapshot_market_value`
*   **Minimum Subscription**: `standard`
*   **Description**:
    *   Returns a real-time market value derived from the last NBBO quote of an option contract.

## Parameters:
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. Use `*` for all expirations. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `