---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/protocol_contract.md
bot_commit: 93d497d
source_sha256: 669a54ddfec796230c7f224fde2ad247db052219b3b9b32ae71026f3c1c818c8
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/protocol_contract.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Protocol Contract

**Domain owner:** Shared protocol schemas and cross-module payload contracts
**Status:** authored and binding
This file defines the ownership, versioning, validation, and placement rules for shared
payload contracts under `/development/src/types/`.

---

## 1. Scope

This blueprint governs:

- the TypeScript interface surface in `src/types/protocol.ts`
- the runtime validation surface in `src/types/validators.ts`
- the placement of FSM state types that cross module boundaries
- backward-compatibility expectations once multiple consumers exist

It does not define execution flow, RPC behavior, or venue sequencing.

---

## 2. Canonical file ownership

| File | Owns |
| --- | --- |
| `src/types/protocol.ts` | shared TypeScript interfaces and event types |
| `src/types/validators.ts` | `zod` schemas that mirror the shared interfaces at runtime boundaries |
| `src/decision/fsm/macroStateMachine.ts` | the Q004 `MacroState` type and macro reducer-local state/context |
| `src/decision/fsm/stateMachine.ts` | the operational `FsmState` type only |

`MacroState` and `FsmState` are intentionally separate ownership surfaces. The macro state
type must never be merged into the operational `FsmState` union.

---

## 3. Validation boundary rule

Every shared payload that can cross a module boundary at runtime must have:

1. a TypeScript interface in `src/types/protocol.ts`
2. a mirrored `zod` schema in `src/types/validators.ts`

The schema must mirror the interface field-for-field and discriminate unions explicitly.
The schema file is the runtime boundary; the interface file is the compile-time boundary.

Required initial validators:

- `SolGexSignalPayload`
- `EvDecisionPayload`
- `HedgeFeasibilityPayload`
- `WithdrawalExecutionStatusEvent`
- `ExecutionIntentEvent`
- `SolOptionChainSnapshot`

No other module owns ad hoc copies of these validators.

`SolOptionChainSnapshot` is a shared runtime boundary. It must live in
`src/types/protocol.ts`, and its mirrored strict `zod` validator must live in
`src/types/validators.ts`. Feature modules may still own venue-wire schemas and purely local
helper types, but they may not own the repository's normalized snapshot contract once that
snapshot crosses the Market Data → Intelligence boundary.

---

## 4. Shared event boundary

`ExecutionIntentEvent` is the sole forward payload that crosses from macro strategy into
operational execution.

```ts
export interface ExecutionIntentEvent {
  readonly eventType: 'EXECUTION_INTENT';
  readonly action: 'WITHDRAW' | 'REDEPLOY';
  readonly priorityFeeMode: 'NORMAL' | 'AGGRESSIVE';
}
```

Any future field added to this event must be added in both `protocol.ts` and
`validators.ts` in the same change.

---

## 5. FSM type placement rule

The Q004 macro state type belongs in `src/decision/fsm/macroStateMachine.ts`.

It must:

- be declared locally to the macro strategy layer
- remain separate from the operational `FsmState`
- never widen the operational union defined for the actuator FSM
- cross the macro/operational boundary only through `ExecutionIntentEvent`

The operational FSM may consume facts emitted by the macro layer, but it may not read the
macro reducer's private state directly.

The corresponding runtime boundary objects used by that macro layer still belong under
the shared protocol domain:

- shared input payloads remain in `src/types/protocol.ts`
- shared runtime schemas remain in `src/types/validators.ts`
- only the reducer-local `MacroState` and macro context stay in `macroStateMachine.ts`

---

## 6. Compatibility policy

Once more than one runtime consumer exists, changes to shared payload contracts are
versioned by additive discipline:

- additive optional fields are preferred
- renames and removals require an ADR and coordinated consumer migration
- validators must reject structurally invalid payloads rather than coercing them silently

Until a formal transport version field exists, the interface name plus field set is the
compatibility boundary.

---

## 7. Prohibitions

- Do not place runtime validators inside feature modules.
- Do not define a second copy of a shared interface in a downstream module.
- Do not merge `MacroState` into the operational `FsmState`.
- Do not let execution modules infer payload validity without passing through the shared
  validator surface when data crosses a runtime boundary.
