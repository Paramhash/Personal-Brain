---
tags: ["tastytrade", "API", "orders", "trading", "positions"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Orders

Orders are the primary mechanism for trading and managing [[../concepts/tastytrade-api-positions.md|positions]] within the tastytrade API.

## Order Structure

Each order can have a maximum of four "legs." Each leg specifies:

*   **Symbol**: The [[../concepts/tastytrade-api-symbology.md|symbol]] of the [[../concepts/tastytrade-api-instruments.md|instrument]] to be traded.
*   **Quantity**: The number of units of the instrument.
*   **Action**: Combines a direction (Buy/Sell) and an effect (Open/Close).
    *   **Open**: "Increase my position." If no position exists, a new one is created upon order fill.
    *   **Close**: "Decrease my position."

## Order Actions Explained

*   **Buy to Open**: Increases a long position or creates a new long position.
    *   *Example*: To buy 100 shares of AAPL, you submit an order with one leg: `Symbol: AAPL`, `Quantity: 100`, `Action: Buy to Open`. Upon fill, a long position of 100 AAPL shares is created.
*   **Sell to Close**: Decreases an existing position (long or short).
    *   *Example*: If you are long 100 AAPL shares and want to sell 10, you submit an order: `Symbol: AAPL`, `Quantity: 10`, `Action: Sell to Close`. Your long position reduces to 90 shares.
    *   It is acceptable to close an entire position in a single order (e.g., Sell to Close 100 shares if long 100).
*   **Sell to Open**: Initiates a short position (often called "selling short").
    *   *Example*: To short 50 shares of TSLA, you submit an order: `Symbol: TSLA`, `Quantity: 50`, `Action: Sell to Open`. Upon fill, a short position of 50 TSLA shares is created.
*   **Buy to Close**: Decreases an existing short position.

## Position Restrictions

*   **No Simultaneous Long/Short**: tastytrade does not permit holding both a long and a short position in the same instrument simultaneously.
    *   You cannot `Sell to Open` if you have an existing long position.
    *   You cannot `Buy to Open` if you have an existing short position.
    *   If you are long and continue to `Sell to Close` past zero quantity, your position direction will flip to short.

## Order Status Lifecycle

Orders have a status that changes throughout their lifecycle (e.g., pending, filled, cancelled, rejected). The specific order flow and status transitions are detailed in the tastytrade API documentation on the "Order Flow" page.

For more information on how orders affect your holdings, see [[../concepts/tastytrade-api-positions.md|tastytrade API Positions]]. For an overall understanding of the API, refer to the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].