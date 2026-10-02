---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-042
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/042-adr033-window-recorder-runs-as-moham.md
bot_commit: df5a53c
source_sha256: c34128867f9fdbb3928c518397af2536ab852195d98eb4ecb454181f570e041f
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/042-adr033-window-recorder-runs-as-moham.md` at commit `df5a53c`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-042-adr033-window-recorder-runs-as-moham|ADR-042]] — The [[adr-033-fee-yield-measurement-route|ADR-033]] Window's Recorder Runs as `moham`, an Accepted Exception to Recorder Account Isolation

- **Date:** 2026-09-27
- **Status:** **Active. Decided by the dispatcher 2026-09-27.** An exception, not a design change: the intended
  end state — the recorder under its own `dlmm-observer` account — is unchanged and remains TICKET L's.
- **Scope:** the [[adr-033-fee-yield-measurement-route|ADR-033]] 21-day observation window, and any recorder run on this host until TICKET L is
  executed. Nothing else.

---

## 1. The decision

The recorder for the [[adr-033-fee-yield-measurement-route|ADR-033]] window runs as **`moham`**, the host's only enabled account, not as
`dlmm-observer`. This is recorded as an accepted exception to the account isolation that Tickets L and I
describe, rather than left as an unstated deviation.

**Consequently, `windows_preflight.ps1` check 5 FAILing is accepted for the window**, and the window's
preflight gate is: **every check passes except check 5**, whose FAIL lines must be only the two
"does not exist — ACL isolation cannot be verified" lines for `production\.env` and `production\.state`.
Any other check-5 line, or any FAIL in another check, still blocks the window.

## 2. The facts that make this the right call

- **`dlmm-observer` does not exist.** Verified 2026-09-27: the local accounts are `Administrator`,
  `DefaultAccount`, `Guest`, `moham`, `WDAGUtilityAccount`. TICKET L, which creates it, was **deferred
  2026-09-26** (`todo/deferred.md`) on the ground that it is deployment hygiene for a bot that is not deployed.
- **The deferral already anticipated this.** One of L's recorded wake triggers is "the recorder is to run as
  anything other than `moham`". Running as `moham` is the condition under which L stays asleep; this ADR makes
  that choice explicit instead of implied.
- **The soak that proved the recorder ran as `moham`.** TICKET J intended its soak to run as `dlmm-observer`
  so that it would also demonstrate L's acceptance. It did not: every archive file under
  `soak-phase2-2026-09-26\` and `soak-phase3-2026-09-27\` is owned by `DESKTOP-PQP9JPL\moham`. J2 and J3 are
  therefore evidence about the recorder, **not** about the account boundary, and running the window under
  the same account keeps the window on the configuration that was actually tested.
- **The one exposure with live value is already closed.** `C:\observation\observer.env` carries an explicit
  ACL (`SYSTEM:(F)`, `Administrators:(F)`, `moham:(R)`, no inheritance), applied and verified 2026-09-26.

## 3. Recorded cost

- **No enforced single writer.** Blueprint §3 rule 5's single writer is conventional, not enforced:
  `C:\observation` still inherits `Authenticated Users: Modify`, and on this host that means `moham` —
  the same account that runs the trading process, the monitor, TICKET T's recon, and every shell. Any of
  them could write into the archive. The protection is procedural: nothing else is configured with the
  window's archive root.
- **The recorder can read what `moham` can read**, including anything the trading process can. It holds no
  signer and imports no `src/execution/` module ([[adr-032-observation-archive-ownership-and-isolation|ADR-032]]), so this widens what a compromised recorder could
  read, not what it could sign.
- **Check 5 stops meaning anything for the window.** A FAIL the operator has been told to accept is a FAIL
  the operator learns to skip. §1 limits the acceptance to two exact lines for that reason.
- **The alarm shares the constraint.** `observer-health` also runs as `moham`, Interactive, so it fires only
  while `moham` is logged on. That was already true and is unchanged by this ADR.

## 4. What reverses this exception

Any one of these ends it, and the recorder moves to `dlmm-observer` under TICKET L before the next run:

- a second account is created on this host, for any reason;
- `production\.env` or `production\.state` is about to exist — TICKET F2 is staged;
- the archive is required to have an enforced single writer;
- the trading process is to run live against capital on this host while the recorder is running.

## 5. Not decided here

- **The promotion boundary** (ADR-037, reserved for TICKET I) — untouched.
- **How the recorder is supervised and stopped** — TICKET I, which now carries the requirement that the
  recorder be stoppable cleanly (see its 2026-09-27 amendment).

---

## Amendment 2026-09-27 — terminology: this is not the [[adr-033-fee-yield-measurement-route|ADR-033]] fee window

This ADR's title and §1 say "the [[adr-033-fee-yield-measurement-route|ADR-033]] window". **That is inaccurate and is corrected here** rather than
edited, because `docs/decisions/` is append-only.

The run this ADR governs is **the 21-day archive run**: the archive's route-independent series — pool state,
`bins[]`, spot — recorded with `fee_observation: null`. [[adr-033-fee-yield-measurement-route|ADR-033]]'s own Consequences anticipate exactly this
("the recording start date and the fee-measurement start date differ"). **It cannot ratify the fee-yield
constant**, because [[adr-033-fee-yield-measurement-route|ADR-033]]'s ratification rule — seven 3-day sub-window *yields*, the 3× stability test, the
10th-percentile floor — needs fee accrual from a live position, and [[adr-033-fee-yield-measurement-route|ADR-033]]'s capital gate is unapproved.

What it does feed: the σ axis of [[adr-033-fee-yield-measurement-route|ADR-033]]'s required (fee yield, σ) surface, and the concentration multiplier.
**σ alone can decide against deployment** — [[adr-033-fee-yield-measurement-route|ADR-033]] records that at 1.5× the assumed σ no plausible fee yield
saves the gate — so the run can return a no-go without fee data, but never a go.

**The decision in §1 is unchanged**, and it applies to every recorder run on this host until TICKET L is
executed, **including the future [[adr-033-fee-yield-measurement-route|ADR-033]] fee window** if that starts before L. The accepted check-5 FAIL lines
are unchanged.

## Amendment 2026-10-01 16:49Z — `moham` is the standing recorder account on this host (TICKETS L and I retired)

- **Status:** **Active. Decided by the dispatcher 2026-10-01.**
- **What changes:** on this single-account host, the recorder running as `moham` under `dlmm-observer` stops being a
  window-scoped exception. It becomes the standing arrangement. TICKET L, which held the `dlmm-observer`-account end
  state, is retired.
- **What reverses it:** §4's conditions still apply unchanged — a second account, production secrets about to exist,
  an enforced single writer, or live trading beside the recorder. They are now carried by
  `docs/meta/promotion_workflow.md` §9 (host preconditions for the first trading-bot promotion), not by TICKET L. If any
  becomes true, account separation is done as §9 item 3 describes, before the next recorder run.
- **§5 "Not decided here":**
  - **The promotion boundary** (formerly reserved for TICKET I): now `promotion_workflow.md` §9 item 1.
  - **Recorder supervision and the clean stop:** done 2026-09-27 (`observer_start.ps1`, `observer_stop.ps1`, a verified
    `RUN_STOP`) and in use.
