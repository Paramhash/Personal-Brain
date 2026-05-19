---
tags: ["API", "Parameters", "Request", "Query"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# API Parameters

This document outlines the common and specific parameters used across the [Theta Data v3](../entities/theta-data-v3.md) API endpoints. Understanding these parameters is crucial for constructing effective API requests.

## Required Parameters

### `symbol`
*   **Type**: `string` or `array` of `string`
*   **Description**: The stock or index symbol, or underlying symbol for options.
    *   `single_symbol`: Used when only one symbol is expected (e.g., `symbol=AAPL`).
    *   `multi_symbol`: Used when multiple symbols or all symbols are allowed (e.g., `symbol=AAPL,SPY` or `symbol=*`).
    *   `opt_multi_symbol`: Optional version of `multi_symbol`.
*   **Related Concepts**: [Symbols](../concepts/symbols.md)

### `date`
*   **Type**: `string` (`YYYY-MM-DD` format)
*   **Description**: The specific date to fetch data for.
    *   `date`: Required for single-day requests.
    *   `opt_date`: Optional; if present, overrides `start_date` and `end_date`.

### `start_date` / `end_date`
*   **Type**: `string` (`YYYY-MM-DD` format)
*   **Description**: Defines a date range (inclusive) for historical data requests.
    *   `start_date`: The beginning of the date range.
    *   `end_date`: The end of the date range.
    *   `opt_start_date` / `opt_end_date`: Optional versions.

### `year`
*   **Type**: `string`
*   **Description**: The year to fetch data for, typically used for calendar endpoints.

### `time_of_day`
*   **Type**: `string` (`HH:mm:ss.SSS` format)
*   **Description**: A specific time within a day to fetch data for; assumed to be America/New_York timezone.

### `expiration`
*   **Type**: `string` (`YYYY-MM-DD` or `YYYYMMDD` format, or `*`)
*   **Description**: The expiration date of an options contract. `*` can be used for all expirations in some contexts.
    *   `expiration`: Allows `*` wildcard.
    *   `expiration_no_star`: Does not allow `*` wildcard.
*   **Related Concepts**: [Expirations](../concepts/expirations.md)

### `strike`
*   **Type**: `string` or `number`
*   **Description**: The strike price of an options contract in dollars (e.g., `100.00`). `*` can be used for all strikes.
*   **Default**: `*` (if not specified)
*   **Related Concepts**: [Strike Prices](../concepts/strike-prices.md)

### `interval`
*   **Type**: `string`
*   **Description**: The size of the time interval for aggregated data. Intervals less than 1m are typically for single-day requests.
*   **Enum**: `tick`, `10ms`, `100ms`, `500ms`, `1s`, `5s`, `10s`, `15s`, `30s`, `1m`, `5m`, `10m`, `15m`, `30m`, `1h`
*   **Default**: `1s`
*   **Related Concepts**: [Time Intervals](../concepts/time-intervals.md)

### `request_type`
*   **Type**: `string`
*   **Description**: Specifies whether to fetch trade or quote data.
*   **Enum**: `trade`, `quote`

## Optional Parameters

### `annual_dividend`
*   **Type**: `number` (float)
*   **Description**: The annualized expected dividend amount to be used in [Option Greeks](../concepts/option-greeks.md) calculations.

### `end_time`
*   **Type**: `string` (`HH:MM:SS.SSS` format)
*   **Description**: The end time (inclusive) within the specified day.
*   **Default**: `16:00:00`

### `exclusive`
*   **Type**: `boolean`
*   **Description**: If `true`, matches quotes with timestamps *less than* the trade timestamp. Otherwise, matches if timestamp is *less than or equal to* trade timestamp.
*   **Default**: `true`

### `format`
*   **Type**: `string`
*   **Description**: The desired output format of the data.
*   **Enum**: `csv`, `json`, `ndjson`, `html`
*   **Default**: `csv`
*   **Related Concepts**: [Data Formats](../concepts/data-formats.md)

### `rate_type`
*   **Type**: `string`
*   **Description**: The interest rate type to be used in [Option Greeks](../concepts/option-greeks.md) calculations.
*   **Enum**: `sofr`, `treasury_m1`, `treasury_m3`, `treasury_m6`, `treasury_y1`, `treasury_y2`, `treasury_y3`, `treasury_y5`, `treasury_y7`, `treasury_y10`, `treasury_y20`, `treasury_y30`
*   **Default**: `sofr`

### `rate_value`
*   **Type**: `number` (float)
*   **Description**: The interest rate, as a percent, to be used in [Option Greeks](../concepts/option-greeks.md) calculations (e.g., `5.0` for 5%).

### `right`
*   **Type**: `string`
*   **Description**: The right (call or put) of the options contract.
*   **Enum**: `call`, `put`, `both`
*   **Default**: `both`

### `start_time`
*   **Type**: `string` (`HH:MM:SS.SSS` format)
*   **Description**: The start time (inclusive) within the specified day.
*   **Default**: `09:30:00`

### `stock_price`
*   **Type**: `number` (float)
*   **Description**: The underlying stock price to be used in [Option Greeks](../concepts/option-greeks.md) calculations.

### `venue`
*   **Type**: `string`
*   **Description**: Specifies the data venue for real-time or historic requests.
*   **Enum**: `nqb` (Nasdaq Basic), `utp_cta` (merged UTP & CTA)
*   **Default**: `nqb`
*   **Related Concepts**: [Data Feeds](../concepts/data-feeds.md), [Exchanges](../concepts/exchanges.md)

### `greeks_version`
*   **Type**: `string`
*   **Description**: Adjusts the [Option Greeks](../concepts/option-greeks.md) calculation methodology. "1" uses a fixed .15 DTE for 0DTE; "latest" uses real TTE (down to a minimum of 1 hour).
*   **Enum**: `"latest"`, `"1"`
*   **Default**: `"latest"`

### `underlyer_use_nbbo`
*   **Type**: `boolean`
*   **Description**: Determines underlying pricing for [Option Greeks](../concepts/option-greeks.md) calculation. `true` uses the midpoint of the NBBO; `false` uses the last trade price.
*   **Default**: `false`

### `max_dte`
*   **Type**: `integer` (int32)
*   **Description**: Filters options contracts to include only those with "Days to Expiration" (DTE) less than or equal to this number.
*   **Minimum**: `0`

### `strike_range`
*   **Type**: `integer` (int32)
*   **Description**: Limits the number of contracts returned relative to the underlying's spot price. For a value 'n', returns 'n' strikes above and 'n' strikes below the spot price, plus one at-the-money (ATM) strike, for a maximum of `2n + 1` strikes.
*   **Minimum**: `1`

### `min_time`
*   **Type**: `string` (`HH:mm:ss.SSS` format)
*   **Description**: Filters snapshots to include only data with a timestamp greater than or equal to the specified value.

### `use_market_value`
*   **Type**: `boolean`
*   **Description**: If `true`, uses the market value bid, ask, and price for calculations.
*   **Default**: `false`

---