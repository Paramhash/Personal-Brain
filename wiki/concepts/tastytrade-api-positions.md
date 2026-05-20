---
tags: ["tastytrade", "API", "positions", "trading"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Positions

A position represents your current holdings in a specific [[../concepts/tastytrade-api-instruments.md|tradeable instrument]] within your [[../concepts/tastytrade-api-accounts.md|account]]. Positions are created or adjusted when an [[../concepts/tastytrade-api-orders.md|order]] fills.

## Position Attributes

Each position is defined by:

*   **Symbol**: The unique [[../concepts/tastytrade-api-symbology.md|symbol]] of the instrument (e.g., `AAPL`, `/ESZ2`).
*   **Quantity**: The number of units of the instrument held. This is always a positive number.
*   **Direction**: Indicates whether the position is `Long` (you own the instrument) or `Short` (you have sold the instrument you don't own).

## Position Management

*   **Creation/Adjustment**: When an order fills, it either creates a new position (if none existed for that symbol) or adjusts the quantity and/or direction of an existing one.
*   **Unique Symbol Rule**: You cannot create multiple positions with the same symbol. For example, you cannot simultaneously be long AAPL stock and short AAPL stock.
    *   If you are long AAPL stock and submit a sell order, the quantity of your long position will decrease.
    *   If you continue to sell after your long quantity reaches zero, the direction of your position will flip from `Long` to `Short`, and the quantity will increase in the short direction.

For more detailed information, refer to the tastytrade "Account Positions Api Guide."

This concept is closely related to [[../concepts/tastytrade-api-orders.md|Orders]] and is a core component of the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].