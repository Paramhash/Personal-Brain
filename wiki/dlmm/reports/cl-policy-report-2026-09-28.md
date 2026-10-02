---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- report
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-09-28.md
bot_commit: 1a03346
source_sha256: 7e47c2e13c60d42db52cbfc9b4e5d10a3edb119205671a4fd4eeb7c7a59a30a4
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-09-28.md` at commit `1a03346`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# CL policy report — where to deploy, when to close and redeploy

> **Units of V; not calibrated yield ([[adr-033-fee-yield-measurement-route|ADR-033]]).** No fee volume is recorded. Fees are counted in units of `V`,
> the unknown quote volume per second through the active bin, and every policy is reported by its **break-even**:
> the volume (and the fee yield on capital) at which fees would cover its losses. A lower break-even ranks a
> policy better. **It does not show that any policy is profitable.** Produced by `src/backtest/research/`
> (blueprint `backtest_research.md`, [[adr-043-research-simulator-reads-archive-offline|ADR-043]]).

## Data

- Archive roots: C:\observation\archive, C:\observation\soak-phase2-2026-09-26
- Recon (wall) roots: C:\observation\recon-evidence-T-2026-09-27, C:\observation\recon-evidence-T2-2026-09-28 — separate runs are never joined
- Span: 2026-09-26 11:16 → 2026-09-28 14:11 UTC; 5796 usable 30 s ticks in 6 gap-free segments
- Wall-covered: 2811 ticks, 2026-09-27 11:54 → 2026-09-28 14:11 UTC
- Gaps (never bridged): 2026-09-27 13:40 → 2026-09-27 14:30 (run change); 2026-09-27 14:36 → 2026-09-27 14:36 (run change); 2026-09-27 15:51 → 2026-09-27 15:53 (run change); 2026-09-28 09:07 → 2026-09-28 10:53 (run change); 2026-09-28 11:00 → 2026-09-28 11:00 (run change)

## Parameters (UNRATIFIED placeholders unless stated)

- Capital per open: 50 SOL-equivalent. Shape: Curve (the live strategy) unless stated.
- Hedge: band 0.0625 SOL (hedge_engine.md), taker 5 bps, funding 1 bps / 8 h.
- Re-ratio slippage: 10 bps on the swapped notional. Bin-array rent: charged for every array not yet initialised in the run (worst case); see the pre-initialised table for the other bound.
- Money columns are in quote (USDC) over the whole span. **IL** = HODL − position (unhedged loss). **LVR-eq** = capital − position − short P&L (hedged loss, direction netted out).

## A. All policies, wall-covered span (ranked by hedged break-even volume)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 5m \| now | 96.0% | 97.0% | 9 | 26.08 | 0.02 | 16.07 | 148.20 | 101.61 | 128.87 | 35.91M | 25.07M | 479.95 | 335.10 |
| 2 | σ×0.5 trailing 1h \| out 0m \| now | 96.0% | 99.8% | 9 | 26.13 | 0.01 | 17.28 | 130.07 | 110.58 | 137.75 | 36.67M | 21.81M | 513.36 | 305.27 |
| 3 | σ×0.5 trailing 1h \| out 120m \| stable 20m | 91.8% | 80.8% | 5 | 26.01 | 0.01 | 6.75 | 91.41 | 83.67 | 98.35 | 36.95M | 21.36M | 395.80 | 228.84 |
| 4 | σ×0.5 trailing 1h \| recentre 4h \| now | 96.1% | 78.2% | 8 | 26.12 | 0.01 | 15.45 | 135.39 | 88.24 | 112.34 | 37.91M | 27.70M | 425.68 | 311.08 |
| 5 | σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 91.9% | 85.9% | 5 | 26.13 | 0.01 | 8.51 | 94.68 | 81.21 | 96.72 | 39.23M | 23.87M | 391.10 | 237.94 |
| 6 | σ×0.5 trailing 1h \| out 30m \| stable 20m | 91.9% | 90.9% | 5 | 26.13 | 0.01 | 8.97 | 87.84 | 87.64 | 102.91 | 39.62M | 21.59M | 415.51 | 226.39 |
| 7 | σ×0.5 trailing 1h \| out 120m \| now | 96.2% | 79.5% | 5 | 26.11 | 0.01 | 8.74 | 86.02 | 93.68 | 107.56 | 40.10M | 20.53M | 415.30 | 212.63 |
| 8 | σ×0.5 trailing 1h \| recentre 4h \| stable 20m | 88.9% | 89.9% | 7 | 35.02 | 0.01 | 13.98 | 109.12 | 67.21 | 90.50 | 40.11M | 30.68M | 392.36 | 300.14 |
| 9 | σ×0.5 trailing 1h \| recentre 12h \| now | 96.2% | 82.8% | 5 | 26.12 | 0.01 | 8.76 | 82.71 | 95.85 | 109.31 | 40.18M | 19.68M | 422.34 | 206.89 |
| 10 | σ×0.5 trailing 1h \| bot exits \| stable 20m | 93.3% | 64.2% | 4 | 26.03 | 0.00 | 6.15 | 115.89 | 70.85 | 81.95 | 40.24M | 32.21M | 333.78 | 267.19 |
| 11 | σ×0.5 trailing 1h \| recentre 24h \| stable 20m | 93.3% | 64.2% | 4 | 26.03 | 0.00 | 6.15 | 115.89 | 70.85 | 81.95 | 40.24M | 32.21M | 333.78 | 267.19 |
| 12 | σ×0.5 trailing 1h \| wall 10% \| stable 20m | 93.3% | 64.2% | 4 | 26.03 | 0.00 | 6.15 | 115.89 | 70.85 | 81.95 | 40.24M | 32.21M | 333.78 | 267.19 |
| 13 | σ×0.5 trailing 1h \| wall 15% \| stable 20m | 93.3% | 64.2% | 4 | 26.03 | 0.00 | 6.15 | 115.89 | 70.85 | 81.95 | 40.24M | 32.21M | 333.78 | 267.19 |
| 14 | σ×0.5 trailing 1h \| wall 2% \| stable 20m | 93.3% | 64.2% | 4 | 26.03 | 0.00 | 6.15 | 115.89 | 70.85 | 81.95 | 40.24M | 32.21M | 333.78 | 267.19 |
| 15 | σ×0.5 trailing 1h \| wall 5% \| stable 20m | 93.3% | 64.2% | 4 | 26.03 | 0.00 | 6.15 | 115.89 | 70.85 | 81.95 | 40.24M | 32.21M | 333.78 | 267.19 |
| 16 | σ×0.5 trailing 1h \| out 30m \| now | 96.2% | 86.3% | 5 | 26.14 | 0.01 | 8.60 | 77.39 | 96.70 | 110.57 | 40.29M | 18.67M | 425.75 | 197.27 |
| 17 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 92.2% | 87.1% | 5 | 26.06 | 0.01 | 7.13 | 84.21 | 85.66 | 100.19 | 40.53M | 21.72M | 401.58 | 215.24 |
| 18 | σ×0.5 trailing 1h \| bot exits \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 19 | σ×0.5 trailing 1h \| hold \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 20 | σ×0.5 trailing 1h \| recentre 24h \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 21 | σ×0.5 trailing 1h \| wall 10% \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 22 | σ×0.5 trailing 1h \| wall 15% \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 23 | σ×0.5 trailing 1h \| wall 2% \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 24 | σ×0.5 trailing 1h \| wall 5% \| now | 96.2% | 60.2% | 4 | 26.01 | 0.00 | 5.99 | 103.34 | 83.08 | 92.33 | 40.64M | 26.52M | 363.65 | 237.29 |
| 25 | σ×0.5 trailing 24h \| out 120m \| now | 99.8% | 84.5% | 6 | 26.21 | 0.01 | 7.92 | 77.01 | 88.98 | 107.18 | 41.53M | 20.05M | 390.01 | 188.23 |
| 26 | σ×0.5 trailing 6h \| recentre 4h \| now | 99.7% | 89.7% | 9 | 26.28 | 0.02 | 14.78 | 112.20 | 88.28 | 115.33 | 41.74M | 26.15M | 414.49 | 259.64 |
| 27 | σ×0.5 trailing 1h \| out 0m \| stable 20m | 87.3% | 99.8% | 8 | 26.27 | 0.01 | 12.97 | 118.25 | 91.51 | 115.47 | 41.91M | 26.81M | 476.21 | 304.61 |
| 28 | σ×0.5 trailing 6h \| out 120m \| now | 99.8% | 87.6% | 6 | 26.21 | 0.01 | 7.35 | 71.59 | 93.49 | 110.80 | 41.91M | 18.53M | 403.28 | 178.30 |
| 29 | σ×0.5 trailing 24h \| recentre 4h \| now | 99.7% | 91.6% | 9 | 26.28 | 0.01 | 15.20 | 117.10 | 91.16 | 118.19 | 41.93M | 26.51M | 424.91 | 268.64 |
| 30 | σ×0.5 trailing 6h \| out 0m \| now | 99.7% | 99.9% | 8 | 26.28 | 0.02 | 14.94 | 113.37 | 104.73 | 129.37 | 42.07M | 23.62M | 466.91 | 262.18 |
| 31 | σ×0.5 trailing 24h \| recentre 12h \| stable 20m | 92.2% | 92.4% | 5 | 26.13 | 0.01 | 8.66 | 87.49 | 84.95 | 99.61 | 42.48M | 23.68M | 401.86 | 224.04 |
| 32 | σ×0.5 trailing 24h \| out 30m \| now | 99.8% | 95.4% | 6 | 26.29 | 0.01 | 9.36 | 70.48 | 93.85 | 112.06 | 42.53M | 18.69M | 409.39 | 179.88 |
| 33 | σ×0.5 trailing 24h \| out 5m \| now | 99.8% | 99.0% | 6 | 26.28 | 0.01 | 9.45 | 71.59 | 104.19 | 121.87 | 42.54M | 17.44M | 444.19 | 182.09 |
| 34 | σ×0.5 trailing 24h \| out 0m \| stable 20m | 89.3% | 99.9% | 7 | 26.26 | 0.01 | 11.72 | 106.08 | 96.23 | 119.11 | 42.55M | 24.20M | 480.75 | 273.41 |
| 35 | σ×0.5 trailing 6h \| out 30m \| now | 99.8% | 94.0% | 6 | 26.26 | 0.01 | 8.30 | 66.78 | 97.29 | 114.33 | 42.55M | 17.52M | 417.56 | 171.90 |
| 36 | σ×0.5 trailing 24h \| recentre 12h \| now | 99.8% | 97.5% | 6 | 26.29 | 0.01 | 9.35 | 69.74 | 97.54 | 115.10 | 42.56M | 18.06M | 420.94 | 178.66 |
| 37 | σ×0.5 trailing 24h \| out 30m \| stable 20m | 92.2% | 97.2% | 5 | 26.14 | 0.01 | 8.83 | 77.85 | 90.85 | 105.15 | 42.56M | 20.79M | 423.48 | 206.85 |
| 38 | σ×0.5 trailing 1h \| out 5m \| stable 20m | 88.9% | 97.8% | 7 | 26.25 | 0.01 | 12.19 | 109.75 | 93.10 | 113.69 | 42.72M | 25.82M | 466.26 | 281.76 |
| 39 | σ×0.5 trailing 24h \| recentre 4h \| stable 20m | 89.3% | 89.2% | 7 | 26.11 | 0.01 | 13.88 | 109.03 | 72.91 | 94.23 | 42.83M | 30.82M | 391.44 | 281.63 |
| 40 | σ×0.5 trailing 24h \| out 0m \| now | 99.7% | 99.9% | 8 | 26.27 | 0.01 | 15.68 | 121.63 | 101.94 | 126.45 | 43.01M | 26.03M | 458.61 | 277.51 |

## B. σ-window policies, full archive span

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 24h \| out 5m \| now | 98.8% | 99.0% | 8 | 25.88 | 0.01 | 13.44 | 146.70 | 173.93 | 209.58 | 24.57M | 10.81M | 350.41 | 154.17 |
| 2 | σ×0.5 trailing 1h \| out 5m \| now | 96.7% | 98.5% | 9 | 34.65 | 0.02 | 18.25 | 196.52 | 160.47 | 197.48 | 25.54M | 15.50M | 347.48 | 210.95 |
| 3 | σ×0.5 trailing 24h \| out 30m \| now | 98.8% | 95.9% | 8 | 34.79 | 0.01 | 13.58 | 164.34 | 153.00 | 191.17 | 25.66M | 13.91M | 325.08 | 176.15 |
| 4 | σ×0.5 trailing 24h \| out 120m \| now | 98.8% | 87.7% | 8 | 25.82 | 0.01 | 12.71 | 162.32 | 142.75 | 179.63 | 25.77M | 14.34M | 299.05 | 166.43 |
| 5 | σ×0.5 trailing 6h \| out 5m \| now | 98.8% | 98.6% | 10 | 34.74 | 0.02 | 18.71 | 186.70 | 168.46 | 209.52 | 26.05M | 14.50M | 357.50 | 199.00 |
| 6 | σ×0.5 trailing 24h \| out 0m \| now | 98.8% | 99.9% | 12 | 25.88 | 0.02 | 22.90 | 184.19 | 181.71 | 221.94 | 26.20M | 13.49M | 375.05 | 193.14 |
| 7 | σ×0.5 trailing 6h \| out 30m \| now | 98.8% | 95.9% | 8 | 34.76 | 0.02 | 12.96 | 157.26 | 156.56 | 192.81 | 26.26M | 13.56M | 328.97 | 169.82 |
| 8 | σ×0.5 trailing 1h \| recentre 24h \| now | 96.8% | 72.6% | 5 | 25.78 | 0.01 | 8.57 | 167.28 | 136.13 | 156.35 | 26.49M | 16.34M | 276.50 | 170.57 |
| 9 | σ×0.5 trailing 1h \| out 120m \| now | 96.8% | 85.9% | 6 | 34.77 | 0.01 | 11.90 | 168.78 | 146.33 | 173.97 | 26.55M | 15.59M | 310.58 | 182.34 |
| 10 | σ×0.5 trailing 1h \| hold \| now | 96.8% | 68.7% | 4 | 25.78 | 0.00 | 5.88 | 133.08 | 126.41 | 143.66 | 26.82M | 14.64M | 255.44 | 139.47 |
| 11 | σ×0.5 trailing 1h \| out 30m \| now | 96.8% | 92.6% | 6 | 34.80 | 0.01 | 10.91 | 156.20 | 150.34 | 177.29 | 26.92M | 14.56M | 315.70 | 170.74 |
| 12 | σ×0.5 trailing 6h \| out 120m \| now | 98.8% | 89.6% | 8 | 34.71 | 0.02 | 12.18 | 154.87 | 147.58 | 182.98 | 26.98M | 14.42M | 312.94 | 167.28 |
| 13 | σ×0.5 trailing 6h \| out 0m \| now | 98.8% | 99.9% | 11 | 34.74 | 0.02 | 22.04 | 174.26 | 180.46 | 217.81 | 27.05M | 13.73M | 377.09 | 191.47 |
| 14 | σ×0.5 trailing 1h \| out 0m \| now | 96.7% | 99.9% | 10 | 34.69 | 0.02 | 22.94 | 181.25 | 172.77 | 206.42 | 27.07M | 14.80M | 369.36 | 201.99 |
| 15 | σ×0.5 trailing 24h \| recentre 24h \| now | 98.8% | 79.9% | 7 | 25.79 | 0.01 | 9.80 | 157.12 | 137.82 | 166.01 | 27.42M | 15.57M | 281.27 | 159.70 |
| 16 | σ×0.5 trailing 1h \| recentre 12h \| now | 96.8% | 83.4% | 7 | 25.89 | 0.01 | 11.61 | 143.73 | 150.00 | 177.50 | 27.50M | 13.65M | 309.35 | 153.60 |
| 17 | σ×0.5 trailing 24h \| hold \| now | 98.9% | 76.1% | 6 | 25.79 | 0.01 | 7.31 | 123.77 | 128.33 | 153.68 | 27.75M | 13.81M | 261.30 | 130.09 |
| 18 | σ×0.5 trailing 6h \| recentre 24h \| now | 98.8% | 78.8% | 7 | 25.79 | 0.01 | 9.40 | 155.99 | 137.80 | 165.50 | 27.76M | 15.68M | 280.50 | 158.43 |
| 19 | σ×0.5 placeholder \| out 5m \| now | 99.9% | 99.4% | 8 | 34.69 | 0.02 | 10.39 | 152.28 | 123.58 | 153.34 | 27.93M | 17.12M | 264.78 | 162.29 |
| 20 | σ×0.5 trailing 6h \| hold \| now | 98.9% | 74.9% | 6 | 25.79 | 0.01 | 7.25 | 124.37 | 129.15 | 154.17 | 27.94M | 13.91M | 262.33 | 130.54 |
| 21 | σ×0.5 trailing 24h \| recentre 12h \| now | 98.8% | 90.4% | 9 | 25.89 | 0.01 | 12.69 | 132.68 | 150.84 | 186.15 | 28.47M | 12.98M | 311.77 | 142.18 |
| 22 | σ×0.5 trailing 1h \| recentre 4h \| now | 96.7% | 80.1% | 14 | 25.89 | 0.02 | 29.62 | 215.63 | 155.47 | 200.08 | 28.59M | 18.86M | 348.24 | 229.71 |
| 23 | σ×0.5 trailing 6h \| recentre 12h \| now | 98.8% | 89.7% | 9 | 25.89 | 0.02 | 12.05 | 125.69 | 149.54 | 184.26 | 28.73M | 12.65M | 308.59 | 135.84 |
| 24 | σ×0.5 placeholder \| out 30m \| now | 99.9% | 97.7% | 8 | 34.71 | 0.02 | 11.63 | 157.65 | 113.95 | 145.84 | 29.08M | 19.38M | 251.59 | 167.65 |
| 25 | σ×1 trailing 24h \| out 0m \| now | 98.8% | 100.0% | 8 | 43.30 | 0.02 | 9.09 | 115.03 | 109.02 | 136.85 | 29.39M | 16.50M | 247.22 | 138.78 |

## C. Where to deploy — best close/redeploy rule for each placement (wall-covered span)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 5m \| now | 96.0% | 97.0% | 9 | 26.08 | 0.02 | 16.07 | 148.20 | 101.61 | 128.87 | 35.91M | 25.07M | 479.95 | 335.10 |
| 2 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 92.2% | 87.1% | 5 | 26.06 | 0.01 | 7.13 | 84.21 | 85.66 | 100.19 | 40.53M | 21.72M | 401.58 | 215.24 |
| 3 | σ×0.5 trailing 6h \| recentre 4h \| now | 99.7% | 89.7% | 9 | 26.28 | 0.02 | 14.78 | 112.20 | 88.28 | 115.33 | 41.74M | 26.15M | 414.49 | 259.64 |
| 4 | σ×0.5 placeholder \| out 5m \| now | 99.8% | 99.2% | 6 | 35.02 | 0.01 | 5.67 | 74.12 | 81.55 | 98.92 | 43.47M | 22.57M | 375.35 | 194.87 |
| 5 | σ×1 trailing 1h \| out 5m \| now | 96.2% | 99.5% | 5 | 35.08 | 0.01 | 6.35 | 65.18 | 78.91 | 92.25 | 44.55M | 22.34M | 374.09 | 187.62 |
| 6 | σ×1 trailing 24h \| out 0m \| now | 99.8% | 100.0% | 6 | 43.74 | 0.02 | 5.16 | 64.34 | 65.99 | 83.61 | 49.33M | 28.14M | 336.88 | 192.18 |
| 7 | σ×1 trailing 6h \| out 5m \| now | 99.8% | 99.6% | 6 | 43.73 | 0.02 | 4.76 | 66.44 | 65.31 | 82.58 | 50.97M | 29.84M | 333.30 | 195.08 |
| 8 | σ×1 placeholder \| recentre 12h \| now | 99.8% | 100.0% | 6 | 43.99 | 0.02 | 4.31 | 29.96 | 47.78 | 66.01 | 56.89M | 27.47M | 274.84 | 132.71 |
| 9 | σ×2 trailing 1h \| bot exits \| now | 96.2% | 100.0% | 4 | 43.72 | 0.01 | 3.67 | 52.24 | 45.73 | 56.88 | 56.94M | 37.82M | 263.03 | 174.71 |
| 10 | σ×2 trailing 24h \| bot exits \| now | 99.8% | 100.0% | 5 | 61.45 | 0.03 | 3.31 | 40.95 | 37.19 | 52.53 | 70.28M | 48.09M | 261.07 | 178.66 |
| 11 | σ×2 trailing 6h \| bot exits \| now | 99.8% | 100.0% | 5 | 61.45 | 0.03 | 3.11 | 40.65 | 36.88 | 52.21 | 71.52M | 48.98M | 259.67 | 177.82 |
| 12 | σ×2 placeholder \| recentre 12h \| now | 99.8% | 100.0% | 6 | 70.67 | 0.04 | 2.39 | 16.47 | 27.05 | 45.62 | 90.23M | 55.44M | 247.13 | 151.86 |
| 13 | walls buffered k=0.25 \| recentre 12h \| now | 99.8% | 100.0% | 6 | 115.10 | 0.09 | 0.99 | 7.26 | 11.96 | 29.29 | 220.13M | 172.60M | 266.90 | 209.27 |
| 14 | walls raw \| recentre 12h \| now | 99.8% | 100.0% | 6 | 159.37 | 0.12 | 1.11 | 5.37 | 8.80 | 25.59 | 369.08M | 314.14M | 330.58 | 281.38 |

## D. Stability — hedged break-even volume/day of the top 10, per UTC day

| policy | 2026-09-27 | 2026-09-28 |
| --- | ---: | ---: |
| σ×0.5 trailing 1h \| out 5m \| now | 29.31M | 67.29M |
| σ×0.5 trailing 1h \| out 0m \| now | 29.60M | 67.77M |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 30.55M | 51.70M |
| σ×0.5 trailing 1h \| recentre 4h \| now | 30.85M | 54.27M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 30.55M | 87.43M |
| σ×0.5 trailing 1h \| out 30m \| stable 20m | 30.55M | 60.05M |
| σ×0.5 trailing 1h \| out 120m \| now | 30.22M | 66.27M |
| σ×0.5 trailing 1h \| recentre 4h \| stable 20m | 30.85M | 68.30M |
| σ×0.5 trailing 1h \| recentre 12h \| now | 30.22M | 85.17M |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 30.55M | 87.43M |

## E. Sensitivity of the top 5 — size, rent bound, shape (hedged break-even volume/day)

| policy | 5 SOL | 50 SOL | 500 SOL | arrays pre-initialised | Spot shape (reference only) |
| --- | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| out 5m \| now | 65.71M | 35.91M | 36.94M | 32.47M | 42.30M |
| σ×0.5 trailing 1h \| out 0m \| now | 65.12M | 36.67M | 37.97M | 33.39M | 41.22M |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 75.99M | 36.95M | 36.70M | 32.47M | 42.03M |
| σ×0.5 trailing 1h \| recentre 4h \| now | 73.04M | 37.91M | 38.86M | 33.82M | 43.44M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 81.02M | 39.23M | 38.63M | 34.41M | 42.80M |

## Caveats

- **Short data.** The archive run started 2026-09-27; walls exist only where TICKET T recorded them. Trust a ranking only once it holds across UTC days and [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-windows.
- **Only the sampled active bin earns.** A 30 s interval that crossed several bins earned in each; this credits one.
- **Pool liquidity is the latest 5-minute snapshot**, and the position dilutes only through its share of the active bin.
- **No measured volume, funding or taker series.** Those costs are placeholders; the fee side is in units of V.
- **Shape weights follow the Meteora SDK as value shares at open**, not its exact per-side token amounts.
- **The σ-window placement is unclamped by walls** (the pure [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] policy); the live planner also clamps to the buffered envelope, which does not bind at today's σ.
