---
name: step-function-construction
description: Generate step function patterns with exact integral constraint.
---

# Step Function Construction

## Core Requirement
For N=800 intervals: sum(h) = 400 exactly
Values must be in {0.0, 0.5, 1.0}

## Patterns to Try
1. Bimodal: ones at edges [1]*200 + [0.5]*400 + [1]*200
2. Golomb: ones at [0, 200, 500, 750, 800] with 0.5 fill
3. Alternating: [1, 0.5, 1, 0.5] * 200
4. Concentrated: [1]*150 + [0.5]*400 + [1]*50

## Editing Guide
Replace _get_best_initialization() return with your step pattern.
Verify sum(h) ≈ 400 before calling evaluate_solution.
