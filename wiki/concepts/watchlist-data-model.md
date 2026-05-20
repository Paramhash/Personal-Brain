---
tags: ["data-model", "watchlist", "API", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "watchlists.md"
---
# Watchlist Data Model

The `Watchlist` data model represents a collection of financial instruments. It is used by the [[../entities/tastytrade-watchlists-api.md|tastytrade Watchlists API]] for both user-defined and public watchlists.

## Structure

| Field             | Type    | Description                                                              |
| :---------------- | :------ | :----------------------------------------------------------------------- |
| `name`            | string  | The unique name of the watchlist.                                        |
| `watchlist-entries` | object  | An array of instruments included in the watchlist. Each entry contains:  |
|                   |         | - `symbol` (string): The instrument symbol (e.g., `AAPL`, `/ESM6`).    |
|                   |         | - `instrument-type` (string, optional): The type of instrument (e.g., `Equity`, `Future`). |
| `group-name`      | string  | An optional name for grouping related watchlists.                        |
| `order-index`     | integer | An optional display order index for sorting watchlists (default: `9999`). |
| `cms-id`          | string  | A CMS identifier, primarily used for public watchlists managed via content management systems. |

## Example

```json
{
  "name": "AI Infrastructure",
  "group-name": "Thematic ETFs",
  "watchlist-entries": [
    { "symbol": "VRT", "instrument-type": "Equity" },
    { "symbol": "DELL", "instrument-type": "Equity" },
    { "symbol": "DLR", "instrument-type": "Equity" },
    { "symbol": "SMCI", "instrument-type": "Equity" }
  ],
  "order-index": 100
}
```

## Usage

This model is central to creating, retrieving, and updating user watchlists, and for fetching tastytrade's curated public watchlists via the [[../entities/tastytrade-watchlists-api.md|Watchlists API]].