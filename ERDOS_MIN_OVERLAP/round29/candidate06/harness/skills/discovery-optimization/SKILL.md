---
name: discovery-optimization
description: "Focus on structural mutations of h (shift peaks, split/merge regions). Use mutate_h_structure to generate diverse step functions, screen with probe, evaluate top candidates."
---

# Structural Search for Erdos C5

## Phase 1: Structural Mutation (PRIMARY STRATEGY)

1. CALL mutate_h_structure(original_h) - this creates NEW step functions by:
   - Shifting existing peaks left/right
   - Splitting wide peaks into narrower peaks
   - Merging nearby peaks
   - Adding/removing peaks

2. CALL probe_solution on each new h to get approximate c5_bound

3. Keep candidates with c5_bound < 0.375

4. CALL evaluate_solution on BEST 2 candidates

5. If no improvement: Repeat Phase 1 with different mutation types

## Phase 2: Hyperparameter Tuning (LAST RESORT)

Only if Phase 1 fails 2x:
- Vary num_intervals: 400, 800, 1600
- Vary penalty_strength: 40, 80, 120
- Vary learning_rate: 0.001, 0.005, 0.01

## Critical Rules
- ALWAYS try structural mutations FIRST
- NEVER waste evals on hyperparameter tuning before trying 2x structural search
- Use probe_solution to screen before full evaluation
- Track all c5_bound values to avoid redundant searches
