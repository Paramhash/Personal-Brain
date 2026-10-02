---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-029
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/029-binance-premium-index-mark-price.md
bot_commit: 93d497d
source_sha256: 484b8277e6eee0514c7d4fc21243fa2f65a713f9204451fed390ca244b7490ca
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/029-binance-premium-index-mark-price.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-029-binance-premium-index-mark-price|ADR-029]] — Binance Flat-Account Mark Price Comes From Premium Index

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** Binance Futures Testnet returns `positionRisk.markPrice = 0.00000000` when the account is flat, even though the market has a valid mark price. The boot `fetchHedgeState` path used that zero field and therefore returned `null` or could feed invalid pricing into EV assembly on the exact cold-start state the bot must support. The same REST call already queried `premiumIndex` for funding data, whose `markPrice` is position-independent and valid for a flat account.
- **Decision:** Assign each Binance REST endpoint the fact it owns: `positionRisk` supplies executed position amount, `balance` supplies cross-wallet collateral, and `premiumIndex` supplies mark price and funding data. Use `premiumIndex.markPrice` for `mark_price_t`, require it to be finite and strictly positive, and fail the snapshot read with `null` if the endpoint is unavailable or invalid. Preserve the WebSocket normalizer's `markPrice > 0` invariant.
- **Consequences:** Flat-account boot reconciliation can produce a usable Binance hedge snapshot with a valid market mark, so pool-native EV gas and funding terms can be evaluated without fabricating an active position. A premium-index failure is no longer fail-soft; boot fails closed rather than publishing a snapshot with an unknown mark. Implemented and verified against Binance Testnet read-only plus `531/531` offline tests; formal architect ratification remains pending.
- **Alternatives rejected:** Continue reading `positionRisk.markPrice` — it is zero on flat accounts; default a missing premium mark to zero — erases EV validity and hides a venue-read failure; use Deribit spot as a fallback — crosses the intelligence/execution boundary; remove the positive-mark guard — permits corrupted EV inputs.
