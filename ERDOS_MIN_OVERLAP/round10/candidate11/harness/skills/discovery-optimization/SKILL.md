---
name: discovery-optimization
description: "Structural initialization injection for Erdos optimizer with probe-based screening."
---

# Erdos Minimum Overlap - Structural Initialization Strategy

## Why Structural Innovation is Critical
The seed optimizer uses continuous optimization with 12 fixed initialization patterns.
This approach gets trapped in local minima. The Erdos minimum overlap problem likely
requires discrete combinatorial structures that lie outside the optimizer's natural
basin of attraction.

## Phase 1: Inject Diverse Structural Patterns

Edit _get_best_initialization() to add NEW initialization patterns:

### 1. Bimodal Tight Patterns
Two narrow peaks with optimized separation at positions like (0.2, 0.8), (0.25, 0.75)

### 2. Asymmetric Step Functions  
h(x) = alpha for x < tau, h(x) = beta for x >= tau, tuned for integral=1

### 3. Triangular Patterns
Linear ramps creating peak/trough structures at various positions

### 4. Multi-Level Step Functions
3-4 levels with strategic transitions

### 5. Periodic Combinations
sin/cos combinations with different frequencies

## Phase 2: Enhanced Hyperparameter Exploration
For each NEW pattern, test 2-3 hyperparameter combinations:
- num_intervals: 400, 800
- base_learning_rate: 0.003, 0.007, 0.015
- penalty_strength: 100, 500

## Screening Strategy
1. Use probe_solution to quickly check constraint satisfaction
2. Only evaluate variants with good probe scores
3. Track best combined_score across ALL patterns
