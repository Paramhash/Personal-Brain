---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-022
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/022-range-planner-numeraire-alignment.md
bot_commit: 93d497d
source_sha256: 28983a2c1f186c0381dce87c967b66554e6da00b8570cd02c0bd08fbb4007a40
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/022-range-planner-numeraire-alignment.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-022-range-planner-numeraire-alignment|ADR-022]] — Range Planner Numeraire Alignment

- **Date:** 2026-09-19
- **Status:** Active
- **Context:** [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]] corrected EV AMM terms to use the pool's native numeraire, but the range planner's `createBinStepConversion` still maps wall prices without token-decimal scaling. When `baseDecimals !== quoteDecimals`, such as the Devnet pool's 9-decimal base and 6-decimal quote, mapping USD-denominated GEX wall strikes to Meteora bins produces a large offset, approximately 867 bins in the observed configuration. The EV gate and range planner therefore reason about different price units.
- **Decision:** `createBinStepConversion`, or the logic invoking it, must receive `baseDecimals` and `quoteDecimals` and explicitly apply the decimal conversion when mapping a wall price to a bin id. For a wall price expressed in quote tokens per whole base token, use `10^(quoteDecimals - baseDecimals)` inside the logarithm: `binId = log(price * 10^(quoteDecimals - baseDecimals)) / log(1 + binStep / 10000)`, with the existing inward floor/ceil rules. This is equivalent to applying the inverse `10^(baseDecimals - quoteDecimals)` factor when interpreting the geometric bin ratio as quote units per whole base token. The range planner and EV gate must therefore operate in the exact same pool numeraire.
- **Consequences:** GEX wall strikes map to the correct Meteora DLMM bins on asymmetric-decimal pools, so the planned deployment interval is aligned with the active-bin price used by EV calculations. The conversion remains pure, deterministic, offline-testable, and explicit about decimal metadata. Existing callers and fixtures must supply the decimal pair rather than silently assuming equal precision.
- **Alternatives rejected:** Leave the planner unscaled and rely on 9/9 test fixtures — hides the production Devnet error; apply a fixed 1,000x adjustment — works only for one decimal pair and violates pool-metadata ownership; convert walls from wallet balances — invents a price rather than correcting the unit conversion; let the deployment adapter repair bin ids — too late, and it would allow intelligence and execution to disagree about approved bounds.
