---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/state_machine.md
bot_commit: 93d497d
source_sha256: 09b14891fff55883ac884e9ffda6e48de166494faa2de1960dd2bd9c167aab8d
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/state_machine.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Section 4 — Finite State Machine

**Domain owner:** Module 3 · State, EV, and Hedge Orchestration
**Status:** blueprint. No implementation exists yet — `/development/src/` is empty.
This document is the specification the TypeScript implementation must conform to,
not a description of code already written.

---

## 4.0 Hierarchical boundary

This blueprint defines the **operational actuator FSM**, not the macro regime controller.
The architecture has two distinct state machines:

| Layer | Owner | States | Responsibility | May touch a venue? |
| --- | --- | --- | --- | --- |
| Macro Strategy FSM | Q004 | `MONITORING`, `THREAT_EVALUATION`, `DEFENSIVE_WITHDRAWAL`, `REGIME_OBSERVATION`, `REDEPLOYMENT` | consume GEX, EV, hedge feasibility, and execution confirmations; decide regime intent | no |
| Operational Actuator FSM | Module 3 orchestration + execution modules | `INITIALIZING`, `MONITORING`, `EVALUATING`, `UNWINDING`, `REBALANCING`, `DEPLOYING`, `HEDGING`, `DEFENSIVE_HOLD` | reconcile venues and sequence jobs | yes |

These state sets are hierarchical, not additive. **Do not flatten them into a single
13-state loop.** Shared names such as `MONITORING` are valid only because each layer has
its own state type, context, and transition rules.

### Sole boundary payload

`ExecutionIntentEvent` is the only transport payload that crosses from macro policy into
operational execution.

```ts
export interface ExecutionIntentEvent {
  eventType: 'EXECUTION_INTENT';
  action: 'WITHDRAW' | 'REDEPLOY';
  priorityFeeMode: 'NORMAL' | 'AGGRESSIVE';
}
```

The macro layer emits this event and remains pure. The operational layer consumes it and
decides which execution state sequence to run.

### Macro intent -> operational execution map

| Macro state | Boundary output | Operational consequence |
| --- | --- | --- |
| `MONITORING` | no event | operational hub remains read-only and waits |
| `THREAT_EVALUATION` | no event | no venue action; operational layer stays passive |
| `DEFENSIVE_WITHDRAWAL` | `ExecutionIntentEvent { action: 'WITHDRAW' }` | operational FSM enters `UNWINDING` |
| `REGIME_OBSERVATION` | no event | operational layer remains flat after confirmed withdrawal |
| `REDEPLOYMENT` | `ExecutionIntentEvent { action: 'REDEPLOY' }` | operational FSM runs `EVALUATING -> REBALANCING -> DEPLOYING`, then `HEDGING` if needed |

Reverse flow does not carry state assignments back into Q004. The operational layer only
returns reconciled facts such as withdrawal confirmation, redeploy completion, and hedge
status; Q004 consumes those facts on its next pure transition.

---

## 4.1 The operational hub principle

The FSM has exactly one resting state: **`MONITORING`**.

Every other state is a *job*: it is entered with a purpose, it runs to a confirmed
outcome, and it hands control back. Nothing else is allowed to rest. A bot sitting in
`REBALANCING` or `DEPLOYING` is, by definition, mid-flight — if it stops making progress
there, that is a fault, not a state.

`INITIALIZING` is a **boot gateway**, not an anchor. It runs once per process, reconciles
the three sources of truth, decides which mode the hub wakes in, and is never re-entered
without a restart. It holds no policy and makes no trading decision.

The practical consequence: **self-healing is the hub's job, not the gateway's.** Idle
capital found at boot is not a special INITIALIZING branch — it is simply the hub waking
in `IDLE` with a deployment trigger already satisfied. A mismatched short is not a boot
branch either — it is the hub waking in `ACTIVE` with hedge drift already outside band.
This is what collapses the old fan-out from the gateway into a single edge.

---

## 4.2 Asset scope

The wallet holds **exactly two tokens**:

| Role | Token | DLMM side | Notes |
| --- | --- | --- | --- |
| Base | SOL | `tokenX` | the volatile leg; this is what gets hedged |
| Quote | USDC | `tokenY` | the numeraire; all EV and PnL are denominated here |

No third asset enters the wallet. Anything else appearing there is an anomaly for
`INITIALIZING` to report, not something the FSM is designed to manage.

Delta exposure is the Base balance implied by the DLMM position, hedged by a short
`SOLUSDT` USDⓈ-M perpetual. Funding settles every 8 hours and is a term in the EV gate,
not a state.

