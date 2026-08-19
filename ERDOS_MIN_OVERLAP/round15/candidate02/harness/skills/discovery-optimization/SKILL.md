---
name: discovery-optimization
description: "Generate complete h(x) step functions with diverse structures, bypass the seed''s lazy initialization, and screen with probes."
---

# Break Through Erdos Optimization
## Problem The seed's 12 initialization patterns all produce similar smooth sigmoidal h(x) functions. This creates local minima that the optimizer cannot escape.
## Strategy
### Step 1: Generate Complete h(x) Vectors Call create_piecewise_h to get ready-to-use h(x) vectors (already in [0,1], integral=1). Patterns to try: - Piecewise constant with 3-5 breakpoints - Golomb-ruler inspired spacing - Asymmetric multi-modal - Sharp threshold functions
### Step 2: Inject h(x) into Seed EDIT _get_best_initialization to return ONLY the new h(x): ```python def _get_best_initialization(self, seed: int) -> jnp.ndarray: return jnp.array([your_h_vector_here])  # already sigmoided, in [0,1] ```
### Step 3: Screen with Probes Call probe_solution to check: - integral(h) ≈ 1 (within 5%) - c5_bound < 0.37 Skip any candidate that fails.
### Step 4: Evaluate Promising Candidates Call evaluate_solution on at most 3 candidates that pass probe.
### Step 5: Analyze and Iterate Call analyze_structure on the current best to understand its shape, then design h(x) with opposite properties.
## Success - combined_score > 1.0 (c5_bound < 0.380923) - Found h(x) with c5_bound < 0.37
