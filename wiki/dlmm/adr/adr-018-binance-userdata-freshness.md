---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-018
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/018-binance-userdata-freshness.md
bot_commit: 93d497d
source_sha256: 6c976892c93bea7d551dcfbc2c12113e22f34b4b3523e6c0df93d88421567f19
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/018-binance-userdata-freshness.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-018-binance-userdata-freshness|ADR-018]] — Binance User-Data Freshness and Collateral Alignment

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** The Binance `ACCOUNT_UPDATE` stream is event-driven: it pushes on fills, transfers, funding, and related account events, but it is silent during normal idle periods. Applying the clocked `snapshotFreshnessBudgetMs` of 7.5 seconds therefore falsely latches the authenticated feed as stale while the websocket and listen-key session remain healthy, which blocks downstream FSM deployment. The stream and boot REST read also measure different collateral fields: user data carries `cw` while the existing REST path uses `availableBalance`/`ab`, so the two ingress paths cannot be reconciled as the same metric.
- **Decision 1 (Freshness):** Exempt authenticated, event-driven streams from clocked freshness budgets. Implement **Latched-Until-Contradicted** semantics: the Binance user-data stream is considered fresh as long as its websocket is open, its listen key is valid, and the listen-key keepalive loop is succeeding. A valid `ACCOUNT_UPDATE` establishes the source state; normal event silence does not age it out. Socket closure, listen-key expiry or invalidation, keepalive failure, malformed state, or an explicit transport error contradicts freshness and latches the source stale until a new valid authenticated session and event restore it.
- **Decision 2 (Collateral Alignment):** Standardize the collateral metric on `cw` (Cross Wallet Balance) for the user-data payload. Update the REST boot read to fetch the matching cross-wallet balance metric, Binance's `crossWalletBalance` field from the account balance response, so boot and streaming ingress expose identical collateral semantics.
- **Consequences:** Public mark-price data continues to use its clocked freshness budget, while authenticated account data no longer degrades during legitimate idle periods. A composite `BinanceHedgeStateSnapshot` still requires both source states and both source-specific freshness conditions. Boot reconciliation and live user-data updates now compare the same cross-wallet collateral value. The cost is explicit transport health tracking for the listen-key lifecycle and tests for keepalive failure, expiry, and metric alignment.
- **Alternatives rejected:** Keep one 7.5-second clock for both streams — treats event silence as failure and blocks normal operation; refresh account freshness with synthetic or periodic events — invents account facts and hides the actual event-driven contract; continue using `availableBalance` in REST while parsing `cw` in the stream — makes reconciliation compare different quantities; emit the composite as fresh when only the mark-price source is fresh — allows stale account state to reach hedge feasibility.
