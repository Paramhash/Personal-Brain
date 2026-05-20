---
tags: ["api-schema", "data-structure", "trading", "account-status", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "account-status.md"
---
# TradingStatus Object (Tastytrade API)

The `TradingStatus` object is a core data structure returned by the [[../entities/tastytrade-api-account-status.md|Tastytrade Account Status API]]. It encapsulates all relevant fields describing an account's trading permissions, current state, and various configuration parameters across different asset classes.

## Account Identification

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Internal identifier for the trading status record |
| `account-number` | string | The tastytrade account number |
| `clearing-account-number` | string | The account number at the clearing firm |
| `clearing-aggregation-identifier` | string | Identifier used for aggregating accounts at the clearing level |
| `is-aggregated-at-clearing` | boolean | Whether this account is part of an aggregated clearing group |
| `ext-crm-id` | string | External CRM identifier for the account |
| `autotrade-account-type` | string | The autotrade account type designation, if applicable |

## Account State

| Field | Type | Description |
|-------|------|-------------|
| `is-closed` | boolean | Whether the account has been permanently closed |
| `is-frozen` | boolean | Whether the account is frozen (no trading activity permitted) |
| `is-closing-only` | boolean | Whether the account is restricted to closing transactions only (no new positions) |
| `is-risk-reducing-only` | boolean | Whether the account is restricted to risk-reducing trades only |
| `updated-at` | datetime | Timestamp of the last update to the trading status record |

## Options Permissions

| Field | Type | Description |
|-------|------|-------------|
| `options-level` | string | The approved options trading level for the account (determines which strategies are permitted) |
| `short-calls-enabled` | boolean | Whether the account is approved to sell naked (short) calls |
| `are-deep-itm-carry-options-enabled` | boolean | Whether deep in-the-money carry option positions are enabled |
| `are-far-otm-net-options-restricted` | boolean | Whether far out-of-the-money net option positions are restricted |
| `are-options-values-restricted-to-nlv` | boolean | Whether option position values are restricted relative to the account's net liquidating value |
| `are-single-tick-expiring-hedges-ignored` | boolean | Whether single-tick expiring hedges are ignored in margin calculations |

## Equities & Margin

| Field | Type | Description |
|-------|------|-------------|
| `equities-margin-calculation-type` | string | The margin calculation methodology used for equities (e.g., [[../concepts/reg-t-margin.md|Reg-T]], [[../concepts/portfolio-margin.md|portfolio margin]]) |
| `has-intraday-equities-margin` | boolean | Whether the account has access to intraday (reduced) equities margin rates |
| `is-full-equity-margin-required` | boolean | Whether full equity margin is required (no reduced intraday margin) |
| `is-portfolio-margin-enabled` | boolean | Whether [[../concepts/portfolio-margin.md|portfolio margin]] (risk-based) is enabled for the account |
| `is-in-margin-call` | boolean | Whether the account is currently in a margin call |
| `cmta-override` | integer | CMTA (Clearing Member Trade Assignment) override value |

## Day Trading

| Field | Type | Description |
|-------|------|-------------|
| `is-pattern-day-trader` | boolean | Whether the account is flagged as a [[../concepts/pattern-day-trader.md|Pattern Day Trader (PDT)]] under [[../entities/finra.md|FINRA]] rules |
| `day-trade-count` | integer | The current count of day trades within the rolling 5-business-day window |
| `is-in-day-trade-equity-maintenance-call` | boolean | Whether the account is in a day trade equity maintenance call (PDT minimum equity violation) |
| `pdt-reset-on` | date | The date when the PDT flag was last reset, if applicable |
| `is-roll-the-day-forward-enabled` | boolean | Whether the roll-the-day-forward feature is enabled for day trade counting |

## Futures

| Field | Type | Description |
|-------|------|-------------|
| `is-futures-enabled` | boolean | Whether the account is approved for futures trading |
| `is-futures-closing-only` | boolean | Whether futures trading is restricted to closing transactions only |
| `is-futures-intra-day-enabled` | boolean | Whether intraday futures trading (with reduced margin) is enabled |
| `futures-margin-rate-multiplier` | number (double) | Multiplier applied to the base futures margin requirement for this account |
| `is-small-notional-futures-intra-day-enabled` | boolean | Whether intraday trading of small-notional futures products (e.g., /MES, /MNQ) is enabled |
| `small-notional-futures-margin-rate-multiplier` | number (double) | Multiplier applied to the base margin requirement for small-notional futures |

## Cryptocurrency

| Field | Type | Description |
|-------|------|-------------|
| `is-cryptocurrency-enabled` | boolean | Whether cryptocurrency trading is enabled for the account |
| `is-cryptocurrency-closing-only` | boolean | Whether crypto trading is restricted to closing transactions only |

## Equity Offerings

| Field | Type | Description |
|-------|------|-------------|
| `is-equity-offering-enabled` | boolean | Whether the account can participate in equity offerings (e.g., IPOs) |
| `is-equity-offering-closing-only` | boolean | Whether equity offering activity is restricted to closing only |

## Fees & Risk

| Field | Type | Description |
|-------|------|-------------|
| `fee-schedule-name` | string | The name of the fee schedule applied to this account |
| `enhanced-fraud-safeguards-enabled-at` | datetime | Timestamp when enhanced fraud safeguards were enabled for this account |