---

## 4.3 The eight operational states

| State | Kind | Purpose | May touch a venue? |
| --- | --- | --- | --- |
| `INITIALIZING` | gateway | read wallet, DLMM position, perp hedge; reconcile; derive hub mode | reads only |
| `MONITORING` | **hub / resting** | observe venue state, accept macro intents, dispatch local hedge repair | reads only |
| `EVALUATING` | decision | preflight an approved `REDEPLOY` intent against fresh state and EV inputs | reads only |
| `UNWINDING` | job | `removeLiquidity` + claim fees; confirm closed | Solana write |
| `REBALANCING` | job | Jupiter v6 quote → swap to target Base/Quote ratio | Solana write |
| `DEPLOYING` | job | open bins between Put Wall and Call Wall | Solana write |
| `HEDGING` | job | size and send the perp leg; reconcile fills | Binance write |
| `DEFENSIVE_HOLD` | fallback | capital parked, exposure reduced, alert raised | reads only |

`EVALUATING` is an operational preflight state, not the macro regime controller from
Q004. Every state that writes to a venue is a job with a confirmed terminal condition.

---

## 4.4 `MONITORING` — dual-mode observation

The hub has two observation modes. They are **derived from reconciled venue state, never
stored**, so a crash costs nothing: reboot, re-read both venues, resume in whichever mode
the world is actually in.

```ts
export type MonitoringMode = 'IDLE' | 'ACTIVE';

export const deriveMode = (s: VenueSnapshot): MonitoringMode =>
  s.position === null ? 'IDLE' : 'ACTIVE';
```

### `IDLE` — not deployed

Wallet holds Base + Quote; no DLMM position is open.

- waits for a macro `REDEPLOY` intent before spending capital
- watches wallet balances for deposits or manual intervention
- watches local venue health and deployment readiness
- **leaves only** when a macro `REDEPLOY` intent fires → `EVALUATING`

### `ACTIVE` — deployed

DLMM position live across its bin range.

- watches inventory drift: `totalXAmount` / `totalYAmount` as the active bin moves
- watches position ratio against the target range and the wall boundaries
- watches fee accrual (`unclaimedFeeX` / `unclaimedFeeY`)
- watches **hedge drift**: `positionAmt` on the perp against the Base implied by the
  position, `q_t` versus `q*_t`
- **leaves only** when a macro `WITHDRAW` intent fires → `UNWINDING`, or when hedge drift
  exceeds band → `HEDGING`

Hedge maintenance is deliberately a hub dispatch, not a tail of `DEPLOYING`. After
`DEPLOYING` returns, the hub wakes in `ACTIVE`, observes a position with no matching
short, and dispatches `HEDGING` on the next tick. One mechanism covers first hedge,
drift correction, and post-restart repair.

---

## 4.5 Operational transition map

```mermaid
stateDiagram-v2
    direction LR
    [*] --> INITIALIZING

    state "MONITORING — steady-state hub" as MONITORING {
        direction LR
        [*] --> IDLE
        IDLE --> ACTIVE : position opened
        ACTIVE --> IDLE : position closed
    }

    INITIALIZING --> MONITORING : reconciled
    INITIALIZING --> DEFENSIVE_HOLD : venue unreachable

    MONITORING --> EVALUATING : REDEPLOY intent received
    MONITORING --> UNWINDING : WITHDRAW intent received
    MONITORING --> HEDGING : hedge drift outside band
    MONITORING --> DEFENSIVE_HOLD : venue health degraded

    EVALUATING --> MONITORING : preflight failed / intent cleared
    EVALUATING --> UNWINDING : WITHDRAW supersedes redeploy
    EVALUATING --> REBALANCING : REDEPLOY preflight approved
    EVALUATING --> DEFENSIVE_HOLD : preflight cannot confirm safe execution

    UNWINDING --> REBALANCING : liquidity out, fees claimed
    UNWINDING --> DEFENSIVE_HOLD : withdrawal cannot confirm
    REBALANCING --> DEPLOYING : Base/Quote ratio restored
    REBALANCING --> DEFENSIVE_HOLD : swap or venue failure
    DEPLOYING --> MONITORING : position live
    DEPLOYING --> DEFENSIVE_HOLD : deploy cannot confirm

    HEDGING --> MONITORING : delta neutral restored
    HEDGING --> DEFENSIVE_HOLD : margin blocked

    DEFENSIVE_HOLD --> MONITORING : conditions normalise
```

