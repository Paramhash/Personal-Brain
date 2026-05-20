---
tags: [entity, preprocessing, machine-learning, scaling, statistics]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# RobustScaler

`RobustScaler` is a preprocessing technique used in machine learning to scale features. Unlike `StandardScaler` or `MinMaxScaler`, `RobustScaler` is designed to handle outliers effectively. It scales features using statistics that are robust to outliers, specifically the median and the interquartile range (IQR).

**Scaling Formula:** `(x - median) / IQR`

Where:
*   `x` is the feature value.
*   `median` is the median of the feature in the training data.
*   `IQR` is the interquartile range (75th percentile - 25th percentile) of the feature in the training data.

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], `RobustScaler` is applied to all 7 features before they are fed into the [[../concepts/gaussian-hmm.md|GaussianHMM]]. This is crucial because financial market data, especially derived features, can often contain outliers that would disproportionately affect non-robust scaling methods. The scaler is fitted on the training corpus and then saved to `data/models/scaler.pkl` for consistent reuse during live inference.

---