---
tags: ["api", "trading", "alerts", "tastyworks", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/quote-alerts.md"
---
# Tastyworks Quote Alerts API

The Tastyworks Quote Alerts API provides functionality to create, retrieve, and cancel price-based alerts on various financial symbols. These alerts trigger when a specified [[../concepts/market-data-fields.md|market data field]] (such as last price, bid, ask, or [[../concepts/implied-volatility.md|implied volatility]]) crosses a predefined [[../concepts/threshold.md|threshold]].

Alerts are scoped to the authenticated user, not to a specific trading account, meaning an alert created by a user will be visible and managed by that user regardless of which account they might be actively trading with.

## Base Information

*   **Base URL:** `https://api.tastyworks.com`
*   **[[../concepts/api-authentication.md|Authentication]]:** Requires a valid session token passed via the `Authorization` header.
*   **API Version:** 1.23.0

## Endpoints

### Get Quote Alerts

Retrieves all active and historical [[../entities/quote-alert-data-model.md|quote alerts]] for the current user.

*   **Request:** `GET /quote-alerts`
*   **Parameters:** None.
*   **Response:** `200 OK` - Returns an array of [[../entities/quote-alert-data-model.md|QuoteAlert]] objects.

### Create Quote Alert

Creates a new price alert for a specified symbol.

*   **Request:** `POST /quote-alerts`
*   **Content-Type:** `application/json`
*   **Request Body Fields:**
    *   `symbol` (string, required): The symbol to monitor (e.g., `AAPL`, `SPY`, `/ESM6`).
    *   `field` (string, required): The [[../concepts/market-data-fields.md|market data field]] to monitor: `Last` (last trade price), `Bid`, `Ask`, or `IV` ([[../concepts/implied-volatility.md|implied volatility]]).
    *   `operator` (string, required): The comparison operator: `>` (greater than) or `<` (less than).
    *   `threshold` (string, required): The price or value [[../concepts/threshold.md|threshold]] that triggers the alert (e.g., `"200.00"`).
    *   `instrument-type` (string, optional): The instrument type (e.g., `Equity`, `Equity Option`, `Future`).
    *   `dx-symbol` (string, optional): The DXLink streamer symbol (if different from `symbol`).
    *   `threshold-numeric` (string, optional): Numeric representation of the threshold.
    *   `expires-at` (string, optional): When the alert should expire if not triggered (ISO 8601 datetime).
*   **Response:** `201 Created` - Returns the newly created [[../entities/quote-alert-data-model.md|QuoteAlert]] object.

### Cancel Quote Alert

Cancels (deletes) an existing quote alert.

*   **Request:** `DELETE /quote-alerts/{alert_external_id}`
*   **Path Parameters:**
    *   `alert_external_id` (integer, required): The unique external ID of the alert to cancel.
*   **Response:** `204 No Content`

## Important Notes

*   **User-scoped:** Alerts are tied to the authenticated user, not a specific account.
*   **Threshold as string:** The `threshold` field in the request body must be passed as a string (e.g., `"200.00"`), even if it represents a numeric value.
*   **One-shot alerts:** Alerts trigger once and then enter a completed state. To monitor continuously, a new alert must be created after each trigger.
*   **IV field:** When using `field: "IV"`, the threshold represents [[../concepts/implied-volatility.md|implied volatility]] as a decimal (e.g., `"0.35"` for 35% IV), consistent with how IV is returned by the Market Metrics API.

For more general information on the concept of alerts, see [[../concepts/price-alerts.md|Price Alerts]].
This API is part of the broader [[../entities/tastyworks.md|Tastyworks]] platform.

---