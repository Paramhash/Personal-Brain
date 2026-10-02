---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-016
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/016-fsm-withdrawal-guard-and-rpc-binding.md
bot_commit: 93d497d
source_sha256: b48ec7be52cbf1a3acd1535f07d00b2e2bf7cfa53a1b9c7060158bb6582d6957
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/016-fsm-withdrawal-guard-and-rpc-binding.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-016-fsm-withdrawal-guard-and-rpc-binding|ADR-016]] — Guard the EV-Fail Withdrawal Branch and Bind Solana RPC to the Execution NIC

- **Date:** 2026-09-17
- **Status:** Active
- **Context 1:** [[adr-015-fsm-cold-start-and-ev-gate|ADR-015]] wired `evCalculator.ts` into `readVenueState`, making `ev.gate_pass` reachable for the first time. `transitionMacroState`'s `MONITORING` case has an `evGateFailed` branch, named `ev_gate_failed_while_deployed`, that predates `hasActivePosition_t` and is not guarded by it. `src/decision/fsm/__tests__/macroStateMachine.test.ts` already documents this as `F42 — KNOWN GAP`: an unheld bot (`hasActivePosition_t: false`) whose EV gate fails now transitions to `DEFENSIVE_WITHDRAWAL` and emits a `WITHDRAW` intent for a position that does not exist. The withdrawal executor treats "no position on chain" as an idempotent success, so this is a spurious dispatch rather than a fault, but it is a real, newly reachable behavior that should not exist.
- **Context 2:** `createLiveAdapters` in `src/execution/adapters/liveAdapters.ts` constructs the Solana `Connection` with `httpAgent: executionAgent`, the same `https.Agent` bound to `EXECUTION_LOCAL_ADDRESS` that every other Execution-domain client shares. `@solana/web3.js`'s `fetch-impl.ts` resolves its default fetch as `globalThis.fetch` whenever it is defined — which it is, unconditionally, on Node 18+, and this repository's `engines` field requires Node ≥20. Node's native `fetch` is undici-based and does not accept a Node `http.Agent`/`https.Agent` through an `agent` property; that property is silently ignored by native fetch. `httpAgent` therefore never reaches the wire for Solana RPC traffic specifically, breaking the Dual-LAN guarantee `adapterBoundary.test.ts` and `config_contract.md`'s runtime adapter network surface both assume holds for every Execution client.
- **Decision 1:** Require `hasActivePosition_t === true` to trigger the `ev_gate_failed_while_deployed` transition in `MONITORING`. When the gate fails and `hasActivePosition_t` is `false`, the branch falls through the existing chain to `coldStartDeployable` (false, since the gate did not pass) and then to the existing `regime_safe` branch — the bot stays in `MONITORING` and waits for a passing gate, exactly as it already waits when the gate has never passed.
- **Decision 2:** Supply a `fetch` override on the `Connection` config that is *not* `globalThis.fetch`, so the `agent` property `web3.js` already computes from `httpAgent` reaches an implementation that honors it. `@solana/web3.js`'s own request path builds `options.agent` from `httpAgent` regardless of which `fetch` is active and passes it straight through (`fetch(url, options)`); only the *default* fetch — native `fetch` — ignores that member. The minimal correct fix is therefore to pass `fetch: nodeFetch` (an exact-pinned `node-fetch` default export) as `Connection`'s `fetch` config field, leaving `httpAgent: executionAgent` exactly as it is today. An `undici`-`Dispatcher`-with-`localAddress` approach is an acceptable alternative construction of the same override, provided it is bound to `config.executionLocalAddress` and added as an exact-pinned dependency per `config_contract.md` §2 if chosen instead.
- **Consequences:** An unheld bot whose gate fails no longer emits a withdrawal intent it cannot act on meaningfully; F42 changes from a documented known gap to a guarded, tested case. Solana RPC traffic is provably bound to `EXECUTION_LOCAL_ADDRESS` again, closing the one Execution client that `current.md`'s "the dual-LAN binding does not apply to Solana RPC" blocker named as exempt. The cost is one new exact-pinned runtime dependency (`node-fetch` or `undici`), which `config_contract.md` §2 requires to be added without a version range.
- **Alternatives rejected:** Leave the EV-fail branch unguarded and rely on the withdrawal executor's idempotent-no-position handling to absorb it silently — correct today, but makes a no-op dispatch that should never have been requested load-bearing behavior nobody decided on; keep `httpAgent` as the only binding mechanism and hope a future `web3.js` version honors it under native fetch — the source read for this ADR shows it does not and there is no indication that will change; drop the Dual-LAN requirement for Solana RPC specifically — contradicts the existing adapter boundary contract and test suite, which assume every Execution client is bound.
