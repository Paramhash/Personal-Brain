---
tags: ["API", "Financial Data", "Stocks", "Options", "Indices"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Theta Data v3

Theta Data v3 is a comprehensive API providing real-time and historic financial market data for stocks, options, and indices. It offers a wide array of endpoints for listing available symbols and dates, retrieving snapshot data (current day's OHLC, last trade, last quote, market value, open interest), and historical data (end-of-day, OHLC, trades, quotes, trade-quotes, open interest) at various granularities.

The API also includes specialized endpoints for calculating [Option Greeks](../concepts/option-greeks.md) and provides access to [Market Calendar](../concepts/market-calendar.md) and [Interest Rates](../concepts/interest-rates.md) information.

## Key Features:
*   **Data Coverage**: Stocks, Options, Indices.
*   **Data Types**: List data, Snapshot data (real-time/delayed), Historical data (intraday/end-of-day), [Option Greeks](../concepts/option-greeks.md).
*   **Data Sources**: Leverages various [Data Feeds](../concepts/data-feeds.md) including Nasdaq Basic, UTP & CTA, and OPRA.
*   **Subscription Tiers**: Access levels vary based on [Subscription Tiers](../concepts/subscription-tiers.md) (Free, Value, Standard, Professional).
*   **Flexible Output**: Supports multiple [Data Formats](../concepts/data-formats.md) including CSV, JSON, NDJSON, and Python dataframes (pandas, polars).

## API Endpoints Overview:
*   **Stock Endpoints**: Access various types of stock data. See [Stock Data](../concepts/stock-data.md) for more details.
*   **Option Endpoints**: Access various types of options data, including [Option Greeks](../concepts/option-greeks.md). See [Option Data](../concepts/option-data.md) for more details.
*   **Index Endpoints**: Access various types of index data. See [Index Data](../concepts/index-data.md) for more details.
*   **Calendar Endpoints**: Retrieve market schedule and holiday information. See [Market Calendar](../concepts/market-calendar.md) for more details.
*   **Interest Rate Endpoints**: Access historical interest rate data. See [Interest Rates](../concepts/interest-rates.md) for more details.

For detailed information on parameters, refer to [API Parameters](../concepts/api-parameters.md).

## Related Entities:
*   [ThetaClient (Python Library)](../entities/thetaclient-python-library.md)
*   [pandas (Python Library)](../entities/pandas-python-library.md)
*   [polars (Python Library)](../entities/polars-python-library.md)

---