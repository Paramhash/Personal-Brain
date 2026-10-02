---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-051
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/051-inventory-objective-benchmark-hedge.md
bot_commit: 1fa5166
source_sha256: 768aa7ba9adde106ec7913b26c8102746801ae7065ed6a15a8f59651d1b32992
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/051-inventory-objective-benchmark-hedge.md` at commit `1fa5166`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-051-inventory-objective-benchmark-hedge|ADR-051]] — The Inventory Objective Is Growth Against a Benchmark Inventory, and the Hedge Targets That Benchmark

- **Date:** 2026-09-30
- **Status:** **Proposed.** Not decided. The key decision is D1 (the benchmark SOL count). Nothing changes in code until
  the dispatcher decides D1–D4 and marks this Active.
- **Would amend:**
  - `hedge_engine.md` §2 and §6 (the neutrality target `q* = −x`);
  - [[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]] (the 50/50 re-ratio: when the benchmark is taken, relative to it);
  - [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]] (the funding drag's sign and size);
  - [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] (the hurdle's funding term).
- **Leaves unchanged:**
  - the EV gate's inequality (`ev_policy.md` §4);
  - the LVR model;
  - the exits ([[adr-016-fsm-withdrawal-guard-and-rpc-binding|ADR-016]], [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]], the macro FSM);
  - the reserves ([[adr-030-deployment-sol-reserve|ADR-030]]/039).
- **Research this answers:**
  - `todo/research/00 dual-inventory-growth-policy.md`;
  - `todo/research/01 warehouse-manager-cl-inventory-strategy.md`;
  - `todo/research/02 nash-equilibrium-cl-provider-strategies.md` (its payoff U_i is Π below).

## Context

**No ADR states what the bot is trying to grow.** The pieces are scattered:
- the SOL reserve ([[adr-030-deployment-sol-reserve|ADR-030]]/039);
- the 50/50 value re-ratio before deployment ([[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]]);
- the hedge `q* = −x_pos` (`hedge_engine.md` §2, a blueprint rule with no ADR);
- the gate ([[adr-015-fsm-cold-start-and-ev-gate|ADR-015]]/031/040/046).

Nothing defines success at close, and nothing accounts for it live. The research simulator reports P&L against HODL (`backtest_research.md` §4), but the live bot does not.

**The two research notes disagree.**
- The *dual-inventory* note makes growth of **both** token counts a hard gate: E[ΔSOL] > 0 and E[ΔUSDC] > 0.
- The *warehouse-manager* note says both cannot generally be guaranteed. It makes USD equity primary and HODL a
  secondary benchmark.

**Why both counts rarely grow under the current design.**
- A CL position's holdings are a function of price. It sells SOL as price rises and buys it as price falls, so at
  close one count falls unless price returns near its start or fees cover the drift.
- The current hedge, `q* = −x_pos`, neutralises the deployed SOL's price exposure. The book's delta is only the SOL
  outside the position.
- The book therefore grows **USD equity** by Π and lags HODL by `x₀·ΔP` whenever SOL rises, while the SOL count drains
  in rallies.

**The observation that resolves the tension.** Let Π be the net result of a cycle measured against a benchmark:
Π = fees − LVR − funding − hedge cost − gas − rent − slippage. Hedge the book to a **benchmark SOL count**
`S_bench`, not to zero:

q*_t = −(x_pos,t + S_wallet,t − S_bench)

- **Wealth then equals the benchmark plus Π, at any price.**
- At close, the perp is closed and the leftover SOL imbalance swapped, which restores the benchmark counts plus Π.
- Π is then split pro rata to the benchmark's value weights at the closing price. Both counts grow by the same
  percentage, g = Π / (the benchmark's value).
- **Growth of both counts holds exactly when Π > 0**, the same condition as beating the benchmark. The two notes'
  objectives become one.
- The current design is the special case `S_bench = S_wallet,t`, which gives `q* = −x_pos` and the USD-equity
  objective.

Worked example: 25 SOL + $3,000 at $120 ($6,000); Π = +$60 over the cycle; SOL ends at $150.

| Policy | SOL | USD | Value at $150 |
|---|---:|---:|---:|
| HODL | 25 | 3,000 | 6,750 |
| USD-neutral (today, `q* = −x_pos`) | ≈ 20 | ≈ 3,060 | ≈ 6,060 (HODL − ≈ $690) |
| Benchmark = HODL at open, Π split pro rata | 25.22 | 3,026.7 | 6,810 (+0.89% in both counts) |

## Decision (proposed)

1. **Objective hierarchy.** It applies at every cycle and is binding in this order:
   1. **Hard constraints:**
      - the SOL reserve ([[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]) is preserved;
      - a USDC minimum `USDC_min` is preserved (D4);
      - no collateral breach and no forced liquidation;
      - every exit reconciles liquidity and the hedge before completing (`hedge_engine.md` §6, `risk_guardrails.md`).
   2. **Growth against the benchmark:** enter only when E[Π] > 0 at [[adr-033-fee-yield-measurement-route|ADR-033]]'s conservative fee floor. This is the
      existing gate, with its costs completed per §4.
   3. **Distribution:** Π is split per D2, so both counts grow when Π > 0.

   USD equity is **reported**, not maximised, unless D1 chooses the USD benchmark.
2. **Cycle benchmark.**
   - A cycle runs from one deployment's `REBALANCING` entry to its confirmed exit and close-out.
   - The benchmark `(S_bench, U_bench)` is the reconciled wallet inventory at the cycle's start, **before** the [[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]]
     re-ratio swap, reserves included.
   - It resets to the closing counts at every cycle, so growth compounds:
     S_{k+1} = S_k(1+g_k) and U_{k+1} = U_k(1+g_k).
3. **Hedge target.** `hedge_engine.md` §2 becomes q*_t = −(x_pos,t + S_wallet,t − S_bench), from reconciled inventory
   only. §6's unwind rule applies with `x_remaining` in place of `x_pos`.
   - With D1 = HODL, q* ≈ 0 at open, and the perp tracks only the position's drift.
   - That drift turns the perp **long** when SOL rises, since the position has sold SOL. No rule forbids a long perp,
     and collateral guards apply to |q|.
4. **Costs the gate must now carry.**
   - **The close-out swap** (the leftover SOL imbalance) and **the split swap** (D2) at estimated slippage, inside Π.
   - **Funding** on the signed q* above, not on −x_pos. It is smaller in size and can change sign ([[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]] and
     [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s funding term).
   - Hedge churn ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]) is unchanged: the perp still tracks the position's gamma.
5. **Close-out.** After the exit is confirmed:
   1. close the perp;
   2. swap the SOL imbalance back to `S_bench` through the existing Jupiter path (ADR-021, [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]/025, with the same
      zero-amount no-op);
   3. apply D2.

   The benchmark for the next cycle is the result.
6. **Accounting, live and per cycle.** Carried in the decision record and the TICK log, and later on the monitor and in
   the Discord summary ([[adr-049-market-events-and-daily-summary-to-discord|ADR-049]]):
   - the benchmark counts and value;
   - the current counts, including the perp;
   - Π (in USD and as g);
   - USD equity;
   - HODL-at-open value;
   - ΔSOL and ΔUSDC.

   Numbers only, per `observability_contract.md` §2.

## Decision points for the dispatcher

- **D1 — the benchmark SOL count, the one real choice.**
  - **Recommended: HODL at cycle open.** Both counts grow whenever Π > 0, and you keep SOL price exposure by design.
  - **Alternative: wallet SOL only (today's `q* = −x_pos`).** The book is USD-neutral, grows USD equity only, and the
    SOL count is not protected. Choose this if the owner's liabilities are in USD.
- **D2 — the split of Π.**
  - **Recommended: pro rata to the benchmark's value weights at the closing price,** so both counts grow by the same g.
  - **Alternatives:**
    - a fixed weight w;
    - all to USD, which is simplest but grows only USD.
- **D3 — when to split.**
  - **Recommended: at each cycle close only.** No new FSM job, and one swap per cycle.
  - **Alternative:** harvest and split mid-cycle once claimable fees exceed a swap-cost threshold. That adds a job to
    `state_machine.md`, where fees are claimed only in UNWINDING today.
- **D4 — the USDC minimum.** A value, or "none": today there is none.

## What this does not change or promise

- **It does not make Π positive.** Fee yield is unmeasured on DLMM ([[adr-033-fee-yield-measurement-route|ADR-033]], and [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]]'s Route 4). Every benefit here
  is conditional on Π > 0.
- **It does not remove LVR.** The hedge's rebalancing is the LVR cost, under either benchmark.
- **With D1 = HODL, marked USD equity moves with SOL,** as HODL's does. That is the objective, not a risk to be hedged
  away.
- **No growth at a fixed rate is promised.** g varies per cycle and can be negative. The [[adr-033-fee-yield-measurement-route|ADR-033]] floor and the gate
  decide whether a cycle is entered at all.

## Consequences

- **Hedge.** With D1 = HODL:
  - the perp's average size falls from about half the capital to the position's drift;
  - funding drag and collateral both fall;
  - funding can become a credit when the perp is long in a positive-funding market.
- **One more swap per cycle,** priced into the gate.
- **Mark-to-USD volatility of equity** equals HODL's under D1 = HODL, and is near zero under the USD benchmark.
- **Code, once Active** (a later ticket):
  - the hedge engine's target;
  - [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]]'s funding and [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s hurdle funding term;
  - a close-out step after UNWINDING;
  - the per-cycle accounting fields.
- **Research first.** The research simulator gains a hedge-to-benchmark mode beside today's USD-neutral mode, so both
  objectives can be compared on the archive before anything live changes. [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] then supplies the fee side.

## Alternatives considered

- **Gate on P(ΔSOL > 0) and P(ΔUSDC > 0) with an unhedged or USD-hedged position,** as the dual-inventory note proposes.
  This is a directional bet that price returns near its start. Trending markets fail it by construction.
- **USD equity alone,** as the warehouse note proposes. Coherent, and it is D1's alternative, but it cannot deliver growth
  in SOL units.
- **Constant-mix benchmark** (a fixed SOL value weight, rebalanced). LVR is defined against it, which makes it
  analytically clean. It adds a second rebalancing policy for the owner to reason about, and HODL-at-open matches the
  dual-inventory note's wording directly.
- **A multi-provider Nash layer** (the Nash note). At about 0.1–0.2% of a ≈ $4.4M pool the bot is a price-taker, and
  Route 4's per-bin fee counters already net out competitors' liquidity. That note's payoff U_i is Π here.

## Reversed by

- The dispatcher choosing D1 = wallet SOL, which restores today's semantics with the accounting kept.
- Research showing the close-out and split swaps consume Π on typical cycles.
- A funding regime in which a long perp's cost dominates Π.
