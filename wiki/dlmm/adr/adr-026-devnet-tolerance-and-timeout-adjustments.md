---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-026
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/026-devnet-tolerance-and-timeout-adjustments.md
bot_commit: 93d497d
source_sha256: 45d076d11d0454223ee90857ba8af5efab4041720556039d37aed11e47731322
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/026-devnet-tolerance-and-timeout-adjustments.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-026-devnet-tolerance-and-timeout-adjustments|ADR-026]] — Devnet Tolerance and Deribit Timeout Adjustments

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** Devnet pool-price drift can move the wallet just beyond the hardcoded `0.05 SOL` `reRatioReserveToleranceBase`, causing the dynamic policy from [[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]] to request a Jupiter route. Jupiter's mainnet routing API cannot trade the configured Devnet quote token, so a small harmless drift becomes a `TOKEN_NOT_TRADABLE` blocker instead of activating [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]'s zero-amount bypass. Separately, `deribitRequestTimeoutMs = 10000` is too tight for the full USDC option-chain payload of roughly 3,000 rows, producing polling timeouts even though the push stream can maintain tick-to-tick freshness.
- **Decision 1 (Tolerance):** `reRatioReserveToleranceBase` in `strategy.config.ts` must read from the environment variable `REBALANCE_TOLERANCE_BASE`, defaulting to `0.05` for production safety. Devnet operators may override it in `.env` to a larger, explicitly chosen value so small pool-drift corrections return zero and activate [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]. Parsing must validate the value and fail closed on malformed or non-positive configuration rather than silently accepting arbitrary text.
- **Decision 2 (Timeouts):** Increase `deribitRequestTimeoutMs` to `20000` milliseconds to accommodate the heavy USDC option-chain response. The request/response source remains bounded by this timeout, while the Deribit push stream supplies tick-to-tick native-greek freshness; increasing the request ceiling must not weaken stale-latch or overlap protections.
- **Consequences:** Devnet tolerance becomes an explicit operator input instead of a source edit, while the safe default remains unchanged for production. A larger override can intentionally suppress small Devnet re-ratio requests, but it must not be treated as an economic policy for production. The longer Deribit timeout reduces false request failures at the cost of potentially longer in-flight work; the existing sequential loop, skip guard, and freshness semantics remain the protection against overlapping or stale snapshots.
- **Alternatives rejected:** Remove the tolerance and always call Jupiter — fails on every non-tradable Devnet quote; hardcode a large tolerance — unsafe outside Devnet and invisible to operators; restore the old timeout — repeats the measured payload failure; disable timeout or let requests overlap — can accumulate stale responses and violate the ordered snapshot clock.
