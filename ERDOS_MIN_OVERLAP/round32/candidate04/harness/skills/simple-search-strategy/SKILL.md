---
name: simple-search-strategy
description: Use simple functional forms (bipartite, trimodal, symmetric) to escape seed's local minima.
---

# Simple Search Strategy for Erdos C5

## Why This Works

The seed optimizer uses 14 complex initialization patterns that all share similar structures.
This traps the search in local minima. We need STRUCTURALLY DIFFERENT functions.

## Three Simple Forms to Try

### 1. Bipartite (Single Threshold)
h(x) = sigmoid(k*(x - a))
- Simple step function
- Try different threshold positions: a = 0.5, 0.75, 1.0, 1.25, 1.5
- Adjust scaling to ensure integral(h) ≈ 1

### 2. Trimodal (Three Peaks)
h(x) = sum of 3 Gaussian-like peaks
- Place peaks at different configurations
- E.g., [0.3, 1.0, 1.7], [0.25, 0.9, 1.6], [0.4, 1.0, 1.6]
- Vary peak heights and widths

### 3. Symmetric Functions
h(x) ≈ h(2-x)
- Mirror symmetry might reduce overlap
- Try triangular, trapezoidal, or multi-peak symmetric shapes

## Workflow

1. Generate 2-3 candidates from EACH simple form (6-9 total)
2. Call PROBE_SIMPLE on each
3. Keep top 3 with combined_score > 1.0 (c5_bound < 0.382)
4. Call FULL EVALUATION on top 2
5. If no improvement, try LOCALIZED modifications

## Key Rules

- START WITH SIMPLE forms, not complex multi-pattern
- USE PROBE to screen before full eval
- ENSURE integral(h) ≈ 1 (use penalty_strength=100)
- FOCUS on STRUCTURAL diversity, not hyperparameter tuning
