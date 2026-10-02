---
domain: cl-market-making
tags:
- dlmm
- inventory-control
- fee-economics
- market-making-strategy
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-00-dual-inventory-growth-policy.md
ingest_hashes:
- 936a7eb3d3a22951
---
# Dual-Inventory Growth Policy for a Concentrated-Liquidity Bot (internal, 2026)
**Type:** docs
## Claim
A concentrated liquidity (CL) market-making bot should target positive growth in both its base and quote assets independently, rather than merely maximizing overall equity. This "dual-inventory" objective requires a specific policy and a decision gate that evaluates expected growth against a zero-growth baseline, accounting for all costs and risks.
## Method and data
This document outlines a policy for the internal DLMM hedge bot, defining its operational objectives and decision-making framework. It does not present empirical data or a specific research method, but rather a strategic directive for bot behavior.
## Key results
The policy establishes:
1.  A `[[zero-growth-baseline]]` for evaluation: $\Delta SOL = 0, \Delta USDC = 0$.
2.  A `[[dual-inventory-growth-policy]]` objective: $SOL_{close} > SOL_{start}$ and $USDC_{close} > USDC_{start}$, while preserving a rent reserve.
3.  A `[[decision-gate-cl-bot]]` for deployment: $\mathbb{E}[\Delta SOL] > 0$ and $\mathbb{E}[\Delta USDC] > 0$, potentially with probability requirements like $P(\Delta SOL > 0) \geq p_{min}$ and $P(\Delta USDC > 0) \geq p_{min}$.
4.  The necessity of `[[two-accounting-layers]]`: `[[equity-accounting]]` for overall value and `[[inventory-accounting]]` for individual token balances.
## Assumptions and limits
The policy assumes the context of a concentrated liquidity market-making bot operating with SOL and USDC. It implicitly assumes that maintaining and growing specific asset quantities is critical for the bot's long-term operational viability and strategic goals, beyond simple equity maximization. It also assumes the ability to estimate expected fees, LVR, hedge, gas, rent, and slippage costs.
## Concepts introduced or used
[[dual-inventory-growth-policy]], [[zero-growth-baseline]], [[equity-accounting]], [[inventory-accounting]], [[decision-gate-cl-bot]], [[m07-inventory-and-market-making-theory|inventory control]], [[m05-fee-economics|fee economics]], [[m04-lvr-and-impermanent-loss|LVR]]