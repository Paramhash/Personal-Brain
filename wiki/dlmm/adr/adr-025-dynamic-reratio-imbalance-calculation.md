---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-025
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/025-dynamic-reratio-imbalance-calculation.md
bot_commit: 93d497d
source_sha256: 19a472c62f667319d238571be3f9c1b2f7014f61a9cf2de4106614959d032fd3
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/025-dynamic-reratio-imbalance-calculation.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]] — Dynamic 50/50 Re-Ratio Imbalance Calculation

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]] added a zero-amount Jupiter bypass, but the bypass is currently unreachable in the live adapter because `swapPolicy` in `liveAdapters.ts` hardcodes the swap amount from the `.env` variable `SWAP_AMOUNT_BASE_UNITS`. To skip Jupiter on Devnet when the wallet is already balanced, the system must calculate the required re-ratio from reconciled inventory rather than a static amount. The current policy also needs to express trade direction, because a 50/50 correction may sell base for quote or buy base with quote.
- **Decision:** Amend `liquidity_position_manager.md` §2 to define a dynamic 50/50 re-ratio. `swapPolicy` must consume the reconciled `SolanaPoolStateSnapshot` and the pool-native `activeBinPriceQuotePerBase` from [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]]. It calculates total wallet value in pool quote units, determines the signed base-token delta required for each wallet side to represent 50% of that value, converts the trade magnitude to base units using `baseDecimals`, and selects the appropriate input/output mint for the direction. If the required correction is within the configured reserve tolerance, such as less than `0.05 SOL` equivalent, it returns an exact amount of `0` so [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]'s no-op bypass triggers. The calculation is pure and must fail closed when balances, decimals, or active-bin price are unusable.
- **Consequences:** A balanced wallet no longer depends on Jupiter routing and can advance directly to deployment. A skewed wallet receives a deterministic corrective trade amount and direction based on the same pool price used by EV calculations. `SWAP_AMOUNT_BASE_UNITS` is no longer the source of truth for re-ratio sizing and should be removed from the dynamic policy path, though any environment compatibility decision must be explicit. The reserve tolerance becomes a ratified execution policy and must be tested at its boundary.
- **Alternatives rejected:** Keep the static `.env` amount — cannot detect a balanced wallet and can trade the wrong amount; infer imbalance from the Binance mark — violates [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]]'s pool-native AMM numeraire; bypass Jupiter for every Devnet swap — hides meaningful imbalance and is not portable; silently clamp a negative or unpriceable calculation to zero — could deploy an unbalanced wallet and conceal missing facts.
