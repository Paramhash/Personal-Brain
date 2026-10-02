---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-048
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/048-health-alarms-to-the-operators-discord.md
bot_commit: ab766fb
source_sha256: e8d071d2b0acc7405d517d90a65c1d27013306a17d38c3b3848e366263169f41
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/048-health-alarms-to-the-operators-discord.md` at commit `ab766fb`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-048-health-alarms-to-the-operators-discord|ADR-048]] — Health Alarms Are Pushed to the Operator's Own Discord Server by a Separate, Read-Only Notifier

- **Date:** 2026-09-30
- **Status:** **Active. Decided by the dispatcher 2026-09-30**:
  - push to a Discord server the operator owns;
  - start with health alarms.

  Market-state events and periodic summaries are **not** covered here; each needs its own decision.
- **Owns:** `docs/architect/monitor.md` §9; root `src/monitor/notify/`. Implementation: TICKET X.

## Context

**Nothing tells the operator when something stops.**
- The 2026-09-28 recorder outage lasted 105 minutes, and TICKET T's first run died unnoticed.
- The hourly `observer-health` task writes its verdict to `C:\observation\logs\health.log`, which nobody reads.
- The window check runs only when asked.
- The monitors expose `/api/health`, but only on loopback.

Everything this repository has built to *detect* a failure is in place. The missing piece is *delivery*.

The constraints:
- **The monitors are loopback-only and read-only** (`monitor.md` §2). [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]'s amendment permits exactly one outbound host (`api.orca.so`).
- **Nothing may emit an endpoint, credential, path or environment value** (`observability_contract.md` §2).
- **The archive has one writer** and no runtime readers (`observation_archive.md` §4).

A Discord webhook is a second outbound host, and a message leaving the machine is publication. So both the host and the content need a decision.

## Decision

1. **A separate notifier process** (`src/monitor/notify/`) watches and posts. It does not change the monitors, the recorder or TICKET T. It holds no signer, imports no execution or FSM code, and accepts no inbound connections.
2. **One outbound destination:** a Discord webhook on a server the operator owns.
   - **The webhook URL is a credential.** It lives only in `C:\observation\notifier.env` (key `NOTIFIER_DISCORD_WEBHOOK_URL`), which the **operator** creates.
   - It is never logged, echoed, committed or placed in a message.
   - Requests use Node's built-in `fetch`, go only to `https://discord.com/api/webhooks/…` (checked before any request), and refuse redirects.
3. **What it may observe, read-only:**
   - **The monitors' `GET /api/health`** on loopback.
   - **File metadata only** (modification time, size): of the archive's day files, TICKET T's decision files and the Orca recording's day files. **It reads no archive content**, so `observation_archive.md` §4 is untouched.
   - **The last line of `C:\observation\logs\health.log`**, the hourly `observer-health` verdict.
   - **Free space on the observation volume**, via `statfs`.
   - **Whether the pids in the known pid files are alive.**
4. **What a message may contain — an allowlist.**
   - **Allowed:**
     - the check's fixed name (for example `recorder`, `ticket-t`, `monitor-7761`, `monitor-7762`, `orca-recording`, `disk`, `observer-health`);
     - the state (`ALERT`, `RESOLVED`, `HEARTBEAT`);
     - an age in seconds or minutes;
     - counts and percentages;
     - the UTC time;
     - a fixed reason code.
   - **Never:**
     - endpoints, webhook or RPC URLs;
     - file paths, pids or hostnames;
     - environment values;
     - error messages or stack traces;
     - market data or strategy state (walls, prices, windows, hurdles). Those are out of scope for this ADR.
5. **Alert discipline.**
   - A check alerts after **2 consecutive failing evaluations** (60 s apart), not one.
   - It sends **RESOLVED** when it recovers, and repeats an unresolved alert at most once an hour.
   - A **daily heartbeat** (all checks, one line each) proves the notifier itself is alive: silence is never read as health.
   - Discord `429` responses are honoured (`retry_after`). Failed posts are retried with backoff and never block the checks.
6. **It never acts.** An alarm tells the operator; it does not stop, restart or signal anything. The existing rule stands: stop the recorder only with `observer_stop.ps1`.

## Consequences

- Failures reach the operator's phone within about two minutes. The class of outage that went unnoticed for 105 minutes on 09-28 becomes visible.
- **Recorded cost — a second outbound host and a stored credential.** The webhook URL can post to one channel. If leaked, it lets someone post there, nothing more. The operator can revoke it in Discord at any time.
- **Recorded cost — a watcher that can itself die.** The daily heartbeat is the mitigation. A missed heartbeat means the notifier is down.
- The content allowlist makes messages dull on purpose. Anything richer (walls, hurdles, summaries) is a later decision about what may leave the machine.

## Reversed by

A decision to send market-state or strategy content (it needs its own ADR); moving alerting to another channel; or a
production observability stack that supersedes this.
