---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-003
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/003-anchor-version-resolution.md
bot_commit: 93d497d
source_sha256: f92c18ce6ec4a1b21d86a365ff67acbc524e8ea1153e463cc10ab4a7cf531835
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/003-anchor-version-resolution.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-003-anchor-version-resolution|ADR-003]] — Anchor version resolution

- **Date:** 2026-09-14
- **Status:** accepted
- **Context:** The repository currently pins `@coral-xyz/anchor` to `0.32.1` at the root while `@meteora-ag/dlmm` requires `0.31.0`. npm therefore resolves a second nested Anchor copy under the Meteora dependency tree. In a Solana TypeScript codebase this is not a cosmetic duplication: dual Anchor versions create incompatible `BN`, coder, and program class identities across package boundaries, which commonly surfaces as `instanceof` mismatches and account-decoding failures at runtime.
- **Decision:** Downgrade the root repository pin for `@coral-xyz/anchor` to exactly `0.31.0` so it matches the Meteora DLMM SDK requirement and collapses the dependency tree onto a single Anchor version.
- **Consequences:** `package.json` and `package-lock.json` must be updated, and the install must be rerun so npm can collapse the tree. This reduces the risk of cross-boundary Anchor object incompatibility before any FSM or execution code is written. Future upgrades of Anchor now require explicit verification against the Meteora SDK requirement rather than independent version movement at the root.
- **Alternatives rejected:**
  - Keep the root pin at `0.32.1` and tolerate a nested `0.31.0` copy.
  - Use runtime workarounds around `BN` or coder identity mismatches.
  - Force a mismatched override upward without matching the SDK's declared version.
