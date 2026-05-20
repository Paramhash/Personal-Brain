---
tags: ["api", "tastyworks", "data-model", "account-balance", "buying-power", "margin"]
created: 2024-05-15
reviewed: false
source_origin: "balances-and-positions.md"
---
# AccountBalance Data Model (Tastyworks API)

The `AccountBalance` object provides a comprehensive snapshot of an account's current financial state. It includes detailed information across 71 fields covering cash, margin, buying power, and position values for all asset classes.

This data model is returned by the `GET /accounts/{account_number}/balances` and `GET /accounts/{account_number}/balances/{currency}` endpoints of the [[./tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]].

## Fields

### Core Balances

| Field | Type | Description |
|---|---|---|
| `account-number` | string | The tastytrade account number. |
| `currency` | string | The currency of the balance values (typically `USD`). |
| `cash-balance` | number (double) | The total cash balance in the account. |
| `net-liquidating-value` | number (double) | The total account value: cash + long positions − short positions. This is the primary measure of account value. |
| `cash-available-to-withdraw` | number (double) | The amount of cash that can be withdrawn without liquidating positions. |
| `pending-cash` | number (double) | Cash that is pending (e.g., from unsettled trades or pending transfers). |
| `pending-cash-effect` | string | `Debit` or `Credit` — direction of the pending cash. |
| `updated-at` | datetime | Timestamp of the last balance update. |

### Buying Power

| Field | Type | Description |
|---|---|---|
| `available-trading-funds` | number (double) | Total funds available for placing new trades. |
| `equity-buying-power` | number (double) | Buying power available for equity (stock) purchases. |
| `derivative-buying-power` | number (double) | Buying power available for options trades. |
| `day-trading-buying-power` | number (double) | Intraday buying power for day trades (typically 4× margin equity for PDT accounts). |
| `used-derivative-buying-power` | number (double) | The amount of derivative buying power currently in use. |
| `effective-cryptocurrency-buying-power` | number (double) | Buying power available specifically for cryptocurrency trades. |
| `sma-equity-option-buying-power` | number (double) | Special Memorandum Account (SMA) based buying power for equity options. |
| `buying-power-adjustment` | number (double) | Any adjustment applied to buying power. |
| `buying-power-adjustment-effect` | string | `Debit` or `Credit` — direction of the buying power adjustment. |

### Settlement Balances

| Field | Type | Description |
|---|---|---|
| `cash-settle-balance` | number (double) | The settled cash balance. |
| `margin-settle-balance` | number (double) | The settled margin balance. |
| `total-settle-balance` | number (double) | The total settled balance across all settlement types. |
| `closed-loop-available-balance` | number (double) | Balance available under closed-loop withdrawal rules. |

### Margin Requirements

| Field | Type | Description |
|---|---|---|
| `maintenance-requirement` | number (double) | The total maintenance margin requirement for all positions. |
| `maintenance-excess` | number (double) | Excess margin above the maintenance requirement (positive = cushion, negative = margin call). |
| `reg-t-margin-requirement` | number (double) | The Regulation T initial margin requirement. |
| `futures-margin-requirement` | number (double) | Margin requirement for futures positions. |
| `futures-overnight-margin-requirement` | number (double) | Overnight margin requirement for futures positions (typically higher than intraday). |
| `futures-intraday-margin-requirement` | number (double) | Intraday margin requirement for futures positions (typically lower than overnight). |
| `bond-margin-requirement` | number (double) | Margin requirement for bond/fixed-income positions. |
| `cryptocurrency-margin-requirement` | number (double) | Margin requirement for cryptocurrency positions. |
| `equity-offering-margin-requirement` | number (double) | Margin requirement for equity offering positions. |
| `fixed-income-security-margin-requirement` | number (double) | Margin requirement for fixed-income security positions. |

### Margin Calls & Day Trading

