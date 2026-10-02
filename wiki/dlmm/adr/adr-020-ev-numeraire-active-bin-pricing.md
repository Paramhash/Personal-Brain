---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-020
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/020-ev-numeraire-active-bin-pricing.md
bot_commit: 93d497d
source_sha256: e2f43d8ce54ac8689ece7b773a2938fe71c55eb447b9cfafccbb22044f57d3d9
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/020-ev-numeraire-active-bin-pricing.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]] — EV Numeraire Uses Active-Bin Pool Pricing

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** `src/decision/ev/evCalculator.ts` currently calculates `swap_slippage` and `deployableNotionalQuote` by valuing the base token (SOL) with Binance `mark_price_t` in USDT. On Devnet, the Meteora pool's quote token is heavily decoupled from USD — approximately 1 SOL = 6.9M quote units. Mixing these numeraires violates `ev_policy.md` §5 and mathematically distorts slippage penalties because the AMM swaps at its own internal price, not the Binance mark.
- **Decision:** For AMM-facing EV math, value the base side (SOL) in the pool's native quote units using the on-chain pool's active-bin price. Derive that price from the Solana snapshot's `activeBinId` and `binStep`, or consume an explicitly tracked pool price when the snapshot contract provides one. Use this pool-native price for `deployableNotionalQuote` and `swap_slippage`; do not substitute the off-chain Binance mark for those AMM quantities.
- **Consequences:** Re-ratio slippage and deployed notional are calculated in the pool's native quote token, so EV execution math is decoupled from arbitrary Devnet exchange rates and remains coherent with the AMM venue. Tests must pin the active-bin price conversion and prove that a large divergence between pool price and Binance mark does not change these AMM terms. Other EV terms remain unchanged unless a separate decision assigns them a different price source.
- **Alternatives rejected:** Continue using Binance `mark_price_t` for all quote conversion — violates the single-numeraire rule when the pool quote is not USD-pegged; use the Binance mark as a fallback for AMM math — silently reintroduces the mismatch during missing or malformed pool data; infer a pool price from wallet balances — balances are inventory facts, not an authoritative execution price; change the shared snapshot contract without first establishing whether `activeBinId` and `binStep` already provide the required deterministic conversion.
