---
tags: [options, quantitative-finance, machine-learning, hidden-markov-model, market-microstructure, spx, spy]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Near-Expiry Hidden Markov Model for SPX/SPY Options Dynamics

This document outlines the design and implementation of a [[../concepts/hidden-markov-model.md|Hidden Markov Model (HMM)]] specifically tailored to classify latent market microstructure regimes for [[../entities/spx-index.md|SPX]] and [[../entities/spy-etf.md|SPY]] options within the critical 7 Days To Expiry (DTE) to 1 DTE window. Unlike macro regime models, this model focuses on expiry-specific dynamics, identifying states such as pinning, mean-reverting, or gamma-squeeze.

## Context and Purpose

The primary goal is to provide real-time classification of near-expiry options market behavior. This model operates alongside existing data pipelines, consuming [[../entities/chainsnapshot-dataclass.md|ChainSnapshot]] data from [[../entities/dxfeed.md|dxFeed]] and intraday OHLC data.

## Repository Structure

The project is structured into `hmm/` for model components, `data/` for historical and model artifacts, `scripts/` for data ingestion and live operations, and `tests/` for validation.

```
hmm/
  __init__.py
  features.py      # Feature extraction
  train.py         # Baum-Welch training
  inference.py     # Forward algorithm for live inference
  validate.py      # Out-of-sample validation
  schema.py        # Output dataclass: NearExpiryHMMState
data/
  historical/      # ThetaData bulk pull outputs
  models/          # Fitted GaussianHMM pickle files
scripts/
  pull_historical.py   # ThetaData bulk pull
  backfill_features.py # Build DTE-aligned feature matrix
  run_live.py          # Live inference loop
tests/
  test_features.py
  test_hmm_output.py
```

## Data Sources

Historical data is sourced via the [[../entities/thetadata.md|ThetaData]] Python client, pulling SPX and SPY weekly expirations from 2022-01-01 to 2026-04-30. Data is sampled at specific intraday times (09:35, 10:30, 11:30, 12:30, 13:30, 14:30, 15:00, 15:45 ET) for each DTE from 7 down to 1. This includes full options chains (bid, ask, mid, volume, OI, gamma, delta, IV) and underlying 1-minute OHLC bars. [[../entities/vix-index.md|VIX]] data for tiering can also be sourced from ThetaData or [[../entities/polygon-io.md|Polygon.io]].

## Feature Vector

For each (underlying, expiration, snapshot_timestamp, DTE) observation, 7 features are computed:

1.  [[../concepts/gex-concentration-at-expiry.md|GEX Concentration at Expiry]]
2.  [[../concepts/spot-to-gamma-wall-distance.md|Spot to Gamma Wall Distance]]
3.  [[../concepts/atm-gamma-velocity.md|ATM Gamma Velocity]]
4.  [[../concepts/oi-concentration-ratio.md|OI Concentration Ratio]]
5.  [[../concepts/realized-vol-intraday.md|Realized Volatility Intraday]] (using [[../concepts/parkinson-volatility-estimator.md|Parkinson estimator]])
6.  [[../concepts/atm-iv-dte-slope.md|ATM IV DTE Slope]]
7.  [[../concepts/call-put-volume-ratio.md|Call/Put Volume Ratio]]

All features are normalized using [[../entities/robustscaler.md|RobustScaler]], fitted on the training corpus.

## HMM Specification

The model uses `hmmlearn==0.3.x` and is a [[../concepts/gaussian-hmm.md|GaussianHMM]] with `n_components=3`, `covariance_type="full"`, and `n_iter=200`.

### State Labels

States are assigned post-training based on the realized volatility ordering of their mean (`μ_k[realized_vol_intraday]`):

*   **State 0 (lowest μ):** [[../concepts/market-regime-pinning.md|Pinning]]
*   **State 1 (middle μ):** [[../concepts/market-regime-mean-reverting.md|Mean-Reverting]]
*   **State 2 (highest μ):** [[../concepts/market-regime-gamma-squeeze.md|Gamma Squeeze]]

This ordering ensures state label stability across refits.

### Training

Each expiration cycle forms a sequence for training. Models are stratified into two tiers based on [[../entities/vix-index.md|VIX]] at the cycle start:
*   **Tier A:** VIX < 20
*   **Tier B:** VIX ≥ 20

An 80/20 train/test split is used (2022-2025 for training, Jan-Apr 2026 for holdout). A minimum of 200 training cycles per tier is required; otherwise, tiers are merged.

## Output Schema

The model outputs a `NearExpiryHMMState` dataclass containing:
*   `underlying`, `expiration`, `dte`, `snapshot_time`
*   `state_label` (0, 1, 2)
*   `state_semantics` ("pinning", "mean_reverting", "gamma_squeeze")
*   `posterior_probs` (list of probabilities for each state)
*   `transition_row` (transition probabilities from the current state)
*   `regime_persistence_expected_bars` (expected duration in current state)
*   `vix_tier`, `model_fit_date`
*   `features_used` (raw feature values for audit)

This output is emitted as JSON.

## Inference (Live Mode)

Inference involves computing the 7 features for a current snapshot, scaling them, selecting the appropriate VIX-tier model, and then running `model.predict_proba()` (using the [[../concepts/forward-algorithm.md|Forward algorithm]]) and `model.predict()` (for the Viterbi state) to return the `NearExpiryHMMState`. Updates occur every 15 minutes, with nightly model refits.

## Validation

Validation includes:
1.  Log-likelihood on the holdout set.
2.  State assignment consistency for known pinning days.
3.  Event-date spot-checks for specific historical events (e.g., 2024-08-05 VIX spike, 2023-03-10 SVB failure).
4.  State stability across refits (transition matrix Frobenius norm).
5.  AIC/BIC K-selection table to confirm `n_components=3` is optimal.

## Constraints and Caveats

*   **IV Usage:** `atm_iv_dte_slope` is the only feature permitted to use BSM-derived IV.
*   **SPX AM-settlement:** Specific correction for DTE=1 SPX `time_to_expiry_years`.
*   **SPY Dividend Yield:** `dividend_yield=0.013` must be passed to `enrich_contract_snapshot`.
*   **Burn-in:** No live state emission until 30 trading days of data are collected.
*   **State Re-anchoring:** States are re-sorted by `mu_k[realized_vol_intraday]` after every refit.

This system provides a robust framework for understanding and reacting to short-term options market dynamics.

---