| Field | Type | Description |
|---|---|---|
| `margin-equity` | number (double) | The account's margin equity (net liquidating value minus non-margineable assets). |
| `maintenance-call-value` | number (double) | The outstanding maintenance call amount (0 if no call). |
| `reg-t-call-value` | number (double) | The outstanding Reg-T margin call amount. |
| `day-equity-call-value` | number (double) | The outstanding day trade equity call amount. |
| `day-trading-call-value` | number (double) | The outstanding day trading call value. |
| `day-trade-excess` | number (double) | Excess equity above the day trade minimum requirement. |
| `special-memorandum-account-value` | number (double) | The SMA (Special Memorandum Account) value. |
| `special-memorandum-account-apex-adjustment` | number (double) | Apex clearing adjustment to the SMA value. |
| `apex-starting-day-margin-equity` | number (double) | The margin equity value at the start of the trading day as reported by Apex. |
| `pending-margin-interest` | number (double) | Pending margin interest charges. |

### Long Position Values

| Field | Type | Description |
|---|---|---|
| `long-equity-value` | number (double) | Total market value of long equity (stock) positions. |
| `long-derivative-value` | number (double) | Total market value of long options positions. |
| `long-futures-value` | number (double) | Total market value of long futures positions. |
| `long-futures-derivative-value` | number (double) | Total market value of long futures options positions. |
| `long-cryptocurrency-value` | number (double) | Total market value of long cryptocurrency positions. |
| `long-bond-value` | number (double) | Total market value of long bond positions. |
| `long-fixed-income-security-value` | number (double) | Total market value of long fixed-income security positions. |
| `long-margineable-value` | number (double) | Total value of long positions that are margineable. |
| `long-index-derivative-value` | number (double) | Total market value of long index options positions. |

### Short Position Values

| Field | Type | Description |
|---|---|---|
| `short-equity-value` | number (double) | Total market value of short equity positions. |
| `short-derivative-value` | number (double) | Total market value of short options positions. |
| `short-futures-value` | number (double) | Total market value of short futures positions. |
| `short-futures-derivative-value` | number (double) | Total market value of short futures options positions. |
| `short-cryptocurrency-value` | number (double) | Total market value of short cryptocurrency positions. |
| `short-margineable-value` | number (double) | Total value of short positions that are margineable. |
| `short-index-derivative-value` | number (double) | Total market value of short index options positions. |

### Intraday Cash Adjustments

| Field | Type | Description |
|---|---|---|
| `intraday-equities-cash-amount` | number (double) | Intraday cash adjustment for equities activity. |
| `intraday-equities-cash-effect` | string | `Debit` or `Credit` — direction of the equities intraday cash adjustment. |
| `intraday-equities-cash-effective-date` | date | Effective date of the equities intraday cash adjustment. |
| `intraday-futures-cash-amount` | number (double) | Intraday cash adjustment for futures activity. |
| `intraday-futures-cash-effect` | string | `Debit` or `Credit` — direction of the futures intraday cash adjustment. |
| `intraday-futures-cash-effective-date` | date | Effective date of the futures intraday cash adjustment. |

### Cryptocurrency Settlement

| Field | Type | Description |
|---|---|---|
| `unsettled-cryptocurrency-fiat-amount` | number (double) | Unsettled fiat amount from cryptocurrency transactions. |
| `unsettled-cryptocurrency-fiat-effect` | string | `Debit` or `Credit` — direction of unsettled crypto fiat. |
| `previous-day-cryptocurrency-fiat-amount` | number (double) | Previous day's cryptocurrency fiat settlement amount. |
| `previous-day-cryptocurrency-fiat-effect` | string | `Debit` or `Credit` — direction of previous day's crypto fiat. |
| `previous-date-cryptocurrency-fiat-effective-date` | date | Effective date of the previous day crypto fiat calculation. |
| `total-pending-liquidity-pool-rebate` | number (double) | Total pending liquidity pool rebate amount. |

---
## See Also
*   [[./account-balance-snapshot.md|AccountBalanceSnapshot]] - A historical version of the `AccountBalance` object.