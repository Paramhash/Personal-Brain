---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-012
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/012-deribit-linear-options-usdc-settlement.md
bot_commit: 93d497d
source_sha256: ef965b5a0201c6893d9dcf02f0b56b59db92e3620168a970c9108742a537ae05
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/012-deribit-linear-options-usdc-settlement.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-012-deribit-linear-options-usdc-settlement|ADR-012]] — Deribit Linear Options Use USDC Settlement Queries

- **Date:** 2026-09-17
- **Status:** accepted
- **Context:** Querying Deribit for `currency: 'SOL'` returns an empty array because Deribit SOL options are linear and settled in USDC. The real `currency: 'USDC', kind: 'option'` payload contains approximately 3,000 records, including 580 SOL options. Far-out-of-the-money instruments also legitimately lack resting bids or asks, so `bid_price` and `ask_price` are absent or null on a substantial portion of valid rows.
- **Decision:** The Deribit ingestion transport must request `currency: 'USDC', kind: 'option'` and filter the response client-side for `base_currency === 'SOL'` before normalization. The wire normalization schema must treat `bid_price` and `ask_price` as fully optional and nullable; their absence or null value is a valid market condition and must not fail validation or increment `droppedInstrumentCount_t`. `deribitRequestTimeoutMs` is increased to `10000` to accommodate the larger payload.
- **Consequences:** The transport separates settlement currency from instrument underlying, and the normalized SOL chain retains valid far-OTM instruments even when no two-sided quote is resting. The larger response requires a longer request ceiling and client-side filtering before the payload crosses the normalization boundary.
- **Alternatives rejected:** Query `currency: 'SOL'` and treat the empty response as a venue outage; discard rows without both bid and ask; or leave the 2-second timeout unchanged for the larger live response.