Read it as a wheel: `MONITORING` at the centre, one spoke out, work done, spoke back.

**Capital is deployed on the `IDLE` spoke only after a macro `REDEPLOY` intent.** The
full operational path from a flat wallet holding only Base and Quote is:

```text
MONITORING(IDLE) → EVALUATING → REBALANCING → DEPLOYING → MONITORING(ACTIVE)
```

`INITIALIZING` is not on that path and must never be re-entered to deploy — it is a
process-lifetime gateway, and returning to it would mean a restart, discarding the live
position and hedge it had just reconciled. Nothing transitions *into* `INITIALIZING`.
`UNWINDING` is skipped on this path because an idle wallet has no liquidity to withdraw.

---

## 4.6 Operational transition table

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `INITIALIZING` | `MONITORING` | reconcile complete | all three sources agree |
| `INITIALIZING` | `DEFENSIVE_HOLD` | reconcile impossible | RPC or exchange unreachable |
| `MONITORING` | `EVALUATING` | macro `REDEPLOY` intent received | snapshot fresh |
| `MONITORING` | `UNWINDING` | macro `WITHDRAW` intent received | mode `ACTIVE` |
| `MONITORING` | `HEDGING` | `abs(q_t - q*_t) > band` | mode `ACTIVE`, margin available |
| `MONITORING` | `DEFENSIVE_HOLD` | venue health degraded while resting | RPC or exchange unhealthy |
| `EVALUATING` | `MONITORING` | preflight fails or intent cleared | — |
| `EVALUATING` | `UNWINDING` | macro `WITHDRAW` intent supersedes redeploy | mode `ACTIVE` |
| `EVALUATING` | `REBALANCING` | redeploy approved | mode `IDLE` — nothing to withdraw |
| `EVALUATING` | `DEFENSIVE_HOLD` | preflight cannot confirm safe execution | — |
| `UNWINDING` | `REBALANCING` | withdrawal confirmed on-chain | position closed, fees claimed |
| `UNWINDING` | `DEFENSIVE_HOLD` | withdrawal cannot confirm | partial or unconfirmed removal |
| `REBALANCING` | `DEPLOYING` | swap filled | ratio within tolerance of target |
| `REBALANCING` | `DEFENSIVE_HOLD` | swap failed or venue degraded | — |
| `DEPLOYING` | `MONITORING` | liquidity confirmed live | bins match target range |
| `DEPLOYING` | `DEFENSIVE_HOLD` | deploy cannot confirm | partial or unconfirmed add |
| `HEDGING` | `MONITORING` | fill reconciled | `q_t ≈ q*_t` |
| `HEDGING` | `DEFENSIVE_HOLD` | margin blocked or venue degraded | — |
| `DEFENSIVE_HOLD` | `MONITORING` | conditions normalise | regime safe, hedge feasible |

**Every state except `DEFENSIVE_HOLD` itself has an edge into `DEFENSIVE_HOLD`.** That is
not incidental — it is rule 4 of section 4.8 expressed as topology. A job that cannot
confirm has exactly one legal exit, and it is not another job. In the diagram these edges
share a single fault bus into `DEFENSIVE_HOLD`; they are distinct transitions, drawn on
one lane because seven separate lines across the canvas read as noise.

The `MONITORING → UNWINDING` edge is the macro-to-operational withdrawal handoff: the
macro controller does not execute, it emits intent and the operational FSM performs the
confirmed exit. The `EVALUATING → REBALANCING` edge is what makes the idle path work:
entering from `IDLE` there is no liquidity to withdraw, so `UNWINDING` is skipped and
the wallet goes straight to ratio correction.

---

## 4.7 Type definitions

Boundary event from macro strategy into operational execution:

```ts
export interface ExecutionIntentEvent {
  readonly eventType: 'EXECUTION_INTENT';
  readonly action: 'WITHDRAW' | 'REDEPLOY';
  readonly priorityFeeMode: 'NORMAL' | 'AGGRESSIVE';
}
```

Operational state types:

