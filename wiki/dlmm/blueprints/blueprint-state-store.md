---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/state_store.md
bot_commit: 93d497d
source_sha256: a074f71f1f52942a94534b073cdc6e6b05ded61896e4b8fb17f29e8e226c687c
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/state_store.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# State Store

**Domain owner:** State
**Status:** authored and binding
This file fixes the ownership, durability rules, restart-recovery contract, and crash-safety requirements for in-memory and on-disk state in the development repository.

---

## 1. Scope

This blueprint governs:

- in-memory state that tracks the bot's last known durable execution facts
- on-disk persistence of restart-relevant state
- restart recovery during `INITIALIZING`
- partial execution reconciliation inputs and resume points
- atomicity requirements for persisted state writes

It does not authorize venue execution. It stores state and coordinates recovery facts.

---

## 2. Owned durable state

The State domain must durably persist, at minimum:

- `PendingWithdrawalResumePoint`
- the active DLMM position state
- the Binance hedge state

These are not optional caches. They are the minimum restart-recovery facts required to
reconcile an interrupted process against live venues.

If additional execution jobs gain resumable state later, that state belongs here as well,
not in executor-private files.

---

## 3. Boot and recovery rule

On process boot, `INITIALIZING` must reconcile stored state against live venue queries
before the bot resumes operational work.

The rule is binding:

1. load the last durable state snapshot
2. query the live venue facts required to check it
3. reconcile durable state against live DLMM and Binance reality
4. decide whether the process resumes a pending job, clears stale durable state, or routes
   into a fault or observation path

Stored state is evidence of prior intent and prior observed progress. It is not authority
over the venue. The live venue remains authoritative wherever a mismatch exists.

---

## 4. Partial execution reconciliation

The State domain owns persisted reconciliation inputs for interrupted or partially completed
execution jobs.

For defensive withdrawal, this includes durable persistence of `PendingWithdrawalResumePoint`
and the last known active DLMM position facts needed to resume or conclusively terminate the
job.

For hedge execution, this includes the persisted Binance hedge state needed to decide whether
the exchange position already matches, partially matches, or diverges from the intended
state.

Executors may return reconciliation facts. They may not be the sole owners of those facts
across process restarts.

---

## 5. Atomicity and crash safety

State-store writes must be synchronous or atomic enough to prevent torn state on crash.

The minimum requirement is:

- a durable write must not leave half-written JSON, partial records, or mismatched paired
  state visible as if it were valid
- a caller that receives write success must be able to assume the state is durably readable
  on the next process boot
- replacing one durable snapshot with another must occur through an atomic-enough mechanism
  such as write-then-rename, transactional commit, or an equivalent single-commit strategy

The exact file or storage technology is an implementation detail. The atomicity guarantee is
not.

---

## 6. Boundary rules

The State domain is the only module permitted to own durable restart state.

Other modules may:

- request loads
- request saves
- consume reconciled state facts returned by the state store

Other modules may not:

- read another module's private persistence directly
- maintain their own hidden restart files for execution state
- treat in-memory state alone as sufficient for a resumable job

This blueprint is the load-bearing reason `system_index.md` routes cross-module private state
access through `state_store.md` rather than permitting ad hoc file reads.

---

## 7. Data-flow direction

The State domain sits between Market Data and downstream decision and execution domains:

```text
marketdata -> state -> intelligence -> decision -> risk -> execution
```

Reading persisted state against this arrow is permitted where the contract allows it.
Private persistence writes outside this domain are a boundary violation.

---

## 8. Prohibitions

- Do not let execution modules own their own restart-persistence files.
- Do not treat a previously stored resume point as authoritative without live reconciliation.
- Do not acknowledge a durable write before it is synchronous or atomic enough to survive a crash.
- Do not persist only part of a coupled execution state such that a crash can strand torn state.
- Do not bypass the state store to read another module's private restart data.

These prohibitions are binding.
