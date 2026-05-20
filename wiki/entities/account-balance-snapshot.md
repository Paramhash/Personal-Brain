---
tags: ["api", "tastyworks", "data-model", "account-balance", "historical-data", "snapshot"]
created: 2024-05-15
reviewed: false
source_origin: "balances-and-positions.md"
---
# AccountBalanceSnapshot Data Model (Tastyworks API)

The `AccountBalanceSnapshot` object provides a historical record of an account's financial balances at a specific point in time. It is largely identical to the [[./account-balance.md|AccountBalance]] object but includes additional fields for tracking the snapshot date and time, while omitting some real-time-only fields.

This data model is returned by the `GET /accounts/{account_number}/balance-snapshots` endpoint of the [[./tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]].

## Fields

The `AccountBalanceSnapshot` object contains most of the same fields as the [[./account-balance.md|AccountBalance]] object, providing a comprehensive view of cash, margin, buying power, and position values for a historical date.

### Snapshot-Specific Fields

In addition to the fields found in [[./account-balance.md|AccountBalance]], the `AccountBalanceSnapshot` includes:

| Field | Type | Description |
|---|---|---|
| `snapshot-date` | date | The date of the balance snapshot. |
| `time-of-day` | string | The time of day for the snapshot (e.g., `BOD` for beginning of day, `EOD` for end of day). |

### Differences from `AccountBalance`

The `AccountBalanceSnapshot` typically omits a few real-time-only fields present in `AccountBalance`, such as:
*   `updated-at` (as the snapshot date/time serve this purpose)
*   Specific intraday/overnight margin breakdowns for futures (as these are dynamic and less relevant for a historical snapshot).

For a full list and description of the common balance fields, refer to the [[./account-balance.md|AccountBalance]] data model.

---
## Use Cases
*   Tracking portfolio value over time.
*   Analyzing historical margin requirements and buying power.
*   Reconciling past account statements.