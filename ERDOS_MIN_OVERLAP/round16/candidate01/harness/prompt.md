You are solving the Erdos minimum overlap problem: minimize max_k integral h(x)(1-h(x+k)) dx
for a step function h: [0,2] -> [0,1] with integral(h)=1 exactly.

Current best bound: C5 <= 0.38092303510845016 (combined_score = 0.38092303510845016 / c5_bound)

CRITICAL: The seed's optimizer uses JAX and requires you to EDIT the EVOLVE-BLOCK to change hyperparameters or initialization.

STRATEGY: Generate VALID h functions directly (in [0,1] range) that satisfy integral=1, then edit the seed to use ONLY that pattern with num_restarts=1.

Steps:
1. CALL generate_valid_h to get a valid h array (already sigmoid-transformed, normalized to integral=1)
2. EDIT the seed's _get_best_initialization to return ONLY the sigmoid of a pattern-specific latent, then use probe_solution to check: integral(h)≈1 (should be exactly 1), c5_bound estimate
3. Call evaluate_solution on candidates with c5_bound < 0.375
4. If no improvement, try a different pattern

The seed's _compute_c5_bound does FFT-based correlation. The evaluator is fast (probe takes 10s), so screen many candidates.

Key: EDIT to use num_restarts=1 and seed_start=pattern_index to isolate ONE pattern's evaluation.
