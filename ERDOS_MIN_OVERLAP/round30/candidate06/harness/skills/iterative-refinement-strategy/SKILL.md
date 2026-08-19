---
name: iterative-refinement-strategy
description: Use both diverse initialization and iterative refinement to explore solution space.
---

# Iterative Refinement for Erdos C5

## Core Principle
Combine diverse initializations with systematic local search.
Don't rely on hyperparameter tuning alone.

## Step-by-Step Workflow

1. INITIALIZE with search_patterns
   - Generate 5-10 diverse step functions
   - Screen with probe_solution
   - Identify best candidate (lowest c5_bound)

2. REFINEMENT with explore_neighbors (if needed)
   - If best combined_score <= 1.0, call explore_neighbors
   - Strategy choices:
     * shift_peak: Move peaks left/right by small delta
     * split_peak: Divide largest peak into two smaller peaks
     * merge_peaks: Combine adjacent peaks
     * adjust_threshold: Modify threshold positions
   - Set magnitude=0.15 for conservative edits
   - Generate 5-7 variants
   - Screen ALL variants with probe_solution
   - Evaluate only those with c5_bound < 0.375

3. ITERATE
   - If refinement yields improvement, continue refining
   - If no improvement after 2 refinement rounds, try different strategies
   - Eventually try hyperparameter tuning as last resort

## Key Rules
- ALWAYS use probe_solution before evaluate_solution
- Never waste evals on c5_bound > 0.375
- Track best c5_bound across all iterations
- Use magnitude=0.15-0.25 for conservative exploration
- If explore_neighbors fails twice, try shift_peak vs split_peak
