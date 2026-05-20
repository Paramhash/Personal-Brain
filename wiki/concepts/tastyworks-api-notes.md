---
tags: ["api", "tastyworks", "notes", "data-handling", "precision"]
created: 2024-05-15
reviewed: false
source_origin: "balances-and-positions.md"
---
# Tastyworks Balances and Positions API Important Notes

When working with the [[../entities/tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]], it's crucial to understand certain data characteristics and conventions to ensure accurate interpretation and processing.

## Quantity Precision
*   **Detail:** Position quantities (e.g., `quantity` in [[../entities/current-position.md|CurrentPosition]]) are returned as **string-encoded decimals**.
*   **Implication:** This is done to maintain full precision, especially important for fractional shares or cryptocurrency holdings. Always parse these values as decimals or high-precision numbers in your application rather than floating-point numbers directly to avoid potential precision errors.

## Effect Fields
*   **Detail:** Many balance fields (e.g., `pending-cash-effect`, `realized-day-gain-effect`, `cost-effect`) have a corresponding `*-effect` field.
*   **Values:** These fields typically have values of `Debit`, `Credit`, or `None`.
*   **Interpretation:**
    *   `Debit`: Indicates that the associated value reduces the account balance or has a negative impact.
    *   `Credit`: Indicates that the associated value increases the account balance or has a positive impact.
    *   `None`: Indicates no specific directional effect or that the value is neutral.

## Mark vs. Mark Price
*   **Detail:** The [[../entities/current-position.md|CurrentPosition]] object includes both `mark` and `mark-price` fields.
*   **`mark-price`:** Represents the current mark price *per unit* of the instrument.
*   **`mark`:** Represents the *total* mark value of the entire position.
*   **Relationship:** `mark` is calculated as `mark-price × quantity × multiplier`. Always use `mark-price` for per-unit calculations and `mark` for the total position value.

## Options Multiplier
*   **Detail:** The `multiplier` field in the [[../entities/current-position.md|CurrentPosition]] object indicates the contract multiplier.
*   **Standard Equity Options:** For standard equity options, the `multiplier` is typically `100`.
*   **Futures/Other Instruments:** The multiplier can vary significantly for futures and other derivative instruments.
*   **Best Practice:** Always use the `multiplier` value returned by the API rather than assuming a fixed value, as it can impact the total value and P&L calculations.

## OCC Symbol Format for Options
*   **Detail:** Equity option symbols (e.g., in the `symbol` field of [[../entities/current-position.md|CurrentPosition]]) follow the Option Clearing Corporation (OCC) format.
*   **Format:** `SYMBOL  YYMMDDCSSSSSSSS`
    *   `SYMBOL`: The underlying ticker symbol, left-padded with spaces to 6 characters.
    *   `YY`: Two-digit year of expiration.
    *   `MM`: Two-digit month of expiration.
    *   `DD`: Two-digit day of expiration.
    *   `C`/`P`: Call or Put indicator.
    *   `SSSSSSSS`: The strike price as an 8-digit integer (strike price × 1000).
*   **Example:** `AAL   270115C00017000` represents an American Airlines (AAL) Call option expiring January 15, 2027, with a strike price of $17.00.
*   **Implication:** When parsing or generating option symbols, adhere strictly to this format.

---
## Related Concepts
*   [[../entities/tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]]
*   [[tastyworks-api-use-cases.md|Tastyworks Balances and Positions API Use Cases]]