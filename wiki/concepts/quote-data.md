---
tags: ["market-data", "pricing", "api"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# Quote Data

Quote data refers to the real-time or near real-time pricing information for a financial instrument, typically including bid, ask, and last trade prices. This data is crucial for understanding market liquidity and making trading decisions.

In the [[Market Data API (Tastyworks)|Tastyworks Market Data API]], quote data is a core component of the [[MarketData Object]].

## Key Fields in MarketData Object
*   `bid` (number): The highest price a buyer is willing to pay.
*   `bidSize` (number): The quantity of shares/contracts available at the bid price.
*   `ask` (number): The lowest price a seller is willing to accept.
*   `askSize` (number): The quantity of shares/contracts available at the ask price.
*   `mid` (number): The midpoint between the bid and ask prices (`(bid + ask) / 2`). Often used as an indicative fair value.
*   `mark` (number): An exchange-calculated or derived price, often used for valuation (e.g., for portfolio mark-to-market).

## Use Cases
*   **Pre-trade pricing:** Determining an appropriate limit price for an order.
*   **Portfolio valuation:** Using the `mark` price to calculate current portfolio value.
*   **Liquidity assessment:** Analyzing bid/ask sizes to gauge market depth.

## Related
*   [[MarketData Object]]
*   [[Market Data API (Tastyworks)]]