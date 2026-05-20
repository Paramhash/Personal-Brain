---
tags: ["tastytrade", "API", "symbology", "equities", "options", "futures", "cryptocurrencies", "instruments"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Symbology

tastytrade uses specific symbology conventions to identify different tradeable [[../concepts/tastytrade-api-instruments.md|instruments]]. Understanding these formats is crucial for submitting orders and interpreting market data.

## Equities

Equity symbols consist of alphanumeric characters (A-Z, 0-9), occasionally including a `/`.
**Examples:** `AAPL`, `BRK/A`

## Equity Options

Equity option symbols follow conventions similar to the Options Clearing Corporation (OCC), comprising four main parts:

1.  **Root symbol**: 6 alphanumeric digits, whitespace-padded (e.g., `AAPL  `, `FB    `, `BRK/A `).
2.  **Expiration date**: 6 numeric digits in `yymmdd` format.
3.  **Option type**: `P` for Put or `C` for Call.
4.  **Strike price**: 8 numeric digits, front-padded with zeros, no decimals. The strike price is multiplied by 1000 (e.g., 64.0 strike: `00064000`, 1050.55 strike: `01050550`, 0.50 strike: `00000500`).

**Example Equity Option Symbols:**
*   `AAPL June 17, 2022 150 Put`: `AAPL  220617P00150000`
*   `SPY Nov 18, 2022 400 Call`: `SPY   221118C00400000`
*   `SPX May 20, 2022 4025 Call`: `SPXW  220520C04025000`

## Futures

Futures symbols always begin with a slash (`/`), followed by a contract code. The contract code consists of three parts:

1.  **Product code**: 1-3 uppercase letters (A-Z). A full list can be found via the "List Future Products" endpoint.
2.  **Month code**: A single letter representing the expiration month (e.g., `F` for January, `G` for February, `H` for March, `M` for June, `U` for September, `Z` for December).
3.  **Year**: 1-2 digit number for the year.

**Example Futures Symbols:**
*   `E-mini S&P 500 December 2022`: `/ESZ2`
*   `Crude Oil December 2022`: `/CLZ2`
*   `CBOE Volatility Index November 2022`: `/VXX22`

## Future Options

Future options have a more complex symbology due to unique product codes for each expiration series.

*   **Structure**: Always starts with `./`, followed by the future contract code, the option contract code, the expiration date, option type (`C`/`P`), and strike price.
*   **Option Product Codes**: Each future option expiration series has a unique product code (e.g., monthly CL options use `LO`, weekly CL options use `LO1`, `LO2`, etc.). Different future products may have various weekly option codes (e.g., ES weekly Monday options use `E1A`, `E2A`, etc.).
*   **Retrieval**: A full list of supported future option products can be found via the "List Future Option Products" endpoint, where each item's `root-symbol` is the product code.

**Example Future Option Symbols:**
*   `./CLZ2 LO1X2 221104C91`: A November weekly option product (`LO1X2`) that settles into the December CL future contract (`CLZ2`), expiring 2022-11-04, a Call option at the 91 strike.
*   `./ESZ2 E1AZ2 221205P3720`: A weekly Monday option product (`E1A`) for the December ES Future contract (`ESZ2`), expiring 2022-12-05, a Put option at the 3720 strike.

## Cryptocurrencies

Cryptocurrency symbols can be retrieved via the `GET /instruments/cryptocurrencies` endpoint in the `symbol` field of the response data.
**Examples:** `BCH/USD`, `BTC/USD`

This detailed symbology ensures precise identification of all tradeable assets within the tastytrade API. For an overall understanding of the API, refer to the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].