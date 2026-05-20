---
tags: ["tastytrade", "API", "orders", "trade", "positions", "leg-attributes"]
created: 2023-10-27
reviewed: false
source_origin: "getting-started.md"
---
# tastytrade API: Order Submission & Management

The [tastytrade API](../entities/tastytrade.md) allows users to submit and manage trade orders programmatically. This includes opening new positions and closing existing ones.

## Submitting a Trade

To submit a trade, you will interact with the **Submit Order endpoint**. This endpoint requires specific instructions on how to structure an order, which typically includes details such as:

*   Symbol
*   Quantity
*   Order type (e.g., market, limit)
*   Price (for limit orders)
*   Side (buy/sell)
*   Time in force (e.g., day, GTC)

Detailed instructions on how to structure an order can be found on the tastytrade Order Submission page.

### Sandbox Environment Order Logic

The [Sandbox environment](../concepts/tastytrade-api-environments.md) includes custom logic for order submission, making it easy to simulate various scenarios:

*   **Order Fill**: Simulate an order being fully executed.
*   **Partial Fill**: Simulate an order being partially executed.
*   **Live Order**: Simulate an order remaining open without immediate execution.

## Closing a Position

Closing an existing position is achieved by submitting an order that is opposite to the current position.

**Example**:
If you hold a long position of 100 shares of AAPL, you would submit a "Sell to Close" order for 100 shares of AAPL. When this order is filled, your position in AAPL will be zeroed out.

For more information on the attributes related to opening and closing legs of an order, refer to the Leg Attributes section of the Order Submission page.

Submitting orders directly impacts your [account balances and positions](./tastytrade-api-account-data.md). This process is a core part of the [tastytrade API: Getting Started Guide](./tastytrade-api-getting-started.md).