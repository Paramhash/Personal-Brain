---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/hedge_engine.md
bot_commit: 93d497d
source_sha256: 2d3805c64a6b34d7e68e6cb7ad0f83f06d6a3c62b7624863934aac823477475c
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/hedge_engine.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Hedge Engine

**Domain owner:** Hedge target calculation, Binance hedge feasibility, and hedge reconciliation inputs
**Status:** authored and binding
This file fixes how the system derives SOL-perpetual hedge targets, measures hedge error, evaluates collateral feasibility, and interacts with unwind reconciliation.

---

## 1. Scope

This blueprint governs:

- target hedge base calculation
- hedge error calculation and resize quantity derivation
- target notional, required collateral, and collateral-gap calculation
- Binance hedge-state inputs required for feasibility and reconciliation
- the relationship between `UNWINDING` and subsequent hedge recalculation

It does not own macro regime transitions, durable persistence, market-data transport, or Binance order construction. The engine computes feasibility facts; the execution adapter submits orders only after those facts pass guardrails.

---

## 2. Neutrality target

The target short must exactly mirror the remaining pool SOL inventory:

$$
q^*_t = -x_t
$$

where $x_t$ is the reconciled pool SOL inventory and $q^*_t$ is the target Binance SOL-perpetual position in base units. A positive pool inventory requires a negative short target.

Target hedge calculation is always in base units first. Quote notional and collateral are derived from the base target rather than replacing it.

---

## 3. Hedge error and resize rule

Hedge error must be calculated exactly as:

$$
e_t = q^*_t - q_t
$$

where $q_t$ is the reconciled executed Binance position in SOL base units.

The required hedge resize quantity is $e_t$. The engine must not calculate error from stale intelligence prices, intended orders, or a cached pre-reconciliation hedge position.

Strict delta neutrality is measured by:

$$
\lvert x_t + q_t \rvert = \lvert e_t \rvert
$$

The applicable tolerance is a risk configuration concern. This engine supplies the exact base error that risk and the operational FSM consume.

---

## 4. Notional and collateral feasibility

Using the live Binance mark price $P_t$ and configured leverage $L_t$:

$$
\text{targetShortNotional}_t = \lvert q^*_t \rvert \times P_t
$$

$$
\text{requiredCollateral}_t = \frac{\text{targetShortNotional}_t}{L_t} + \text{safetyBuffer}_t
$$

$$
\text{collateralGap}_t = \text{requiredCollateral}_t - \text{availableCollateral}_t
$$

`mark_price_t` is the live execution price for hedge sizing, collateral, and LP valuation. It is distinct from Q003 `spotOffchain_t`, which is the off-chain intelligence input.

---

## 5. Collateral guard

If `collateral_gap_t > 0`, the hedge resize is blocked. The result must route to the guardrail path and must not be sent to the Binance executor as a permissible resize.

This is the hard pre-trade block defined by `risk_guardrails.md` §2. A warning, telemetry event, or partial acknowledgement is not a substitute for blocking the order.

---

## 6. UNWINDING interaction

During `UNWINDING`, the hedge target must be recalculated continuously from the remaining reconciled Solana inventory after every partial withdrawal step:

$$
q^*_{t,\mathrm{unwind}} = -x^{\mathrm{rem}}_t
$$

$$
e_{t,\mathrm{unwind}} = q^*_{t,\mathrm{unwind}} - q_t
$$

The target must never be derived from pre-withdrawal inventory once a withdrawal has started. `PARTIAL` remains a looping state: reconcile remaining Solana inventory, recalculate the target, check collateral, resize only if permitted, reconcile Binance, and then determine whether another withdrawal step remains.

---

## 7. Boundary outputs

The hedge engine emits deterministic feasibility facts for the shared `HedgeFeasibilityPayload` boundary, including:

- `mark_price_t`
- `pool_sol_inventory_t`
- `pool_quote_inventory_t`
- `target_short_base_t`
- `target_short_notional_t`
- `required_collateral_t`
- `collateral_gap_t`

The Binance execution adapter consumes an approved hedge decision and returns the standard execution status payload. Neither output proves a hedge action completed; Binance reconciliation is still required before the operational FSM progresses.

---

## 8. Data-flow and prohibitions

The Hedge Engine computes. It does not submit orders itself:

```text
marketdata -> state -> decision/risk -> execution
```

- Do not compute a hedge target from intended rather than reconciled pool inventory.
- Do not submit or authorize a resize while `collateral_gap_t > 0`.
- Do not treat an order acknowledgement as hedge confirmation.
- Do not calculate unwind hedges from pre-withdrawal inventory.
- Do not let the hedge engine own Binance WebSocket transport or order construction.

These prohibitions are binding.
