---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/risk_guardrails.md
bot_commit: 93d497d
source_sha256: e0a3a8e40a7eb5ce0d9f601943c9c8319c67e76e1971817add4fd1c8b72772c1
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/risk_guardrails.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Risk Guardrails

**Domain owner:** Exposure caps, kill switches, and pre-trade checks
**Status:** authored and binding
This blueprint owns the conditions that veto proposed actions before or during execution.

---

## 1. Scope

This blueprint governs:

- collateral sufficiency checks
- fault-path routing when venue actions cannot confirm
- pre-trade vetoes that stop execution before additional risk is taken
- the mandatory fallback behavior of the operational FSM

It does not size the hedge, classify macro regimes, or build transactions.

---

## 2. Collateral block rule

The F-002 collateral guard is binding:

```text
no hedge resize may be submitted if collateral_gap_t > 0
```

This is a hard pre-trade block, not a soft warning. If collateral is insufficient, the
system may surface a guardrail failure, but it may not submit the resize unless a later
design explicitly introduces a recapitalization path.

---

## 3. DEFENSIVE_HOLD fault-bus rule

`DEFENSIVE_HOLD` is the mandatory fault bus for any operational state that cannot confirm
venue execution.

If an operational state cannot confirm its terminal condition, it does not move sideways
into another job. It routes to `DEFENSIVE_HOLD`.

This applies to:

- `INITIALIZING` when reconciliation cannot complete
- `EVALUATING` when safe execution cannot be confirmed
- `UNWINDING` when withdrawal cannot confirm
- `REBALANCING` when swap or venue execution fails
- `DEPLOYING` when deployment cannot confirm
- `HEDGING` when margin is blocked or venue execution degrades

---

## 4. Confirmation before progression

No action that increases or changes exposure may proceed unless the prior state has been
reconciled against authoritative venue state.

In particular:

- a partial Solana unwind is not permission to continue as if the position were flat
- a hedge resize is blocked when collateral sufficiency fails
- a later operational step may not start while a prior venue step remains unconfirmed

---

## 5. Prohibitions

- Do not submit hedge resizes when `collateral_gap_t > 0`.
- Do not bypass `DEFENSIVE_HOLD` when an operational state cannot confirm execution.
- Do not treat acknowledgement as confirmation.
- Do not let a guardrail breach be downgraded to telemetry-only while execution continues.
