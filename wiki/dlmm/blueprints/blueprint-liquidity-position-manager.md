---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/liquidity_position_manager.md
bot_commit: aebf1c0
source_sha256: 6ac0536c3bde3544be1dfb3c5390e07d0f552a04de4f53cea37177c5d114c0de
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/liquidity_position_manager.md` at commit `aebf1c0`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Liquidity Position Manager

**Domain owner:** Execution
**Status:** authored and binding
This file fixes the DLMM position lifecycle boundary for inventory re-ratio, deploy-bin selection, liquidity-shape choice, transaction sizing, and post-action reconciliation.

---

## 1. Scope

This blueprint governs `REBALANCING` inventory re-ratio, `DEPLOYING` DLMM construction from an
approved range plan, liquidity-shape and bin-count constraints, and Solana transaction sizing,
chunking, and reconciliation.

It does not calculate walls or bin ranges, own Solana market-data intake, or advance FSM state.

---

## 2. REBALANCING

`REBALANCING` must use the Jupiter Swap API in this order (ADR-021 moved the endpoints from the
retired v6 host to `api.jup.ag/swap/v1/*`):

1. request `/quote`
2. request `/swap` using the accepted quote
3. deserialize and submit the returned swap transaction
4. reconcile wallet and pool inventory before allowing `DEPLOYING`

The Jupiter adapter owns REST transport and transaction submission for this workflow. It may
not infer deployment bounds or declare the re-ratio complete from an acknowledgement alone.

### 2a. What `REBALANCING` trades — the dynamic 50/50 re-ratio ([[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]])

The size of the re-ratio is **derived, not configured**. It is computed from a freshly reconciled
`SolanaPoolStateSnapshot` at dispatch:

```text
poolPrice   = activeBinPriceQuotePerBase(snapshot)        // ADR-020, §5a of ev_policy.md
totalQuote  = baseBalance * poolPrice + quoteBalance
targetSide  = totalQuote / 2
correction  = (baseBalance * poolPrice - targetSide) / poolPrice   // signed, whole base tokens
```

- a **positive** correction is base-heavy: sell base for quote, and the Jupiter input mint is the
  base mint
- a **negative** correction is quote-heavy: buy base with quote, and the input mint is the quote
  mint
- the wire amount is always denominated in the **input** mint's base units, so the two directions
  do not share a unit and must not share a conversion

**The base side is valued at the pool's own price.** A perpetual mark is not admissible here for
the same reason `ev_policy.md` §5a gives: it denominates a different venue's quote asset, and on
a pool that does not quote in it the resulting correction is an artefact of an unrelated exchange
rate rather than of the inventory.

**Below the reserve tolerance the correction is exactly zero.** The tolerance is a ratified
constant in `strategy.config.ts`, initially `0.05` whole base tokens, and it exists because the
fee reserve held back from deployment is itself of that order — a correction smaller than the
reserve is chasing a balance the wallet cannot hold anyway. Exact zero routes to [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]'s
idempotent no-op, which returns `SUCCESS` without contacting Jupiter.

**Missing, stale, invalid, or non-positive facts fail closed.** A stale snapshot, a
non-derivable pool price, negative balances, or unusable decimals produce a named rejection and
no trade. They must never collapse into a zero-amount no-op, because "already balanced" and
"cannot tell" are different facts and only one of them permits `DEPLOYING` to follow.

**`SWAP_AMOUNT_BASE_UNITS` is not the source of truth** for this policy and cannot override a
calculated size. The resulting `JupiterQuoteRequest` still carries the ratified slippage cap, and
§4's versioned-transaction rule and step 4's reconciliation requirement are unchanged.

---

## 3. DEPLOYING

`DEPLOYING` consumes a deterministic range plan from `range_planning.md` and must use either
`StrategyType.Curve` or `StrategyType.BidAsk`. Liquidity must be distributed across no fewer
than 20 and no more than 69 bins, inclusive.

The deployment adapter must validate the range plan against freshly reconciled DLMM pool state
before constructing each transaction. It must confirm the deployed bins and resulting position
after submission before reporting success to the operational FSM.

---

### 3a. The deployment SOL reserve ([[adr-030-deployment-sol-reserve|ADR-030]] policy; [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] form)

**A deployment may never spend the wallet's entire SOL balance.** §2a has always referred to "the
fee reserve held back from deployment" as though it were ratified; it was not. Nothing defined it,
and the adapter deployed `walletSolBalance_t` in full. The 2026-09-19 13:14 Devnet soak is what
that costs:

```text
Transfer: insufficient lamports 1222847995, need 1266246275
```

The deposit instruction asked for the whole reconciled balance after earlier instructions *in the
same transaction* had already spent 43,398,280 lamports on rent. A transaction that funds its own
prerequisites out of the amount it is trying to deposit cannot succeed on any cluster.

**What the reserve must cover.** Every lamport the deployment transaction consumes that is not the
deposit itself:

- rent-exempt funding for the position account created by `InitializePosition`
- rent-exempt funding for any associated token account created idempotently alongside it
- rent-exempt funding for **any bin array the range touches that does not yet exist**
- the base transaction fee and any priority fee
- compute-budget costs

The bin-array term dominates and is the reason the reserve cannot be derived from a single
observation. A `BinArray` account is 10,136 bytes, so its rent-exempt minimum is 71,437,440
lamports — on its own, 1.65× the entire shortfall measured above. The measured run happened to
target a range whose bin arrays already existed. A range that crosses into an uninitialized array
pays that cost, and a reserve fitted to the observed number would fail the first time it did.

**Form — amended by [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]], 2026-09-27.** The reserve is **derived from the plan**, as pure
arithmetic over the Meteora SDK's published rent constants (`config/deployRentModel.ts`,
`deployReserveLamports`):

```text
reserve = Σ_chunks rent(position account) + arraysTouched × BIN_ARRAY_FEE
        + TOKEN_ACCOUNT_FEE + chunkCount × base fee + DEPLOY_RESERVE_MARGIN_BASE
```

It was a fixed `0.25 SOL` under [[adr-030-deployment-sol-reserve|ADR-030]], which covered one ≤69-bin position touching two arrays.
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s σ width and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]'s envelope made plans wider, and width creates **positions** (one per
69-bin chunk, each with its own rent) and crosses **bin arrays**; at the 203-bin σ width the worst
case is 1.84× the old constant. The four constraints [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] fixes are binding:

1. **Every touched bin array is assumed uninitialized.** The worst case keeps the computation free of
   RPC, so the guard can still reject before construction; it over-reserves on an established pool,
   deliberately.
2. **Chunk before reserving.** The chunk count is an input to the cost. `chunkBinRange` is pure, so
   the guard still precedes every pool read, build, simulation and signature.
3. **`DEPLOY_SOL_RESERVE_BASE` is a floor, not the value.** It can raise the derived reserve and can
   never lower it; absent, there is no floor.
4. **`DEPLOY_RESERVE_MARGIN_BASE` (0.01 SOL, priority fees and compute) is UNRATIFIED.**

It is still not a percentage of the wallet — the cost is denominated in accounts and signatures, not
in position size — and still not a live estimate: a figure that needs an RPC round trip could not be
checked before construction. Floor division is used for array indices, because the pool's bin ids are
negative and truncation undercounts in the direction that under-funds.

**Minimum balance to enter `DEPLOYING`.** The wallet's base balance must strictly exceed the
reserve. Spendable base is `walletBase - reserve`, and a deployment is permitted only when that
quantity is strictly positive.

**Fail closed, before construction.** When the wallet cannot fund the reserve the adapter must
emit a named deployment failure and must not build, simulate, sign, or send a transaction. An
underfunded wallet is a fact the adapter can establish from reconciled state alone, and
discovering it from a simulation error — which is how it was discovered — makes a configuration
problem look like a venue problem.

**The reserve is held back, not spent.** It is excluded from `totalXAmount` and from nothing else.
Quote-side sizing, chunk apportioning, active-bin containment, the 20–69 bin constraint, and §4's
size rule are all unchanged by it. Most of it comes back: position and ATA rent are refunded on close;
bin-array rent and fees are sunk, and [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] prices that sunk part into the EV gate.

**The planner does not see the wallet.** Capping planned width by what the wallet can afford would make
`range_planning.md` depend on reconciled wallet state, crossing the `intelligence -> decision` arrow. The
planner plans on market inputs; execution refuses what cannot be funded, with the same
`INSUFFICIENT_SOL_RESERVE` rejection as before — more often, and correctly.

---

## 4. Versioned transaction and size rule

All Jupiter and Meteora execution transactions must use `VersionedTransaction`.

Every serialized transaction must respect Solana's 1232-byte limit. A planned action that
would exceed that limit must be explicitly chunked into ordered transactions, each independently
constructed, submitted, and reconciled before the next starts.

Chunking is an execution rule, not a best-effort optimization. The adapter must not assume that
a multi-bin deployment fits into one transaction.

---

## 5. Sequencing and reconciliation

```text
range plan -> Jupiter quote -> Jupiter swap -> inventory reconciliation -> DLMM deploy -> DLMM reconciliation -> hedge recalculation
```

No Binance hedge resize may run concurrently with the Solana swap or deployment step. The
post-deploy hedge target is calculated only from reconciled resulting inventory, per
`execution_router.md`.

---

## 6. Prohibitions

- Do not construct a legacy `Transaction` for Jupiter or Meteora actions.
- Do not submit a transaction larger than 1232 bytes.
- Do not skip explicit chunking when an action exceeds the size limit.
- Do not deploy fewer than 20 or more than 69 bins.
- Do not use a liquidity strategy other than `StrategyType.Curve` or `StrategyType.BidAsk`.
- Do not advance the operational FSM on an acknowledgement without reconciled Solana state.
- Do not calculate deploy bounds inside the execution adapter.
- Do not deploy the wallet's entire base balance. §3a's reserve is held back from every
  deployment, and a transaction that funds its own rent out of its deposit is invalid by
  construction.
- Do not construct, simulate, sign, or send a deployment transaction for a wallet that cannot
  fund the reserve. The rejection is a preflight fact, not a simulation result.

These prohibitions are binding.
