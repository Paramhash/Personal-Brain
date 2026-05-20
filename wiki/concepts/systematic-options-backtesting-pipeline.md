---
tags: ["options-trading", "backtesting", "data-pipeline", "systematic-trading", "low-latency"]
created: 2023-10-27
reviewed: false
source_origin: "HMM-derived probability estimates compare to other methods.md"
---
# Systematic Options Backtesting Pipeline (1DTE-7DTE)

This document outlines a modular, low-latency data processing pipeline specifically designed for systematic options backtesting, targeting short-duration trades (1 Day To Expiration - 1DTE to 7DTE). The architecture emphasizes a [[../concepts/event-driven-architecture.md|strictly decoupled event-driven flow]] to ensure high accuracy and eliminate [[../concepts/look-ahead-bias.md|look-ahead bias]].

## Core Principles

*   **Decoupled Event-Driven Flow:** Ensures that all indicators (e.g., [[../concepts/gamma-exposure-gex.md|GEX]], HMM states) are generated purely on historical data *prior* to the execution window.
*   **High-Fidelity Data:** Requires precise alignment of spot price, options chain dynamics, and structural market indicators, often indexed by nanosecond or millisecond UTC timestamps.

## High-Level Data Flow Architecture

The pipeline progresses through several stages:

1.  **Raw Data Ingestion:**
    *   Spot / Index Bars (1-Min, Hourly, Daily OHLCV)
    *   End-of-Day or Intraday Options Chains (All Strikes, Deltas, Open Interest, Bid/Ask)
2.  **Feature Engineering Engine:**
    *   [[../concepts/gamma-exposure-gex.md|GEX Processor]]: Computes Spot GEX & Gamma Profile Curves.
    *   Volatility Engine: Calculates Rolling [[../concepts/realized-volatility.md|Realized Volatility (RV)]] & Surface [[../concepts/implied-volatility.md|Implied Volatility (IV)]] to isolate [[../concepts/volatility-risk-premium-vrp.md|VRP]].
    *   Signal Assembler: Standardizes Log Returns & Volatility for HMM input.
3.  **Latent Regime Engine (HMM):**
    *   Unsupervised State Classifier (e.g., GaussianHMM) decodes features into a Macro Regime Tag.
4.  **The Pre-Trade State Matrix:**
    *   Joins GEX Profile, HMM Regime, and VRP Matrix by Timestamp into a single, queryable record.
5.  **Strategy Execution & Backtest Core:**
    *   Vectorized / Event-Driven Strategy Engine processes the pre-trade record to generate performance logs and equity curves.

## In-Depth Pipeline Stage Breakdown

### Stage 1: Raw Data Ingestion & Alignment

Requires high-fidelity, time-stamped data for both underlying spot prices and comprehensive options chains. Data is indexed by a unified nanosecond or millisecond UTC timestamp.

### Stage 2: Feature Engineering & Pre-Processors

Raw data is processed in parallel by specialized modules:

*   **A. The GEX Calculation Module:** Calculates Gamma ($\Gamma$) for each option contract and then aggregates total dollar [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] across the chain. Outputs include Net GEX and localized GEX concentrations.
*   **B. The Volatility & VRP Module:**
    *   Computes [[../concepts/realized-volatility.md|Realized Volatility (RV)]] over a short lookback window.
    *   Isolates At-The-Money (ATM) [[../concepts/implied-volatility.md|Implied Volatility (IV)]] for target expirations (1DTE-7DTE).
    *   Calculates [[../concepts/volatility-risk-premium-vrp.md|Volatility Risk Premium (VRP)]] as $\text{IV}_{\text{ATM}} - \text{RV}$.

### Stage 3: The Latent Regime Engine ([[../concepts/hidden-markov-models-in-finance.md|HMM]])

The HMM processes clean feature arrays (e.g., `[Daily_Log_Returns, Intraday_Parkinson_Vol, VRP_Trend, GEX_ZScore]`) rather than raw prices. It is trained using an Anchored or Rolling Walk-Forward Window to prevent [[../concepts/look-ahead-bias.md|look-ahead bias]] and uses Viterbi Decoding to output discrete state labels.

## Data Schema Model (The Combined Pre-Trade Record)

A flat, queryable JSON record is compiled for every discrete execution interval, serving as the single source of truth for trading logic. It includes:
*   `timestamp`, `underlying`, `spot_price`
*   `features` (e.g., `net_gex_billions`, `gex_flip_price`, `current_vrp_bps`, `put_call_skew_30delta`)
*   `regime` (e.g., `hmm_state`, `state_label`, `state_probability`)
*   `chain_snapshot_id`

## Signal Integration & Strategy Gatekeeper Logic

The Backtest Core acts as a state machine, querying the pre-trade record to make decisions. It typically involves sequential checks:
1.  **GEX Check:** Is Net GEX negative or near a flip? (Influences directional vs. premium selling strategies).
2.  **HMM Regime Check:** Evaluate the decoded HMM state (e.g., "Trending" vs. "Mean-Reverting").
3.  **VRP Check:** Is VRP above a strategy threshold? (Determines if premium is sufficient for risk).
4.  **Trade Execution:** If all gates pass, a specific trade structure (e.g., Sell Iron Condor) is executed.

## Production Implementation Tips

*   **Avoid Data Leakage on HMM:** Use a sliding window for HMM updates that strictly precedes the trade entry time.
*   **Handle Option Expirations Cleanly:** Ensure continuous availability of 1DTE-7DTE data; log errors for missing or illiquid expirations.
*   **Incorporate Transaction Costs & Slippage:** Model realistic execution prices (bid for short options, ask for long options) rather than mid-market prices.

This pipeline provides a robust framework for developing and testing short-duration options strategies, integrating advanced indicators like HMM and GEX with rigorous data handling.