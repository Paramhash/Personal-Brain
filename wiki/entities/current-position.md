---
tags: ["api", "tastyworks", "data-model", "position", "portfolio"]
created: 2024-05-15
reviewed: false
source_origin: "balances-and-positions.md"
---
# CurrentPosition Data Model (Tastyworks API)

The `CurrentPosition` object represents a single open (or optionally closed) position within a Tastyworks account. It provides detailed information about the instrument, quantity, cost basis, current valuation, and realized gains.

This data model is returned by the `GET /accounts/{account_number}/positions` endpoint of the [[./tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]].

## Fields

### Position Identification

| Field | Type | Description |
|---|---|---|
| `account-number` | string | The tastytrade account number. |
| `symbol` | string | The full symbol for the position (e.g., `AAPL` for equities, OCC symbol for options). |
| `underlying-symbol` | string | The underlying symbol (e.g., `AAPL` for both the stock and its options). |
| `instrument-type` | string | The instrument type: `Equity`, `Equity Option`, `Future`, `Future Option`, `Cryptocurrency`. |
| `streamer-symbol` | string | The symbol used for the DXLink streaming feed (may differ from `symbol`). |

### Quantity & Direction

| Field | Type | Description |
|---|---|---|
| `quantity` | object | The position quantity (string-encoded decimal for precision). |
| `quantity-direction` | string | `Long` or `Short` — indicates whether the position is a long or short holding. |
| `restricted-quantity` | object | The quantity of the position that is restricted (e.g., from unsettled trades). |
| `multiplier` | number (double) | The contract multiplier (e.g., `1` for equities, `100` for standard equity options). |

### Pricing & Valuation

| Field | Type | Description |
|---|---|---|
| `average-open-price` | number (double) | The average price at which the position was opened (cost basis per unit). |
| `close-price` | number (double) | The most recent closing price of the instrument. |
| `mark` | number (double) | The current total mark value of the position (mark-price × quantity × multiplier). |
| `mark-price` | number (double) | The current mark price per unit of the instrument. |
| `average-daily-market-close-price` | number (double) | The average daily market close price. |
| `average-yearly-market-close-price` | number (double) | The average yearly market close price. |
| `fixing-price` | number (double) | The fixing price (applicable to certain instruments like crypto). |
| `face-value` | number (double) | The face value (applicable to bonds and fixed-income instruments). |
| `par-size` | number (double) | The par size (applicable to bonds and fixed-income instruments). |

### Realized Gains

| Field | Type | Description |
|---|---|---|
| `realized-day-gain` | number (double) | Realized gain/loss for the current trading day. |
| `realized-day-gain-date` | date | The date of the realized day gain calculation. |
| `realized-day-gain-effect` | string | `Debit` or `Credit` — the direction of the realized day gain. |
| `realized-today` | number (double) | Total realized gain/loss today (may include multiple closing transactions). |
| `realized-today-date` | date | The date of the realized-today calculation. |
| `realized-today-effect` | string | `Debit` or `Credit` — the direction of today's realized gain/loss. |

### Position Metadata

| Field | Type | Description |
|---|---|---|
| `cost-effect` | string | `Debit` or `Credit` — whether opening this position was a debit or credit to the account. |
| `is-frozen` | boolean | Whether the position is frozen (cannot be traded). |
| `is-suppressed` | boolean | Whether the position is suppressed from display. |
| `deliverable-type` | string | The deliverable type (relevant for options and futures approaching delivery). |
| `expires-at` | datetime | The expiration date and time for options and futures contracts. |
| `created-at` | datetime | Timestamp when the position was first opened. |
| `updated-at` | datetime | Timestamp of the last update to this position record. |
| `order-id` | integer | The order ID of the most recent order that modified this position. |
| `update-type` | string | The type of the most recent update to the position. |

---
## Example Response

```json
{
  "data": {
    "items": [
      {
        "account-number": "5WX34382",
        "symbol": "AAPL",
        "instrument-type": "Equity",
        "underlying-symbol": "AAPL",
        "quantity": "10",
        "quantity-direction": "Long",
        "average-open-price": "178.50",
        "close-price": "185.25",
        "mark": "1852.50",
        "mark-price": "185.25",
        "multiplier": 1,
        "cost-effect": "Debit",
        "realized-day-gain": "0.0",
        "realized-day-gain-effect": "None",
        "realized-today": "0.0",
        "realized-today-effect": "None",
        "created-at": "2026-02-17T15:30:00.000+00:00",
        "updated-at": "2026-04-09T14:00:00.000+00:00"
      },
      {
        "account-number": "5WX34382",
        "symbol": "AAL   270115C00017000",
        "instrument-type": "Equity Option",
        "underlying-symbol": "AAL",
        "quantity": "1",
        "quantity-direction": "Long",
        "average-open-price": "3.50",
        "multiplier": 100,
        "cost-effect": "Debit",
        "expires-at": "2027-01-15T21:00:00.000+00:00",
        "created-at": "2025-11-01T12:00:00.000+00:00",
        "updated-at": "2026-04-09T14:00:00.000+00:00"
      }
    ]
  }
}