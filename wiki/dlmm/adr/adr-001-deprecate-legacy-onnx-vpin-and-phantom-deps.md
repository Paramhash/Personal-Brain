---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-001
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/001-deprecate-legacy-onnx-vpin-and-phantom-deps.md
bot_commit: 93d497d
source_sha256: 67fc1fa58d1d5943dbafd8ab372c3357041d873eda9b777383b0fc8bfca8be0c
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/001-deprecate-legacy-onnx-vpin-and-phantom-deps.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]] — Deprecate legacy ONNX/VPIN path and phantom dependencies

- **Date:** 2026-09-14
- **Status:** accepted
- **Context:** The legacy PRD and carry-over stack references still mention `@orca-so/whirlpools-sdk`, `onnxruntime-node`, `toxicity_model.onnx`, and VPIN feature engineering. The ratified architecture in F-003 and F-007 replaces that path with a delta-neutral Meteora DLMM design that uses Deribit options summaries as the intelligence source, pure TypeScript GEX analytics, Binance USDⓈ-M hedge execution, and strict runtime dependency pinning. Keeping the legacy model-era dependencies in scope creates phantom implementation paths, ambiguous agent behavior, and unnecessary package surface before code generation begins.
- **Decision:**
  - Strip `@orca-so/whirlpools-sdk` from the active design surface. `@meteora-ag/dlmm` is the sole concentrated-liquidity venue in this repository.
  - Eliminate `onnxruntime-node`, `toxicity_model.onnx`, and all VPIN or related feature-engineering pipelines from the active architecture.
  - Ratify deterministic GEX intelligence as the only approved intelligence path. The canonical implementation roots are `src/intelligence/gex/gexEngine.ts` and `src/intelligence/range/rangePlanner.ts`, consuming Deribit options summaries as specified in F-003 and F-007.
  - Enforce the pinned runtime dependency set: `@meteora-ag/dlmm`, `@solana/web3.js`, `@coral-xyz/anchor`, `ws`, and `zod`. `@project-serum/anchor` is explicitly forbidden.
  - Treat fallback ONNX runtime stubs, VPIN metric accumulators, Orca venue wrappers, and parallel venue abstractions as out of bounds for code generation unless a later ADR supersedes this one.
- **Consequences:** This removes ambiguity from project initialization, keeps the dependency graph aligned to the approved execution path, and narrows the intelligence module to deterministic analytics that can be replayed and audited. It also means no agent may reintroduce model-loading scaffolds, placeholder inference runtimes, feature stores for VPIN-style signals, or unused venue adapters as a convenience layer. Any future return of ML inference, VPIN, or Orca support requires a new ADR and an updated architecture finding.
- **Alternatives rejected:**
  - Keep `onnxruntime-node` and `toxicity_model.onnx` as dormant placeholders for a future model path.
  - Keep `@orca-so/whirlpools-sdk` installed in anticipation of a second venue.
  - Permit agents to generate compatibility wrappers or no-op stubs around retired ML and venue abstractions.
