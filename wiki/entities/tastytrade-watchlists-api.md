---
tags: ["API", "REST", "trading", "financial-data", "watchlist", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "watchlists.md"
---
# tastytrade Watchlists API

The tastytrade Watchlists API provides endpoints for managing user-defined watchlists, accessing tastytrade's curated public watchlists, and retrieving specialized pairs watchlists. User watchlists are scoped to the authenticated user, not to a specific trading account.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 2.2.0

## Endpoints Overview

The API is structured around three main categories of watchlists:

1.  **User Watchlists:**
    *   `GET /watchlists`: Retrieve all watchlists for the authenticated user.
    *   `GET /watchlists/{watchlist_name}`: Retrieve a specific user watchlist by name.
    *   `POST /watchlists`: Create a new user watchlist.
    *   `PUT /watchlists/{watchlist_name}`: Update an existing user watchlist (full replacement).
    *   `DELETE /watchlists/{watchlist_name}`: Delete a user watchlist.

2.  **Public Watchlists:**
    *   `GET /public-watchlists`: Retrieve all tastytrade-curated public watchlists.
    *   `GET /public-watchlists/{watchlist_name}`: Retrieve a specific public watchlist by name.
    *   *Note: Public watchlists are read-only and cannot be modified by users.*

3.  **Pairs Watchlists:**
    *   `GET /pairs-watchlists`: Retrieve all pairs watchlists.
    *   `GET /pairs-watchlists/{pairs_watchlist_name}`: Retrieve a specific pairs watchlist by name.

## Data Models

The API primarily interacts with two data models:

*   [[../concepts/watchlist-data-model.md|Watchlist Data Model]]: Used for user and public watchlists, containing symbols and instrument types.
*   [[../concepts/pairs-watchlist-data-model.md|PairsWatchlist Data Model]]: Used for pairs watchlists, containing symbol pairs and their relationships.

## Common Use Cases

*   **Portfolio Tracking:** Create watchlists for portfolio holdings and use other API endpoints (e.g., Market Data) to fetch bulk data.
*   **Sector Screening:** Utilize public watchlists to get curated sector groupings for analysis, such as finding high-IVR candidates.
*   **Watchlist Synchronization:** Programmatically update user watchlists from external systems.
*   **Organization:** Group watchlists using the `group-name` field for better categorization (e.g., "Thematic ETFs", "Earnings This Week").

## Important Notes

*   **User-Scoped:** User watchlists are tied to the authenticated user, not a specific trading account.
*   **Full Replacement on PUT:** The `PUT` endpoint for updating user watchlists performs a full replacement. All desired entries, including existing ones, must be included in the request body.
*   **Watchlist Name as Identifier:** Watchlist names are used as unique identifiers in URL paths. Choose descriptive and URL-safe names.
*   **Read-Only Public Watchlists:** tastytrade's public watchlists cannot be modified by users.

This API is provided by [[../entities/tastytrade.md|tastytrade]].