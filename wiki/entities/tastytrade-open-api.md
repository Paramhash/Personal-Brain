---
tags: ["api", "rest", "json", "trading", "fintech", "developer-tools"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# tastytrade Open API

The tastytrade Open API is a REST/JSON API that provides programmatic access to the [[../entities/tastytrade.md|tastytrade]] brokerage platform. It is designed for developers, fintech platforms, algorithmic traders, and AI/LLM applications to interact with account data, place trades, retrieve market data, and stream real-time quotes and account updates.

## Key Features
*   **REST/JSON Interface**: Utilizes standard RESTful conventions with JSON payloads.
*   **OAuth2 Authentication**: All requests are secured using OAuth2 bearer tokens.
*   **Comprehensive Functionality**:
    *   Access to account data (balances, positions, transactions).
    *   Order submission and management.
    *   Real-time market data streaming via DXLink WebSocket.
    *   Real-time account updates streaming via WebSocket.
    *   Market data retrieval (quotes, metrics, sessions).
    *   Instrument search and details.
    *   [[../concepts/api-backtesting-tastytrade.md|Backtesting]] capabilities for options strategies.
    *   [[../concepts/api-margin-requirements-tastytrade.md|Margin requirement]] calculations.
    *   [[../concepts/api-watchlists-and-alerts-tastytrade.md|Watchlist and quote alert]] management.
*   **Environments**: Separate production and [[../concepts/api-sandbox-environments.md|sandbox environments]] for development and testing.
*   **SDKs**: Official and community-contributed [[../concepts/api-sdks.md|Software Development Kits]].

## Authentication
API requests are authenticated using [[../concepts/oauth2-authentication.md|OAuth2 bearer tokens]], which are passed in the `Authorization` header. Access tokens typically have a 15-minute expiry and can be refreshed using a refresh token.

## Base URLs
*   **Production**: `https://api.tastyworks.com`
*   **Sandbox**: `https://api.cert.tastyworks.com`

## Core Concepts
*   [[../concepts/oauth2-authentication.md|OAuth2 Authentication]]
*   [[../concepts/api-symbology-tastytrade.md|API Symbology]]
*   [[../concepts/api-streaming-data-tastytrade.md|Streaming Market and Account Data]]
*   [[../concepts/api-order-management-tastytrade.md|Order Submission and Management]]
*   [[../concepts/api-sandbox-environments.md|Sandbox Environments]]
*   [[../concepts/api-sdks.md|SDKs]]
*   [[../concepts/api-backtesting-tastytrade.md|Backtesting]]
*   [[../concepts/api-margin-requirements-tastytrade.md|Margin Requirements]]
*   [[../concepts/api-watchlists-and-alerts-tastytrade.md|Watchlists and Quote Alerts]]

## Source Documentation
This information is derived from the [[../sources/tastytrade-open-api-documentation.md|tastytrade Open API Documentation]].