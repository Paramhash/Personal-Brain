---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-005
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/005-borsh-version-resolution.md
bot_commit: 93d497d
source_sha256: 0e80e7e7c0a124b3cceee26fbc023e5194c74f10194d753a9aec0cdd76623fcb
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/005-borsh-version-resolution.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-005-borsh-version-resolution|ADR-005]] — Borsh version resolution

- **Date:** 2026-09-14
- **Status:** accepted
- **Context:** After the Anchor root pin was aligned to `0.31.0`, the dependency tree still resolves two copies of `@coral-xyz/borsh`. `@coral-xyz/anchor@0.31.0` pulls `@coral-xyz/borsh@^0.31.1` at the root, while `@meteora-ag/dlmm@1.9.14` depends on `@coral-xyz/borsh@0.31.0` exactly. This leaves two account-coder identities in the tree, which is the same class of runtime risk as the prior Anchor split.
- **Decision:** Add an npm `overrides` block to `package.json` forcing `@coral-xyz/borsh` to exactly `0.31.0`.
- **Consequences:** The manifest and lockfile must be refreshed from a clean install so the override takes effect across the tree. This removes the risk of Borsh class or decoder divergence before the operational FSM and downstream account-decoding logic are authored.
- **Alternatives rejected:**
  - Leave the root at `0.31.1` and tolerate a nested `0.31.0` copy under Meteora.
  - Attempt to paper over runtime coder mismatches in feature code.
  - Defer the fix until account decoding fails at runtime.
