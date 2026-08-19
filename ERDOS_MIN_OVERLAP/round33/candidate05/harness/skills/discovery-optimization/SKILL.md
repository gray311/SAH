---
name: discovery-optimization
description: "Hyperparameter tuning first. Systematically vary num_intervals, learning_rate, steps, penalty_strength. Use probe to screen, evaluate best."
---

# Erdos C5 Optimization - Analysis-Driven Approach

## Phase 1: Correlation Analysis (CRITICAL)

1. CALL correlation_analyzer on the current best program
   - This computes the full correlation structure
   - Identifies which shifts k have the highest overlap
   - Returns the top 5 problematic k values

2. EXAMINE the problematic shifts
   - These are the k values where h(x)(1-h(x+k)) is largest
   - We need to reduce overlap at these specific shifts

3. Use structure_inspired_mutations with target_shifts=[problematic_k_values]
   - This creates mutations specifically designed to reduce overlap at those k values
   - Not random mutations - targeted structural changes

## Phase 2: Targeted Search

1. Generate 3-5 targeted mutations using structure_inspired_mutations
2. CALL probe_solution on each to screen
3. Evaluate the best 1-2 candidates

## Phase 3: If No Improvement

If analysis-driven approach fails, try different starting points:
- Bipartite functions (single threshold)
- Multi-modal functions (3-4 peaks)
- Golomb ruler-like distributions

## Key Rules
- ALWAYS start with correlation_analyzer
- Use the problematic k values to guide mutations
- NEVER do random hyperparameter tuning without analysis
- Evaluate only on candidates with c5_bound < 0.375
