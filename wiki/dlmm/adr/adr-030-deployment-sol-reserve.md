---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-030
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/030-deployment-sol-reserve.md
bot_commit: 93d497d
source_sha256: 8fbff84ac7d2fa02dc5c9f9acde3df2f4b703a87e923444c4f76861c948d2ff2
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/030-deployment-sol-reserve.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-030-deployment-sol-reserve|ADR-030]] — Deployment Holds Back a SOL Reserve and Rejects an Underfunded Wallet Before Construction

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** `liveAdapters.ts` sized the deployment's base deposit from the entire reconciled `walletSolBalance_t`. The 2026-09-19 13:14 Devnet Step 6 soak reached deployment construction and the simulation returned `{"InstructionError":[3,{"Custom":1}]}` with the log `Transfer: insufficient lamports 1222847995, need 1266246275` — the deposit asked for the whole wallet after earlier instructions in the same transaction had already spent 43,398,280 lamports on rent for the position account and an idempotent ATA. The transaction was self-defeating by construction and would fail identically on Mainnet; it was not a Devnet artefact. `liquidity_position_manager.md` §2a already referred to "the fee reserve held back from deployment", but no blueprint, ADR, or constant ever defined one, so the reserve was assumed by policy and absent from the code.
- **Decision 1 (Policy):** `liquidity_position_manager.md` gains §3a. A deployment may never spend the wallet's entire base balance. The reserve must cover position-account rent, idempotent ATA rent, rent for any bin array the range touches that does not yet exist, the base transaction fee, priority fees, and compute-budget costs. Spendable base is `walletBase - reserve`, and `DEPLOYING` is permitted only when that quantity is strictly positive.
- **Decision 2 (Form and value):** The reserve is a fixed lamport quantity ratified in `strategy.config.ts` as `DEPLOY_SOL_RESERVE_DEFAULT = 0.25` SOL, operator-overridable through `DEPLOY_SOL_RESERVE_BASE` on the [[adr-026-devnet-tolerance-and-timeout-adjustments|ADR-026]] precedent, parsed with the same fail-closed validation. It is not a percentage of the wallet — the cost it covers is denominated in accounts and signatures, not in position size — and not a live estimate, because the adapter must be able to reject an underfunded wallet before it constructs anything.
- **Decision 3 (Preflight guard):** `executeDlmmDeploy` receives the full reconciled base amount and the reserve, subtracts the reserve itself, and rejects with the named reason `INSUFFICIENT_SOL_RESERVE` when spendable base is not strictly positive. The rejection happens before `buildChunkTransaction`, before simulation, and before signing. Applying the reserve inside the pure module rather than in the adapter is deliberate: the adapter cannot be loaded offline, so a guard placed there would be unassertable.
- **Why 0.25 SOL:** the measured shortfall of 43,398,280 lamports is diagnostic evidence, not the constant. It is the *best* case — the soak's range (bins 1103–1124, bin arrays 15 and 16) targeted arrays that already existed. A `BinArray` is 10,136 bytes and its rent-exempt minimum is 71,437,440 lamports, so a range crossing into two uninitialized arrays adds 142,874,880. Worst case is therefore approximately 186,273,160 lamports (0.18627316 SOL), and 0.25 SOL carries roughly 34% margin above it. The value is deliberately conservative and is documented as such; it is not an exact estimate and must not be described as one.
- **Consequences:** A deployment now deposits `walletBase - reserve` rather than `walletBase`, so the rent the transaction spends on its own prerequisites is funded rather than borrowed from the deposit. An underfunded wallet fails closed with a named reason at preflight instead of surfacing as an opaque `Custom:1` from a simulation. Quote-side sizing, chunk apportioning, active-bin containment, the 20–69 bin rule, the dynamic re-ratio, and [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]'s zero-amount bypass are all unchanged. On a 1.266 SOL Devnet wallet the reserve withholds roughly 20% of the base side, which is a real reduction in deployed base inventory and the cost of correctness here.
- **Alternatives rejected:** Pin the reserve to the observed 43,398,280 lamports — fits one run and fails the first range that touches an uninitialized bin array; express the reserve as a percentage of the wallet — the cost is per-account, not proportional to size; query rent exemption per account at dispatch — accurate but requires live RPC inside the sizing path and still cannot reject before construction without an extra round trip, and the ticket permits a documented conservative constant instead; catch the insufficient-lamports error and retry smaller — the guardrails forbid catching the error, and it would convert a configuration fault into silent size drift; raise the Devnet wallet balance — hides the defect rather than fixing it, and it would still fail on Mainnet.
