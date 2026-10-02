---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-027
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/027-socket-stability-and-boot-validation.md
bot_commit: 93d497d
source_sha256: 2577107e195774c76fd6799de7e8d3515bdde7be31b37a2175a9c3da536aae2b
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/027-socket-stability-and-boot-validation.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-027-socket-stability-and-boot-validation|ADR-027]] — Socket Stability and Boot Validation

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** The Deribit and Binance WebSocket clients currently treat transient socket drops as terminal freshness failures rather than automatically restoring their sessions. The Deribit ticker subscription also attempts to fan out roughly 580 instrument channels at a 100ms interval, saturating the socket and contributing to disconnects. Separately, `fetchHedgeState` in the Binance REST adapter does not enforce the strict `markPrice > 0` invariant already used by the WebSocket normalizer, so a zero mark can enter the initial FSM tick and temporarily corrupt EV calculations.
- **Decision 1 (Reconnect):** Both `deribitWsClient.ts` and `binancePerpStream.ts` must automatically attempt to reconnect after `close` or `error` events, using a bounded timeout and backoff. Reconnect attempts must be single-flight, must preserve stale latches until genuinely fresh data arrives, must not create orphaned sockets or timers, and must stop cleanly on explicit disconnect.
- **Decision 2 (Bandwidth):** Disable the orchestrator's `syncTickerSubscriptions()` call for now. The GEX engine will rely on the local Black-Scholes gamma fallback from ADR-013 until a bulk-ticker endpoint or an explicitly ratified lower-bandwidth subscription strategy exists. The Deribit request/response option-chain path remains the source of normalized snapshots.
- **Decision 3 (REST Validation):** `fetchHedgeState` in `binanceRest.ts` must reject `markPrice <= 0` and return `null`, matching the WebSocket normalizer. Boot therefore fails closed until the stream supplies a valid positive mark price rather than evaluating EV from a corrupted price.
- **Consequences:** Transient venue disconnects become recoverable without operator restarts, but reconnect attempts and backoff must be observable and bounded. Native ticker coverage is temporarily sacrificed for socket stability; local gamma remains deterministic and valid. Boot and stream paths now share the same positive-price invariant, preventing zero-price EV inputs. The reconnect tests must prove no duplicate attempts, clean shutdown, and stale-until-fresh semantics.
- **Alternatives rejected:** Treat every disconnect as terminal and require a process restart — fragile during normal network churn; keep subscribing to every ticker at 100ms — reproduces socket saturation; silently accept zero mark prices until the stream corrects them — allows invalid EV state into the first tick; reconnect without single-flight or cleanup — creates duplicate sockets, timers, and subscriptions.
