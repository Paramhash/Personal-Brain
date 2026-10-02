---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-006
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/006-test-runner-authorization.md
bot_commit: 93d497d
source_sha256: 67c8445ec9dc8b16a067d1e3ea49f79207a3db78a5a13877594fb8de28d93907
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/006-test-runner-authorization.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-006-test-runner-authorization|ADR-006]] — Test runner authorization

- **Date:** 2026-09-15
- **Status:** accepted
- **Context:** The hierarchical FSM work has already produced a substantial offline behavioral test suite, but those tests are not committed because the pinned dependency set does not yet include a test runner. The FSM logic is intentionally pure and deterministic, so it is testable without venue connections; leaving the suite uncommitted increases the risk that future execution-layer work changes transition behavior without preserving the verified state graph.
- **Decision:** Authorize `jest`, `ts-jest`, and `@types/jest` as exact-pinned `devDependencies` for offline deterministic unit testing.
- **Consequences:** The FSM test suites can now be committed under the source tree and run without network access, which preserves transition correctness as execution actuators are added. The manifest grows, but only in dev tooling; no production runtime dependency is added.
- **Alternatives rejected:**
  - Keep the tests uncommitted and rely on ad hoc local harnesses.
  - Delay test-runner authorization until after execution modules are written.
  - Introduce a runner that requires live venue connectivity to validate reducer behavior.
