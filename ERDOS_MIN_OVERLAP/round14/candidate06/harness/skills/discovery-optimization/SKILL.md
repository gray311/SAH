---
name: discovery-optimization
description: "Escape local minima by exploring diverse hyperparameter configurations while preserving the seed's multi-restart diversity."
---

# Erdos Minimum Overlap - Hyperparameter Diversity Strategy

## Problem
The seed optimizer has good initialization diversity but limited hyperparameter exploration.

## Strategy

### Phase 1: Generate Hyperparameter Variations
Use generate_hyper_diversity to get 5-7 fundamentally different hyperparameter sets:
- Vary num_intervals (400, 800, 1200, 1600)
- Vary learning_rate (0.001, 0.01, 0.05, 0.1)
- Vary penalty_strength (10, 50, 100, 200)
- Vary num_restarts (1, 5, 10)
- Vary num_steps (20000, 100000, 200000)

### Phase 2: Screen with Probes (Use All 30 Probes Here!)
For each hyperparameter config:
1. EDIT the seed to use ONLY that config (edit the Hyperparameters dataclass)
2. Keep num_restarts=3 to maintain diversity
3. Call probe_solution to check: constraint satisfaction, c5_bound
4. Skip full evaluation if probe shows c5_bound >= 0.375 or constraint violation
5. Keep candidates with c5_bound < 0.37

### Phase 3: Evaluate Promising Candidates
Call evaluate_solution on top 2-3 candidates from Phase 2.

### Phase 4: If No Improvement, Change Problem Scale
Edit to change num_intervals dramatically (e.g., from 800 to 400 or 1600)

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- Found at least one config with c5_bound < 0.37
