---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-028
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/028-ev-calculator-zero-inventory-support.md
bot_commit: 93d497d
source_sha256: e6b594ac55f86feb0b0ea11a5510bc1cc770e6cfedc47d7b50f8df4301f1b8a9
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/028-ev-calculator-zero-inventory-support.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-028-ev-calculator-zero-inventory-support|ADR-028]] — EV Calculator and FSM Assembler Zero-Inventory Support

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** A flat account can have reconciled Solana wallet capital but no Binance hedge snapshot or active perp position. The prior EV implementation required a Binance snapshot even for pool-native AMM valuation, so `deployableNotionalQuote` and projected LVR collapsed to zero, the EV gate failed, and the FSM could not progress from `MONITORING(IDLE)` toward first deployment. The same composite-health rule treated absent hedge state as an execution-venue failure, parking the bot in `DEFENSIVE_HOLD` even though deployment requires Solana facts and an EV decision but not an existing hedge position.
- **Decision:** In zero-inventory contexts, calculate deployment notional and projected LVR from reconciled wallet/pool capital and the pool-native active-bin price. Keep the EV formula `net_ev = projected_dynamic_fees - projected_lvr_quote - binance_funding_drag` and the canonical `meetsEvHurdle()` comparison unchanged. Funding drag follows the no-position policy and is zero when no hedge snapshot exists; it must not erase the other pool-native terms. Scope composite venue health for deployment to the execution venue: a missing Binance hedge snapshot must not prevent a valid Solana/EV reading or `EVALUATING`, while hedge-dependent actions remain blocked without Binance facts. Never use `spotOffchain_t` as an execution valuation fallback.
- **Consequences:** A flat wallet can compute a meaningful pool-native EV decision and reach the cold-start deployment path without fabricating a Binance mark or hedge snapshot. Hedge sizing and collateral checks remain fail-closed, and the bot cannot enter `HEDGING` without Binance state. The remaining risk is that zero funding drag is an unmeasured cost policy and should be ratified separately if production economics depend on it. Implemented and verified with `529/529` offline tests; formal architect ratification remains pending.
- **Alternatives rejected:** Use Deribit `spotOffchain_t` as an execution price — violates the data-flow boundary and [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]]'s pool numeraire; fabricate a zero Binance snapshot — corrupts hedge facts and collateral semantics; keep venue health dependent on both venues for all states — blocks cold-start deployment unnecessarily; remove hedge collateral guards — authorizes unhedged risk and violates `risk_guardrails.md`.
