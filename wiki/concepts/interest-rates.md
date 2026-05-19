---
tags: ["Interest Rate", "Financial Data", "History"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Interest Rates

Interest rates are a fundamental component of financial markets, influencing everything from bond yields to option pricing. The [Theta Data v3](../../entities/theta-data-v3.md) API provides access to historical interest rate data.

## Key Characteristics:
*   **Symbols**: Interest rates are identified by specific [Symbols](../concepts/symbols.md) (e.g., SOFR, various Treasury rates).
*   **Reporting**: Rates are reported periodically, either in the morning or afternoon, depending on the specific rate.
*   **Usage in Greeks**: Interest rates are a crucial input for calculating [Option Greeks](../concepts/option-greeks.md). The API allows specifying `rate_type` and `rate_value` [API Parameters](../concepts/api-parameters.md#rate-type) for these calculations.

## Available Endpoints:

### History Endpoints:
*   **[Interest Rate History EOD Endpoint](../concepts/interest-rate-history-eod-endpoint.md)**: Returns the End-of-Day (EOD) interest rate for a given symbol over a specified date range.

## Related Concepts:
*   [API Endpoints](../concepts/api-endpoints.md)
*   [API Parameters](../concepts/api-parameters.md)
*   [Option Greeks](../concepts/option-greeks.md)

---