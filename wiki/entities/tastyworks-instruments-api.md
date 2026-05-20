---
tags: ["api", "tastyworks", "financial-data", "instruments"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# tastyworks Instruments API

The tastyworks Instruments API provides a comprehensive set of endpoints for looking up detailed instrument definitions across various asset classes, including equities, equity options, futures, futures options, cryptocurrency, and warrants. It also offers option chain data in multiple formats (full, compact, nested) for both equity and futures options.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 0.0.1 (versioned as `20250715`)

## Endpoints

### Equities

*   **Get Equity by Symbol**
    *   `GET /instruments/equities/{symbol}`
    *   Returns a single [[../concepts/equity-instrument-definition.md|Equity]] instrument definition.
    *   Parameters: `symbol` (path, string, Yes) - Equity ticker symbol (e.g., `AAPL`, `SPY`).

*   **Get Active Equities**
    *   `GET /instruments/equities/active`
    *   Returns all active equity instruments in a paginated fashion.
    *   Parameters: `page-offset` (query, integer, No), `per-page` (query, integer, No), `lendability` (query, string, No) - Filter by lendability status (`Easy To Borrow`, `Locate Required`, `Preborrow`).
    *   Response: Array of [[../concepts/equity-instrument-definition.md|Equity]] objects.

### Equity Options

*   **Get Equity Option by Symbol**
    *   `GET /instruments/equity-options/{symbol}`
    *   Returns a single [[../concepts/equity-option-instrument-definition.md|EquityOption]] instrument definition.
    *   Parameters: `symbol` (path, string, Yes) - The OCC option symbol (e.g., `AAPL  260417C00200000`), `active` (query, boolean, No) - Filter to active options only.

*   **Get Equity Option Chain (Full)**
    *   `GET /option-chains/{symbol}`
    *   Returns the full option chain for an underlying equity symbol.
    *   Parameters: `symbol` (path, string, Yes) - The underlying equity symbol (e.g., `AAPL`).
    *   Response: Array of [[../concepts/equity-option-instrument-definition.md|EquityOption]] objects.

*   **Get Equity Option Chain (Compact)**
    *   `GET /option-chains/{symbol}/compact`
    *   Returns the option chain in a compact form.
    *   Parameters: `symbol` (path, string, Yes) - The underlying equity symbol.
    *   Response: Array of [[../concepts/compact-option-chain-serializer.md|CompactOptionChainSerializer]] objects.

*   **Get Equity Option Chain (Nested)**
    *   `GET /option-chains/{symbol}/nested`
    *   Returns the option chain in a nested structure organized by expiration date, then by strike price.
    *   Parameters: `symbol` (path, string, Yes) - The underlying equity symbol.
    *   Response: Array of [[../concepts/nested-option-chain-serializer.md|NestedOptionChainSerializer]] objects.

### Futures

*   **Get Futures by Symbol(s)**
    *   `GET /instruments/futures`
    *   Returns one or more outright [[../concepts/future-instrument-definition.md|Future]] definitions.
    *   Parameters: `symbol` (query, array, No), `product-code` (query, array, No), `exchange` (query, string, No), `security-id` (query, array, No), `only-active-futures` (query, boolean, No), `page-offset` (query, integer, No), `per-page` (query, integer, No).

*   **Get Single Future by Symbol**
    *   `GET /instruments/futures/{symbol}`
    *   Returns a single outright [[../concepts/future-instrument-definition.md|Future]] definition.
    *   Parameters: `symbol` (path, string, Yes) - The futures symbol (e.g., `/ESM6`).

*   **Get Future Products**
    *   `GET /instruments/future-products`
    *   Returns metadata for all supported [[../concepts/future-product-definition.md|FutureProduct]] objects.
    *   Parameters: `page-offset` (query, integer, No), `per-page` (query, integer, No).

*   **Get Future Product by Exchange and Code**
    *   `GET /instruments/future-products/{exchange}/{code}`
    *   Returns a specific [[../concepts/future-product-definition.md|FutureProduct]] definition.
    *   Parameters: `exchange` (path, string, Yes), `code` (path, string, Yes).

### Futures Options

*   **Get Future Option by Symbol**
    *   `GET /instruments/future-options/{symbol}`
    *   Returns a single [[../concepts/future-option-instrument-definition.md|FutureOption]] definition.
    *   Parameters: `symbol` (path, string, Yes) - The tastytrade futures option symbol.

*   **Get Futures Option Chain (Full)**
    *   `GET /futures-option-chains/{symbol}`
    *   Returns the full futures option chain for a futures product code.
    *   Parameters: `symbol` (path, string, Yes) - The futures product code (e.g., `ES`).

*   **Get Futures Option Chain (Nested)**
    *   `GET /futures-option-chains/{symbol}/nested`
    *   Returns the futures option chain in nested form.
    *   Parameters: `symbol` (path, string, Yes) - The futures product code.
    *   Response: [[../concepts/futures-nested-option-chain-serializer.md|FuturesNestedOptionChainSerializer]] object.

*   **Get Future Option Products**
    *   `GET /instruments/future-option-products`
    *   Returns metadata for all supported [[../concepts/future-option-product-definition.md|FutureOptionProduct]] objects.
    *   Parameters: `page-offset` (query, integer, No), `per-page` (query, integer, No).

*   **Get Future Option Product by Root Symbol**
    *   `GET /instruments/future-option-products/{root_symbol}`
    *   Returns a [[../concepts/future-option-product-definition.md|FutureOptionProduct]] object.
    *   Parameters: `root_symbol` (path, string, Yes).

*   **Get Future Option Product by Exchange and Root Symbol**
    *   `GET /instruments/future-option-products/{exchange}/{root_symbol}`
    *   Returns a [[../concepts/future-option-product-definition.md|FutureOptionProduct]] object.
    *   Parameters: `exchange` (path, string, Yes), `root_symbol` (path, string, Yes).

### Cryptocurrency

*   **Get Cryptocurrencies**
    *   `GET /instruments/cryptocurrencies`
    *   Retrieve one or more [[../concepts/cryptocurrency-instrument-definition.md|Cryptocurrency]] instrument definitions.
    *   Parameters: `symbol` (query, string, No) - One or more cryptocurrency symbols (e.g., `BTC/USD`).

*   **Get Cryptocurrency by Symbol**
    *   `GET /instruments/cryptocurrencies/{symbol}`
    *   Retrieve a single [[../concepts/cryptocurrency-instrument-definition.md|Cryptocurrency]] definition.
    *   Parameters: `symbol` (path, string, Yes) - The cryptocurrency symbol (e.g., `BTC/USD`).

### Warrants

*   **Get Warrants**
    *   `GET /instruments/warrants`
    *   Returns [[../concepts/warrant-instrument-definition.md|Warrant]] definitions.
    *   Parameters: `symbol` (query, string, No) - Filter by warrant symbol(s).

*   **Get Warrant by Symbol**
    *   `GET /instruments/warrants/{symbol}`
    *   Returns a single [[../concepts/warrant-instrument-definition.md|Warrant]] definition.
    *   Parameters: `symbol` (path, string, Yes) - The warrant symbol (e.g., `RGTIW`).

### Utility

*   **Get Quantity Decimal Precisions**
    *   `GET /instruments/quantity-decimal-precisions`
    *   Returns the [[../concepts/quantity-decimal-precision.md|QuantityDecimalPrecision]] rules for all instrument types.

## Data Models

The API returns various data models representing different financial instruments and their related structures. Refer to the following concepts for detailed field descriptions:

*   [[../concepts/equity-instrument-definition.md|Equity Instrument Definition]]
*   [[../concepts/equity-option-instrument-definition.md|Equity Option Instrument Definition]]
*   [[../concepts/future-instrument-definition.md|Future Instrument Definition]]
*   [[../concepts/future-product-definition.md|Future Product Definition]]
*   [[../concepts/future-option-instrument-definition.md|Future Option Instrument Definition]]
*   [[../concepts/future-option-product-definition.md|Future Option Product Definition]]
*   [[../concepts/cryptocurrency-instrument-definition.md|Cryptocurrency Instrument Definition]]
*   [[../concepts/warrant-instrument-definition.md|Warrant Instrument Definition]]
*   [[../concepts/quantity-decimal-precision.md|Quantity Decimal Precision]]
*   [[../concepts/compact-option-chain-serializer.md|Compact Option Chain Serializer]]
*   [[../concepts/nested-option-chain-serializer.md|Nested Option Chain Serializer]]
*   [[../concepts/futures-nested-option-chain-serializer.md|Futures Nested Option Chain Serializer]]

## tastytrade Symbology Reference

The API utilizes specific symbol formats for different instrument types. For details, see [[../concepts/tastytrade-symbology.md|tastytrade Symbology]].

## Common Use Cases

*   **Building an order ticket:** Look up the equity via `GET /instruments/equities/{symbol}` to verify it's active and check `is-fractional-quantity-eligible`, then fetch the option chain via `GET /option-chains/{symbol}/nested` to populate expiration and strike selectors.
*   **Options chain display:** Use the `/nested` endpoint for UI rendering (grouped by expiration) or `/compact` for bandwidth-efficient retrieval. Use the full `/option-chains/{symbol}` endpoint when you need complete `EquityOption` objects for each contract.
*   **Futures product discovery:** Call `GET /instruments/future-products` to list all available futures products, then `GET /instruments/futures?product-code=ES&only-active-futures=true` to get tradeable contracts for a specific product.
*   **Symbol resolution:** When a position returns an OCC symbol like `AAPL  260417C00200000`, use `GET /instruments/equity-options/{symbol}` to get the full contract details including strike, expiration, and greeks availability.
*   **Quantity precision:** Before submitting an order, call `GET /instruments/quantity-decimal-precisions` to verify the minimum increment for the instrument type (critical for cryptocurrency and fractional equity orders).
*   **Short selling availability:** Use `GET /instruments/equities/{symbol}` and check the `lendability` field to determine if a stock can be sold short.