---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/observability_contract.md
bot_commit: 93d497d
source_sha256: b56bce5385967629ed31d167f358b2bc507354417b53cc2761471412d434a1a0
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/observability_contract.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Observability Contract

**Domain owner:** Logging, metrics emission, replay timing, and production telemetry
**Status:** authored and binding
This file fixes the telemetry boundary for the orchestration root and venue adapters.

---

## 1. Scope

This blueprint governs:

- structured application logging
- execution and reconciliation metrics
- withdrawal-loop latency measurements
- replay timing and production telemetry emission

It does not make trading decisions, submit venue actions, or own durable state.

---

## 2. Structured logging

The orchestration `log` port must emit structured JSON records. Every record must be a single
valid JSON object with a stable event name, timestamp, and event-specific fields.

At minimum, records must preserve the root event categories already declared by
`OrchestratorEvent`: boot, tick, skipped tick, withdrawal, hedge, swap, deploy, and error.

Logging must retain machine-readable execution status and reconciliation facts. Human-formatted
strings may be supplemental fields, but they must not replace the structured event object.

Secrets must never be logged. This includes Binance API keys and signatures, signer material,
authorization headers, full REST credentials, and raw private RPC URLs containing credentials.

---

## 3. Withdrawal timing metrics

During the defensive withdrawal loop, telemetry must surface both:

```text
t_liquidity_removed_ms
t_total_exit_ms
```

`t_liquidity_removed_ms` measures elapsed time from the withdrawal decision or dispatch start
to confirmed removal of liquidity. `t_total_exit_ms` measures elapsed time from that same start
to the confirmed terminal exit condition, including required reconciliation and follow-on hedge
convergence where applicable.

Both metrics must be emitted as numeric millisecond fields on structured withdrawal telemetry.
They must be `null` or omitted while their terminal condition is not yet confirmed; an
acknowledgement or `PARTIAL` result must not be represented as a completed latency metric.

---

## 4. Replay and production telemetry

The same event schema must be usable for offline replay and production operation. A replay may
replace live sinks, but it must not change metric names, timing units, or status semantics.

Telemetry is downstream-only:

```text
marketdata -> state -> intelligence -> decision -> risk -> execution -> observability
```

Observability consumers may observe events and metrics, but they may not write back into the
decision, risk, execution, or state domains.

---

## 5. Prohibitions

- Do not emit unstructured-only logs from the orchestration root or venue adapters.
- Do not report an acknowledgement as completed withdrawal latency.
- Do not emit credentials, private keys, tokens, signatures, or sensitive endpoint material.
- Do not let logging or metric delivery block, reorder, or alter the execution pipeline.
- Do not allow observability code to mutate strategy state or invoke venue actions.

These prohibitions are binding.
