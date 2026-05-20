---
tags: ["options trading", "systematic trading", "data pipeline", "backtesting", "1DTE", "7DTE"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Systematic Options Trading Pipeline (1DTE-7DTE)

This document outlines a modular, low-latency data processing pipeline designed for systematic options trading strategies targeting short-duration expirations (1 Day To Expiry - 1DTE, up to 7 Days To Expiry - 7DTE). The core objective is to accurately align spot price, options chain dynamics, and structural market indicators to inform trading decisions, while strictly eliminating [[../concepts/look-ahead-bias-in-backtesting.md|look-ahead bias]].

The pipeline relies on a [[../concepts/event-driven-architecture-for-trading.md|strictly decoupled event-driven flow]] to ensure indicators like [[../concepts/hidden-markov-model-hmm-in-finance.md|Hidden Markov Model (HMM)]] regimes and [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] profiles are generated purely on historical data *prior* to the execution window.

## The Structural Triad

Advanced systematic options traders utilize a "structural triad" formed by combining:
1.  **[[../concepts/hidden-markov-model-hmm-in-finance.md|Hidden Markov Model (HMM)]]:** For identifying latent market regimes.
2.  **[[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] Profile:** To understand market positioning and potential price magnets/repellents.
3.  **[[../concepts/volatility-risk-premium-vrp.md|Volatility Risk Premium (VRP)]] (IV-HV Skew):** To assess the attractiveness of selling or buying volatility.

These three components are integrated into a "Pre-Trade State Matrix" that serves as the single source of truth for strategy execution.

## High-Level Data Flow Architecture

The pipeline progresses through distinct stages:

```
  [ Raw Data Ingestion ]
           │
           ├──► Spot / Index Bars (1-Min, Hourly, Daily)
           └──► End-of-Day or Intraday Options Chains (All Strikes, Deltas, Open Interest)
           │
  [ Stage 1: Feature Engineering Engine ]
           │
           ├──► GEX Processor ──► Compute Spot GEX & Gamma Profile Curves
           ├──► Volatility Engine ──► Calculate Rolling RV & Surface IV to isolate VRP
           └──► Signal Assembler ──► Standardize Log Returns & Volatility for HMM
           │
  [ Stage 2: Latent Regime Engine (HMM) ]
           │
           └──► Unsupervised State Classifier (e.g., GaussianHMM) ──► Macro Regime Tag
           │
  [ Stage 3: The Pre-Trade State Matrix ]
           │
           └──► Join: [ GEX Profile ] + [ HMM Regime ] + [ VRP Matrix ] by Timestamp
           │
  [ Stage 4: Strategy Execution & Backtest Core ]
           │
           └──► Vectorized / Event-Driven Strategy Engine ──► Performance Logs / Equity Curve
```

## Pipeline Stage Breakdown

### Stage 1: Raw Data Ingestion & Alignment

Requires high-fidelity, time-stamped data:
*   **Spot Feed:** 1-minute or hourly OHLCV data for the underlying index/equity.
*   **Options Chain Feed:** Time-stamped chains with Strike, Expiry, Type, Implied Volatility, Delta, Open Interest, Bid/Ask.
*   **Ingestion Rule:** Data is indexed by a unified nanosecond/millisecond UTC timestamp to prevent mismatches.

### Stage 2: Feature Engineering & Pre-Processors

Raw data is processed in parallel:
*   **[[../concepts/gamma-exposure-gex.md|GEX Calculation Module]]:** Computes total dollar Gamma Exposure.
*   **[[../concepts/volatility-risk-premium-vrp.md|Volatility & VRP Module]]:** Calculates Realized Volatility (RV), At-The-Money (ATM) Implied Volatility (IV), and the Volatility Risk Premium (VRP).

### Stage 3: The Latent Regime Engine (HMM)

The [[../concepts/hidden-markov-model-hmm-in-finance.md|HMM]] ingests a clean feature array (e.g., `[Daily_Log_Returns, Intraday_Parkinson_Vol, VRP_Trend, GEX_ZScore]`) and decodes features into discrete state sequences. Crucially, it uses an [[../concepts/hidden-markov-model-hmm-in-finance.md#training-window-constraints|Anchored or Rolling Walk-Forward Window]] for training to avoid look-ahead bias.

### Stage 4: The Pre-Trade State Matrix

Before execution, a flat, queryable data record is compiled for each interval, combining GEX profile, HMM regime, and VRP matrix by timestamp. This record acts as the single source of truth for trading logic.

## Strategy Execution & Backtest Core

The Backtest Core functions as a state machine, querying the pre-trade record to make decisions based on GEX, HMM state, and VRP thresholds. For detailed considerations in this stage, refer to [[../research/backtesting-best-practices-for-short-duration-options.md|Backtesting Best Practices for Short-Duration Options]].