---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/execution_router.md
bot_commit: 93d497d
source_sha256: ee330e8c511591e9187c93ab36e6864d8cd747f7cdabcd06fbaca262ebdeb914
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/execution_router.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Execution Router

**Domain owner:** Solana and Binance transaction sequencing and venue reconciliation
**Status:** authored and binding
This blueprint owns cross-venue ordering, transaction sequencing, retry boundaries, and
the reconciliation rules that stop Solana and Binance actions from racing each other.

---

## 1. Scope

This blueprint governs:

- sequencing between Solana liquidity actions and Binance hedge actions
- interpretation of `PARTIAL`, `SUCCESS`, and `FAILED` execution states
- venue reconciliation before any subsequent cross-venue step
- the handoff between `UNWINDING`, hedge recomputation, and later execution jobs

It does not decide macro regime transitions. It consumes boundary intents and reconciled
facts.

---

## 2. Cross-venue sequencing rule

Cross-venue actions are strictly sequential.

The router must not allow Solana withdrawal, Binance hedge resize, swap, and redeploy
steps to run concurrently against drifting assumptions. The next step begins only after
the previous venue step is reconciled against authoritative state.

Canonical ordering during unwind:

1. execute the Solana withdrawal step
2. reconcile the remaining Solana inventory
3. recompute the Binance hedge target from remaining inventory
4. resize or confirm the hedge on Binance
5. reconcile the Binance position
6. decide whether another unwind step remains

---

## 3. Partial withdrawal rule

During `UNWINDING`, Solana `PARTIAL` execution status is a looping condition, not a
terminal success.

`PARTIAL` means:

- some withdrawal work may have landed
- active liquidity still remains
- the operational FSM stays in `UNWINDING`
- the hedge target must be recomputed from the remaining reconciled inventory

No upstream layer may treat `PARTIAL` as permission to leave the unwind path.

---

## 4. Hedge recomputation rule

During unwind, the Binance hedge target is always derived from the remaining reconciled
Solana inventory, never from the pre-withdrawal inventory and never from in-memory intent.

```text
q*_{t, unwind} = -x^{rem}_t
```

where:

- `x^{rem}_t` is the remaining reconciled Solana inventory after the latest withdrawal step
- `q*_{t, unwind}` is the updated hedge target in base units

The router must not permit a Binance hedge resize until `x^{rem}_t` is known from the
chain.

---

## 5. Authoritative-state rule

The chain is authoritative for LP inventory and position-close progress.
Binance is authoritative for the executed hedge.

The router must therefore reconcile:

- Solana state after every withdrawal, swap, or deploy step
- Binance position state after every hedge action

No subsequent venue step is built from stale cached intentions.

---

## 6. Ordered execution boundaries

### Defensive withdrawal path

1. consume `ExecutionIntentEvent { action: 'WITHDRAW' }`
2. enter `UNWINDING`
3. execute Solana withdrawal work
4. if result is `PARTIAL`, remain in `UNWINDING`
5. recompute hedge target from reconciled remaining inventory
6. hedge only the delta required by the updated target
7. finish only when liquidity is removed and the hedge converges inside tolerance

### Redeploy path

1. consume `ExecutionIntentEvent { action: 'REDEPLOY' }`
2. preflight and rebalance on Solana
3. deploy liquidity on Solana
4. reconcile the new LP inventory
5. compute the new hedge target from reconciled inventory
6. resize hedge on Binance

---

## 7. Prohibitions

- Do not run Solana and Binance mutation steps in parallel.
- Do not treat Solana `PARTIAL` as a terminal unwind result.
- Do not compute the unwind hedge target from original inventory after a partial withdrawal.
- Do not let Binance hedge logic proceed from macro state alone; it must consume reconciled
  venue facts.
- Do not advance the operational FSM past a venue step that has not been reconciled.
