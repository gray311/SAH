---
name: discovery-optimization
description: "Escape local minima by trying fundamentally different step function structures (bipartite, multi-plateau, piecewise constant) with short optimization runs and multiple restarts. Use the 30 eval budget to test 4-6 diverse candidates thoroughly."
---

# Erdos Minimum Overlap - Diverse Initialization Strategy

## Problem
The seed optimizer uses 12 similar initialization patterns (Gaussian, sinusoidal, threshold-based).
To find better solutions, we need initializations with DIFFERENT STRUCTURES.

## Strategy

### Phase 1: Generate Structurally Diverse Initializations
Use generate_diverse_init to create 4+ fundamentally different patterns:
- Golomb ruler-based (optimal spacing for 5-7 marks)
- Bipartite split (h=0 on [0,a), h=1 on [a,2-a], h=0 on [2-a,2])
- Multi-modal with 3-5 peaks at specific locations
- Truncated Gaussian with sharp cutoffs

### Phase 2: Screen with Probes (Use All 30 Probes Here!)
For each new initialization:
1. EDIT the seed to use ONLY that pattern (set num_restarts=1, use the pattern's latent as seed)
2. Call probe_solution to check: constraint satisfaction, c5_bound
3. Skip full evaluation if probe shows c5_bound >= 0.375 or constraint violation
4. Keep candidates with c5_bound < 0.37

### Phase 3: Evaluate Promising Candidates
Call evaluate_solution on top 2-3 candidates from Phase 2.

### Phase 4: If No Improvement, Add New Structure
Edit _get_best_initialization to add a completely new pattern:
- Piecewise constant with 3-4 breakpoints at "golden ratio" locations
- Asymmetric triangular wave
- Optimized 3-step function (high on [0,a], medium on [a,b], low on [b,2])

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- Found at least one initialization with c5_bound < 0.37
