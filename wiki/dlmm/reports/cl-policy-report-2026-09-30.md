---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- report
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-09-30.md
bot_commit: ab766fb
source_sha256: 41f52c7b695eaa66f90c672223e242a13f1cefa4af98b97acf1a0a5a280ce3c6
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-09-30.md` at commit `ab766fb`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# CL policy report — where to deploy, when to close and redeploy

> **Units of V; not calibrated yield ([[adr-033-fee-yield-measurement-route|ADR-033]]).** No fee volume is recorded. Fees are counted in units of `V`,
> the unknown quote volume per second through the active bin, and every policy is reported by its **break-even**:
> the volume (and the fee yield on capital) at which fees would cover its losses. A lower break-even ranks a
> policy better. **It does not show that any policy is profitable.** Produced by `src/backtest/research/`
> (blueprint `backtest_research.md`, [[adr-043-research-simulator-reads-archive-offline|ADR-043]]).

## Data

- Archive roots: C:\observation\archive, C:\observation\soak-phase2-2026-09-26
- Recon (wall) roots: C:\observation\recon-evidence-T-2026-09-27, C:\observation\recon-evidence-T2-2026-09-28 — separate runs are never joined
- Span: 2026-09-26 11:16 → 2026-09-30 14:32 UTC; 11597 usable 30 s ticks in 6 gap-free segments
- Wall-covered: 8609 ticks, 2026-09-27 11:54 → 2026-09-30 14:32 UTC
- Gaps (never bridged): 2026-09-27 13:40 → 2026-09-27 14:30 (run change); 2026-09-27 14:36 → 2026-09-27 14:36 (run change); 2026-09-27 15:51 → 2026-09-27 15:53 (run change); 2026-09-28 09:07 → 2026-09-28 10:53 (run change); 2026-09-28 11:00 → 2026-09-28 11:00 (run change)

## Parameters (UNRATIFIED placeholders unless stated)

- Capital per open: 50 SOL-equivalent. Shape: Curve (the live strategy) unless stated.
- Hedge: band 0.0625 SOL (hedge_engine.md), taker 5 bps, funding 1 bps / 8 h.
- Re-ratio slippage: 10 bps on the swapped notional. Bin-array rent: charged for every array not yet initialised in the run (worst case); see the pre-initialised table for the other bound.
- Money columns are in quote (USDC) over the whole span. **IL** = HODL − position (unhedged loss). **LVR-eq** = capital − position − short P&L (hedged loss, direction netted out).

## A. All policies, wall-covered span (ranked by hedged break-even volume)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 120m \| stable 20m | 94.2% | 82.9% | 8 | 34.59 | 0.02 | 14.45 | 203.70 | 278.69 | 296.51 | 38.39M | 15.54M | 370.77 | 150.12 |
| 2 | σ×0.5 trailing 1h \| wall 10% \| stable 20m | 94.9% | 77.4% | 7 | 34.61 | 0.01 | 13.84 | 230.69 | 265.87 | 280.11 | 39.51M | 18.55M | 349.90 | 164.31 |
| 3 | σ×0.5 trailing 1h \| wall 2% \| stable 20m | 94.9% | 77.4% | 7 | 34.61 | 0.01 | 13.84 | 230.69 | 265.87 | 280.11 | 39.51M | 18.55M | 349.90 | 164.31 |
| 4 | σ×0.5 trailing 1h \| wall 5% \| stable 20m | 94.9% | 77.4% | 7 | 34.61 | 0.01 | 13.84 | 230.69 | 265.87 | 280.11 | 39.51M | 18.55M | 349.90 | 164.31 |
| 5 | σ×0.5 trailing 1h \| bot exits \| stable 20m | 92.7% | 81.0% | 8 | 34.61 | 0.01 | 16.71 | 199.89 | 279.67 | 296.06 | 39.71M | 15.91M | 377.55 | 151.26 |
| 6 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 94.5% | 93.2% | 8 | 26.06 | 0.02 | 15.54 | 205.78 | 267.77 | 286.46 | 39.90M | 16.57M | 352.54 | 146.37 |
| 7 | σ×0.5 trailing 1h \| recentre 24h \| stable 20m | 94.4% | 79.4% | 8 | 34.61 | 0.01 | 16.35 | 208.23 | 273.04 | 288.69 | 39.93M | 16.89M | 362.33 | 153.29 |
| 8 | σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 92.7% | 89.0% | 11 | 34.71 | 0.02 | 19.93 | 170.71 | 281.83 | 306.45 | 40.36M | 14.15M | 387.48 | 135.82 |
| 9 | σ×0.5 trailing 1h \| out 30m \| stable 20m | 91.9% | 91.7% | 9 | 34.49 | 0.02 | 19.55 | 222.61 | 279.48 | 298.96 | 40.43M | 17.68M | 385.78 | 168.75 |
| 10 | σ×0.5 trailing 1h \| out 120m \| now | 98.7% | 79.5% | 10 | 26.11 | 0.02 | 20.38 | 306.17 | 268.16 | 292.18 | 40.54M | 23.56M | 344.60 | 200.27 |
| 11 | σ×0.5 trailing 24h \| out 30m \| stable 20m | 94.0% | 97.0% | 8 | 26.14 | 0.02 | 17.23 | 199.42 | 272.97 | 291.42 | 40.64M | 16.24M | 361.80 | 144.54 |
| 12 | σ×0.5 trailing 6h \| out 120m \| stable 20m | 94.5% | 92.4% | 8 | 43.51 | 0.02 | 14.29 | 200.91 | 277.00 | 295.72 | 40.78M | 16.73M | 373.16 | 153.12 |
| 13 | σ×0.5 trailing 6h \| out 30m \| stable 20m | 93.5% | 96.7% | 8 | 35.18 | 0.02 | 16.24 | 186.75 | 281.43 | 300.78 | 40.86M | 15.36M | 378.92 | 142.44 |
| 14 | σ×0.5 trailing 1h \| out 5m \| now | 98.6% | 98.2% | 17 | 34.43 | 0.03 | 34.98 | 382.80 | 298.13 | 345.72 | 40.90M | 25.93M | 404.24 | 256.30 |
| 15 | σ×0.5 trailing 24h \| wall 10% \| stable 20m | 95.0% | 87.9% | 7 | 26.03 | 0.01 | 14.44 | 227.80 | 256.32 | 270.61 | 40.94M | 19.36M | 333.53 | 157.70 |
| 16 | σ×0.5 trailing 24h \| wall 2% \| stable 20m | 95.0% | 87.9% | 7 | 26.03 | 0.01 | 14.44 | 227.80 | 256.32 | 270.61 | 40.94M | 19.36M | 333.53 | 157.70 |
| 17 | σ×0.5 trailing 24h \| wall 5% \| stable 20m | 95.0% | 87.9% | 7 | 26.03 | 0.01 | 14.44 | 227.80 | 256.32 | 270.61 | 40.94M | 19.36M | 333.53 | 157.70 |
| 18 | σ×0.5 trailing 6h \| wall 10% \| stable 20m | 95.0% | 87.0% | 7 | 35.08 | 0.02 | 13.86 | 225.40 | 266.70 | 282.02 | 41.24M | 18.93M | 351.32 | 161.27 |
| 19 | σ×0.5 trailing 6h \| wall 2% \| stable 20m | 95.0% | 87.0% | 7 | 35.08 | 0.02 | 13.86 | 225.40 | 266.70 | 282.02 | 41.24M | 18.93M | 351.32 | 161.27 |
| 20 | σ×0.5 trailing 6h \| wall 5% \| stable 20m | 95.0% | 87.0% | 7 | 35.08 | 0.02 | 13.86 | 225.40 | 266.70 | 282.02 | 41.24M | 18.93M | 351.32 | 161.27 |
| 21 | σ×0.5 trailing 24h \| recentre 24h \| stable 20m | 94.5% | 89.5% | 8 | 26.03 | 0.02 | 15.67 | 202.65 | 262.46 | 278.84 | 41.44M | 17.37M | 344.35 | 144.33 |
| 22 | σ×0.5 trailing 24h \| bot exits \| stable 20m | 92.8% | 89.9% | 8 | 26.03 | 0.02 | 16.09 | 193.42 | 262.93 | 279.05 | 41.50M | 16.73M | 351.21 | 141.63 |
| 23 | σ×0.5 trailing 6h \| recentre 24h \| stable 20m | 94.5% | 88.1% | 8 | 35.08 | 0.02 | 15.65 | 205.15 | 272.83 | 289.78 | 41.66M | 17.38M | 362.27 | 151.14 |
| 24 | σ×0.5 trailing 6h \| bot exits \| stable 20m | 92.8% | 89.2% | 8 | 35.08 | 0.02 | 15.92 | 193.95 | 275.55 | 292.74 | 41.66M | 16.48M | 372.36 | 147.29 |
| 25 | σ×0.5 trailing 24h \| recentre 12h \| stable 20m | 92.8% | 96.6% | 11 | 26.13 | 0.02 | 19.38 | 178.65 | 272.30 | 298.16 | 41.75M | 15.20M | 370.77 | 134.94 |
| 26 | σ×0.5 trailing 6h \| recentre 12h \| stable 20m | 92.8% | 93.7% | 11 | 35.18 | 0.02 | 19.81 | 176.12 | 283.11 | 309.98 | 41.81M | 14.91M | 390.09 | 139.12 |
| 27 | σ×0.5 trailing 6h \| out 120m \| now | 99.9% | 89.4% | 10 | 26.21 | 0.02 | 19.08 | 298.38 | 260.84 | 285.90 | 41.81M | 24.27M | 332.06 | 192.77 |
| 28 | σ×0.5 trailing 1h \| out 0m \| stable 20m | 89.1% | 99.9% | 13 | 34.60 | 0.03 | 26.70 | 280.47 | 265.95 | 300.83 | 41.91M | 22.81M | 394.02 | 214.41 |
| 29 | σ×0.5 trailing 24h \| out 120m \| now | 99.9% | 86.7% | 10 | 26.21 | 0.02 | 19.89 | 317.08 | 245.44 | 271.10 | 41.96M | 27.08M | 315.58 | 203.71 |
| 30 | σ×0.5 trailing 6h \| out 30m \| now | 99.9% | 94.7% | 12 | 26.26 | 0.03 | 21.30 | 255.16 | 298.61 | 331.87 | 42.12M | 18.80M | 379.92 | 169.63 |
| 31 | σ×0.5 placeholder \| out 30m \| stable 20m | 94.5% | 97.8% | 8 | 35.12 | 0.02 | 14.50 | 185.56 | 234.80 | 251.70 | 42.19M | 18.51M | 317.13 | 139.13 |
| 32 | σ×0.5 trailing 1h \| out 5m \| stable 20m | 90.5% | 98.3% | 12 | 34.61 | 0.02 | 25.84 | 271.23 | 276.87 | 307.66 | 42.27M | 21.74M | 398.19 | 204.78 |
| 33 | σ×0.5 trailing 24h \| out 30m \| now | 99.9% | 95.4% | 12 | 26.29 | 0.02 | 22.56 | 277.71 | 279.34 | 313.30 | 42.37M | 21.57M | 359.71 | 183.12 |
| 34 | σ×0.5 placeholder \| out 120m \| stable 20m | 94.5% | 95.6% | 8 | 35.07 | 0.02 | 13.35 | 194.47 | 231.14 | 247.73 | 42.41M | 19.53M | 311.78 | 143.62 |
| 35 | σ×0.5 trailing 1h \| out 0m \| now | 98.6% | 99.9% | 17 | 34.47 | 0.03 | 35.74 | 342.64 | 297.67 | 341.43 | 42.42M | 24.69M | 401.24 | 233.54 |
| 36 | σ×0.5 placeholder \| out 5m \| stable 20m | 93.4% | 99.5% | 8 | 35.19 | 0.02 | 15.71 | 187.87 | 236.51 | 253.59 | 42.65M | 18.83M | 323.71 | 142.88 |
| 37 | σ×0.5 placeholder \| out 0m \| stable 20m | 93.0% | 100.0% | 8 | 35.19 | 0.02 | 15.69 | 182.50 | 235.69 | 253.04 | 42.67M | 18.46M | 324.57 | 140.38 |
| 38 | σ×0.5 trailing 1h \| recentre 12h \| now | 98.7% | 71.2% | 11 | 26.12 | 0.02 | 22.99 | 224.65 | 288.07 | 306.38 | 42.74M | 18.18M | 363.51 | 154.64 |
| 39 | σ×0.5 trailing 24h \| out 5m \| stable 20m | 91.2% | 98.7% | 10 | 34.50 | 0.02 | 22.96 | 237.83 | 276.64 | 299.90 | 42.87M | 19.97M | 388.63 | 181.02 |
| 40 | σ×0.5 trailing 1h \| out 30m \| now | 98.7% | 90.0% | 11 | 34.51 | 0.02 | 22.90 | 297.01 | 283.95 | 306.37 | 43.13M | 23.60M | 368.14 | 201.44 |

## B. σ-window policies, full archive span

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 24h \| out 120m \| now | 99.4% | 89.8% | 8 | 25.82 | 0.01 | 12.71 | 155.70 | 317.76 | 356.36 | 30.08M | 8.20M | 296.77 | 80.89 |
| 2 | σ×0.5 trailing 1h \| out 120m \| now | 98.4% | 79.4% | 8 | 34.77 | 0.01 | 18.03 | 276.89 | 306.01 | 338.97 | 30.70M | 14.51M | 293.86 | 138.84 |
| 3 | σ×0.5 trailing 1h \| hold \| now | 98.4% | 72.5% | 4 | 25.78 | 0.00 | 5.88 | 122.06 | 322.97 | 346.45 | 30.82M | 6.76M | 295.23 | 64.73 |
| 4 | σ×0.5 trailing 6h \| out 120m \| now | 99.4% | 91.2% | 8 | 34.71 | 0.02 | 12.18 | 148.59 | 318.70 | 354.86 | 30.84M | 8.37M | 300.11 | 81.44 |
| 5 | σ×0.5 trailing 24h \| out 30m \| now | 99.4% | 95.4% | 11 | 34.79 | 0.02 | 22.57 | 376.83 | 341.54 | 386.53 | 31.30M | 17.30M | 326.73 | 180.62 |
| 6 | σ×0.5 trailing 24h \| out 5m \| now | 99.4% | 98.9% | 12 | 34.22 | 0.02 | 25.50 | 306.26 | 376.64 | 414.86 | 31.33M | 13.47M | 354.34 | 152.35 |
| 7 | σ×0.5 trailing 24h \| hold \| now | 99.4% | 84.0% | 6 | 25.79 | 0.01 | 7.31 | 117.15 | 303.34 | 330.41 | 31.68M | 7.14M | 277.81 | 62.60 |
| 8 | σ×0.5 trailing 6h \| out 30m \| now | 99.4% | 95.7% | 11 | 34.76 | 0.02 | 21.91 | 386.86 | 343.48 | 386.15 | 31.84M | 17.96M | 327.26 | 184.60 |
| 9 | σ×0.5 trailing 6h \| hold \| now | 99.4% | 83.9% | 6 | 25.79 | 0.01 | 7.25 | 118.10 | 300.27 | 326.04 | 31.87M | 7.31M | 274.69 | 62.97 |
| 10 | σ×0.5 trailing 1h \| out 5m \| now | 98.3% | 98.6% | 14 | 42.99 | 0.03 | 33.16 | 426.73 | 358.64 | 406.59 | 32.43M | 19.38M | 353.54 | 211.31 |
| 11 | σ×0.5 trailing 1h \| recentre 24h \| now | 98.4% | 74.4% | 7 | 25.78 | 0.01 | 12.44 | 170.38 | 372.08 | 391.02 | 32.63M | 8.49M | 336.70 | 87.65 |
| 12 | σ×0.5 trailing 1h \| recentre 12h \| now | 98.4% | 81.6% | 11 | 25.89 | 0.01 | 15.08 | 140.09 | 369.68 | 402.76 | 32.76M | 7.29M | 342.07 | 76.15 |
| 13 | σ×0.5 trailing 24h \| recentre 24h \| now | 99.4% | 88.5% | 9 | 25.79 | 0.02 | 11.78 | 160.02 | 332.12 | 358.72 | 33.09M | 8.98M | 302.81 | 82.14 |
| 14 | σ×0.5 trailing 6h \| recentre 24h \| now | 99.4% | 86.3% | 9 | 25.79 | 0.02 | 11.39 | 159.01 | 341.47 | 369.59 | 33.29M | 8.73M | 311.06 | 81.56 |
| 15 | σ×0.5 trailing 24h \| out 0m \| now | 99.3% | 99.9% | 18 | 25.88 | 0.03 | 41.22 | 388.28 | 392.84 | 436.47 | 33.40M | 16.97M | 373.51 | 189.75 |
| 16 | σ×0.5 trailing 1h \| out 30m \| now | 98.4% | 91.7% | 10 | 43.17 | 0.02 | 22.85 | 420.09 | 334.40 | 365.41 | 33.43M | 21.22M | 322.67 | 204.82 |
| 17 | σ×1 trailing 24h \| out 5m \| now | 99.4% | 99.6% | 8 | 43.31 | 0.02 | 9.31 | 128.42 | 232.24 | 256.70 | 33.44M | 11.18M | 225.54 | 75.40 |
| 18 | σ×0.5 placeholder \| out 30m \| now | 99.9% | 97.5% | 9 | 34.71 | 0.02 | 14.75 | 281.29 | 278.89 | 310.51 | 33.47M | 17.33M | 264.85 | 137.12 |
| 19 | σ×0.5 trailing 6h \| out 5m \| now | 99.3% | 98.6% | 16 | 43.06 | 0.03 | 36.48 | 420.05 | 379.95 | 428.47 | 33.49M | 18.84M | 370.09 | 208.23 |
| 20 | σ×0.5 trailing 24h \| recentre 12h \| now | 99.4% | 94.2% | 13 | 25.89 | 0.02 | 16.27 | 137.08 | 349.57 | 389.94 | 33.85M | 7.76M | 325.41 | 74.63 |
| 21 | σ×1 trailing 24h \| out 0m \| now | 99.4% | 100.0% | 9 | 43.30 | 0.03 | 12.18 | 223.56 | 240.25 | 265.67 | 33.87M | 16.83M | 233.73 | 116.18 |
| 22 | σ×0.5 trailing 6h \| recentre 12h \| now | 99.4% | 92.1% | 13 | 25.89 | 0.02 | 16.10 | 131.36 | 352.71 | 394.80 | 33.88M | 7.44M | 328.68 | 72.18 |
| 23 | σ×1 trailing 24h \| out 30m \| now | 99.4% | 98.5% | 8 | 43.30 | 0.02 | 9.29 | 129.68 | 227.02 | 252.27 | 33.95M | 11.64M | 221.39 | 75.88 |
| 24 | σ×0.5 trailing 1h \| out 0m \| now | 98.3% | 99.9% | 16 | 43.03 | 0.03 | 41.24 | 414.08 | 354.91 | 397.50 | 33.99M | 20.25M | 350.99 | 209.06 |
| 25 | σ×1 trailing 1h \| hold \| now | 98.4% | 89.7% | 4 | 25.97 | 0.01 | 5.39 | 97.30 | 259.95 | 272.86 | 34.13M | 7.78M | 237.57 | 54.18 |

## C. Where to deploy — best close/redeploy rule for each placement (wall-covered span)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 120m \| stable 20m | 94.2% | 82.9% | 8 | 34.59 | 0.02 | 14.45 | 203.70 | 278.69 | 296.51 | 38.39M | 15.54M | 370.77 | 150.12 |
| 2 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 94.5% | 93.2% | 8 | 26.06 | 0.02 | 15.54 | 205.78 | 267.77 | 286.46 | 39.90M | 16.57M | 352.54 | 146.37 |
| 3 | σ×0.5 trailing 6h \| out 120m \| stable 20m | 94.5% | 92.4% | 8 | 43.51 | 0.02 | 14.29 | 200.91 | 277.00 | 295.72 | 40.78M | 16.73M | 373.16 | 153.12 |
| 4 | σ×0.5 placeholder \| out 30m \| stable 20m | 94.5% | 97.8% | 8 | 35.12 | 0.02 | 14.50 | 185.56 | 234.80 | 251.70 | 42.19M | 18.51M | 317.13 | 139.13 |
| 5 | σ×1 trailing 1h \| out 0m \| stable 20m | 92.8% | 100.0% | 8 | 60.99 | 0.03 | 12.69 | 162.41 | 207.60 | 223.89 | 44.65M | 20.87M | 304.37 | 142.26 |
| 6 | σ×1 trailing 6h \| out 0m \| stable 20m | 94.5% | 100.0% | 8 | 43.81 | 0.03 | 11.98 | 155.13 | 187.42 | 204.25 | 45.29M | 21.35M | 264.69 | 124.78 |
| 7 | σ×1 trailing 24h \| out 0m \| stable 20m | 94.5% | 100.0% | 8 | 43.81 | 0.03 | 12.39 | 153.96 | 180.45 | 197.19 | 45.58M | 22.08M | 256.63 | 124.33 |
| 8 | σ×1 placeholder \| out 0m \| stable 20m | 95.0% | 100.0% | 7 | 43.78 | 0.03 | 9.45 | 125.74 | 142.15 | 156.93 | 48.51M | 24.64M | 207.11 | 105.22 |
| 9 | σ×2 trailing 6h \| out 0m \| stable 20m | 95.0% | 100.0% | 7 | 61.52 | 0.04 | 7.43 | 97.94 | 110.02 | 127.05 | 54.10M | 29.51M | 179.90 | 98.13 |
| 10 | σ×2 trailing 24h \| out 0m \| stable 20m | 95.0% | 100.0% | 7 | 61.52 | 0.04 | 7.32 | 93.76 | 102.98 | 120.00 | 55.39M | 30.87M | 171.56 | 95.60 |
| 11 | σ×2 trailing 1h \| hold \| now | 98.7% | 100.0% | 7 | 95.59 | 0.04 | 7.64 | 89.36 | 140.33 | 154.55 | 56.04M | 27.11M | 224.20 | 108.47 |
| 12 | σ×2 placeholder \| hold \| now | 99.9% | 100.0% | 8 | 70.67 | 0.06 | 4.88 | 55.12 | 86.47 | 107.54 | 63.26M | 30.67M | 149.97 | 72.72 |
| 13 | walls buffered k=0.25 \| out 0m \| stable 20m | 95.0% | 100.0% | 7 | 115.33 | 0.10 | 2.77 | 34.83 | 39.91 | 60.36 | 108.16M | 75.76M | 128.42 | 89.95 |
| 14 | walls raw \| recentre 12h \| now | 99.9% | 100.0% | 12 | 159.37 | 0.23 | 2.63 | 22.53 | 33.11 | 67.95 | 161.00M | 112.97M | 146.90 | 103.08 |

## D. Stability — hedged break-even volume/day of the top 10, per UTC day

| policy | 2026-09-27 | 2026-09-28 | 2026-09-29 | 2026-09-30 |
| --- | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 30.55M | 44.74M | 41.78M | 51.81M |
| σ×0.5 trailing 1h \| wall 10% \| stable 20m | 30.55M | 50.40M | 36.34M | 51.81M |
| σ×0.5 trailing 1h \| wall 2% \| stable 20m | 30.55M | 50.40M | 36.34M | 51.81M |
| σ×0.5 trailing 1h \| wall 5% \| stable 20m | 30.55M | 50.40M | 36.34M | 51.81M |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 30.55M | 50.40M | 37.83M | 51.81M |
| σ×0.5 trailing 24h \| out 120m \| stable 20m | 32.18M | 53.87M | 37.84M | 55.41M |
| σ×0.5 trailing 1h \| recentre 24h \| stable 20m | 30.55M | 50.40M | 36.34M | 51.81M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 30.55M | 52.70M | 36.34M | 51.70M |
| σ×0.5 trailing 1h \| out 30m \| stable 20m | 30.55M | 47.69M | 42.29M | 51.81M |
| σ×0.5 trailing 1h \| out 120m \| now | 30.22M | 49.99M | 43.50M | 52.00M |

## E. Sensitivity of the top 5 — size, rent bound, shape (hedged break-even volume/day)

| policy | 5 SOL | 50 SOL | 500 SOL | arrays pre-initialised | Spot shape (reference only) |
| --- | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 56.57M | 38.39M | 40.03M | 36.26M | 40.44M |
| σ×0.5 trailing 1h \| wall 10% \| stable 20m | 59.22M | 39.51M | 41.08M | 37.21M | 41.31M |
| σ×0.5 trailing 1h \| wall 2% \| stable 20m | 59.22M | 39.51M | 41.08M | 37.21M | 41.31M |
| σ×0.5 trailing 1h \| wall 5% \| stable 20m | 59.22M | 39.51M | 41.08M | 37.21M | 41.31M |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 58.41M | 39.71M | 41.41M | 37.52M | 42.24M |

## F. [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model vs simulator — LVR and hedge-taker cost, bps of capital per day (UNRATIFIED model; evidence for ratification)

> Each open evaluates the model for its own range, σ (trailing 24 h at the open) and capital; its rates accrue over
> the same deployed seconds the simulator accounts exactly. "LVR-eq sim" is the hedged loss (market direction netted
> out); "hedge taker sim" is the discrete hedge's taker cost. Lifespan compares the model's expected first exit
> (plus the out-of-range delay, capped by re-centre) with observed episodes — which a segment end can cut short.

| policy | LVR-eq sim | LVR model | model/sim | hedge taker sim | hedge model | model/sim | life sim (d) | life model (d) | closes compared |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 placeholder \| hold \| now | 104.55 | 248.48 | 2.38 | 111.60 | 313.24 | 2.81 | — | — | 0 |
| σ×0.5 placeholder \| out 0m \| now | 131.10 | 246.88 | 1.88 | 139.50 | 312.13 | 2.24 | 0.366 | 0.468 | 11 |
| σ×0.5 placeholder \| out 5m \| now | 125.56 | 251.89 | 2.01 | 136.80 | 315.27 | 2.30 | 0.366 | 0.474 | 11 |
| σ×0.5 placeholder \| out 30m \| now | 115.62 | 238.20 | 2.06 | 127.45 | 306.62 | 2.41 | 0.447 | 0.510 | 9 |
| σ×0.5 placeholder \| out 120m \| now | 108.73 | 239.30 | 2.20 | 119.41 | 307.26 | 2.57 | 0.503 | 0.588 | 8 |
| σ×0.5 placeholder \| recentre 4h \| now | 115.48 | 205.73 | 1.78 | 147.37 | 283.20 | 1.92 | 0.143 | 0.167 | 28 |
| σ×0.5 placeholder \| recentre 12h \| now | 121.44 | 232.70 | 1.92 | 134.01 | 301.64 | 2.25 | 0.309 | 0.500 | 13 |
| σ×0.5 placeholder \| recentre 24h \| now | 114.76 | 255.18 | 2.22 | 122.81 | 317.33 | 2.58 | 0.447 | 1.000 | 9 |
| σ×0.5 trailing 1h \| hold \| now | 136.00 | 403.34 | 2.97 | 144.74 | 571.76 | 3.95 | — | — | 0 |
| σ×0.5 trailing 1h \| out 0m \| now | 148.88 | 254.89 | 1.71 | 165.01 | 353.55 | 2.14 | 0.247 | 0.422 | 16 |
| σ×0.5 trailing 1h \| out 5m \| now | 150.69 | 258.44 | 1.72 | 169.32 | 367.79 | 2.17 | 0.283 | 0.373 | 14 |
| σ×0.5 trailing 1h \| out 30m \| now | 140.89 | 276.78 | 1.96 | 152.68 | 391.15 | 2.56 | 0.396 | 0.445 | 10 |
| σ×0.5 trailing 1h \| out 120m \| now | 128.87 | 351.41 | 2.73 | 141.54 | 506.24 | 3.58 | 0.495 | 0.285 | 8 |
| σ×0.5 trailing 1h \| recentre 4h \| now | 155.42 | 348.41 | 2.24 | 188.36 | 500.44 | 2.66 | 0.152 | 0.167 | 26 |
| σ×0.5 trailing 1h \| recentre 12h \| now | 155.46 | 409.12 | 2.63 | 167.89 | 550.65 | 3.28 | 0.360 | 0.500 | 11 |
| σ×0.5 trailing 1h \| recentre 24h \| now | 156.34 | 425.64 | 2.72 | 162.82 | 590.45 | 3.63 | 0.566 | 1.000 | 7 |
| σ×0.5 trailing 6h \| hold \| now | 125.09 | 244.22 | 1.95 | 134.54 | 373.88 | 2.78 | — | — | 0 |
| σ×0.5 trailing 6h \| out 0m \| now | 170.06 | 262.64 | 1.54 | 190.16 | 384.33 | 2.02 | 0.200 | 0.276 | 20 |
| σ×0.5 trailing 6h \| out 5m \| now | 158.35 | 274.02 | 1.73 | 177.28 | 388.43 | 2.19 | 0.250 | 0.284 | 16 |
| σ×0.5 trailing 6h \| out 30m \| now | 142.95 | 254.35 | 1.78 | 159.29 | 372.19 | 2.34 | 0.364 | 0.322 | 11 |
| σ×0.5 trailing 6h \| out 120m \| now | 132.76 | 243.03 | 1.83 | 146.48 | 367.69 | 2.51 | 0.500 | 0.397 | 8 |
| σ×0.5 trailing 6h \| recentre 4h \| now | 134.72 | 272.47 | 2.02 | 167.46 | 398.17 | 2.38 | 0.143 | 0.167 | 28 |
| σ×0.5 trailing 6h \| recentre 12h \| now | 146.83 | 284.12 | 1.93 | 162.89 | 406.39 | 2.49 | 0.308 | 0.500 | 13 |
| σ×0.5 trailing 6h \| recentre 24h \| now | 141.95 | 291.88 | 2.06 | 152.10 | 422.27 | 2.78 | 0.445 | 1.000 | 9 |
| σ×0.5 trailing 24h \| hold \| now | 126.37 | 250.88 | 1.99 | 136.37 | 382.18 | 2.80 | — | — | 0 |
| σ×0.5 trailing 24h \| out 0m \| now | 163.68 | 277.47 | 1.70 | 180.49 | 382.01 | 2.12 | 0.222 | 0.262 | 18 |
| σ×0.5 trailing 24h \| out 5m \| now | 156.78 | 282.29 | 1.80 | 171.27 | 384.55 | 2.25 | 0.333 | 0.264 | 12 |
| σ×0.5 trailing 24h \| out 30m \| now | 142.07 | 261.83 | 1.84 | 159.31 | 382.18 | 2.40 | 0.364 | 0.282 | 11 |
| σ×0.5 trailing 24h \| out 120m \| now | 132.32 | 253.54 | 1.92 | 147.05 | 382.51 | 2.60 | 0.500 | 0.344 | 8 |
| σ×0.5 trailing 24h \| recentre 4h \| now | 136.59 | 261.78 | 1.92 | 169.12 | 382.47 | 2.26 | 0.143 | 0.167 | 28 |
| σ×0.5 trailing 24h \| recentre 12h \| now | 145.52 | 265.18 | 1.82 | 160.87 | 383.21 | 2.38 | 0.308 | 0.500 | 13 |
| σ×0.5 trailing 24h \| recentre 24h \| now | 138.06 | 259.35 | 1.88 | 147.60 | 382.82 | 2.59 | 0.445 | 1.000 | 9 |
| σ×1 placeholder \| hold \| now | 69.82 | 121.82 | 1.74 | 74.62 | 153.56 | 2.06 | — | — | 0 |
| σ×1 placeholder \| out 0m \| now | 69.82 | 121.82 | 1.74 | 74.62 | 153.56 | 2.06 | 0.671 | 1.843 | 6 |
| σ×1 placeholder \| out 5m \| now | 69.82 | 121.82 | 1.74 | 74.62 | 153.56 | 2.06 | 0.671 | 1.846 | 6 |
| σ×1 placeholder \| out 30m \| now | 69.82 | 121.82 | 1.74 | 74.62 | 153.56 | 2.06 | 0.671 | 1.864 | 6 |
| σ×1 placeholder \| out 120m \| now | 69.82 | 121.82 | 1.74 | 74.62 | 153.56 | 2.06 | 0.671 | 1.926 | 6 |
| σ×1 placeholder \| recentre 4h \| now | 73.43 | 100.86 | 1.37 | 104.84 | 138.84 | 1.32 | 0.143 | 0.167 | 28 |
| σ×1 placeholder \| recentre 12h \| now | 74.86 | 114.08 | 1.52 | 87.53 | 147.88 | 1.69 | 0.309 | 0.500 | 13 |
| σ×1 placeholder \| recentre 24h \| now | 72.54 | 125.10 | 1.72 | 80.35 | 155.57 | 1.94 | 0.447 | 1.000 | 9 |
| σ×1 trailing 1h \| hold \| now | 109.47 | 207.00 | 1.89 | 113.65 | 293.25 | 2.58 | — | — | 0 |
| σ×1 trailing 1h \| out 0m \| now | 109.01 | 177.49 | 1.63 | 116.99 | 248.30 | 2.12 | 0.440 | 1.474 | 9 |
| σ×1 trailing 1h \| out 5m \| now | 109.57 | 177.16 | 1.62 | 112.35 | 248.64 | 2.21 | 0.566 | 1.338 | 7 |
| σ×1 trailing 1h \| out 30m \| now | 107.46 | 170.15 | 1.58 | 114.52 | 241.22 | 2.11 | 0.495 | 1.125 | 8 |
| σ×1 trailing 1h \| out 120m \| now | 110.54 | 207.42 | 1.88 | 116.31 | 293.39 | 2.52 | 0.793 | 0.665 | 5 |
| σ×1 trailing 1h \| recentre 4h \| now | 114.57 | 176.47 | 1.54 | 143.73 | 253.49 | 1.76 | 0.152 | 0.167 | 26 |
| σ×1 trailing 1h \| recentre 12h \| now | 119.41 | 210.44 | 1.76 | 128.75 | 282.70 | 2.20 | 0.360 | 0.500 | 11 |
| σ×1 trailing 1h \| recentre 24h \| now | 123.46 | 221.06 | 1.79 | 128.26 | 305.99 | 2.39 | 0.566 | 1.000 | 7 |
| σ×1 trailing 6h \| hold \| now | 87.28 | 122.58 | 1.40 | 92.51 | 187.66 | 2.03 | — | — | 0 |
| σ×1 trailing 6h \| out 0m \| now | 93.87 | 121.75 | 1.30 | 103.32 | 183.13 | 1.77 | 0.445 | 1.233 | 9 |
| σ×1 trailing 6h \| out 5m \| now | 92.60 | 121.47 | 1.31 | 101.02 | 182.72 | 1.81 | 0.500 | 1.244 | 8 |
| σ×1 trailing 6h \| out 30m \| now | 91.40 | 122.15 | 1.34 | 100.21 | 185.56 | 1.85 | 0.500 | 1.164 | 8 |
| σ×1 trailing 6h \| out 120m \| now | 87.28 | 122.58 | 1.40 | 92.51 | 187.66 | 2.03 | 0.667 | 1.181 | 6 |
| σ×1 trailing 6h \| recentre 4h \| now | 97.25 | 137.76 | 1.42 | 128.31 | 201.49 | 1.57 | 0.143 | 0.167 | 28 |
| σ×1 trailing 6h \| recentre 12h \| now | 99.33 | 143.48 | 1.44 | 112.52 | 205.25 | 1.82 | 0.308 | 0.500 | 13 |
| σ×1 trailing 6h \| recentre 24h \| now | 98.01 | 146.63 | 1.50 | 105.95 | 212.13 | 2.00 | 0.445 | 1.000 | 9 |
| σ×1 trailing 24h \| hold \| now | 89.73 | 127.45 | 1.42 | 95.12 | 193.93 | 2.04 | — | — | 0 |
| σ×1 trailing 24h \| out 0m \| now | 100.02 | 129.26 | 1.29 | 109.19 | 193.76 | 1.77 | 0.445 | 1.000 | 9 |
| σ×1 trailing 24h \| out 5m \| now | 96.72 | 129.39 | 1.34 | 105.50 | 193.86 | 1.84 | 0.500 | 1.000 | 8 |
| σ×1 trailing 24h \| out 30m \| now | 94.49 | 128.09 | 1.36 | 103.57 | 193.98 | 1.87 | 0.500 | 1.019 | 8 |
| σ×1 trailing 24h \| out 120m \| now | 89.73 | 127.45 | 1.42 | 95.12 | 193.93 | 2.04 | 0.667 | 1.081 | 6 |
| σ×1 trailing 24h \| recentre 4h \| now | 96.68 | 132.59 | 1.37 | 127.45 | 193.57 | 1.52 | 0.143 | 0.167 | 28 |
| σ×1 trailing 24h \| recentre 12h \| now | 96.18 | 133.50 | 1.39 | 108.85 | 193.08 | 1.77 | 0.308 | 0.500 | 13 |
| σ×1 trailing 24h \| recentre 24h \| now | 93.19 | 130.90 | 1.40 | 100.48 | 193.15 | 1.92 | 0.445 | 1.000 | 9 |
| σ×2 placeholder \| hold \| now | 41.57 | 64.01 | 1.54 | 47.02 | 80.69 | 1.72 | — | — | 0 |
| σ×2 placeholder \| out 0m \| now | 41.57 | 64.01 | 1.54 | 47.02 | 80.69 | 1.72 | 0.671 | 7.048 | 6 |
| σ×2 placeholder \| out 5m \| now | 41.57 | 64.01 | 1.54 | 47.02 | 80.69 | 1.72 | 0.671 | 7.051 | 6 |
| σ×2 placeholder \| out 30m \| now | 41.57 | 64.01 | 1.54 | 47.02 | 80.69 | 1.72 | 0.671 | 7.069 | 6 |
| σ×2 placeholder \| out 120m \| now | 41.57 | 64.01 | 1.54 | 47.02 | 80.69 | 1.72 | 0.671 | 7.131 | 6 |
| σ×2 placeholder \| recentre 4h \| now | 42.54 | 52.99 | 1.25 | 75.12 | 72.95 | 0.97 | 0.143 | 0.167 | 28 |
| σ×2 placeholder \| recentre 12h \| now | 42.92 | 59.94 | 1.40 | 56.85 | 77.70 | 1.37 | 0.309 | 0.500 | 13 |
| σ×2 placeholder \| recentre 24h \| now | 42.29 | 65.73 | 1.55 | 51.27 | 81.74 | 1.59 | 0.447 | 1.000 | 9 |
| σ×2 trailing 1h \| hold \| now | 76.00 | 104.18 | 1.37 | 77.98 | 147.76 | 1.89 | — | — | 0 |
| σ×2 trailing 1h \| out 0m \| now | 76.00 | 104.18 | 1.37 | 77.98 | 147.76 | 1.89 | 0.991 | 2.310 | 4 |
| σ×2 trailing 1h \| out 5m \| now | 76.00 | 104.18 | 1.37 | 77.98 | 147.76 | 1.89 | 0.991 | 2.313 | 4 |
| σ×2 trailing 1h \| out 30m \| now | 76.00 | 104.18 | 1.37 | 77.98 | 147.76 | 1.89 | 0.991 | 2.331 | 4 |
| σ×2 trailing 1h \| out 120m \| now | 76.00 | 104.18 | 1.37 | 77.98 | 147.76 | 1.89 | 0.991 | 2.393 | 4 |
| σ×2 trailing 1h \| recentre 4h \| now | 70.93 | 88.62 | 1.25 | 100.27 | 127.33 | 1.27 | 0.152 | 0.167 | 26 |
| σ×2 trailing 1h \| recentre 12h \| now | 75.82 | 105.27 | 1.39 | 85.58 | 141.40 | 1.65 | 0.360 | 0.500 | 11 |
| σ×2 trailing 1h \| recentre 24h \| now | 79.68 | 110.42 | 1.39 | 85.22 | 153.19 | 1.80 | 0.566 | 1.000 | 7 |
| σ×2 trailing 6h \| hold \| now | 54.57 | 62.93 | 1.15 | 59.86 | 96.21 | 1.61 | — | — | 0 |
| σ×2 trailing 6h \| out 0m \| now | 54.57 | 62.93 | 1.15 | 59.86 | 96.21 | 1.61 | 0.667 | 4.202 | 6 |
| σ×2 trailing 6h \| out 5m \| now | 54.57 | 62.93 | 1.15 | 59.86 | 96.21 | 1.61 | 0.667 | 4.205 | 6 |
| σ×2 trailing 6h \| out 30m \| now | 54.57 | 62.93 | 1.15 | 59.86 | 96.21 | 1.61 | 0.667 | 4.223 | 6 |
| σ×2 trailing 6h \| out 120m \| now | 54.57 | 62.93 | 1.15 | 59.86 | 96.21 | 1.61 | 0.667 | 4.285 | 6 |
| σ×2 trailing 6h \| recentre 4h \| now | 57.31 | 69.15 | 1.21 | 89.46 | 101.10 | 1.13 | 0.143 | 0.167 | 28 |
| σ×2 trailing 6h \| recentre 12h \| now | 58.50 | 72.18 | 1.23 | 72.11 | 103.29 | 1.43 | 0.308 | 0.500 | 13 |
| σ×2 trailing 6h \| recentre 24h \| now | 59.98 | 75.05 | 1.25 | 68.69 | 108.43 | 1.58 | 0.445 | 1.000 | 9 |
| σ×2 trailing 24h \| hold \| now | 54.99 | 63.42 | 1.15 | 60.25 | 96.86 | 1.61 | — | — | 0 |
| σ×2 trailing 24h \| out 0m \| now | 54.99 | 63.42 | 1.15 | 60.25 | 96.86 | 1.61 | 0.667 | 3.831 | 6 |
| σ×2 trailing 24h \| out 5m \| now | 54.99 | 63.42 | 1.15 | 60.25 | 96.86 | 1.61 | 0.667 | 3.834 | 6 |
| σ×2 trailing 24h \| out 30m \| now | 54.99 | 63.42 | 1.15 | 60.25 | 96.86 | 1.61 | 0.667 | 3.852 | 6 |
| σ×2 trailing 24h \| out 120m \| now | 54.99 | 63.42 | 1.15 | 60.25 | 96.86 | 1.61 | 0.667 | 3.914 | 6 |
| σ×2 trailing 24h \| recentre 4h \| now | 55.66 | 65.86 | 1.18 | 87.72 | 96.28 | 1.10 | 0.143 | 0.167 | 28 |
| σ×2 trailing 24h \| recentre 12h \| now | 56.18 | 67.28 | 1.20 | 69.57 | 97.41 | 1.40 | 0.308 | 0.500 | 13 |
| σ×2 trailing 24h \| recentre 24h \| now | 55.53 | 65.73 | 1.18 | 63.95 | 97.24 | 1.52 | 0.445 | 1.000 | 9 |

### F.2 Stability — model / simulator (LVR + hedge) per UTC day, headline top 10

| policy | 2026-09-27 | 2026-09-28 | 2026-09-29 | 2026-09-30 |
| --- | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 2.11 | 2.35 | 3.55 | 2.33 |
| σ×0.5 trailing 1h \| wall 10% \| stable 20m | 2.11 | 2.68 | 5.40 | 2.33 |
| σ×0.5 trailing 1h \| wall 2% \| stable 20m | 2.11 | 2.68 | 5.40 | 2.33 |
| σ×0.5 trailing 1h \| wall 5% \| stable 20m | 2.11 | 2.68 | 5.40 | 2.33 |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 2.11 | 2.68 | 3.87 | 2.25 |
| σ×0.5 trailing 24h \| out 120m \| stable 20m | 1.96 | 1.81 | 3.01 | 1.73 |
| σ×0.5 trailing 1h \| recentre 24h \| stable 20m | 2.11 | 2.68 | 5.40 | 2.33 |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 2.11 | 2.60 | 4.95 | 2.21 |
| σ×0.5 trailing 1h \| out 30m \| stable 20m | 2.11 | 2.30 | 2.83 | 2.31 |
| σ×0.5 trailing 1h \| out 120m \| now | 2.35 | 2.30 | 4.86 | 1.74 |

## G. Regime σ multipliers — measured, not ratified ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §2.4)

All 829 non-overlapping 300 s returns: σ = 1.186e-4/s. 20 wall-covered ticks skipped for a missing spot.

| regime (label \| spot vs ZGL) | returns | σ per second | multiplier | 95% interval of σ |
| --- | ---: | ---: | ---: | ---: |
| POSITIVE_GEX\|above | 262 | 1.277e-4 | 1.077 | 1.17e-4 – 1.39e-4 |
| POSITIVE_GEX\|below | 541 | 1.130e-4 | 0.953 | 1.06e-4 – 1.20e-4 |
| ZERO_GAMMA_PROXIMITY\|above | 6 | 7.968e-5 | 0.672 | 3.46e-5 – 1.25e-4 |
| ZERO_GAMMA_PROXIMITY\|below | 20 | 1.477e-4 | 1.246 | 1.02e-4 – 1.93e-4 |

## H. σ forecast check — trailing σ at t against σ realized over the next 24 h (evidence for the σ-estimator ADR)

43 hourly forecasts from 2026-09-27 12:00 to 2026-09-29 14:00 UTC, each scored against the σ realized over the next 24 h (mean 1.136e-4/s). **About 3 independent pairs** — the forecast windows overlap, so the grid count overstates the evidence. Lower RMSE is better; a mean log ratio near 0 is unbiased.

| estimator | pairs | mean ln(forecast/realized) | forecast/realized (geometric) | RMSE of ln ratio |
| --- | ---: | ---: | ---: | ---: |
| trailing 1 h | 43 | -0.115 | 0.891 | 0.407 |
| trailing 6 h | 43 | -0.006 | 0.994 | 0.331 |
| trailing 24 h | 43 | 0.011 | 1.011 | 0.336 |
| placeholder 1.4e-4/s | 43 | 0.223 | 1.249 | 0.279 |

## Caveats

- **Short data.** The archive run started 2026-09-27; walls exist only where TICKET T recorded them. Trust a ranking only once it holds across UTC days and [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-windows.
- **Only the sampled active bin earns.** A 30 s interval that crossed several bins earned in each; this credits one.
- **Pool liquidity is the latest 5-minute snapshot**, and the position dilutes only through its share of the active bin.
- **No measured volume, funding or taker series.** Those costs are placeholders; the fee side is in units of V.
- **Shape weights follow the Meteora SDK as value shares at open**, not its exact per-side token amounts.
- **The σ-window placement is unclamped by walls** (the pure [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] policy); the live planner also clamps to the buffered envelope, which does not bind at today's σ.
