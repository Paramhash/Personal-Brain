---
tags: ["data-model", "pairs-trading", "watchlist", "API", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "watchlists.md"
---
# PairsWatchlist Data Model

The `PairsWatchlist` data model is specifically designed for watchlists containing symbol pairs used in pairs trading strategies. It is distinct from the standard [[./watchlist-data-model.md|Watchlist Data Model]] and is used by the [[../entities/tastytrade-watchlists-api.md|tastytrade Watchlists API]] for pairs watchlists.

## Structure

| Field             | Type    | Description                                                 |
| :---------------- | :------ | :---------------------------------------------------------- |
| `name`            | string  | The unique name of the pairs watchlist.                     |
| `pairs-equations` | object  | An object containing the equations or definitions for the symbol relationships in the pairs. |
| `order-index`     | integer | An optional display order index for sorting watchlists.     |

## Usage

This model is used when retrieving pairs watchlists through the dedicated endpoints of the [[../entities/tastytrade-watchlists-api.md|Watchlists API]]. It allows traders to define and track specific pairs for arbitrage or other relative value strategies.