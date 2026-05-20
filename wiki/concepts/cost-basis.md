---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# Cost Basis

**Cost basis** is the original value of an asset for tax purposes. It typically includes the purchase price of the asset plus any commissions, fees, or other expenses incurred to acquire it. The cost basis is a critical figure used to calculate capital gains or losses when an asset is sold, as it is subtracted from the sale price to determine the taxable profit or loss.

## Tastyworks Transactions API Context

The [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md) provides information related to [cost basis](../concepts/cost-basis.md) within its [Transaction](../concepts/transaction.md) data model:

*   **`lots` field:** This object provides granular, lot-level details for a transaction. It includes information such as the individual lot execution price, quantity, direction (buy/sell), and transaction date. This detail is essential for calculating cost basis, especially when dealing with multiple purchases of the same security at different prices.
*   **`cost-basis-reconciliation-date`:** This field indicates the date when the cost basis information for the account was last reconciled with the clearing firm.

### Important Note on Reconciliation

It's important to note that [cost basis](../concepts/cost-basis.md) data may lag behind actual trades by approximately one day. This delay is due to the nightly reconciliation process performed with the clearing firm. Users should check the `cost-basis-reconciliation-date` to understand the recency of the available cost basis information.

---
**Source:** [Tastyworks Transactions API Documentation](../sources/tastyworks-transactions-api-docs.md)