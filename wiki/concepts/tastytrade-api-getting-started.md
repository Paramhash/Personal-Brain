---
tags: ["tastytrade", "API", "getting-started", "introduction"]
created: 2023-10-27
reviewed: false
source_origin: "getting-started.md"
---
# tastytrade API: Getting Started Guide

This guide provides an introduction to the [tastytrade API](../entities/tastytrade.md) and walks new users through key features such as logging in, submitting orders, viewing positions, and closing positions.

For a broader understanding of API rules and patterns, refer to the general API Overview. Core tastytrade concepts relevant to the API can be found in the High-level Concepts section of the API Overview. For direct API documentation, consult the API Docs page.

## Initial Steps

To begin using the tastytrade API, follow these steps:

1.  **Create a Sandbox Account**: Start by creating an account in the [Sandbox environment](./tastytrade-api-environments.md). This dedicated test environment allows you to build and test your applications without using real money.
2.  **Generate an OAuth2 Access Token**: Every request to the API requires an `Authorization` header with a valid access token. More information on session management and authorization can be found in the [Authorization & Authentication guide](./tastytrade-api-authorization.md).
3.  **Submit a Trade**: Learn how to submit orders using the Submit Order endpoint. Detailed instructions on order structure are available in the [Order Submission & Management guide](./tastytrade-api-order-submission.md). The Sandbox environment offers custom logic to simulate order fills, partial fills, or live orders.
4.  **Fetch Account Balance and Positions**: After an order fills, a new position is created, and your account balance updates. Use the List Account Positions endpoint to fetch your current positions and the List Account Balances endpoint to view your account balance. See [Account Balances, Positions & Updates](./tastytrade-api-account-data.md) for more details.
5.  **Stream Market Data**: Obtain real-time (Production) or delayed (Sandbox) quotes by streaming market data. Refer to the [Market Data & Option Chains guide](./tastytrade-api-market-data.md) for details.
6.  **Fetch Market Data**: Alternatively, fetch quotes via HTTP. The Market Data Guide provides further assistance.
7.  **Stream Account Updates**: Receive real-time updates regarding your account by utilizing streaming account data. More information is in the [Account Balances, Positions & Updates guide](./tastytrade-api-account-data.md).
8.  **Close a Position**: Close an open position by submitting an order in the opposite direction. For example, to close a long position of 100 shares of AAPL, submit a Sell to Close order for 100 shares of AAPL. This will zero out your position upon fill. Further information on opening and closing positions, including Leg Attributes, is available in the [Order Submission & Management guide](./tastytrade-api-order-submission.md).
9.  **Fetch an Option Chain**: Retrieve a full option chain for a given ticker symbol, including put and call symbols, expirations, and the [DxLink](../entities/dxlink.md) `streamer-symbol` for subscribing to quote data. This is covered in the [Market Data & Option Chains guide](./tastytrade-api-market-data.md).

## Support

If you encounter issues or have questions, check the FAQ page. For further assistance, submit a ticket by emailing api.support@tastytrade.com.