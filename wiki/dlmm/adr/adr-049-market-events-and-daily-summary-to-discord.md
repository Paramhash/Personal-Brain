---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-049
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/049-market-events-and-daily-summary-to-discord.md
bot_commit: ab766fb
source_sha256: 90e48cbe780c0e815c6b0fd1f85f6d4774c71396dbe2038054d7ac47e07f38a6
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/049-market-events-and-daily-summary-to-discord.md` at commit `ab766fb`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-049-market-events-and-daily-summary-to-discord|ADR-049]] — Market-State Events and a Daily Summary May Be Posted to the Operator's Discord

- **Date:** 2026-09-30
- **Status:** **Active. Decided by the dispatcher 2026-09-30**, with the §6 defaults accepted as written: a second
  webhook for market messages when set; the summary at 00:05Z; the hurdle line included, labelled. Implementation:
  TICKET Y.
- **Extends:** [[adr-048-health-alarms-to-the-operators-discord|ADR-048]], which permitted health alarms only and excluded market or strategy content. Owns
  `monitor.md` §9.2. Implementation: TICKET Y.

## Context

The health notifier ([[adr-048-health-alarms-to-the-operators-discord|ADR-048]]) tells the operator when something **stops**. The monitors also see things worth knowing
away from the screen: a wall moving, spot crossing the ZGL, the planner blocking, a regime change. They also show
where the day ended up. Today the only way to learn any of this is to open the page.

[[adr-048-health-alarms-to-the-operators-discord|ADR-048]] kept all market data out of messages on purpose, because a message leaving the machine is publication. This
ADR decides which market facts may go, to whom, and how often.

**What makes this low-risk.**
- The channel is the operator's own server.
- Every fact below is derived from public data: Deribit option summaries and on-chain pool state. The derived
  outputs (walls, window, hurdle) are this repository's analysis, not a secret credential.
- **There is still no position, wallet, key or order to leak.** No capital is deployed ([[adr-033-fee-yield-measurement-route|ADR-033]]'s gate is unapproved).

**What still needs care.**
- **Frequency.** The window recentres with price every 30 s, so a naive notifier would post constantly.
- **Labelling.** Unratified figures (the hurdle model, σ, the width multiple) must travel with their status, exactly as
  on the page.

## Decision

1. **Source.** The notifier reads the monitors' own `GET /api/frame` on loopback, which is the same frame the page
   draws. The DLMM monitor (7761) is the source for GEX, walls, ZGL, status and window. The Orca monitor (7762) is the
   source only for Orca-specific facts (its pool price, measured volume and derived yield). The notifier still reads no
   archive content and holds no signer.
2. **Events.** Each fires only after it has **held for 2 consecutive frames**, so a single flicker does not post:
   - **Status change** into or out of ACTIONABLE (to BLOCKED with its reason code, STALE, or PEAKS CONTESTED).
   - **A wall moving:** the call or put wall strike changes (from → to), with spot and the new distance.
   - **ZGL crossing:** spot moves to the other side of the zero-gamma level.
   - **Regime change,** for example into or out of NEGATIVE_GEX.

   **Not events:** the window recentring, and price moving within the window. Both are routine every 30 s and belong
   in the summary.
3. **Daily summary** at a fixed UTC hour (default 00:05Z, just after the health heartbeat). It covers the last 24 h
   **as the notifier observed it**:
   - spot high, low and last;
   - walls and ZGL now, and how many times each changed;
   - share of time in each status;
   - the current window (price bounds and width);
   - the modelled hurdle (**labelled UNRATIFIED model**);
   - from Orca: 24 h volume, fees and TVL (**labelled whole pool, not a position**) and the derived position yield.

   Where the notifier was down for part of the day, the summary says what share of the 24 h it observed.
4. **Rate cap:** at most **6 market messages an hour**. Beyond that, events are folded into one "N more events"
   message at the next hour. Health alarms are never capped or delayed by market messages.
5. **Content rules** carry over from [[adr-048-health-alarms-to-the-operators-discord|ADR-048]], with the allowlist widened to:
   - prices, strikes and bin or tick numbers;
   - percentages, bps/day and quote amounts;
   - fixed enum labels (status, regime, rejection reason);
   - UTC times.

   **Still never:** URLs, paths, pids, hostnames, environment values, error text, or anything about a wallet or
   position. Each unratified figure carries its label in the message.
6. **Defaults the dispatcher is asked to accept:**
   - **(a) Channel:** market messages go to a **second webhook** (`NOTIFIER_DISCORD_MARKET_WEBHOOK_URL`), if one is
     set, so alarms stay easy to see; if not set, they go to the alarm channel.
   - **(b) Summary hour:** 00:05Z (08:05 local).
   - **(c) Hurdle line:** the daily summary includes the modelled hurdle and the Orca-derived yield, both labelled.

## Consequences

- The operator learns of structural changes (walls, ZGL, regime, blocking) within about a minute, and gets one daily
  digest instead of having to check the page.
- **Recorded cost — more content leaving the machine,** all of it public-derived analysis, on the operator's own server.
- **Recorded cost — noise.** It is mitigated by 2-frame persistence, the hourly cap and excluding window moves. The
  settings can be tuned after a week of use.
- A summary built from what the notifier saw is only as complete as its uptime; it states its coverage.

## Reversed by

Sharing the server with others (content scope then needs revisiting); a live position existing (position content would
need its own decision, and wallet or position data stays excluded until then); or noise the rate cap cannot contain.
