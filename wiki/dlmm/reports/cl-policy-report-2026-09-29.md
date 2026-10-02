---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- report
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-09-29.md
bot_commit: 72bc8fe
source_sha256: 220f7273a361ee91577e06846fdc3089d1d7fd26f9fce95d57be887fe6d83e72
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/research/CL_POLICY_REPORT_2026-09-29.md` at commit `72bc8fe`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# CL policy report — where to deploy, when to close and redeploy

> **Units of V; not calibrated yield ([[adr-033-fee-yield-measurement-route|ADR-033]]).** No fee volume is recorded. Fees are counted in units of `V`,
> the unknown quote volume per second through the active bin, and every policy is reported by its **break-even**:
> the volume (and the fee yield on capital) at which fees would cover its losses. A lower break-even ranks a
> policy better. **It does not show that any policy is profitable.** Produced by `src/backtest/research/`
> (blueprint `backtest_research.md`, [[adr-043-research-simulator-reads-archive-offline|ADR-043]]).

## Data

- Archive roots: C:\observation\archive, C:\observation\soak-phase2-2026-09-26
- Recon (wall) roots: C:\observation\recon-evidence-T-2026-09-27, C:\observation\recon-evidence-T2-2026-09-28 — separate runs are never joined
- Span: 2026-09-26 11:16 → 2026-09-28 16:25 UTC; 6064 usable 30 s ticks in 6 gap-free segments
- Wall-covered: 3079 ticks, 2026-09-27 11:54 → 2026-09-28 16:25 UTC
- Gaps (never bridged): 2026-09-27 13:40 → 2026-09-27 14:30 (run change); 2026-09-27 14:36 → 2026-09-27 14:36 (run change); 2026-09-27 15:51 → 2026-09-27 15:53 (run change); 2026-09-28 09:07 → 2026-09-28 10:53 (run change); 2026-09-28 11:00 → 2026-09-28 11:00 (run change)

## Parameters (UNRATIFIED placeholders unless stated)

- Capital per open: 50 SOL-equivalent. Shape: Curve (the live strategy) unless stated.
- Hedge: band 0.0625 SOL (hedge_engine.md), taker 5 bps, funding 1 bps / 8 h.
- Re-ratio slippage: 10 bps on the swapped notional. Bin-array rent: charged for every array not yet initialised in the run (worst case); see the pre-initialised table for the other bound.
- Money columns are in quote (USDC) over the whole span. **IL** = HODL − position (unhedged loss). **LVR-eq** = capital − position − short P&L (hedged loss, direction netted out).

## A. All policies, wall-covered span (ranked by hedged break-even volume)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 5m \| now | 96.4% | 97.3% | 9 | 26.08 | 0.02 | 16.07 | 147.89 | 116.99 | 139.97 | 37.52M | 23.84M | 479.53 | 304.67 |
| 2 | σ×0.5 trailing 1h \| out 0m \| now | 96.4% | 99.8% | 9 | 26.13 | 0.01 | 17.28 | 130.72 | 127.30 | 149.81 | 38.30M | 20.81M | 513.70 | 279.10 |
| 3 | σ×0.5 trailing 1h \| out 120m \| stable 20m | 92.5% | 82.4% | 5 | 26.01 | 0.01 | 6.75 | 102.53 | 125.80 | 129.27 | 41.43M | 19.47M | 481.50 | 226.33 |
| 4 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 92.9% | 88.3% | 5 | 26.06 | 0.01 | 7.13 | 92.86 | 114.40 | 121.15 | 43.58M | 20.44M | 447.47 | 209.89 |
| 5 | σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 92.6% | 86.9% | 5 | 26.13 | 0.01 | 8.51 | 105.80 | 123.34 | 127.64 | 43.59M | 21.43M | 477.11 | 234.60 |
| 6 | σ×0.5 trailing 1h \| out 30m \| stable 20m | 92.6% | 91.5% | 5 | 26.13 | 0.01 | 8.97 | 98.96 | 129.77 | 133.83 | 43.73M | 19.63M | 499.33 | 224.11 |
| 7 | σ×0.5 trailing 1h \| recentre 4h \| now | 96.4% | 80.2% | 9 | 34.56 | 0.01 | 17.72 | 143.39 | 121.51 | 139.93 | 43.91M | 27.39M | 503.00 | 313.73 |
| 8 | σ×0.5 trailing 1h \| out 0m \| stable 20m | 88.4% | 99.9% | 8 | 26.27 | 0.01 | 12.97 | 119.94 | 110.39 | 129.10 | 43.96M | 25.11M | 486.79 | 278.01 |
| 9 | σ×0.5 trailing 1h \| out 120m \| now | 96.5% | 81.2% | 5 | 26.11 | 0.01 | 8.74 | 97.14 | 135.81 | 138.48 | 44.02M | 18.80M | 495.73 | 211.66 |
| 10 | σ×0.5 trailing 1h \| recentre 12h \| now | 96.5% | 84.1% | 5 | 26.12 | 0.01 | 8.76 | 93.82 | 137.99 | 140.24 | 44.04M | 18.11M | 502.16 | 206.43 |
| 11 | σ×0.5 trailing 1h \| out 30m \| now | 96.5% | 87.3% | 5 | 26.14 | 0.01 | 8.60 | 88.51 | 138.84 | 141.49 | 44.12M | 17.26M | 505.27 | 197.66 |
| 12 | σ×0.5 trailing 24h \| out 120m \| now | 99.8% | 85.8% | 6 | 26.21 | 0.01 | 7.92 | 84.94 | 118.49 | 128.68 | 44.52M | 18.85M | 435.67 | 184.43 |
| 13 | σ×0.5 trailing 6h \| out 0m \| now | 99.7% | 99.9% | 8 | 26.28 | 0.02 | 14.94 | 121.64 | 135.75 | 151.97 | 44.71M | 22.14M | 510.10 | 252.57 |
| 14 | σ×0.5 trailing 6h \| out 120m \| now | 99.8% | 88.7% | 6 | 26.21 | 0.01 | 7.35 | 79.86 | 124.50 | 133.40 | 44.93M | 17.49M | 451.90 | 175.87 |
| 15 | σ×0.5 trailing 1h \| out 5m \| stable 20m | 89.9% | 98.0% | 7 | 26.25 | 0.01 | 12.19 | 111.81 | 113.17 | 128.11 | 44.95M | 24.15M | 481.00 | 258.39 |
| 16 | σ×0.5 trailing 1h \| bot exits \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 17 | σ×0.5 trailing 1h \| hold \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 18 | σ×0.5 trailing 1h \| recentre 24h \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 19 | σ×0.5 trailing 1h \| wall 10% \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 20 | σ×0.5 trailing 1h \| wall 15% \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 21 | σ×0.5 trailing 1h \| wall 2% \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 22 | σ×0.5 trailing 1h \| wall 5% \| now | 96.5% | 63.6% | 4 | 26.01 | 0.00 | 5.99 | 114.46 | 125.21 | 123.25 | 44.96M | 23.48M | 448.39 | 234.15 |
| 23 | σ×0.5 trailing 1h \| bot exits \| stable 20m | 93.9% | 67.2% | 4 | 26.03 | 0.00 | 6.15 | 127.01 | 112.98 | 112.87 | 45.02M | 27.78M | 423.48 | 261.26 |
| 24 | σ×0.5 trailing 1h \| recentre 24h \| stable 20m | 93.9% | 67.2% | 4 | 26.03 | 0.00 | 6.15 | 127.01 | 112.98 | 112.87 | 45.02M | 27.78M | 423.48 | 261.26 |
| 25 | σ×0.5 trailing 1h \| wall 10% \| stable 20m | 93.9% | 67.2% | 4 | 26.03 | 0.00 | 6.15 | 127.01 | 112.98 | 112.87 | 45.02M | 27.78M | 423.48 | 261.26 |
| 26 | σ×0.5 trailing 1h \| wall 15% \| stable 20m | 93.9% | 67.2% | 4 | 26.03 | 0.00 | 6.15 | 127.01 | 112.98 | 112.87 | 45.02M | 27.78M | 423.48 | 261.26 |
| 27 | σ×0.5 trailing 1h \| wall 2% \| stable 20m | 93.9% | 67.2% | 4 | 26.03 | 0.00 | 6.15 | 127.01 | 112.98 | 112.87 | 45.02M | 27.78M | 423.48 | 261.26 |
| 28 | σ×0.5 trailing 1h \| wall 5% \| stable 20m | 93.9% | 67.2% | 4 | 26.03 | 0.00 | 6.15 | 127.01 | 112.98 | 112.87 | 45.02M | 27.78M | 423.48 | 261.26 |
| 29 | σ×0.5 trailing 24h \| out 0m \| stable 20m | 90.2% | 99.9% | 7 | 26.26 | 0.01 | 11.72 | 114.74 | 124.97 | 140.08 | 45.11M | 22.74M | 520.60 | 262.38 |
| 30 | σ×0.5 trailing 24h \| out 5m \| now | 99.8% | 99.1% | 6 | 26.28 | 0.01 | 9.45 | 79.52 | 133.69 | 143.37 | 45.15M | 16.64M | 485.29 | 178.81 |
| 31 | σ×0.5 trailing 24h \| recentre 4h \| now | 99.7% | 92.4% | 10 | 26.28 | 0.02 | 16.17 | 134.16 | 119.45 | 142.13 | 45.24M | 26.28M | 471.23 | 273.74 |
| 32 | σ×0.5 trailing 24h \| recentre 12h \| now | 99.8% | 97.7% | 6 | 26.29 | 0.01 | 9.35 | 77.66 | 127.05 | 136.60 | 45.30M | 17.15M | 464.00 | 175.67 |
| 33 | σ×0.5 trailing 24h \| out 30m \| now | 99.8% | 95.8% | 6 | 26.29 | 0.01 | 9.36 | 78.41 | 123.35 | 133.56 | 45.34M | 17.68M | 453.42 | 176.78 |
| 34 | σ×0.5 trailing 24h \| out 30m \| stable 20m | 92.9% | 97.4% | 5 | 26.14 | 0.01 | 8.83 | 86.50 | 119.59 | 126.11 | 45.35M | 19.63M | 467.36 | 202.27 |
| 35 | σ×0.5 trailing 24h \| recentre 12h \| stable 20m | 92.9% | 93.1% | 5 | 26.13 | 0.01 | 8.66 | 96.15 | 113.69 | 120.58 | 45.40M | 22.10M | 447.69 | 217.89 |
| 36 | σ×0.5 trailing 6h \| out 30m \| now | 99.8% | 94.6% | 6 | 26.26 | 0.01 | 8.30 | 75.05 | 128.31 | 136.93 | 45.44M | 16.61M | 464.97 | 170.02 |
| 37 | σ×0.5 trailing 24h \| out 0m \| now | 99.7% | 99.9% | 8 | 26.27 | 0.01 | 15.68 | 129.56 | 131.45 | 147.94 | 45.53M | 24.30M | 498.47 | 266.06 |
| 38 | σ×0.5 placeholder \| out 5m \| now | 99.8% | 99.3% | 6 | 35.02 | 0.01 | 5.67 | 80.79 | 105.82 | 116.60 | 45.96M | 21.22M | 408.31 | 188.53 |
| 39 | σ×0.5 trailing 6h \| recentre 12h \| now | 99.8% | 96.0% | 6 | 26.29 | 0.01 | 8.55 | 73.42 | 128.19 | 136.72 | 46.01M | 16.62M | 464.70 | 167.85 |
| 40 | σ×0.5 trailing 6h \| out 5m \| now | 99.7% | 97.9% | 8 | 26.26 | 0.02 | 14.42 | 123.09 | 132.06 | 147.24 | 46.07M | 23.58M | 496.37 | 254.06 |

## B. σ-window policies, full archive span

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 24h \| out 5m \| now | 98.9% | 99.0% | 8 | 25.88 | 0.01 | 13.44 | 155.11 | 203.43 | 231.08 | 26.35M | 10.81M | 375.50 | 154.10 |
| 2 | σ×0.5 trailing 1h \| out 5m \| now | 96.9% | 98.6% | 9 | 34.65 | 0.02 | 18.25 | 196.21 | 175.85 | 208.58 | 26.56M | 15.13M | 353.23 | 201.21 |
| 3 | σ×0.5 trailing 24h \| out 30m \| now | 98.9% | 96.1% | 8 | 34.79 | 0.01 | 13.58 | 172.76 | 182.51 | 212.67 | 27.60M | 13.76M | 351.26 | 175.12 |
| 4 | σ×0.5 trailing 6h \| out 5m \| now | 98.8% | 98.6% | 10 | 34.74 | 0.02 | 18.71 | 194.76 | 196.56 | 229.99 | 27.75M | 14.35M | 380.35 | 196.69 |
| 5 | σ×0.5 trailing 24h \| out 120m \| now | 98.9% | 88.3% | 8 | 25.82 | 0.01 | 12.71 | 170.73 | 172.26 | 201.13 | 27.88M | 14.16M | 326.39 | 165.82 |
| 6 | σ×0.5 trailing 24h \| out 0m \| now | 98.8% | 99.9% | 12 | 25.88 | 0.02 | 22.90 | 192.61 | 211.21 | 243.43 | 27.91M | 13.38M | 399.07 | 191.36 |
| 7 | σ×0.5 trailing 6h \| out 30m \| now | 98.9% | 96.1% | 8 | 34.76 | 0.02 | 12.96 | 165.32 | 184.66 | 213.28 | 28.10M | 13.44M | 353.07 | 168.79 |
| 8 | σ×0.5 trailing 1h \| out 0m \| now | 96.9% | 99.9% | 10 | 34.69 | 0.02 | 22.94 | 181.90 | 189.48 | 218.48 | 28.13M | 14.47M | 376.00 | 193.45 |
| 9 | σ×0.5 trailing 6h \| out 0m \| now | 98.8% | 99.9% | 11 | 34.74 | 0.02 | 22.04 | 182.32 | 208.56 | 238.28 | 28.68M | 13.62M | 399.09 | 189.49 |
| 10 | σ×0.5 trailing 6h \| out 120m \| now | 98.9% | 90.1% | 8 | 34.71 | 0.02 | 12.18 | 162.93 | 175.68 | 203.45 | 28.92M | 14.25M | 337.76 | 166.35 |
| 11 | σ×0.5 trailing 1h \| out 120m \| now | 96.9% | 86.4% | 6 | 34.77 | 0.01 | 11.90 | 179.90 | 188.46 | 204.89 | 29.42M | 15.15M | 355.80 | 183.20 |
| 12 | σ×0.5 trailing 1h \| recentre 24h \| now | 96.9% | 73.7% | 5 | 25.78 | 0.01 | 8.57 | 178.40 | 178.27 | 187.27 | 29.68M | 15.79M | 323.22 | 171.96 |
| 13 | σ×0.5 trailing 24h \| recentre 24h \| now | 98.9% | 80.8% | 7 | 25.79 | 0.01 | 9.80 | 165.54 | 167.33 | 187.51 | 29.69M | 15.30M | 309.38 | 159.39 |
| 14 | σ×0.5 trailing 1h \| out 30m \| now | 96.9% | 92.8% | 6 | 34.80 | 0.01 | 10.91 | 167.32 | 192.47 | 208.22 | 29.76M | 14.20M | 360.66 | 172.12 |
| 15 | σ×0.5 placeholder \| out 5m \| now | 99.9% | 99.5% | 8 | 34.69 | 0.02 | 10.39 | 159.33 | 147.85 | 171.02 | 29.91M | 16.80M | 286.29 | 160.79 |
| 16 | σ×0.5 trailing 6h \| recentre 24h \| now | 98.9% | 79.7% | 7 | 25.79 | 0.01 | 9.40 | 164.05 | 165.90 | 185.97 | 29.94M | 15.41M | 306.72 | 157.89 |
| 17 | σ×0.5 trailing 24h \| hold \| now | 98.9% | 77.1% | 6 | 25.79 | 0.01 | 7.31 | 132.18 | 157.84 | 175.17 | 30.18M | 13.63M | 290.31 | 131.07 |
| 18 | σ×0.5 trailing 1h \| hold \| now | 97.0% | 70.0% | 4 | 25.78 | 0.00 | 5.88 | 144.20 | 168.55 | 174.58 | 30.26M | 14.20M | 303.14 | 142.24 |
| 19 | σ×0.5 trailing 6h \| hold \| now | 98.9% | 76.1% | 6 | 25.79 | 0.01 | 7.25 | 132.43 | 157.25 | 174.64 | 30.27M | 13.72M | 289.37 | 131.22 |
| 20 | σ×0.5 trailing 1h \| recentre 12h \| now | 96.9% | 84.0% | 7 | 25.89 | 0.01 | 11.61 | 154.85 | 192.14 | 208.42 | 30.40M | 13.35M | 354.69 | 155.75 |
| 21 | σ×0.5 trailing 24h \| recentre 12h \| now | 98.9% | 90.8% | 9 | 25.89 | 0.01 | 12.69 | 141.10 | 180.34 | 207.65 | 30.54M | 12.87M | 338.60 | 142.63 |
| 22 | σ×0.5 trailing 6h \| recentre 12h \| now | 98.9% | 90.2% | 9 | 25.89 | 0.02 | 12.05 | 133.75 | 177.64 | 204.73 | 30.74M | 12.56M | 333.63 | 136.29 |
| 23 | σ×1 trailing 24h \| out 0m \| now | 98.9% | 100.0% | 8 | 43.30 | 0.02 | 9.09 | 120.05 | 125.97 | 149.21 | 30.92M | 16.28M | 259.64 | 136.69 |
| 24 | σ×0.5 placeholder \| out 30m \| now | 99.9% | 97.8% | 8 | 34.71 | 0.02 | 11.63 | 164.69 | 138.22 | 163.52 | 31.17M | 18.90M | 273.66 | 165.92 |
| 25 | σ×1 trailing 24h \| out 5m \| now | 98.9% | 99.5% | 8 | 43.31 | 0.02 | 9.31 | 137.10 | 122.60 | 146.77 | 31.18M | 18.37M | 255.17 | 150.35 |

## C. Where to deploy — best close/redeploy rule for each placement (wall-covered span)

| # | policy (placement \| close \| redeploy) | deployed | in range | opens | rent sunk | tx | slip | IL (unhedged) | LVR-eq (hedged) | hedge costs | BE volume/day hedged | BE volume/day unhedged | BE bps/day hedged | BE bps/day unhedged |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | σ×0.5 trailing 1h \| out 5m \| now | 96.4% | 97.3% | 9 | 26.08 | 0.02 | 16.07 | 147.89 | 116.99 | 139.97 | 37.52M | 23.84M | 479.53 | 304.67 |
| 2 | σ×0.5 trailing 24h \| out 120m \| stable 20m | 92.9% | 88.3% | 5 | 26.06 | 0.01 | 7.13 | 92.86 | 114.40 | 121.15 | 43.58M | 20.44M | 447.47 | 209.89 |
| 3 | σ×0.5 trailing 6h \| out 0m \| now | 99.7% | 99.9% | 8 | 26.28 | 0.02 | 14.94 | 121.64 | 135.75 | 151.97 | 44.71M | 22.14M | 510.10 | 252.57 |
| 4 | σ×0.5 placeholder \| out 5m \| now | 99.8% | 99.3% | 6 | 35.02 | 0.01 | 5.67 | 80.79 | 105.82 | 116.60 | 45.96M | 21.22M | 408.31 | 188.53 |
| 5 | σ×1 trailing 1h \| out 5m \| now | 96.5% | 99.5% | 5 | 35.08 | 0.01 | 6.35 | 73.40 | 105.97 | 111.99 | 47.25M | 20.92M | 416.09 | 184.21 |
| 6 | σ×1 trailing 24h \| out 0m \| now | 99.8% | 100.0% | 6 | 43.74 | 0.02 | 5.16 | 69.10 | 82.95 | 95.97 | 50.97M | 26.40M | 353.52 | 183.12 |
| 7 | σ×1 trailing 6h \| out 5m \| now | 99.8% | 99.6% | 6 | 43.73 | 0.02 | 4.76 | 71.55 | 83.54 | 95.87 | 52.61M | 27.71M | 353.68 | 186.30 |
| 8 | σ×1 placeholder \| recentre 12h \| now | 99.8% | 100.0% | 6 | 43.99 | 0.02 | 4.31 | 33.66 | 60.81 | 75.52 | 57.84M | 25.68M | 286.27 | 127.09 |
| 9 | σ×2 trailing 1h \| bot exits \| now | 96.5% | 100.0% | 4 | 43.72 | 0.01 | 3.67 | 57.03 | 60.74 | 67.84 | 58.05M | 34.45M | 281.35 | 166.96 |
| 10 | σ×2 trailing 24h \| bot exits \| now | 99.8% | 100.0% | 5 | 61.45 | 0.03 | 3.31 | 43.45 | 45.91 | 58.93 | 69.85M | 44.57M | 262.16 | 167.29 |
| 11 | σ×2 trailing 6h \| bot exits \| now | 99.8% | 100.0% | 5 | 61.45 | 0.03 | 3.11 | 43.35 | 46.32 | 59.12 | 70.92M | 45.02M | 262.80 | 166.83 |
| 12 | σ×2 placeholder \| recentre 12h \| now | 99.8% | 100.0% | 6 | 70.67 | 0.04 | 2.39 | 18.52 | 34.16 | 50.85 | 87.69M | 50.81M | 245.11 | 142.04 |
| 13 | walls buffered k=0.25 \| recentre 12h \| now | 99.8% | 100.0% | 6 | 115.10 | 0.09 | 0.99 | 8.21 | 15.23 | 31.75 | 203.56M | 155.20M | 252.93 | 192.84 |
| 14 | walls raw \| recentre 12h \| now | 99.8% | 100.0% | 6 | 159.37 | 0.12 | 1.11 | 6.09 | 11.26 | 27.46 | 335.97M | 280.97M | 309.01 | 258.41 |

## D. Stability — hedged break-even volume/day of the top 10, per UTC day

| policy | 2026-09-27 | 2026-09-28 |
| --- | ---: | ---: |
| σ×0.5 trailing 1h \| out 5m \| now | 29.31M | 67.62M |
| σ×0.5 trailing 1h \| out 0m \| now | 29.60M | 68.05M |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 30.55M | 56.09M |
| σ×0.5 trailing 24h \| out 120m \| stable 20m | 32.18M | 70.45M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 30.55M | 74.74M |
| σ×0.5 trailing 1h \| out 30m \| stable 20m | 30.55M | 61.61M |
| σ×0.5 trailing 1h \| recentre 4h \| now | 30.85M | 62.83M |
| σ×0.5 trailing 1h \| out 0m \| stable 20m | 31.33M | 64.79M |
| σ×0.5 trailing 1h \| out 120m \| now | 30.22M | 65.59M |
| σ×0.5 trailing 1h \| recentre 12h \| now | 30.22M | 75.21M |

## E. Sensitivity of the top 5 — size, rent bound, shape (hedged break-even volume/day)

| policy | 5 SOL | 50 SOL | 500 SOL | arrays pre-initialised | Spot shape (reference only) |
| --- | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 trailing 1h \| out 5m \| now | 65.83M | 37.52M | 38.78M | 34.25M | 43.80M |
| σ×0.5 trailing 1h \| out 0m \| now | 65.24M | 38.30M | 39.82M | 35.18M | 42.76M |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 73.91M | 41.43M | 42.65M | 37.69M | 46.05M |
| σ×0.5 trailing 24h \| out 120m \| stable 20m | 80.56M | 43.58M | 43.42M | 39.35M | 47.46M |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 77.94M | 43.59M | 44.58M | 39.60M | 46.67M |

## F. [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model vs simulator — LVR and hedge-taker cost, bps of capital per day (UNRATIFIED model; evidence for ratification)

> Each open evaluates the model for its own range, σ (trailing 24 h at the open) and capital; its rates accrue over
> the same deployed seconds the simulator accounts exactly. "LVR-eq sim" is the hedged loss (market direction netted
> out); "hedge taker sim" is the discrete hedge's taker cost. Lifespan compares the model's expected first exit
> (plus the out-of-range delay, capped by re-centre) with observed episodes — which a segment end can cut short.

| policy | LVR-eq sim | LVR model | model/sim | hedge taker sim | hedge model | model/sim | life sim (d) | life model (d) | closes compared |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| σ×0.5 placeholder \| hold \| now | 92.27 | 275.43 | 2.99 | 102.66 | 327.40 | 3.19 | — | — | 0 |
| σ×0.5 placeholder \| out 0m \| now | 119.61 | 253.74 | 2.12 | 132.80 | 313.13 | 2.36 | 0.263 | 0.503 | 8 |
| σ×0.5 placeholder \| out 5m \| now | 116.30 | 252.82 | 2.17 | 133.28 | 312.85 | 2.35 | 0.263 | 0.504 | 8 |
| σ×0.5 placeholder \| out 30m \| now | 108.66 | 256.31 | 2.36 | 127.24 | 315.11 | 2.48 | 0.263 | 0.514 | 8 |
| σ×0.5 placeholder \| out 120m \| now | 100.21 | 257.99 | 2.57 | 117.49 | 316.04 | 2.69 | 0.263 | 0.588 | 8 |
| σ×0.5 placeholder \| recentre 4h \| now | 109.97 | 167.36 | 1.52 | 146.60 | 254.33 | 1.73 | 0.124 | 0.167 | 17 |
| σ×0.5 placeholder \| recentre 12h \| now | 110.09 | 211.44 | 1.92 | 126.54 | 285.02 | 2.25 | 0.234 | 0.500 | 9 |
| σ×0.5 placeholder \| recentre 24h \| now | 97.81 | 263.52 | 2.69 | 110.91 | 319.55 | 2.88 | 0.300 | 1.000 | 7 |
| σ×0.5 trailing 1h \| hold \| now | 136.32 | 274.48 | 2.01 | 139.85 | 454.39 | 3.25 | — | — | 0 |
| σ×0.5 trailing 1h \| out 0m \| now | 153.02 | 223.48 | 1.46 | 174.76 | 362.50 | 2.07 | 0.204 | 0.382 | 10 |
| σ×0.5 trailing 1h \| out 5m \| now | 142.03 | 214.29 | 1.51 | 166.85 | 355.31 | 2.13 | 0.227 | 0.376 | 9 |
| σ×0.5 trailing 1h \| out 30m \| now | 155.50 | 253.37 | 1.63 | 166.73 | 405.94 | 2.43 | 0.340 | 0.437 | 6 |
| σ×0.5 trailing 1h \| out 120m \| now | 152.39 | 276.17 | 1.81 | 164.19 | 443.56 | 2.70 | 0.340 | 0.289 | 6 |
| σ×0.5 trailing 1h \| recentre 4h \| now | 152.79 | 295.03 | 1.93 | 182.80 | 488.48 | 2.67 | 0.136 | 0.167 | 15 |
| σ×0.5 trailing 1h \| recentre 12h \| now | 155.57 | 276.72 | 1.78 | 167.36 | 448.80 | 2.68 | 0.292 | 0.500 | 7 |
| σ×0.5 trailing 1h \| recentre 24h \| now | 144.09 | 275.66 | 1.91 | 149.94 | 455.97 | 3.04 | 0.408 | 1.000 | 5 |
| σ×0.5 trailing 6h \| hold \| now | 124.69 | 227.62 | 1.83 | 137.07 | 388.60 | 2.84 | — | — | 0 |
| σ×0.5 trailing 6h \| out 0m \| now | 165.26 | 223.98 | 1.36 | 187.25 | 365.88 | 1.95 | 0.189 | 0.297 | 11 |
| σ×0.5 trailing 6h \| out 5m \| now | 155.75 | 222.54 | 1.43 | 180.67 | 367.88 | 2.04 | 0.208 | 0.303 | 10 |
| σ×0.5 trailing 6h \| out 30m \| now | 146.29 | 222.41 | 1.52 | 167.42 | 369.58 | 2.21 | 0.260 | 0.342 | 8 |
| σ×0.5 trailing 6h \| out 120m \| now | 139.28 | 225.36 | 1.62 | 159.80 | 376.80 | 2.36 | 0.260 | 0.397 | 8 |
| σ×0.5 trailing 6h \| recentre 4h \| now | 138.31 | 226.83 | 1.64 | 174.68 | 382.49 | 2.19 | 0.122 | 0.167 | 17 |
| σ×0.5 trailing 6h \| recentre 12h \| now | 141.00 | 220.45 | 1.56 | 161.09 | 369.34 | 2.29 | 0.231 | 0.500 | 9 |
| σ×0.5 trailing 6h \| recentre 24h \| now | 131.46 | 226.34 | 1.72 | 145.90 | 385.76 | 2.64 | 0.297 | 1.000 | 7 |
| σ×0.5 trailing 24h \| hold \| now | 125.15 | 224.29 | 1.79 | 137.49 | 382.61 | 2.78 | — | — | 0 |
| σ×0.5 trailing 24h \| out 0m \| now | 167.42 | 232.31 | 1.39 | 191.39 | 381.52 | 1.99 | 0.173 | 0.264 | 12 |
| σ×0.5 trailing 24h \| out 5m \| now | 161.21 | 232.49 | 1.44 | 181.60 | 383.36 | 2.11 | 0.260 | 0.266 | 8 |
| σ×0.5 trailing 24h \| out 30m \| now | 144.53 | 233.06 | 1.61 | 166.81 | 382.32 | 2.29 | 0.260 | 0.283 | 8 |
| σ×0.5 trailing 24h \| out 120m \| now | 136.49 | 229.37 | 1.68 | 157.82 | 383.23 | 2.43 | 0.260 | 0.344 | 8 |
| σ×0.5 trailing 24h \| recentre 4h \| now | 142.56 | 228.95 | 1.61 | 178.33 | 382.00 | 2.14 | 0.122 | 0.167 | 17 |
| σ×0.5 trailing 24h \| recentre 12h \| now | 143.14 | 229.78 | 1.61 | 163.38 | 382.02 | 2.34 | 0.231 | 0.500 | 9 |
| σ×0.5 trailing 24h \| recentre 24h \| now | 132.59 | 224.64 | 1.69 | 147.11 | 382.71 | 2.60 | 0.297 | 1.000 | 7 |
| σ×1 placeholder \| hold \| now | 61.09 | 135.03 | 2.21 | 72.21 | 160.50 | 2.22 | — | — | 0 |
| σ×1 placeholder \| out 0m \| now | 61.09 | 135.03 | 2.21 | 72.21 | 160.50 | 2.22 | 0.351 | 1.843 | 6 |
| σ×1 placeholder \| out 5m \| now | 61.09 | 135.03 | 2.21 | 72.21 | 160.50 | 2.22 | 0.351 | 1.846 | 6 |
| σ×1 placeholder \| out 30m \| now | 61.09 | 135.03 | 2.21 | 72.21 | 160.50 | 2.22 | 0.351 | 1.864 | 6 |
| σ×1 placeholder \| out 120m \| now | 61.09 | 135.03 | 2.21 | 72.21 | 160.50 | 2.22 | 0.351 | 1.926 | 6 |
| σ×1 placeholder \| recentre 4h \| now | 66.70 | 82.05 | 1.23 | 103.99 | 124.68 | 1.20 | 0.124 | 0.167 | 17 |
| σ×1 placeholder \| recentre 12h \| now | 66.80 | 103.66 | 1.55 | 84.86 | 139.73 | 1.65 | 0.234 | 0.500 | 9 |
| σ×1 placeholder \| recentre 24h \| now | 62.49 | 129.19 | 2.07 | 76.15 | 156.65 | 2.06 | 0.300 | 1.000 | 7 |
| σ×1 trailing 1h \| hold \| now | 99.54 | 140.69 | 1.41 | 102.30 | 232.63 | 2.27 | — | — | 0 |
| σ×1 trailing 1h \| out 0m \| now | 110.10 | 132.59 | 1.20 | 118.71 | 211.49 | 1.78 | 0.340 | 1.442 | 6 |
| σ×1 trailing 1h \| out 5m \| now | 110.94 | 140.54 | 1.27 | 120.12 | 222.57 | 1.85 | 0.340 | 1.425 | 6 |
| σ×1 trailing 1h \| out 30m \| now | 106.98 | 134.64 | 1.26 | 116.45 | 217.38 | 1.87 | 0.340 | 1.235 | 6 |
| σ×1 trailing 1h \| out 120m \| now | 101.59 | 141.46 | 1.39 | 107.39 | 232.86 | 2.17 | 0.408 | 0.665 | 5 |
| σ×1 trailing 1h \| recentre 4h \| now | 115.69 | 149.51 | 1.29 | 146.33 | 247.47 | 1.69 | 0.136 | 0.167 | 15 |
| σ×1 trailing 1h \| recentre 12h \| now | 110.01 | 141.12 | 1.28 | 120.84 | 228.65 | 1.89 | 0.292 | 0.500 | 7 |
| σ×1 trailing 1h \| recentre 24h \| now | 102.82 | 141.29 | 1.37 | 108.07 | 233.43 | 2.16 | 0.408 | 1.000 | 5 |
| σ×1 trailing 6h \| hold \| now | 83.36 | 114.25 | 1.37 | 94.72 | 195.06 | 2.06 | — | — | 0 |
| σ×1 trailing 6h \| out 0m \| now | 96.13 | 112.98 | 1.18 | 113.09 | 186.90 | 1.65 | 0.260 | 1.208 | 8 |
| σ×1 trailing 6h \| out 5m \| now | 93.49 | 112.16 | 1.20 | 110.91 | 185.65 | 1.67 | 0.260 | 1.244 | 8 |
| σ×1 trailing 6h \| out 30m \| now | 91.20 | 113.45 | 1.24 | 109.37 | 191.06 | 1.75 | 0.260 | 1.164 | 8 |
| σ×1 trailing 6h \| out 120m \| now | 83.36 | 114.25 | 1.37 | 94.72 | 195.06 | 2.06 | 0.347 | 1.181 | 6 |
| σ×1 trailing 6h \| recentre 4h \| now | 93.96 | 115.09 | 1.22 | 130.89 | 194.28 | 1.48 | 0.122 | 0.167 | 17 |
| σ×1 trailing 6h \| recentre 12h \| now | 89.46 | 111.44 | 1.25 | 108.53 | 186.88 | 1.72 | 0.231 | 0.500 | 9 |
| σ×1 trailing 6h \| recentre 24h \| now | 85.39 | 113.61 | 1.33 | 99.23 | 193.63 | 1.95 | 0.297 | 1.000 | 7 |
| σ×1 trailing 24h \| hold \| now | 83.85 | 112.95 | 1.35 | 95.02 | 192.58 | 2.03 | — | — | 0 |
| σ×1 trailing 24h \| out 0m \| now | 99.85 | 116.51 | 1.17 | 116.76 | 192.22 | 1.65 | 0.260 | 1.001 | 8 |
| σ×1 trailing 24h \| out 5m \| now | 97.15 | 116.64 | 1.20 | 114.78 | 192.44 | 1.68 | 0.260 | 1.000 | 8 |
| σ×1 trailing 24h \| out 30m \| now | 92.92 | 114.19 | 1.23 | 111.10 | 192.68 | 1.73 | 0.260 | 1.019 | 8 |
| σ×1 trailing 24h \| out 120m \| now | 83.85 | 112.95 | 1.35 | 95.02 | 192.58 | 2.03 | 0.347 | 1.081 | 6 |
| σ×1 trailing 24h \| recentre 4h \| now | 96.96 | 115.96 | 1.20 | 133.51 | 193.28 | 1.45 | 0.122 | 0.167 | 17 |
| σ×1 trailing 24h \| recentre 12h \| now | 91.99 | 115.89 | 1.26 | 110.93 | 192.57 | 1.74 | 0.231 | 0.500 | 9 |
| σ×1 trailing 24h \| recentre 24h \| now | 86.70 | 113.12 | 1.30 | 100.31 | 192.63 | 1.92 | 0.297 | 1.000 | 7 |
| σ×2 placeholder \| hold \| now | 36.55 | 70.95 | 1.94 | 48.87 | 84.33 | 1.73 | — | — | 0 |
| σ×2 placeholder \| out 0m \| now | 36.55 | 70.95 | 1.94 | 48.87 | 84.33 | 1.73 | 0.351 | 7.048 | 6 |
| σ×2 placeholder \| out 5m \| now | 36.55 | 70.95 | 1.94 | 48.87 | 84.33 | 1.73 | 0.351 | 7.051 | 6 |
| σ×2 placeholder \| out 30m \| now | 36.55 | 70.95 | 1.94 | 48.87 | 84.33 | 1.73 | 0.351 | 7.069 | 6 |
| σ×2 placeholder \| out 120m \| now | 36.55 | 70.95 | 1.94 | 48.87 | 84.33 | 1.73 | 0.351 | 7.131 | 6 |
| σ×2 placeholder \| recentre 4h \| now | 38.07 | 43.11 | 1.13 | 76.55 | 65.51 | 0.86 | 0.124 | 0.167 | 17 |
| σ×2 placeholder \| recentre 12h \| now | 38.09 | 54.47 | 1.43 | 57.50 | 73.42 | 1.28 | 0.234 | 0.500 | 9 |
| σ×2 placeholder \| recentre 24h \| now | 36.92 | 67.88 | 1.84 | 51.69 | 82.31 | 1.59 | 0.300 | 1.000 | 7 |
| σ×2 trailing 1h \| hold \| now | 65.57 | 71.26 | 1.09 | 70.84 | 117.99 | 1.67 | — | — | 0 |
| σ×2 trailing 1h \| out 0m \| now | 65.57 | 71.26 | 1.09 | 70.84 | 117.99 | 1.67 | 0.510 | 2.310 | 4 |
| σ×2 trailing 1h \| out 5m \| now | 65.57 | 71.26 | 1.09 | 70.84 | 117.99 | 1.67 | 0.510 | 2.313 | 4 |
| σ×2 trailing 1h \| out 30m \| now | 65.57 | 71.26 | 1.09 | 70.84 | 117.99 | 1.67 | 0.510 | 2.331 | 4 |
| σ×2 trailing 1h \| out 120m \| now | 65.57 | 71.26 | 1.09 | 70.84 | 117.99 | 1.67 | 0.510 | 2.393 | 4 |
| σ×2 trailing 1h \| recentre 4h \| now | 69.91 | 75.41 | 1.08 | 102.68 | 124.75 | 1.21 | 0.136 | 0.167 | 15 |
| σ×2 trailing 1h \| recentre 12h \| now | 67.17 | 71.05 | 1.06 | 79.83 | 115.02 | 1.44 | 0.292 | 0.500 | 7 |
| σ×2 trailing 1h \| recentre 24h \| now | 66.52 | 71.57 | 1.08 | 74.25 | 118.40 | 1.59 | 0.408 | 1.000 | 5 |
| σ×2 trailing 6h \| hold \| now | 53.34 | 57.73 | 1.08 | 65.56 | 98.64 | 1.50 | — | — | 0 |
| σ×2 trailing 6h \| out 0m \| now | 53.34 | 57.73 | 1.08 | 65.56 | 98.64 | 1.50 | 0.347 | 4.202 | 6 |
| σ×2 trailing 6h \| out 5m \| now | 53.34 | 57.73 | 1.08 | 65.56 | 98.64 | 1.50 | 0.347 | 4.205 | 6 |
| σ×2 trailing 6h \| out 30m \| now | 53.34 | 57.73 | 1.08 | 65.56 | 98.64 | 1.50 | 0.347 | 4.223 | 6 |
| σ×2 trailing 6h \| out 120m \| now | 53.34 | 57.73 | 1.08 | 65.56 | 98.64 | 1.50 | 0.347 | 4.285 | 6 |
| σ×2 trailing 6h \| recentre 4h \| now | 54.32 | 57.71 | 1.06 | 92.77 | 97.36 | 1.05 | 0.122 | 0.167 | 17 |
| σ×2 trailing 6h \| recentre 12h \| now | 52.66 | 56.06 | 1.06 | 72.13 | 94.00 | 1.30 | 0.231 | 0.500 | 9 |
| σ×2 trailing 6h \| recentre 24h \| now | 53.43 | 57.36 | 1.07 | 68.13 | 97.83 | 1.44 | 0.297 | 1.000 | 7 |
| σ×2 trailing 24h \| hold \| now | 53.40 | 57.76 | 1.08 | 65.61 | 98.64 | 1.50 | — | — | 0 |
| σ×2 trailing 24h \| out 0m \| now | 53.40 | 57.76 | 1.08 | 65.61 | 98.64 | 1.50 | 0.347 | 3.831 | 6 |
| σ×2 trailing 24h \| out 5m \| now | 53.40 | 57.76 | 1.08 | 65.61 | 98.64 | 1.50 | 0.347 | 3.834 | 6 |
| σ×2 trailing 24h \| out 30m \| now | 53.40 | 57.76 | 1.08 | 65.61 | 98.64 | 1.50 | 0.347 | 3.852 | 6 |
| σ×2 trailing 24h \| out 120m \| now | 53.40 | 57.76 | 1.08 | 65.61 | 98.64 | 1.50 | 0.347 | 3.914 | 6 |
| σ×2 trailing 24h \| recentre 4h \| now | 55.35 | 58.10 | 1.05 | 93.61 | 96.96 | 1.04 | 0.122 | 0.167 | 17 |
| σ×2 trailing 24h \| recentre 12h \| now | 54.64 | 58.95 | 1.08 | 74.15 | 97.98 | 1.32 | 0.231 | 0.500 | 9 |
| σ×2 trailing 24h \| recentre 24h \| now | 54.00 | 57.80 | 1.07 | 68.66 | 98.56 | 1.44 | 0.297 | 1.000 | 7 |

### F.2 Stability — model / simulator (LVR + hedge) per UTC day, headline top 10

| policy | 2026-09-27 | 2026-09-28 |
| --- | ---: | ---: |
| σ×0.5 trailing 1h \| out 5m \| now | 1.76 | 1.37 |
| σ×0.5 trailing 1h \| out 0m \| now | 1.68 | 1.20 |
| σ×0.5 trailing 1h \| out 120m \| stable 20m | 2.11 | 1.82 |
| σ×0.5 trailing 24h \| out 120m \| stable 20m | 1.96 | 1.65 |
| σ×0.5 trailing 1h \| recentre 12h \| stable 20m | 2.11 | 2.21 |
| σ×0.5 trailing 1h \| out 30m \| stable 20m | 2.11 | 1.78 |
| σ×0.5 trailing 1h \| recentre 4h \| now | 2.42 | 1.58 |
| σ×0.5 trailing 1h \| out 0m \| stable 20m | 1.91 | 1.31 |
| σ×0.5 trailing 1h \| out 120m \| now | 2.35 | 1.82 |
| σ×0.5 trailing 1h \| recentre 12h \| now | 2.35 | 2.07 |

## G. Regime σ multipliers — measured, not ratified ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §2.4)

All 291 non-overlapping 300 s returns: σ = 1.275e-4/s. 14 wall-covered ticks skipped for a missing spot.

| regime (label \| spot vs ZGL) | returns | σ per second | multiplier | 95% interval of σ |
| --- | ---: | ---: | ---: | ---: |
| POSITIVE_GEX\|above | 254 | 1.203e-4 | 0.943 | 1.10e-4 – 1.31e-4 |
| POSITIVE_GEX\|below | 37 | 1.689e-4 | 1.325 | 1.30e-4 – 2.07e-4 |

## Caveats

- **Short data.** The archive run started 2026-09-27; walls exist only where TICKET T recorded them. Trust a ranking only once it holds across UTC days and [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-windows.
- **Only the sampled active bin earns.** A 30 s interval that crossed several bins earned in each; this credits one.
- **Pool liquidity is the latest 5-minute snapshot**, and the position dilutes only through its share of the active bin.
- **No measured volume, funding or taker series.** Those costs are placeholders; the fee side is in units of V.
- **Shape weights follow the Meteora SDK as value shares at open**, not its exact per-side token amounts.
- **The σ-window placement is unclamped by walls** (the pure [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] policy); the live planner also clamps to the buffered envelope, which does not bind at today's σ.
