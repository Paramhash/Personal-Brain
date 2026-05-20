---
tags: ["api", "watchlists", "alerts", "market-monitoring", "trading", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# API Watchlists and Quote Alerts (tastytrade)

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] offers comprehensive CRUD (Create, Read, Update, Delete) capabilities for managing user watchlists and setting up real-time quote alerts. These features are essential for market monitoring and timely trading decisions.

## Watchlists
*   **User Watchlists**: Full CRUD operations are available for managing personal watchlists. This includes creating new watchlists, adding/removing symbols, retrieving watchlist contents, and deleting watchlists. `PUT` operations typically imply a full replacement of the watchlist content.
*   **Public Watchlists**: Read-only access to watchlists curated by tastytrade or other public sources.
*   **Pairs Watchlists**: Specific watchlists designed for monitoring pairs trading strategies.

## Quote Alerts
*   **CRUD for Price Alerts**: Users can create, retrieve, update, and delete price alerts.
*   **Monitoring Parameters**: Alerts can be configured to monitor `Last`, `Bid`, `Ask`, or `Implied Volatility (IV)` of an instrument.
*   **Operators**: Alerts can be triggered when a monitored value is `>` (greater than) or `<` (less than) a specified threshold.
*   **User-Scoped**: Alerts are typically tied to the user's account.
*   **One-Shot Triggers**: Many alert systems are "one-shot," meaning they trigger once and then need to be re-enabled or re-created.

These API features allow developers to build custom market monitoring tools, integrate watchlist management into their applications, and automate notifications for specific market conditions.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]
*   [[../concepts/api-streaming-data-tastytrade.md|Streaming Market and Account Data]]