---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-043
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/043-research-simulator-reads-archive-offline.md
bot_commit: 1a03346
source_sha256: 6c5a1f56be9ad450badb33d9b067acd0dc7476eb13ad7645befcf21a43bbd7e7
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/043-research-simulator-reads-archive-offline.md` at commit `1a03346`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-043-research-simulator-reads-archive-offline|ADR-043]] — An Offline Research Simulator May Read the Observation Archive; Its Results Are Not Fee Ratification

- **Date:** 2026-09-28
- **Status:** **Active. Decided by the dispatcher 2026-09-28** (plan "CL policy simulator": hedged and unhedged
  side by side; research simulator and report; no change to the live bot).
- **Owns:** `docs/architect/backtest_research.md`, root `src/backtest/research/`.

## Context

Profitability of the concentrated-liquidity position turns on two open decisions: **where** to deploy (the
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] σ window, or between the put and call walls) and **when** to close and redeploy. The live bot has no
out-of-range exit, [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]]'s proximity threshold `t` is deferred, and each close-and-redeploy sinks ~0.30 SOL of
bin-array rent at 203 bins ([[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]/040). Answering these needs a simulation over recorded data. Two rules stood
in the way of doing that honestly:

1. `observation_archive.md` §4: "No other domain reads the archive at runtime." Silent on offline readers.
2. [[adr-033-fee-yield-measurement-route|ADR-033]]: fee yield is measured only by direct accrual on a live position; inferred yield must not be presented
   as calibrated. No fee or volume series exists.

## Decision

1. **An offline, read-only research simulator may read the archive's day files** (and recon decision files),
   after the fact, writing nothing but its own report. This is not a runtime reader and not a writer, so §4's
   single-writer and isolation guarantees are unaffected.
2. **Its fee figures are expressed only in units of an unknown volume `V`** and reported as **break-even** — the
   volume, or fee yield on capital, at which a policy's losses would be covered. Every such figure is labelled
   **"units of V; not calibrated yield ([[adr-033-fee-yield-measurement-route|ADR-033]])"**. A break-even ranks policies; it never establishes
   profitability and never ratifies a fee constant.
3. **It imports no execution, FSM or signer code** (import-graph test), and **changes no live behaviour.** A
   policy it favours reaches the bot only through a later ADR in the owning domain.

## Consequences

- The "where / when" question gets evidence: time in range, cycles, sunk rent (with bin-array memory), impermanent
  loss, hedged LVR-equivalent and hedge costs, per policy, per UTC day and per [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-window.
- The answer is **conditional on volume**. It can say "policy A needs half the volume policy B needs to break
  even"; it cannot say either earns. That remains [[adr-033-fee-yield-measurement-route|ADR-033]]'s to establish.
- Data is short: ~1.5 days of archive at adoption, 21 days by 2026-10-18; walls only from 2026-09-28 11:01Z.
  Rankings are trusted only once they hold across sub-windows.
