---
tags: ["api", "tastytrade", "account-management", "trading"]
created: 2023-10-27
reviewed: false
source_origin: "account-status.md"
---
# Tastytrade Account Status API

The Tastytrade Account Status API provides comprehensive information about a trading account's current permissions, restrictions, and configuration. This API is crucial for determining authorized asset classes, trading strategies, identifying restricted states (e.g., margin call, closing-only, frozen), and understanding key margin and day-trading parameters.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 6.0.0

## Endpoints

### Get Account Trading Status

Retrieves the current trading status for a specific account.

**Request**

```
GET /accounts/{account_number}/trading-status
```

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `account_number` | string | Yes | The tastytrade account number (e.g., `5WX34382`) |

**Response** — `200 OK`

Returns a [[../concepts/trading-status-object.md|TradingStatus object]] wrapped in the standard tastytrade response envelope under `data`.

## Example Response

```json
{
  "data": {
    "account-number": "5WX34382",
    "options-level": "Advanced",
    "is-cryptocurrency-enabled": true,
    "is-futures-enabled": true,
    "is-pattern-day-trader": false,
    "day-trade-count": 0,
    "is-closing-only": false,
    "is-frozen": false,
    "is-in-margin-call": false,
    "equities-margin-calculation-type": "Reg-T",
    "is-portfolio-margin-enabled": false,
    "futures-margin-rate-multiplier": 1.0,
    "short-calls-enabled": true,
    "updated-at": "2026-03-15T14:22:00.000+00:00"
  }
}
```

Note: The response is wrapped in the standard [[../entities/tastytrade.md|Tastytrade]] API envelope with a `data` key. Not all fields are returned in every response — only fields relevant to the account's current configuration will be present.

## Common Use Cases

*   **Pre-trade validation:** Check `is-closing-only`, `is-frozen`, or `is-risk-reducing-only` before attempting to submit an order to avoid unnecessary rejections.
*   **Asset class gating:** Verify `is-futures-enabled`, `is-cryptocurrency-enabled`, or `options-level` to determine which instruments are available for the account.
*   **Margin monitoring:** Check `is-in-margin-call` and `is-in-day-trade-equity-maintenance-call` to detect accounts that need attention.
*   **[[../concepts/pattern-day-trader.md|PDT]] awareness:** Use `is-pattern-day-trader` and `day-trade-count` to warn users approaching the PDT threshold on accounts under $25K.