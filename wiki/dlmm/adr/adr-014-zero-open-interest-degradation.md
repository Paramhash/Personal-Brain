---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-014
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/014-zero-open-interest-degradation.md
bot_commit: 93d497d
source_sha256: 4564e565c52ee18823f81755f7940f73a66d97d5e4290a0a2bb69707037cc2dd
exported_at: '2026-10-02T12:50:25Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/014-zero-open-interest-degradation.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-014-zero-open-interest-degradation|ADR-014]] — Zero Open Interest Is Excluded Before the Drop Counter

- **Date:** 2026-09-17
- **Status:** Active
- **Context:** `normalizeBookSummaryRows` in `src/marketdata/deribit/deribitTypes.ts` drops and counts any row whose `open_interest` is not strictly positive, on the same footing as a malformed instrument name or a non-finite spot. On the live SOL chain ([[adr-012-deribit-linear-options-usdc-settlement|ADR-012]], F-015), 227 of 580 rows (39.1%) carry exactly zero open interest and are dropped for that reason alone — every other check (wire schema, instrument grammar, underlying price, implied volatility) passes on all 580. The 39.1% drop ratio exceeds `invalidRowTolerancePct = 0.05`, so `exceedsInvalidRowTolerance` returns true and `classifyGexRegime` returns `DEGRADED` unconditionally, on every tick, regardless of the true GEX profile. An option with zero open interest is unheld, not malformed.
- **Decision:** Treat `open_interest = 0` as a valid market condition. Exclude these rows from the chain **before** the `droppedInstrumentCount_t` counter increments — the same point in the pipeline `filterSolOptionRows` already uses to exclude foreign base currencies before normalization even sees them, not a special case inside the drop-and-count loop itself. A zero-open-interest row is therefore neither counted as dropped nor carried into the normalized snapshot.
- **Consequences:** The drop ratio on the live chain falls to the share of rows genuinely unusable (malformed, non-positive underlying, or non-positive IV). `invalidRowTolerancePct` regains its diagnostic meaning: it trips on a real drop event rather than being permanently exceeded by an ordinary distribution of unheld strikes. No change is required in `gex_intelligence.md` or `gexEngine.ts`, since an excluded row never reaches the aggregation. The cost is that `instrumentCount_t` no longer reflects the venue's full listed chain, only the subset carrying open interest.
- **Alternatives rejected:** Keep zero-open-interest rows in the normalized snapshot and merely exempt them from the drop counter — leaves a zero-weight row inside `instrumentCount_t` and the aggregation for no analytical benefit; raise `invalidRowTolerancePct` above the observed ratio — blunts the detector permanently; leave the rows dropped and accept a permanently `DEGRADED` regime on the real chain — makes the strategy's core intelligence signal unusable against the venue it is built for.
