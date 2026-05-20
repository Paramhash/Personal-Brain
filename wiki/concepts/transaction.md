---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# Transaction (Financial)

A **transaction** in a financial context refers to any event or activity that affects the balance or holdings within a financial account. This can include a wide range of activities such as buying or selling securities (trades), receiving dividends, incurring [financial fees](../concepts/financial-fees.md), or transferring funds. Transactions form the fundamental record of an account's history.

## Tastyworks Transactions API Data Model

Within the [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md), a `Transaction` object represents a single record of account activity. It provides comprehensive details about the event, including execution specifics, associated costs, and identifiers.

### Core Fields

*   `id`: Unique transaction identifier.
*   `account-number`: The associated tastytrade account number.
*   `transaction-type`: Broad category (e.g., `Trade`, `Receive Deliver`, `Dividend`, `Money Movement`, `Transfer`).
*   `transaction-sub-type`: Specific action within the type (e.g., `Sell to Open`, `Buy to Close`, `Assignment`, `Expiration`, `Dividend`).
*   `transaction-date`: Date the transaction occurred.
*   `executed-at`: Exact execution timestamp.
*   `created-at`: When the transaction record was created.
*   `description`: Human-readable description.

### Instrument

*   `symbol`: The instrument's ticker symbol.
*   `underlying-symbol`: The symbol of the underlying asset.
*   `instrument-type`: Type of instrument (e.g., `Equity`, `Equity Option`, `Future`).

### Execution Details

*   `action`: The trade action (e.g., `Buy to Open`, `Sell to Close`).
*   `quantity`: The quantity traded.
*   `price`: Execution price per unit.
*   `value`: Total value of the transaction.
*   `value-effect`: Indicates if `value` is a [Debit or Credit](../concepts/debit-credit-effect.md).
*   `net-value`: Total value after all [financial fees](../concepts/financial-fees.md).
*   `net-value-effect`: Indicates if `net-value` is a [Debit or Credit](../concepts/debit-credit-effect.md).
*   `order-id`: The ID of the originating order.
*   `leg-count`: Number of legs in the originating order.
*   `destination-venue`: Venue where executed.
*   `exchange`: The exchange.
*   `exchange-affiliation-identifier`: Exchange affiliation ID.

### Fees & Commissions

These fields detail various charges associated with the transaction. Each monetary fee field has a corresponding `*-effect` field (e.g., `commission-effect`) indicating its [Debit or Credit](../concepts/debit-credit-effect.md) impact.

*   `commission`
*   `clearing-fees`
*   `regulatory-fees`
*   `proprietary-index-option-fees`
*   `currency-conversion-fees`
*   `other-charge`
*   `other-charge-description`
*   `is-estimated-fee`: Boolean indicating if fees are estimated.

For more details, see [Financial Fees](../concepts/financial-fees.md).

### Pricing

*   `principal-price`: The principal price.
*   `agency-price`: The agency price (if applicable).
*   `currency`: The currency of transaction values.

### Lot & Cost Basis

*   `lots`: Object containing lot-level details (execution price, quantity, direction, date).
*   `cost-basis-reconciliation-date`: Date when [cost basis](../concepts/cost-basis.md) was reconciled.
*   `reverses-id`: ID of a reversed transaction, if applicable.

For more details, see [Cost Basis](../concepts/cost-basis.md).

### External Identifiers

*   `exec-id`, `ext-exec-id`
*   `ext-exchange-order-number`
*   `ext-global-order-number`
*   `ext-group-fill-id`, `ext-group-id`

---
**Source:** [Tastyworks Transactions API Documentation](../sources/tastyworks-transactions-api-docs.md)