---
tags: ["api", "tastyworks", "search", "instrument-data"]
created: 2023-10-27
reviewed: false
source_origin: "symbol-search.md"
---
# Tastyworks Symbol Search API

The Tastyworks Symbol Search API provides a dedicated endpoint for looking up financial instruments by their symbol or partial symbol match. It is primarily used to build typeahead/autocomplete search functionality and to resolve symbol fragments into full instrument details.

This API is part of the broader [[../entities/tastyworks-api.md|Tastyworks API]] ecosystem.

## Base URL
`https://api.tastyworks.com`

## Authentication
Requires a valid session token passed via the `Authorization` header. See [[../concepts/api-authentication.md|API Authentication]] for more details.

## API Version
1.0.0

## Endpoints

### Search Symbols

Searches for instruments by symbol or partial symbol. Results can include matching [[../concepts/equity-instrument.md|equities]], [[../concepts/options-instrument.md|options]] underlyings, [[../concepts/futures-instrument.md|futures]], and other instrument types.

**Request**
`GET /symbols/search/{symbol}`

**Path Parameters**
*   `symbol` (string, Required): The symbol or symbol fragment to search (e.g., `AAP` will return results for `AAP`, `AAPL`, and other matches).

**Response** — `200 OK`
Returns an array of [[../concepts/symbol-data-model.md|SymbolData]] objects matching the search query.

**Example Response**
```json
{
  "data": {
    "items": [
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "listed-market": "NASDAQ",
        "instrument-type": "Equity",
        "options": true,
        "price-increments": "$0.01 to $1.00: $0.01, above $1.00: $0.01",
        "trading-hours": "09:30-16:00 ET"
      },
      {
        "symbol": "AAP",
        "description": "Advance Auto Parts Inc.",
        "listed-market": "NYSE",
        "instrument-type": "Equity",
        "options": true,
        "price-increments": "$0.01 to $1.00: $0.01, above $1.00: $0.01",
        "trading-hours": "09:30-16:00 ET"
      }
    ]
  }
}
```

## Common Use Cases

*   **Search/autocomplete:** Build a typeahead search box that calls this endpoint as the user types. A query of `AAP` returns both `AAP` and `AAPL`.
*   **Symbol validation:** Verify that a user-entered symbol exists before attempting to fetch quotes or place orders.
*   **Options availability check:** Use the `options` boolean field from [[../concepts/symbol-data-model.md|SymbolData]] to determine whether an option chain can be fetched for a given symbol.
*   **Instrument type discovery:** Use the `instrument-type` field from [[../concepts/symbol-data-model.md|SymbolData]] to determine the instrument type and route to the appropriate order ticket.

## Important Notes

*   **Partial matching:** The search performs prefix matching. Entering `SP` will return `SPY`, `SPXL`, `SPLG`, etc.
*   **Single endpoint:** Unlike most other Tastyworks API services, Symbol Search has only one endpoint. For detailed instrument data (tick sizes, option chains, futures products), use the [[../entities/tastyworks-instruments-api.md|Instruments API]] after resolving the symbol.
*   **No pagination:** Results are returned in a single response without pagination parameters.