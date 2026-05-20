---
tags: ["api", "margin", "risk-management", "trading", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# API Margin Requirements (tastytrade)

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] provides functionalities to access and estimate margin requirements, which are critical for risk management and understanding trading capacity.

## Key Endpoints
*   **`GET /margin/accounts/{account_number}/requirements`**: Retrieves the current margin report for a specified account. This report details the margin held against existing positions.
*   **`POST /margin/accounts/{account_number}/dry-run`**: Allows users to estimate the margin impact of a *prospective order* without actually placing it. This "dry run" feature is invaluable for pre-trade analysis, helping traders understand how a new position would affect their buying power and margin utilization.

## Additional Risk Parameters
The API also exposes other risk-related configurations:
*   **Position Limits**: Information on maximum allowable positions.
*   **Per-Symbol Margin Requirements**: Specific margin rules that may apply to individual symbols.
*   **Public Risk-Free Rate**: Configuration for the public risk-free rate.
*   **Raw SPAN Margin Data**: For CME/CFE products, access to raw SPAN margin data.

These features empower users to integrate sophisticated risk management and capital allocation strategies directly into their automated trading systems.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]
*   [[../concepts/api-order-management-tastytrade.md|Order Submission and Management]]