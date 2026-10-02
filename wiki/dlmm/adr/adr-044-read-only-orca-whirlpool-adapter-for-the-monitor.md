---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-044
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/044-read-only-orca-whirlpool-adapter-for-the-monitor.md
bot_commit: 766f0ac
source_sha256: 1174f63927a9eaacf8d37afb593eb8f968f0880f23f2462ce2143a5b970f7938
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/044-read-only-orca-whirlpool-adapter-for-the-monitor.md` at commit `766f0ac`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] — A Read-Only Orca Whirlpool Adapter May Feed the Monitor; Meteora DLMM Remains the Sole Trading Venue

- **Date:** 2026-09-28
- **Status:** **Active. Decided by the dispatcher 2026-09-28** (plan "Orca Whirlpools SOL/USDC monitoring with
  GEX overlay": feasible via an adapter; monitoring only; ADR and monitor blueprint first).
- **Supersedes, in part:** [[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]]'s prohibition of "Orca venue wrappers, and parallel venue abstractions", **for
  the monitor only** (`src/monitor/`). [[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]] is otherwise unchanged and remains in force for every other domain.
- **Owns:** `docs/architect/monitor.md` §6, root `src/monitor/venue/`.

## Context

The monitor (TICKET P) overlays the Deribit SOL GEX profile, the walls, ZGL and the [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] recommended window
on the Meteora DLMM SOL/USDC pool. The operator wants the same view for Orca Whirlpools SOL/USDC, to compare
where liquidity sits on each venue against the same dealer-gamma structure.

Feasibility was established on 2026-09-28:

1. **The GEX side has no venue in it.** Strikes are USD; walls are selected against off-chain spot, deliberately
   not the pool price (`gexEngine.ts`). A venue contributes only a pool price and a liquidity distribution.
2. **Both venues are geometric price grids with exact closed forms.** DLMM: `p = (1+binStep/1e4)^bin · 10^(dx−dy)`.
   Whirlpool: `p = 1.0001^tick · 10^(dA−dB) = (sqrtPriceX64/2^64)^2 · 10^(dA−dB)`. The [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] half-width
   generalises as `ceil(ln(1+mult·σ·√h) / stepLn)` in grid units, with Whirlpool bounds snapped to `tickSpacing`.
3. **The read is cheap.** The Whirlpool account (653 bytes) and ~7 fixed tick arrays (9,988 bytes each, ±10%) fit
   one `getMultipleAccounts`. The main pool, `Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE` (tickSpacing 4,
   0.04%; SOL = tokenA), held >99% of Orca SOL/USDC TVL on the day of assessment. Layouts and discriminators were
   checked against mainnet.

Two rules stood in the way: [[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]] names `@meteora-ag/dlmm` the sole CL venue and bans Orca wrappers and venue
abstractions; and `system_index.md` states no source root exists for Orca venue adapters. The monitor also had
no blueprint — `system_index.md` had no row for `src/monitor/`, and TICKET P's scope served as its spec.

## Decision

1. **A read-only Orca Whirlpool pool adapter may exist under `src/monitor/venue/`**, behind a venue-neutral
   `PoolVenue` port that the Meteora DLMM read is refactored behind as well. It reads pool state and tick arrays
   and returns a price, a price grid, and a liquidity profile. **Nothing else.**
2. **No Orca SDK.** Accounts are decoded by a pure, hand-written layout reader over `getMultipleAccounts` bytes,
   verifying the Anchor discriminator and account size and **failing closed** on any mismatch. The monitor's
   third-party surface (test P94) stays `@meteora-ag/dlmm`, `@solana/web3.js`, `ws`, `zod`. Adding any
   `@orca-so/*` package needs a further ADR.
3. **Monitoring only.** The adapter holds no signer, builds no transaction, reads no position account, and is not
   imported by `src/index.ts`, `src/execution/**`, `src/decision/**`, `src/observation/**` or
   `src/backtest/**`. Meteora DLMM remains **the sole trading venue**; [[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]]'s decision and its rejected
   alternatives stand for execution, planning and the FSM.
4. **The Orca view is a second monitor process**, on its own port, selected by monitor configuration. The Meteora
   monitor process is unaffected by its existence. Its RPC cost is **measured before it runs continuously**
   alongside the recorder, and recorded in `monitor_rpc_budget.md`.
5. **Not authorised by this ADR:** recording Orca into the observation archive; Orca replay; Orca in the research
   simulator; calls to Orca's HTTP API (network egress to a new host). Each needs its own decision.
6. **The monitor now has a blueprint**, `docs/architect/monitor.md`, routed from `system_index.md`. It codifies
   TICKET P's standing rules and adds the venue adapter's boundary (§6).

## Consequences

- The operator can compare Meteora and Orca liquidity against one GEX profile, on one USD axis, with the same
  planner window expressed in each venue's grid.
- The view model gains `venue` and a grid descriptor (schema 5 → 6). Bin-denominated fields remain for DLMM and
  replay; tick-denominated equivalents are added, not substituted, so existing replay files still load.
- **Recorded cost — layout drift.** A hand decoder breaks silently if Orca changes an account layout without
  changing its discriminator or size. Mitigation is fail-closed validation plus a fixture test on captured bytes;
  a drift therefore stops frames rather than corrupting them.
- **Recorded cost — dynamic tick arrays.** Orca's variable-size `DynamicTickArray` layout was not verified at
  adoption. Until a fixture-backed decoder exists, such arrays are reported as "not decoded", never guessed.
- **Recorded cost — RPC.** A second monitor process invalidates the measured budget until re-measured.
- [[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]]'s text is unchanged (the decisions directory is append-only); this ADR is its exception, as [[adr-032-observation-archive-ownership-and-isolation|ADR-032]] is
  for `src/observation/`.

## Reversed by

A decision to trade on Orca (that needs its own ADR across range planning, position management, execution and
the FSM — not an extension of this one); a layout change that the fail-closed decoder cannot express; or the
Orca monitor's measured RPC cost displacing the recorder's coverage.

## Amendment — 2026-09-28: measured pool volume from Orca's stats API (dispatcher decision)

Decision §5 listed "calls to Orca's HTTP API (network egress to a new host)" as not authorised. **The dispatcher
authorised one such call on 2026-09-28**, for TICKET U, because it supplies what no other source in this repository
does: a **measured** volume series (the archive records no fees or volume, [[adr-033-fee-yield-measurement-route|ADR-033]]).

- **Permitted:** `GET https://api.orca.so/v2/solana/pools/<configured pool>` from the Orca monitor process only. Host
  and path are code constants; no key, no other route, no redirect to another host; Node built-ins only (P94
  unchanged); its own cadence (default 5 min), independent of the pool tick. Detail: `monitor.md` §6.6.
- **Meaning:** whole-pool volume, fees and TVL as reported by Orca. It is **not** a position's fee income and **does
  not ratify** the [[adr-033-fee-yield-measurement-route|ADR-033]] fee-yield constant.
- **Still not authorised:** persisting it, recording it in the archive, or feeding it to the planner, EV gate or
  research simulator. Each needs its own decision.
- **Recorded cost:** a second outbound host, whose availability and correctness this repository cannot verify
  beyond schema validation and a price cross-check against the chain. A stats outage degrades only the stats panel.
- The 24/7 running of the Orca monitor on port 7762 was also decided (TICKET U), conditional on the RPC
  measurement in decision §4.

## Implementation note — 2026-09-28 (TICKET U)

- **Dynamic tick arrays are now decoded.** The recorded cost above ("not verified at adoption") is resolved: the
  layout was verified against Orca's `dynamic_tick_array.rs` and two populated mainnet accounts captured read-only,
  which is the condition this ADR and TICKET U set. The decoder still fails closed (bitmap/tag disagreement,
  trailing bytes, wrong size).
- **No planner change was needed.** A Whirlpool is presented to the unchanged `planDeployRange` in grid indices with
  an equivalent step (`monitor.md` §6.4), so no planning formula is restated.
- **Measured cost:** one `getMultipleAccounts` (8 accounts, ~93 KB) per 30 s tick; combined with the recorder and the
  DLMM monitor, 26,784 calls/day (0.310 req/s), burst 12 (`monitor_rpc_budget.md`). The Orca monitor runs 24/7 on
  port 7762 from 2026-09-28.
