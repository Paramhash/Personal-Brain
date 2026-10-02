---
domain: cl-market-making
tags:
- dlmm
- inventory-control
- risk-management
- strategy
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- fae7383e353beebd
---
# Warehouse Manager CL Inventory Strategy (dlmm, 2026)
**Type:** docs
## Claim
The document outlines a comprehensive strategy for a Concentrated Liquidity (CL) market-making bot, emphasizing hierarchical inventory management, disciplined capital allocation, and robust entry/exit conditions to prioritize operational survival and achieve positive equity growth relative to a passive benchmark.
## Method and data
This document is a policy recommendation for the design and operation of a CL market-making bot. It defines operational principles, mathematical conditions for deployment and withdrawal, and success metrics. It draws upon concepts like GEX walls, volatility allowances, and economic hurdle rates, referencing internal repository components (e.g., `hurdleRate.ts`, `binanceHedge.ts`).
## Key results
The core policy recommends:
1.  **Inventory Segregation:** Maintain untouched [[sol-rent-reserve]] and [[sol-execution-reserve]].
2.  **Strategic Deployment:** Deploy only surplus capital into a [[cl-position]] within a [[buffered-policy-envelope]], using a narrower [[sigma-derived-deployed-window]].
3.  **Hedging:** Continuously hedge the [[sol-inventory]] to manage directional exposure.
4.  **Proactive Exit:** Withdraw before the range becomes unsafe ([[boundary-threat-exit]]) or economically unviable ([[negative-economics-exit]]), or upon [[regime-deterioration-exit]].
5.  **Success Metrics:** Prioritize operational integrity (no collateral breach, reserves preserved) and aim for equity growth ($E_{close} > E_{start}$) and outperformance of a [[hodl-benchmark]].
## Assumptions and limits
This document assumes the existence of a CL market-making bot capable of managing multiple inventories, executing hedges, and monitoring various market signals (GEX, volatility). It is an internal policy document, not a research paper with empirical evidence. The effectiveness of the strategy depends on the accuracy of volatility forecasts, GEX signals, and the ability to execute trades efficiently.
## Concepts introduced or used
[[warehouse-manager-cl-inventory-strategy]]
[[sol-inventory]]
[[usdc-inventory]]
[[cl-position]]
[[sol-rent-reserve]]
[[sol-execution-reserve]]
[[market-boundaries-cl]]
[[buffered-policy-envelope]]
[[sigma-derived-deployed-window]]
[[cl-entry-strategy]]
[[economic-hurdle-rate-cl]]
[[capital-allocation-rule-cl]]
[[cl-position-monitoring]]
[[cl-hedge-target]]
[[cl-rebalancing-condition]]
[[cl-exit-strategy]]
[[boundary-threat-exit]]
[[negative-economics-exit]]
[[regime-deterioration-exit]]
[[cl-closing-procedure]]
[[cl-success-metrics]]
[[hodl-benchmark]]
[[slippage]]
[[risk-premium]]
[[transaction-latency]]
[[network-congestion]]
[[liquidity-concentration]]
[[zero-gamma-level]]
[[market-regime-transition]]