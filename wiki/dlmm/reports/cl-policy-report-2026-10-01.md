---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- report
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-10-01.md
bot_commit: e532796
source_sha256: 79039b9278c9ffaaed2d67f8ad1565a879e50ee31009ae402b2ac89add1d46a1
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-10-01.md` at commit `e532796`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# CL policy report — where to deploy, when to close and redeploy

> **Units of V; not calibrated yield ([[adr-033-fee-yield-measurement-route|ADR-033]]).** No fee volume is recorded. Fees are counted in units of `V`,
> the unknown quote volume per second through the active bin, and every policy is reported by its **break-even**:
> the volume (and the fee yield on capital) at which fees would cover its losses. A lower break-even ranks a
> policy better. **It does not show that any policy is profitable.** Produced by `src/backtest/research/`
> (blueprint `backtest_research.md`, [[adr-043-research-simulator-reads-archive-offline|ADR-043]]).

## Data

- Archive roots: C:/observation/archive, C:/observation/soak-phase2-2026-09-26
- Recon (wall) roots: C:/observation/recon-evidence-T-2026-09-27, C:/observation/recon-evidence-T2-2026-09-28 — separate runs are never joined
- Span: 2026-09-26 11:16 → 2026-10-01 15:58 UTC; 14649 usable 30 s ticks in 6 gap-free segments
- Wall-covered: 11661 ticks, 2026-09-27 11:54 → 2026-10-01 15:58 UTC
- Gaps (never bridged): 2026-09-27 13:40 → 2026-09-27 14:30 (run change); 2026-09-27 14:36 → 2026-09-27 14:36 (run change); 2026-09-27 15:51 → 2026-09-27 15:53 (run change); 2026-09-28 09:07 → 2026-09-28 10:53 (run change); 2026-09-28 11:00 → 2026-09-28 11:00 (run change)

## Parameters (UNRATIFIED placeholders unless stated)

- Capital per open: 50 SOL-equivalent. Shape: Curve (the live strategy) unless stated.
- Hedge: band 0.0625 SOL (hedge_engine.md), taker 5 bps, funding 1 bps / 8 h.
- Re-ratio slippage: 10 bps on the swapped notional. Bin-array rent: charged for every array not yet initialised in the run (worst case); see the pre-initialised table for the other bound.
- Money columns are in quote (USDC) over the whole span. **IL** = HODL − position (unhedged loss). **LVR-eq** = capital − position − short P&L (hedged loss, direction netted out).

## A. All policies, wall-covered span (ranked by hedged break-even volume)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| bot exits \| stable 20m | 92.3% | 82.1% | 11 | 34.61 | 0.02 | 20.48 | 236.17 | 346.68 | 389.55 | 36.16M | 13.31M | 354.09 | 130.33 |
| 2 | σ×0.5 trailing 24h \| out 30m \| stable 20m | 95.0% | 96.9% | 9 | 26.14 | 0.02 | 20.24 | 240.23 | 340.37 | 374.67 | 36.90M | 13.89M | 331.87 | 124.93 |
| 3 | σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 93.9% | 91.4% | 13 | 34.71 | 0.03 | 22.48 | 182.03 | 348.23 | 386.65 | 37.26M | 11.25M | 348.51 | 105.27 |
| 4 | σ×0.5 trailing 24h \| out 120m \| now | 99.9% | 87.2% | 11 | 26.21 | 0.02 | 22.90 | 341.27 | 305.08 | 346.52 | 37.28M | 20.77M | 290.51 | 161.86 |
| 5 | σ×0.5 trailing 1h \| out 120m \| stable 20m | 95.7% | 87.6% | 8 | 34.59 | 0.02 | 14.45 | 227.04 | 308.58 | 331.61 | 37.33M | 14.96M | 297.06 | 119.00 |
| 6 | σ×0.5 trailing 24h \| out 30m \| now | 99.9% | 95.1% | 13 | 26.29 | 0.03 | 25.46 | 304.13 | 342.91 | 392.87 | 37.78M | 17.07M | 326.58 | 147.58 |
| 7 | σ×0.5 trailing 6h \| bot exits \| stable 20m | 92.4% | 91.9% | 11 | 35.08 | 0.02 | 20.17 | 234.61 | 344.07 | 384.67 | 37.99M | 14.05M | 350.44 | 129.58 |
| 8 | σ×0.5 trailing 24h \| bot exits \| stable 20m | 92.4% | 92.5% | 11 | 26.03 | 0.02 | 20.31 | 236.50 | 328.01 | 366.89 | 38.02M | 14.51M | 331.34 | 126.44 |
| 9 | σ×0.5 trailing 1h \| bot exits \| now | 97.5% | 59.6% | 27 | 34.70 | 0.05 | 23.20 | 195.62 | 353.17 | 432.34 | 38.07M | 11.45M | 355.94 | 107.01 |
| 10 | σ×0.5 trailing 1h \| wall 10% \| stable 20m | 96.2% | 83.5% | 7 | 34.61 | 0.01 | 13.84 | 254.04 | 295.76 | 315.21 | 38.24M | 17.54M | 282.36 | 129.53 |
| 11 | σ×0.5 trailing 1h \| wall 2% \| stable 20m | 96.2% | 83.5% | 7 | 34.61 | 0.01 | 13.84 | 254.04 | 295.76 | 315.21 | 38.24M | 17.54M | 282.36 | 129.53 |
| 12 | σ×0.5 trailing 1h \| wall 5% \| stable 20m | 96.2% | 83.5% | 7 | 34.61 | 0.01 | 13.84 | 254.04 | 295.76 | 315.21 | 38.24M | 17.54M | 282.36 | 129.53 |
| 13 | σ×0.5 trailing 6h \| out 30m \| now | 99.9% | 94.4% | 13 | 34.65 | 0.03 | 24.30 | 292.66 | 364.03 | 410.57 | 38.40M | 16.20M | 345.79 | 145.87 |
| 14 | σ×0.5 placeholder \| out 30m \| stable 20m | 95.5% | 97.8% | 9 | 43.56 | 0.02 | 17.51 | 219.24 | 297.42 | 328.66 | 38.42M | 15.68M | 297.70 | 121.44 |
| 15 | σ×0.5 trailing 24h \| out 5m \| stable 20m | 92.2% | 98.9% | 11 | 34.50 | 0.02 | 25.97 | 270.19 | 344.03 | 383.08 | 38.48M | 16.16M | 353.76 | 148.53 |
| 16 | σ×0.5 trailing 6h \| recentre 12h \| stable 20m | 94.0% | 92.8% | 13 | 43.56 | 0.03 | 23.34 | 192.88 | 359.82 | 401.12 | 38.54M | 12.09M | 363.92 | 114.21 |
| 17 | σ×0.5 placeholder \| out 5m \| stable 20m | 94.3% | 99.5% | 9 | 43.62 | 0.02 | 18.71 | 232.38 | 299.13 | 330.51 | 38.74M | 16.50M | 303.70 | 129.35 |
| 18 | σ×0.5 trailing 1h \| recentre 4h \| stable 20m | 89.0% | 89.0% | 24 | 43.47 | 0.04 | 38.89 | 276.84 | 314.96 | 399.90 | 38.75M | 17.46M | 370.96 | 167.16 |
| 19 | σ×0.5 placeholder \| out 0m \| stable 20m | 93.3% | 100.0% | 9 | 43.62 | 0.02 | 18.69 | 218.59 | 298.09 | 329.61 | 38.77M | 15.78M | 305.97 | 124.57 |
| 20 | σ×0.5 trailing 1h \| recentre 24h \| stable 20m | 95.5% | 84.9% | 9 | 34.61 | 0.02 | 18.43 | 231.83 | 307.85 | 332.20 | 38.92M | 16.00M | 298.96 | 122.88 |
| 21 | σ×0.5 placeholder \| out 30m \| now | 99.9% | 96.9% | 12 | 43.49 | 0.03 | 21.41 | 274.84 | 306.60 | 349.87 | 38.92M | 18.33M | 299.07 | 140.86 |
| 22 | σ×0.5 trailing 6h \| out 5m \| stable 20m | 91.9% | 99.1% | 12 | 43.56 | 0.03 | 28.47 | 303.34 | 340.15 | 382.83 | 38.93M | 18.38M | 358.65 | 169.35 |
| 23 | σ×0.5 trailing 24h \| out 0m \| stable 20m | 91.3% | 99.9% | 14 | 34.66 | 0.03 | 31.77 | 336.90 | 346.92 | 395.23 | 38.97M | 19.44M | 366.63 | 182.89 |
| 24 | σ×0.5 trailing 1h \| recentre 4h \| now | 98.9% | 81.9% | 28 | 34.56 | 0.05 | 53.49 | 453.36 | 371.65 | 467.79 | 38.97M | 22.75M | 387.80 | 226.38 |
| 25 | σ×0.5 trailing 1h \| out 30m \| stable 20m | 94.0% | 94.0% | 9 | 34.49 | 0.02 | 19.55 | 245.96 | 309.36 | 334.06 | 39.09M | 16.81M | 306.45 | 131.81 |
| 26 | σ×0.5 trailing 1h \| recentre 12h \| now | 99.0% | 77.9% | 13 | 26.12 | 0.02 | 26.58 | 242.67 | 357.79 | 392.51 | 39.24M | 14.44M | 334.30 | 122.97 |
| 27 | σ×0.5 trailing 1h \| out 120m \| now | 99.0% | 84.9% | 10 | 26.11 | 0.02 | 20.38 | 334.76 | 292.64 | 321.34 | 39.42M | 22.75M | 275.11 | 158.81 |
| 28 | σ×0.5 trailing 24h \| out 5m \| now | 99.9% | 98.8% | 14 | 34.61 | 0.03 | 32.23 | 368.44 | 375.97 | 422.70 | 39.42M | 19.83M | 359.44 | 180.78 |
| 29 | σ×0.5 placeholder \| out 5m \| now | 99.9% | 99.2% | 13 | 43.46 | 0.03 | 21.78 | 276.96 | 321.74 | 363.20 | 39.64M | 18.08M | 311.17 | 141.95 |
| 30 | σ×0.5 trailing 6h \| out 120m \| now | 99.9% | 83.8% | 11 | 26.21 | 0.02 | 21.96 | 326.86 | 306.33 | 340.34 | 39.68M | 21.42M | 287.30 | 155.07 |
| 31 | σ×0.5 trailing 6h \| out 0m \| stable 20m | 89.4% | 99.9% | 14 | 43.60 | 0.03 | 33.58 | 393.80 | 315.62 | 363.32 | 39.72M | 24.74M | 350.64 | 218.42 |
| 32 | σ×0.5 trailing 6h \| out 120m \| stable 20m | 96.0% | 92.2% | 8 | 43.51 | 0.02 | 14.29 | 234.01 | 305.82 | 330.16 | 39.74M | 16.72M | 298.25 | 125.45 |
| 33 | σ×0.5 trailing 24h \| recentre 12h \| stable 20m | 94.0% | 92.9% | 13 | 34.51 | 0.03 | 22.83 | 197.98 | 331.60 | 370.01 | 39.79M | 13.39M | 333.64 | 112.25 |
| 34 | σ×0.5 trailing 1h \| out 5m \| now | 99.0% | 98.6% | 17 | 34.43 | 0.03 | 34.98 | 411.39 | 322.61 | 374.88 | 39.89M | 25.01M | 318.98 | 199.98 |
| 35 | σ×0.5 placeholder \| out 0m \| now | 99.9% | 100.0% | 13 | 35.07 | 0.03 | 24.00 | 252.25 | 330.44 | 370.51 | 39.95M | 16.37M | 315.31 | 129.17 |
| 36 | σ×0.5 trailing 6h \| wall 10% \| stable 20m | 96.3% | 88.3% | 7 | 35.08 | 0.02 | 13.86 | 258.49 | 295.53 | 316.46 | 40.09M | 18.65M | 282.73 | 131.52 |
| 37 | σ×0.5 trailing 6h \| wall 2% \| stable 20m | 96.3% | 88.3% | 7 | 35.08 | 0.02 | 13.86 | 258.49 | 295.53 | 316.46 | 40.09M | 18.65M | 282.73 | 131.52 |
| 38 | σ×0.5 trailing 6h \| wall 5% \| stable 20m | 96.3% | 88.3% | 7 | 35.08 | 0.02 | 13.86 | 258.49 | 295.53 | 316.46 | 40.09M | 18.65M | 282.73 | 131.52 |
| 39 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 95.6% | 82.5% | 9 | 26.06 | 0.02 | 18.56 | 232.36 | 304.40 | 330.54 | 40.10M | 16.34M | 293.27 | 119.54 |
| 40 | σ×1 trailing 1h \| bot exits \| stable 20m | 92.3% | 97.0% | 11 | 61.01 | 0.04 | 14.97 | 159.10 | 262.47 | 298.71 | 40.21M | 14.84M | 285.12 | 105.21 |

## B. σ-window policies, full archive span

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 120m \| now | 98.7% | 82.6% | 8 | 34.77 | 0.01 | 18.03 | 272.87 | 401.79 | 447.95 | 29.61M | 10.68M | 300.85 | 108.56 |
| 2 | σ×0.5 trailing 24h \| out 120m \| now | 99.5% | 91.9% | 8 | 25.82 | 0.01 | 12.71 | 167.20 | 392.33 | 441.40 | 29.86M | 7.04M | 287.90 | 67.91 |
| 3 | σ×0.5 trailing 1h \| hold \| now | 98.7% | 75.4% | 4 | 25.78 | 0.00 | 5.88 | 134.44 | 408.77 | 444.53 | 30.44M | 5.71M | 294.72 | 55.32 |
| 4 | σ×0.5 trailing 6h \| out 120m \| now | 99.5% | 93.0% | 8 | 34.71 | 0.02 | 12.18 | 159.56 | 391.22 | 437.54 | 30.47M | 7.18M | 289.09 | 68.16 |
| 5 | σ×0.5 trailing 24h \| out 30m \| now | 99.5% | 96.2% | 12 | 34.79 | 0.02 | 25.48 | 398.22 | 403.14 | 462.68 | 30.97M | 15.33M | 305.31 | 151.16 |
| 6 | σ×0.5 trailing 1h \| out 5m \| now | 98.7% | 98.8% | 15 | 42.99 | 0.03 | 36.04 | 456.34 | 431.96 | 495.83 | 31.09M | 16.53M | 334.80 | 178.03 |
| 7 | σ×0.5 trailing 24h \| hold \| now | 99.5% | 87.3% | 6 | 25.79 | 0.01 | 7.31 | 128.65 | 377.91 | 415.45 | 31.11M | 6.09M | 272.86 | 53.41 |
| 8 | σ×0.5 trailing 6h \| hold \| now | 99.5% | 87.3% | 6 | 25.79 | 0.01 | 7.25 | 129.07 | 372.79 | 408.73 | 31.25M | 6.22M | 268.93 | 53.53 |
| 9 | σ×0.5 trailing 6h \| out 30m \| now | 99.5% | 96.3% | 12 | 34.76 | 0.03 | 24.84 | 403.20 | 395.20 | 450.55 | 31.51M | 16.11M | 298.54 | 152.61 |
| 10 | σ×0.5 trailing 24h \| out 5m \| now | 99.5% | 98.8% | 15 | 34.22 | 0.03 | 34.41 | 415.91 | 444.00 | 498.70 | 31.64M | 15.16M | 333.97 | 160.02 |
| 11 | σ×0.5 trailing 1h \| recentre 12h \| now | 98.7% | 81.0% | 13 | 25.89 | 0.02 | 20.28 | 163.06 | 461.80 | 517.80 | 32.03M | 6.53M | 341.28 | 69.62 |
| 12 | σ×1 trailing 24h \| out 5m \| now | 99.5% | 99.7% | 8 | 43.31 | 0.02 | 9.31 | 135.07 | 281.05 | 312.55 | 32.54M | 9.45M | 213.30 | 61.96 |
| 13 | σ×1 trailing 1h \| hold \| now | 98.7% | 91.9% | 4 | 25.97 | 0.01 | 5.39 | 105.39 | 332.00 | 355.04 | 32.73M | 6.23M | 239.26 | 45.54 |
| 14 | σ×0.5 placeholder \| out 30m \| now | 99.9% | 97.8% | 10 | 34.71 | 0.02 | 17.67 | 299.00 | 332.64 | 377.87 | 32.77M | 15.09M | 250.74 | 115.49 |
| 15 | σ×0.5 trailing 6h \| out 5m \| now | 99.5% | 98.9% | 16 | 43.06 | 0.03 | 36.48 | 432.09 | 436.57 | 493.12 | 32.87M | 16.66M | 333.25 | 168.94 |
| 16 | σ×0.5 trailing 1h \| out 30m \| now | 98.7% | 93.2% | 11 | 43.17 | 0.02 | 25.79 | 431.72 | 380.43 | 423.27 | 32.90M | 18.88M | 290.51 | 166.68 |
| 17 | σ×1 trailing 24h \| out 30m \| now | 99.5% | 98.8% | 8 | 43.30 | 0.02 | 9.29 | 136.34 | 275.82 | 308.12 | 32.93M | 9.78M | 210.02 | 62.34 |
| 18 | σ×0.5 placeholder \| out 5m \| now | 99.9% | 99.2% | 12 | 34.69 | 0.03 | 22.25 | 342.57 | 364.15 | 407.56 | 32.94M | 15.88M | 272.75 | 131.51 |
| 19 | σ×0.5 placeholder \| out 120m \| now | 99.9% | 94.8% | 8 | 34.71 | 0.02 | 10.66 | 167.17 | 327.64 | 365.58 | 33.00M | 9.50M | 242.99 | 69.93 |
| 20 | σ×0.5 trailing 1h \| recentre 24h \| now | 98.7% | 73.1% | 8 | 25.78 | 0.01 | 15.46 | 199.19 | 438.46 | 467.20 | 33.00M | 8.38M | 314.42 | 79.84 |
| 21 | σ×0.5 trailing 6h \| recentre 12h \| now | 99.5% | 92.9% | 15 | 25.89 | 0.03 | 20.39 | 147.60 | 439.08 | 500.60 | 33.13M | 6.52M | 325.40 | 63.99 |
| 22 | σ×1 trailing 1h \| out 120m \| now | 98.7% | 92.6% | 5 | 34.44 | 0.01 | 6.31 | 92.80 | 334.46 | 361.21 | 33.17M | 6.02M | 245.32 | 44.49 |
| 23 | σ×0.5 trailing 24h \| recentre 12h \| now | 99.5% | 94.7% | 15 | 25.89 | 0.03 | 20.16 | 151.90 | 431.23 | 489.53 | 33.21M | 6.80M | 319.08 | 65.34 |
| 24 | σ×1 trailing 24h \| out 0m \| now | 99.5% | 100.0% | 10 | 43.30 | 0.03 | 15.18 | 243.09 | 283.09 | 318.42 | 33.23M | 15.18M | 217.79 | 99.52 |
| 25 | σ×1 trailing 6h \| out 5m \| now | 99.5% | 99.8% | 8 | 43.32 | 0.03 | 8.87 | 127.76 | 268.08 | 298.30 | 33.24M | 9.67M | 204.17 | 59.40 |

## C. Where to deploy — best close/redeploy rule for each placement (wall-covered span)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| bot exits \| stable 20m | 92.3% | 82.1% | 11 | 34.61 | 0.02 | 20.48 | 236.17 | 346.68 | 389.55 | 36.16M | 13.31M | 354.09 | 130.33 |
| 2 | σ×0.5 trailing 24h \| out 30m \| stable 20m | 95.0% | 96.9% | 9 | 26.14 | 0.02 | 20.24 | 240.23 | 340.37 | 374.67 | 36.90M | 13.89M | 331.87 | 124.93 |
| 3 | σ×0.5 trailing 6h \| bot exits \| stable 20m | 92.4% | 91.9% | 11 | 35.08 | 0.02 | 20.17 | 234.61 | 344.07 | 384.67 | 37.99M | 14.05M | 350.44 | 129.58 |
| 4 | σ×0.5 placeholder \| out 30m \| stable 20m | 95.5% | 97.8% | 9 | 43.56 | 0.02 | 17.51 | 219.24 | 297.42 | 328.66 | 38.42M | 15.68M | 297.70 | 121.44 |
| 5 | σ×1 trailing 1h \| bot exits \| stable 20m | 92.3% | 97.0% | 11 | 61.01 | 0.04 | 14.97 | 159.10 | 262.47 | 298.71 | 40.21M | 14.84M | 285.12 | 105.21 |
| 6 | σ×1 trailing 6h \| recentre 12h \| stable 20m | 94.0% | 100.0% | 13 | 43.87 | 0.04 | 15.70 | 124.11 | 245.35 | 283.05 | 41.19M | 12.87M | 258.49 | 80.76 |
| 7 | σ×1 trailing 24h \| out 0m \| stable 20m | 96.0% | 100.0% | 8 | 43.81 | 0.03 | 12.39 | 180.06 | 211.78 | 234.03 | 42.53M | 20.02M | 215.73 | 101.53 |
| 8 | σ×1 placeholder \| out 0m \| stable 20m | 96.3% | 100.0% | 7 | 43.78 | 0.03 | 9.45 | 148.17 | 171.43 | 191.31 | 44.14M | 21.37M | 177.95 | 86.16 |
| 9 | σ×2 trailing 1h \| bot exits \| stable 20m | 92.3% | 100.0% | 11 | 95.48 | 0.06 | 8.90 | 90.44 | 159.15 | 194.32 | 48.09M | 20.47M | 204.89 | 87.20 |
| 10 | σ×2 trailing 6h \| recentre 12h \| stable 20m | 94.0% | 100.0% | 13 | 61.62 | 0.07 | 9.04 | 70.25 | 141.92 | 180.68 | 48.12M | 17.25M | 172.91 | 61.98 |
| 11 | σ×2 trailing 24h \| out 0m \| stable 20m | 96.3% | 100.0% | 7 | 61.52 | 0.04 | 7.32 | 108.32 | 124.30 | 145.20 | 49.29M | 25.81M | 144.75 | 75.80 |
| 12 | σ×2 placeholder \| out 0m \| stable 20m | 96.3% | 100.0% | 7 | 79.26 | 0.05 | 5.64 | 85.55 | 101.56 | 123.38 | 54.99M | 30.25M | 132.56 | 72.93 |
| 13 | walls buffered k=0.25 \| out 0m \| stable 20m | 96.3% | 100.0% | 7 | 115.33 | 0.10 | 2.77 | 42.09 | 51.13 | 74.21 | 84.99M | 55.94M | 104.18 | 68.57 |
| 14 | walls raw \| out 0m \| stable 20m | 96.3% | 100.0% | 7 | 159.69 | 0.14 | 1.96 | 30.76 | 37.85 | 60.48 | 122.44M | 90.63M | 111.27 | 82.36 |

## D. Stability — hedged break-even volume/day of the top 10, per UTC day

| policy | 2026-09-27 | 2026-09-28 | 2026-09-29 | 2026-09-30 | 2026-10-01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 30.55M | 50.40M | 37.83M | 46.19M | 25.35M |
| σ×0.5 trailing 24h \| out 30m \| stable 20m | 32.18M | 54.04M | 37.84M | 47.54M | 28.98M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 30.55M | 52.70M | 36.34M | 48.81M | 27.34M |
| σ×0.5 trailing 24h \| out 120m \| now | 32.83M | 51.53M | 47.00M | 48.64M | 29.19M |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 30.55M | 44.74M | 41.78M | 48.91M | 32.90M |
| σ×0.5 trailing 24h \| out 30m \| now | 32.83M | 54.23M | 44.32M | 47.27M | 29.19M |
| σ×0.5 trailing 6h \| bot exits \| stable 20m | 35.94M | 55.73M | 38.20M | 47.68M | 28.07M |
| σ×0.5 trailing 24h \| bot exits \| stable 20m | 32.18M | 57.01M | 39.69M | 50.94M | 28.98M |
| σ×0.5 trailing 1h \| bot exits \| now | 30.22M | 52.25M | 54.38M | 50.94M | 26.09M |
| σ×0.5 trailing 1h \| wall 10% \| stable 20m | 30.55M | 50.40M | 36.34M | 48.91M | 25.35M |

## E. Sensitivity of the top 5 — size, rent bound, shape (hedged break-even volume/day)

| policy | 5 SOL | 50 SOL | 500 SOL | arrays pre-initialised | Spot shape (reference only) |
| --- | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 49.29M | 36.16M | 38.27M | 34.58M | 37.25M |
| σ×0.5 trailing 24h \| out 30m \| stable 20m | 47.26M | 36.90M | 38.34M | 35.64M | 39.64M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 50.67M | 37.26M | 39.12M | 35.62M | 38.83M |
| σ×0.5 trailing 24h \| out 120m \| now | 48.48M | 37.28M | 38.80M | 35.88M | 39.62M |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 52.71M | 37.33M | 38.80M | 35.46M | 38.89M |

## F. [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model vs simulator — LVR and hedge-taker cost, bps of capital per day (UNRATIFIED model; evidence for ratification)

> Each open evaluates the model for its own range, σ (trailing 24 h at the open) and capital; its rates accrue over
> the same deployed seconds the simulator accounts exactly. "LVR-eq sim" is the hedged loss (market direction netted
> out); "hedge taker sim" is the discrete hedge's taker cost. Lifespan compares the model's expected first exit
> (plus the out-of-range delay, capped by re-centre) with observed episodes — which a segment end can cut short.

| policy | LVR-eq sim | LVR model | model/sim | hedge taker sim | hedge model | model/sim | life sim (d) | life model (d) | closes compared |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 placeholder \| hold \| now | 104.47 | 131.26 | 1.26 | 112.71 | 141.23 | 1.25 | — | — | 0 |
| σ×0.5 placeholder \| out 0m \| now | 124.74 | 135.91 | 1.09 | 135.28 | 143.73 | 1.06 | 0.424 | 0.592 | 12 |
| σ×0.5 placeholder \| out 5m \| now | 119.86 | 132.54 | 1.11 | 132.83 | 141.85 | 1.07 | 0.424 | 0.607 | 12 |
| σ×0.5 placeholder \| out 30m \| now | 109.33 | 134.29 | 1.23 | 122.73 | 142.81 | 1.16 | 0.508 | 0.632 | 10 |
| σ×0.5 placeholder \| out 120m \| now | 107.79 | 127.32 | 1.18 | 118.91 | 139.07 | 1.17 | 0.635 | 0.735 | 8 |
| σ×0.5 placeholder \| recentre 4h \| now | 115.34 | 115.84 | 1.00 | 150.32 | 131.96 | 0.88 | 0.145 | 0.167 | 35 |
| σ×0.5 placeholder \| recentre 12h \| now | 119.16 | 123.80 | 1.04 | 134.06 | 136.55 | 1.02 | 0.339 | 0.500 | 15 |
| σ×0.5 placeholder \| recentre 24h \| now | 111.11 | 132.35 | 1.19 | 120.67 | 141.54 | 1.17 | 0.508 | 1.000 | 10 |
| σ×0.5 trailing 1h \| hold \| now | 136.13 | 232.80 | 1.71 | 146.72 | 270.81 | 1.85 | — | — | 0 |
| σ×0.5 trailing 1h \| out 0m \| now | 130.10 | 125.46 | 0.96 | 144.35 | 143.35 | 0.99 | 0.314 | 0.545 | 16 |
| σ×0.5 trailing 1h \| out 5m \| now | 143.64 | 143.05 | 1.00 | 163.36 | 167.60 | 1.03 | 0.335 | 0.468 | 15 |
| σ×0.5 trailing 1h \| out 30m \| now | 126.64 | 142.91 | 1.13 | 139.48 | 164.83 | 1.18 | 0.456 | 0.586 | 11 |
| σ×0.5 trailing 1h \| out 120m \| now | 133.93 | 187.51 | 1.40 | 148.08 | 226.25 | 1.53 | 0.628 | 0.344 | 8 |
| σ×0.5 trailing 1h \| recentre 4h \| now | 158.06 | 192.90 | 1.22 | 195.48 | 228.76 | 1.17 | 0.152 | 0.167 | 33 |
| σ×0.5 trailing 1h \| recentre 12h \| now | 153.64 | 233.46 | 1.52 | 170.70 | 261.16 | 1.53 | 0.386 | 0.500 | 13 |
| σ×0.5 trailing 1h \| recentre 24h \| now | 145.59 | 213.34 | 1.47 | 153.45 | 251.52 | 1.64 | 0.628 | 1.000 | 8 |
| σ×0.5 trailing 6h \| hold \| now | 123.08 | 134.50 | 1.09 | 133.53 | 168.85 | 1.26 | — | — | 0 |
| σ×0.5 trailing 6h \| out 0m \| now | 155.41 | 136.42 | 0.88 | 173.86 | 165.45 | 0.95 | 0.253 | 0.356 | 20 |
| σ×0.5 trailing 6h \| out 5m \| now | 144.15 | 142.56 | 0.99 | 161.40 | 166.02 | 1.03 | 0.316 | 0.366 | 16 |
| σ×0.5 trailing 6h \| out 30m \| now | 130.31 | 134.73 | 1.03 | 147.02 | 160.72 | 1.09 | 0.422 | 0.429 | 12 |
| σ×0.5 trailing 6h \| out 120m \| now | 129.15 | 134.04 | 1.04 | 143.00 | 166.68 | 1.17 | 0.633 | 0.489 | 8 |
| σ×0.5 trailing 6h \| recentre 4h \| now | 132.36 | 157.03 | 1.19 | 168.25 | 186.75 | 1.11 | 0.144 | 0.167 | 35 |
| σ×0.5 trailing 6h \| recentre 12h \| now | 144.91 | 157.69 | 1.09 | 163.65 | 187.96 | 1.15 | 0.337 | 0.500 | 15 |
| σ×0.5 trailing 6h \| recentre 24h \| now | 134.65 | 156.91 | 1.17 | 145.94 | 190.03 | 1.30 | 0.506 | 1.000 | 10 |
| σ×0.5 trailing 24h \| hold \| now | 124.77 | 138.61 | 1.11 | 135.75 | 173.30 | 1.28 | — | — | 0 |
| σ×0.5 trailing 24h \| out 0m \| now | 157.42 | 153.38 | 0.97 | 176.87 | 174.07 | 0.98 | 0.241 | 0.338 | 21 |
| σ×0.5 trailing 24h \| out 5m \| now | 146.62 | 153.34 | 1.05 | 163.26 | 174.63 | 1.07 | 0.337 | 0.340 | 15 |
| σ×0.5 trailing 24h \| out 30m \| now | 132.90 | 148.00 | 1.11 | 150.93 | 174.19 | 1.15 | 0.422 | 0.357 | 12 |
| σ×0.5 trailing 24h \| out 120m \| now | 129.49 | 139.77 | 1.08 | 144.22 | 173.44 | 1.20 | 0.633 | 0.420 | 8 |
| σ×0.5 trailing 24h \| recentre 4h \| now | 136.08 | 145.74 | 1.07 | 171.87 | 174.15 | 1.01 | 0.144 | 0.167 | 35 |
| σ×0.5 trailing 24h \| recentre 12h \| now | 142.32 | 144.60 | 1.02 | 160.00 | 174.12 | 1.09 | 0.337 | 0.500 | 15 |
| σ×0.5 trailing 24h \| recentre 24h \| now | 130.72 | 141.76 | 1.08 | 141.49 | 174.44 | 1.23 | 0.506 | 1.000 | 10 |
| σ×1 placeholder \| hold \| now | 68.08 | 65.53 | 0.96 | 73.42 | 70.50 | 0.96 | — | — | 0 |
| σ×1 placeholder \| out 0m \| now | 68.08 | 65.53 | 0.96 | 73.42 | 70.50 | 0.96 | 0.847 | 2.380 | 6 |
| σ×1 placeholder \| out 5m \| now | 68.08 | 65.53 | 0.96 | 73.42 | 70.50 | 0.96 | 0.847 | 2.383 | 6 |
| σ×1 placeholder \| out 30m \| now | 68.08 | 65.53 | 0.96 | 73.42 | 70.50 | 0.96 | 0.847 | 2.400 | 6 |
| σ×1 placeholder \| out 120m \| now | 68.08 | 65.53 | 0.96 | 73.42 | 70.50 | 0.96 | 0.847 | 2.463 | 6 |
| σ×1 placeholder \| recentre 4h \| now | 71.46 | 57.83 | 0.81 | 104.80 | 65.87 | 0.63 | 0.145 | 0.167 | 35 |
| σ×1 placeholder \| recentre 12h \| now | 72.38 | 61.80 | 0.85 | 86.00 | 68.17 | 0.79 | 0.339 | 0.500 | 15 |
| σ×1 placeholder \| recentre 24h \| now | 69.87 | 66.07 | 0.95 | 78.46 | 70.66 | 0.90 | 0.508 | 1.000 | 10 |
| σ×1 trailing 1h \| hold \| now | 110.57 | 119.93 | 1.08 | 116.88 | 139.48 | 1.19 | — | — | 0 |
| σ×1 trailing 1h \| out 0m \| now | 92.77 | 84.38 | 0.91 | 99.90 | 99.20 | 0.99 | 0.558 | 1.903 | 9 |
| σ×1 trailing 1h \| out 5m \| now | 100.44 | 97.08 | 0.97 | 104.06 | 112.50 | 1.08 | 0.628 | 1.542 | 8 |
| σ×1 trailing 1h \| out 30m \| now | 98.20 | 87.87 | 0.89 | 105.39 | 102.90 | 0.98 | 0.628 | 1.446 | 8 |
| σ×1 trailing 1h \| out 120m \| now | 111.42 | 120.12 | 1.08 | 118.98 | 139.54 | 1.17 | 1.004 | 0.835 | 5 |
| σ×1 trailing 1h \| recentre 4h \| now | 112.10 | 98.34 | 0.88 | 144.65 | 116.62 | 0.81 | 0.152 | 0.167 | 33 |
| σ×1 trailing 1h \| recentre 12h \| now | 116.98 | 120.25 | 1.03 | 129.88 | 134.39 | 1.03 | 0.386 | 0.500 | 13 |
| σ×1 trailing 1h \| recentre 24h \| now | 114.82 | 110.79 | 0.96 | 121.43 | 130.40 | 1.07 | 0.628 | 1.000 | 8 |
| σ×1 trailing 6h \| hold \| now | 84.26 | 68.01 | 0.81 | 90.24 | 85.38 | 0.95 | — | — | 0 |
| σ×1 trailing 6h \| out 0m \| now | 84.76 | 66.64 | 0.79 | 94.84 | 81.16 | 0.86 | 0.506 | 1.644 | 10 |
| σ×1 trailing 6h \| out 5m \| now | 88.48 | 67.59 | 0.76 | 96.99 | 83.65 | 0.86 | 0.633 | 1.606 | 8 |
| σ×1 trailing 6h \| out 30m \| now | 87.53 | 67.83 | 0.77 | 96.35 | 84.63 | 0.88 | 0.633 | 1.497 | 8 |
| σ×1 trailing 6h \| out 120m \| now | 84.26 | 68.01 | 0.81 | 90.24 | 85.38 | 0.95 | 0.844 | 1.501 | 6 |
| σ×1 trailing 6h \| recentre 4h \| now | 93.57 | 79.68 | 0.85 | 127.20 | 94.86 | 0.75 | 0.144 | 0.167 | 35 |
| σ×1 trailing 6h \| recentre 12h \| now | 97.10 | 79.91 | 0.82 | 111.90 | 95.27 | 0.85 | 0.337 | 0.500 | 15 |
| σ×1 trailing 6h \| recentre 24h \| now | 93.79 | 79.65 | 0.85 | 102.92 | 96.47 | 0.94 | 0.506 | 1.000 | 10 |
| σ×1 trailing 24h \| hold \| now | 87.22 | 70.96 | 0.81 | 93.46 | 88.65 | 0.95 | — | — | 0 |
| σ×1 trailing 24h \| out 0m \| now | 93.41 | 73.17 | 0.78 | 103.59 | 88.35 | 0.85 | 0.506 | 1.290 | 10 |
| σ×1 trailing 24h \| out 5m \| now | 92.76 | 71.82 | 0.77 | 101.69 | 88.66 | 0.87 | 0.633 | 1.290 | 8 |
| σ×1 trailing 24h \| out 30m \| now | 91.00 | 71.24 | 0.78 | 100.16 | 88.67 | 0.89 | 0.633 | 1.310 | 8 |
| σ×1 trailing 24h \| out 120m \| now | 87.22 | 70.96 | 0.81 | 93.46 | 88.65 | 0.95 | 0.844 | 1.372 | 6 |
| σ×1 trailing 24h \| recentre 4h \| now | 93.13 | 74.10 | 0.80 | 126.24 | 88.52 | 0.70 | 0.144 | 0.167 | 35 |
| σ×1 trailing 24h \| recentre 12h \| now | 93.30 | 73.45 | 0.79 | 107.33 | 88.51 | 0.82 | 0.337 | 0.500 | 15 |
| σ×1 trailing 24h \| recentre 24h \| now | 89.28 | 72.01 | 0.81 | 97.85 | 88.61 | 0.91 | 0.506 | 1.000 | 10 |
| σ×2 placeholder \| hold \| now | 40.14 | 33.94 | 0.85 | 45.33 | 36.51 | 0.81 | — | — | 0 |
| σ×2 placeholder \| out 0m \| now | 40.14 | 33.94 | 0.85 | 45.33 | 36.51 | 0.81 | 0.847 | 9.101 | 6 |
| σ×2 placeholder \| out 5m \| now | 40.14 | 33.94 | 0.85 | 45.33 | 36.51 | 0.81 | 0.847 | 9.105 | 6 |
| σ×2 placeholder \| out 30m \| now | 40.14 | 33.94 | 0.85 | 45.33 | 36.51 | 0.81 | 0.847 | 9.122 | 6 |
| σ×2 placeholder \| out 120m \| now | 40.14 | 33.94 | 0.85 | 45.33 | 36.51 | 0.81 | 0.847 | 9.184 | 6 |
| σ×2 placeholder \| recentre 4h \| now | 41.06 | 29.95 | 0.73 | 74.61 | 34.12 | 0.46 | 0.145 | 0.167 | 35 |
| σ×2 placeholder \| recentre 12h \| now | 41.30 | 32.01 | 0.78 | 55.18 | 35.31 | 0.64 | 0.339 | 0.500 | 15 |
| σ×2 placeholder \| recentre 24h \| now | 40.60 | 34.22 | 0.84 | 49.52 | 36.59 | 0.74 | 0.508 | 1.000 | 10 |
| σ×2 trailing 1h \| hold \| now | 74.80 | 60.66 | 0.81 | 78.17 | 70.59 | 0.90 | — | — | 0 |
| σ×2 trailing 1h \| out 0m \| now | 74.80 | 60.66 | 0.81 | 78.17 | 70.59 | 0.90 | 1.256 | 2.983 | 4 |
| σ×2 trailing 1h \| out 5m \| now | 74.80 | 60.66 | 0.81 | 78.17 | 70.59 | 0.90 | 1.256 | 2.986 | 4 |
| σ×2 trailing 1h \| out 30m \| now | 74.80 | 60.66 | 0.81 | 78.17 | 70.59 | 0.90 | 1.256 | 3.004 | 4 |
| σ×2 trailing 1h \| out 120m \| now | 74.80 | 60.66 | 0.81 | 78.17 | 70.59 | 0.90 | 1.256 | 3.066 | 4 |
| σ×2 trailing 1h \| recentre 4h \| now | 67.94 | 49.76 | 0.73 | 99.45 | 59.02 | 0.59 | 0.152 | 0.167 | 33 |
| σ×2 trailing 1h \| recentre 12h \| now | 73.18 | 60.72 | 0.83 | 84.90 | 67.86 | 0.80 | 0.386 | 0.500 | 13 |
| σ×2 trailing 1h \| recentre 24h \| now | 73.39 | 55.89 | 0.76 | 79.94 | 65.88 | 0.82 | 0.628 | 1.000 | 8 |
| σ×2 trailing 6h \| hold \| now | 51.87 | 34.87 | 0.67 | 57.11 | 43.76 | 0.77 | — | — | 0 |
| σ×2 trailing 6h \| out 0m \| now | 51.87 | 34.87 | 0.67 | 57.11 | 43.76 | 0.77 | 0.844 | 5.426 | 6 |
| σ×2 trailing 6h \| out 5m \| now | 51.87 | 34.87 | 0.67 | 57.11 | 43.76 | 0.77 | 0.844 | 5.430 | 6 |
| σ×2 trailing 6h \| out 30m \| now | 51.87 | 34.87 | 0.67 | 57.11 | 43.76 | 0.77 | 0.844 | 5.447 | 6 |
| σ×2 trailing 6h \| out 120m \| now | 51.87 | 34.87 | 0.67 | 57.11 | 43.76 | 0.77 | 0.844 | 5.509 | 6 |
| σ×2 trailing 6h \| recentre 4h \| now | 54.67 | 40.30 | 0.74 | 88.22 | 47.97 | 0.54 | 0.144 | 0.167 | 35 |
| σ×2 trailing 6h \| recentre 12h \| now | 56.48 | 40.42 | 0.72 | 70.48 | 48.20 | 0.68 | 0.337 | 0.500 | 15 |
| σ×2 trailing 6h \| recentre 24h \| now | 56.95 | 40.59 | 0.71 | 65.95 | 49.14 | 0.75 | 0.506 | 1.000 | 10 |
| σ×2 trailing 24h \| hold \| now | 52.33 | 35.72 | 0.68 | 57.56 | 44.70 | 0.78 | — | — | 0 |
| σ×2 trailing 24h \| out 0m \| now | 52.33 | 35.72 | 0.68 | 57.56 | 44.70 | 0.78 | 0.844 | 4.947 | 6 |
| σ×2 trailing 24h \| out 5m \| now | 52.33 | 35.72 | 0.68 | 57.56 | 44.70 | 0.78 | 0.844 | 4.950 | 6 |
| σ×2 trailing 24h \| out 30m \| now | 52.33 | 35.72 | 0.68 | 57.56 | 44.70 | 0.78 | 0.844 | 4.968 | 6 |
| σ×2 trailing 24h \| out 120m \| now | 52.33 | 35.72 | 0.68 | 57.56 | 44.70 | 0.78 | 0.844 | 5.030 | 6 |
| σ×2 trailing 24h \| recentre 4h \| now | 52.94 | 37.36 | 0.71 | 86.21 | 44.64 | 0.52 | 0.144 | 0.167 | 35 |
| σ×2 trailing 24h \| recentre 12h \| now | 54.08 | 37.35 | 0.69 | 67.76 | 45.00 | 0.66 | 0.337 | 0.500 | 15 |
| σ×2 trailing 24h \| recentre 24h \| now | 52.82 | 36.38 | 0.69 | 61.52 | 44.80 | 0.73 | 0.506 | 1.000 | 10 |

### F.2 Stability — model / simulator (LVR + hedge) per UTC day, headline top 10

| policy | 2026-09-27 | 2026-09-28 | 2026-09-29 | 2026-09-30 | 2026-10-01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| bot exits \| stable 20m | 1.03 | 1.32 | 1.90 | 1.07 | 1.68 |
| σ×0.5 trailing 24h \| out 30m \| stable 20m | 0.96 | 0.86 | 1.50 | 1.03 | 1.06 |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 1.03 | 1.28 | 2.44 | 1.09 | 1.50 |
| σ×0.5 trailing 24h \| out 120m \| now | 0.92 | 0.78 | 1.72 | 1.07 | 1.23 |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 1.03 | 1.15 | 1.75 | 1.14 | 1.77 |
| σ×0.5 trailing 24h \| out 30m \| now | 0.92 | 0.77 | 1.44 | 1.00 | 1.23 |
| σ×0.5 trailing 6h \| bot exits \| stable 20m | 0.94 | 1.01 | 1.58 | 1.03 | 1.22 |
| σ×0.5 trailing 24h \| bot exits \| stable 20m | 0.96 | 1.03 | 1.29 | 0.91 | 1.06 |
| σ×0.5 trailing 1h \| bot exits \| now | 1.14 | 1.24 | 2.63 | 0.84 | 1.77 |
| σ×0.5 trailing 1h \| wall 10% \| stable 20m | 1.03 | 1.32 | 2.66 | 1.14 | 1.68 |

### F.3 [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] form test — the gate's LVR and hedge-drag model with the realized pool σ

> The EV gate's LVR and hedge-drag model ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]], `rangeCostRates`) with the pool's σ realized over the next 24 h, against the simulator's exact accounting, Curve shape, 96 σ-window policies. The σ forecast is taken out on purpose: it is [[adr-047-provisional-sigma-estimator|ADR-047]]'s question (§H). Criteria ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2): median model ÷ simulator within ±25% per term, and no judged UTC day outside ±50%. Days under 18 h are shown, not judged.

**Result: PASS** — LVR 0.98 (pass), hedge drag 0.98 (pass), days pass.

| UTC day | hours | judged | LVR model ÷ sim | hedge model ÷ sim |
| --- | ---: | --- | ---: | ---: |
| 2026-09-26 | 12.7 | no | 0.91 | 1.11 |
| 2026-09-27 | 23.1 | yes | 1.37 | 1.06 |
| 2026-09-28 | 22.2 | yes | 0.79 | 0.75 |
| 2026-09-29 | 24.0 | yes | 0.90 | 0.86 |
| 2026-09-30 | 24.0 | yes | 0.85 | 0.89 |
| 2026-10-01 | 16.0 | no | 0.87 | 0.83 |

## G. Regime σ multipliers — measured, not ratified ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §2.4)

All 1125 non-overlapping 300 s returns: σ = 1.121e-4/s. 14 wall-covered ticks skipped for a missing spot.

| regime (label \| spot vs ZGL) | returns | σ per second | multiplier | 95% interval of σ |
| --- | ---: | ---: | ---: | ---: |
| NEGATIVE_GEX\|none | 13 | 1.010e-4 | 0.901 | 6.22e-5 – 1.40e-4 |
| POSITIVE_GEX\|above | 262 | 1.277e-4 | 1.140 | 1.17e-4 – 1.39e-4 |
| POSITIVE_GEX\|below | 824 | 1.060e-4 | 0.945 | 1.01e-4 – 1.11e-4 |
| ZERO_GAMMA_PROXIMITY\|above | 6 | 7.968e-5 | 0.711 | 3.46e-5 – 1.25e-4 |
| ZERO_GAMMA_PROXIMITY\|below | 20 | 1.477e-4 | 1.318 | 1.02e-4 – 1.93e-4 |

## H. σ forecast check — trailing σ at t against σ realized over the next 24 h (evidence for the σ-estimator ADR)

68 hourly forecasts from 2026-09-27 12:00 to 2026-09-30 15:00 UTC, each scored against the σ realized over the next 24 h (mean 1.116e-4/s). **About 4 independent pairs** — the forecast windows overlap, so the grid count overstates the evidence. Lower RMSE is better; a mean log ratio near 0 is unbiased.

| estimator | pairs | mean ln(forecast/realized) | forecast/realized (geometric) | RMSE of ln ratio |
| --- | ---: | ---: | ---: | ---: |
| trailing 1 h | 68 | -0.132 | 0.876 | 0.422 |
| trailing 6 h | 68 | -0.054 | 0.947 | 0.317 |
| trailing 24 h | 68 | -0.026 | 0.974 | 0.282 |
| placeholder 1.4e-4/s | 68 | 0.236 | 1.266 | 0.274 |

### Live σ chain, as the monitors recorded it ([[adr-047-provisional-sigma-estimator|ADR-047]], TICKET Z)

Each monitor computes the [[adr-047-provisional-sigma-estimator|ADR-047]] chain (24 h → 6 h → placeholder) from its own in-memory spot history and records it. Only `observedAtMs` and `sigmaEstimate` are read from the recordings ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1 A4). Scored at hourly points against the σ realized over the next 24 h, with the archive's trailing 24 h σ and the placeholder on the same points.

**Orca recording:** 2961 recorded estimates (PLACEHOLDER 706, TRAILING_6H 2160, TRAILING_24H 95); about 0 independent pairs.

_No scored pairs yet: needs a recorded estimate at an hourly point and a full covered 24 h after it._

**Meteora recording:** 2962 recorded estimates (PLACEHOLDER 706, TRAILING_6H 2160, TRAILING_24H 96); about 0 independent pairs.

_No scored pairs yet: needs a recorded estimate at an hourly point and a full covered 24 h after it._


## I. Measured fee yield — [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Route 4 (on-chain per-bin fee counters)

279 fee-growth samples from 2026-09-30T16:48Z to 2026-10-01T15:55Z (cadence 5 min; 0 lines skipped).

A hypothetical position is credited its share of each bin's measured LP fees: share = own value / (bin value + own value), from the program's per-bin fee-per-share counters.
Only whole sample intervals during which a position was open throughout are credited, so partial intervals at open and close are left out (conservative).
"Coverage" is the share of deployed time those intervals cover. "Net" is the measured yield minus the hedged break-even yield from the same run.
**Measured on the recorded pool, not ratified. Ratification is [[adr-033-fee-yield-measurement-route|ADR-033]]'s path ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D1).**

**Standing reconciliation (aggregate over 272 intervals):** LP ÷ (LP + protocol) = SOL 0.8997, USDC 0.9000; expected 0.9000. A short interval can read low when liquidity enters and leaves inside it; the aggregate is the check.

| policy | coverage | measured fee yield bps/day | break-even bps/day (hedged) | net bps/day |
| --- | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| out 120m \| now | 19% | 167.75 | 300.85 | -133.10 |
| σ×0.5 trailing 24h \| out 120m \| now | 19% | 117.63 | 287.90 | -170.27 |
| σ×0.5 trailing 1h \| hold \| now | 19% | 125.05 | 294.72 | -169.68 |
| σ×0.5 trailing 6h \| out 120m \| now | 19% | 115.38 | 289.09 | -173.71 |
| σ×0.5 trailing 24h \| out 30m \| now | 19% | 104.25 | 305.31 | -201.06 |
| σ×0.5 trailing 1h \| out 5m \| now | 19% | 144.32 | 334.80 | -190.48 |
| σ×0.5 trailing 24h \| hold \| now | 19% | 117.63 | 272.86 | -155.23 |
| σ×0.5 trailing 6h \| hold \| now | 19% | 115.38 | 268.93 | -153.56 |
| σ×0.5 trailing 6h \| out 30m \| now | 19% | 89.28 | 298.54 | -209.26 |
| σ×0.5 trailing 24h \| out 5m \| now | 19% | 112.56 | 333.97 | -221.42 |

### I.2 [[adr-033-fee-yield-measurement-route|ADR-033]] sub-windows (3 days from the sampler's first run_start) — measured fee yield, bps/day

| policy | 2026-09-30 (in progress) | p10 of eligible |
| --- | ---: | ---: |
| _sampler coverage_ | 100% | |
| σ×0.5 trailing 1h \| out 120m \| now | 123.10 | — |
| σ×0.5 trailing 24h \| out 120m \| now | 63.34 | — |
| σ×0.5 trailing 1h \| hold \| now | 20.84 | — |
| σ×0.5 trailing 6h \| out 120m \| now | 46.70 | — |
| σ×0.5 trailing 24h \| out 30m \| now | 108.72 | — |

Eligible windows (complete, sampler coverage ≥ 95%): 0 of 1. [[adr-033-fee-yield-measurement-route|ADR-033]] needs seven with max/min ≤ 3×.

## Caveats

- **Short data.** The archive run started 2026-09-27; walls exist only where TICKET T recorded them. Trust a ranking only once it holds across UTC days and [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-windows.
- **Only the sampled active bin earns.** A 30 s interval that crossed several bins earned in each; this credits one.
- **Pool liquidity is the latest 5-minute snapshot**, and the position dilutes only through its share of the active bin.
- **No measured volume, funding or taker series.** Those costs are placeholders; the fee side is in units of V.
- **Shape weights follow the Meteora SDK as value shares at open**, not its exact per-side token amounts.
- **The σ-window placement is unclamped by walls** (the pure [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] policy); the live planner also clamps to the buffered envelope, which does not bind at today's σ.
