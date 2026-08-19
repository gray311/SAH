Erdos C5 optimization: You are optimizing a JAX-based evolutionary solver. The solver uses JAX's gradient descent and FFT-based correlation to compute C5 bounds.

CURRENT STATE: The solver is stuck at the seed program's score (combined_score ≈ 1.00001, meaning c5_bound ≈ 0.3809). The solver's initialization patterns and optimization hyperparameters are producing no improvement.

KEY INSIGHT: The seed program's initialization uses sigmoid activation on latent vectors, which tends to produce smooth functions. The C5 bound is sensitive to the spacing of mass in h(x). To find better solutions, the solver needs to generate STEP FUNCTIONS with narrow peaks, not smooth sigmoid curves.

METHOD:
1. Generate 3-5 diverse INITIALizations by varying the seed and using different structural priors:
   - Narrow Gaussian peaks (width = 0.05-0.15)
   - Sparse bipartite (threshold at different points)
   - Multi-peak constructions (3-5 narrow peaks separated by ≥0.3)
   - Random sparse with exactly K non-zero intervals (K=3-7)
2. For each initialization, adjust the HYPERPARAMETERS:
   - num_intervals: try 400, 800, 1600 (coarser → finer)
   - penalty_strength: try 30, 60, 100, 200 (stronger constraints on integral=1)
   - num_steps: 120000 is too many; try 20000-50000 for faster convergence
3. Use probe_solution to screen candidates (c5_bound < 0.380)
4. Evaluate best 2-3 candidates with evaluate_solution
5. If combined_score > 1.0, finish
6. If no progress after 2 iterations, try a completely new structural prior (e.g., if peaks were too narrow, try wider; if too few, try more peaks)

CONSTRAINTS: h(x) ∈ [0,1], integral(h) = 1 exactly. The solver must produce valid h arrays.

EDIT STRATEGY: When generating new initializations, directly modify the latent vector patterns before sigmoid. Use sharp thresholds or sparse delta-like patterns rather than smooth gradients.