```ts
export type FsmState =
  | 'INITIALIZING'
  | 'MONITORING'
  | 'EVALUATING'
  | 'UNWINDING'
  | 'REBALANCING'
  | 'DEPLOYING'
  | 'HEDGING'
  | 'DEFENSIVE_HOLD';

/** The hub is the only resting state; everything else is a job. */
export type RestingState = Extract<FsmState, 'MONITORING'>;
export type JobState = Exclude<FsmState, 'MONITORING' | 'INITIALIZING' | 'DEFENSIVE_HOLD'>;

export type TransitionMap = { readonly [S in FsmState]: readonly FsmState[] };

export const TRANSITIONS: TransitionMap = {
  INITIALIZING:   ['MONITORING', 'DEFENSIVE_HOLD'],
  MONITORING:     ['EVALUATING', 'UNWINDING', 'HEDGING', 'DEFENSIVE_HOLD'],
  EVALUATING:     ['MONITORING', 'UNWINDING', 'REBALANCING', 'DEFENSIVE_HOLD'],
  UNWINDING:      ['REBALANCING', 'DEFENSIVE_HOLD'],
  REBALANCING:    ['DEPLOYING', 'DEFENSIVE_HOLD'],
  DEPLOYING:      ['MONITORING', 'DEFENSIVE_HOLD'],
  HEDGING:        ['MONITORING', 'DEFENSIVE_HOLD'],
  DEFENSIVE_HOLD: ['MONITORING'],
} as const;
```

The reconciled view of the world — the only thing the FSM trusts:

```ts
export interface VenueSnapshot {
  readonly takenAt: number;
  readonly wallet: { readonly base: BN; readonly quote: BN };  // SOL, USDC
  readonly position: DlmmPositionSnapshot | null;              // null => IDLE
  readonly hedge: PerpHedgeSnapshot;
}

export interface DlmmPositionSnapshot {
  readonly positionPubkey: PublicKey;
  readonly lbPair: PublicKey;
  readonly lowerBinId: number;
  readonly upperBinId: number;
  readonly activeBinId: number;
  readonly totalXAmount: BN;      // Base  (tokenX)
  readonly totalYAmount: BN;      // Quote (tokenY)
  readonly unclaimedFeeX: BN;
  readonly unclaimedFeeY: BN;
}

export interface PerpHedgeSnapshot {
  readonly symbol: 'SOLUSDT';
  readonly positionAmt: number;   // negative = short
  readonly markPrice: number;
  readonly lastFundingRate: number;
  readonly nextFundingTime: number;
}
```

**Macro policy is upstream of this file.** If an implementation needs the five Q004
macro states in the same module tree, define them separately and bridge only through
`ExecutionIntentEvent`. Do not widen `FsmState` to include macro regime names.

**Hub reachability is an invariant, not a convention.** Assert it in a unit test so a
future edge cannot quietly create a loop that bypasses the hub:

```ts
/** From every state, MONITORING must be reachable. */
export function assertHubReachable(map: TransitionMap = TRANSITIONS): void {
  for (const start of Object.keys(map) as FsmState[]) {
    const seen = new Set<FsmState>([start]);
    const queue: FsmState[] = [start];
    let found = start === 'MONITORING';
    while (queue.length && !found) {
      for (const next of map[queue.shift()!]) {
        if (next === 'MONITORING') { found = true; break; }
        if (!seen.has(next)) { seen.add(next); queue.push(next); }
      }
    }
    if (!found) throw new Error(`${start} cannot reach MONITORING`);
  }
}
```

---

## 4.8 Preventing cross-venue collisions

The FSM exists to make a Solana write and a Binance write structurally unable to race.
Four rules carry that:

1. **One state, one transition.** A trigger arriving while a transition is in flight is
   queued on the hub and evaluated against fresh state when the hub regains control. It
   is never applied to a job already running.
2. **A transition holds a lease.** A job state acquires a lease naming the venues it will
   touch. No second lease is granted until the first closes.
3. **Idempotency keys survive retries.** The lease id is reused for every retry of the
   same leg, so a replayed Jupiter swap or a resent perp order cannot double-fill.
4. **Reconcile before advancing.** A job advances only on confirmed venue state — a
   landed transaction, a filled order — never on an assumed success. A partial result
   returns to the last reconciled state.

```ts
export interface TransitionLease {
  readonly id: string;                                   // idempotency key, stable across retries
  readonly from: FsmState;
  readonly to: FsmState;
  readonly openedAt: number;
  readonly venues: ReadonlySet<'SOLANA' | 'BINANCE'>;
}
```

Deadlock is preferable to a race: a job that cannot confirm goes to `DEFENSIVE_HOLD`,
never sideways into another job.

---

## 4.9 What this section does not decide

- GEX construction and wall extraction — Module 2, see `metrics_engine.md`
- EV formulation, LVR, funding drag — Module 3 economics, owned by the EV gate
- Bin selection and strategy shape — `liquidity_position_manager.md`
- Transaction building, retries, RPC choice — `execution_router.md`

The FSM consumes those verdicts. It does not compute them.
