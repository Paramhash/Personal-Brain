---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-024
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/024-rebalance-bypass-and-telemetry-fixes.md
bot_commit: 93d497d
source_sha256: 17b902832b2191321de0ada38018b49c55783b4322ac7376b82aad2e1a7e9d80
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/024-rebalance-bypass-and-telemetry-fixes.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]] — Zero-Amount Rebalance Bypass and Telemetry Field Separation

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** During the Devnet Step 6 soak, the macro FSM reached `REDEPLOYMENT` and the EV gate passed, but the required Jupiter re-ratio was blocked because Jupiter's mainnet routing API returned `TOKEN_NOT_TRADABLE` for the Devnet quote mint. The wallet was already balanced, so the required swap amount was effectively zero and no Jupiter route was needed. The run also exposed two observability defects: the `ev` payload was missing from `TickResult`, and action-specific `dryRun` fields were emitted under the same `dry_run` key as the process-level execution posture.
- **Decision 1 (Rebalance Bypass):** When the requested re-ratio amount is zero or below a documented minimum tradable epsilon, `executeInventoryReRatio` returns an idempotent `SUCCESS` immediately without calling Jupiter `/quote` or `/swap`, building a transaction, simulating, submitting, or reconciling a swap. The result must clearly represent a no-op success with no signature and must allow the operational FSM to advance to `DEPLOYING`. The epsilon must be deterministic, unit-aware, and small enough that treating the amount as no-op cannot conceal a meaningful inventory imbalance.
- **Decision 2 (Telemetry):** Add the computed `EvDecisionPayload | null` to `TickResult` so structured tick telemetry can expose `gate_pass` and the EV terms directly. Rename action-specific swap/deploy dry-run fields emitted by `structuredLog.ts` from `dry_run` to `action_dry_run`; reserve `dry_run` for the process-level execution posture.
- **Consequences:** A balanced Devnet wallet no longer depends on a Jupiter route for a no-op re-ratio, so the deployment arm can be exercised while preserving the live routing constraint for non-zero swaps. Telemetry consumers can distinguish process posture from action outcome and inspect the EV decision without inferring it from FSM transitions. Tests must prove zero-amount requests make no transport calls and that both telemetry fields remain distinct.
- **Alternatives rejected:** Treat every Jupiter `TOKEN_NOT_TRADABLE` response as a successful no-op — would hide real failures for non-zero rebalances; bypass the adapter in the orchestrator — duplicates execution policy outside the swap boundary; emit `ev` only in a separate log event — leaves `TickResult` incomplete for callers and structured tick projection; keep one overloaded `dry_run` key — makes a failed pre-simulation action look like a live process.
