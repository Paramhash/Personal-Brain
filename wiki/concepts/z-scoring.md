---
tags: ["data-preprocessing", "normalization", "statistics"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Z-scoring

Z-scoring, also known as standardization, is a data normalization technique that transforms data to have a mean of 0 and a standard deviation of 1. It is calculated by subtracting the mean of the dataset from each data point and then dividing by the standard deviation.

## Formula
$Z = (X - \mu) / \sigma$
Where:
*   $X$ is an individual data point
*   $\mu$ is the mean of the dataset
*   $\sigma$ is the standard deviation of the dataset

## Application in Zero-Cost Feature Engineering
In the context of [[../concepts/zero-cost-feature-engineering.md]], Z-scoring is applied **cross-sectionally** to the engineered features. This means that for a given feature (e.g., [[../concepts/cross-sectional-momentum.md]]), the values for all 100 stocks in the [[../entities/nasdaq-100.md]] index are standardized against each other at a specific point in time.

This cross-sectional Z-scoring is crucial because it:
*   **Enables Comparison**: Allows the [[../concepts/reinforcement-learning-agent.md]] to compare stocks relative to each other within the same universe, rather than relying on absolute values which might have different scales or distributions.
*   **Removes Bias**: Helps to remove potential biases introduced by differing magnitudes of features across different stocks or over time.
*   **Improves Model Performance**: Standardized inputs can often lead to faster convergence and better performance for machine learning models.

---
### Related Concepts
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../concepts/cross-sectional-momentum.md]]
*   [[../concepts/feature-engineering.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].