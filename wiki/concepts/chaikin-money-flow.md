---
tags: ["feature-engineering", "technical-analysis", "volume-analysis", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Chaikin Money Flow (CMF)

Chaikin Money Flow (CMF) is a technical indicator used as a feature in [[../concepts/zero-cost-feature-engineering.md]] to track equity capital flow, serving as a replacement for options Put/Call Volume data.

## Logic
CMF measures the amount of money flowing into or out of a security. It assesses whether a stock is closing in the upper or lower half of its daily range, and then multiplies this by volume. A negative CMF divergence, particularly when prices remain flat, can indicate heavy institutional distribution (selling pressure).

## Calculation
CMF is calculated based on standard daily high, low, close, and volume data. The specific formula typically involves:
1.  **Money Flow Multiplier (MFM)**: `((Close - Low) - (High - Close)) / (High - Low)`
2.  **Money Flow Volume (MFV)**: `MFM * Volume`
3.  **CMF**: Sum of MFV over a specified period (e.g., 20 or 21 days) divided by the sum of volume over the same period.

## Data Cost
This feature can be derived entirely from standard daily high, low, close, and volume data, incurring $0.00 in data costs.

---
### Related Concepts
*   [[../concepts/feature-engineering.md]]
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../entities/pandas-ta.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].