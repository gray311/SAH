Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL STRATEGY (READ CAREFULLY):

1. FIRST, CALL generate_ready_candidates() to get 3 pre-computed candidates with:
   - h: latent vector (already sigmoided, values in [0,1])
   - integral: sum(h)*dx (should be ~1.0)
   - c5_bound: precomputed via FFT (no training needed!)
   - pattern_type: label

2. EXAMINE candidates: Keep ONLY those with c5_bound < 0.375. Discard rest.

3. CALL evaluate_solution on kept candidates. If none beat current best, STOP and call finish.

4. Only after exhausting candidates, if STILL stuck, THEN call analyze_fft_spectrum() on seed to diagnose:
   - Where are the peaks in frequency domain?
   - What's the energy distribution?
   - Are there obvious conflicts (e.g., overlapping high-frequency components)?

5. Based on FFT diagnosis, EDIT ONE parameter: Either num_intervals (400/800/1600) OR base_learning_rate (0.001/0.005/0.01)
   to experiment with convergence behavior.

6. Never edit multiple parameters at once. Never ignore generate_ready_candidates.

Your ONLY goal: Spend all 30 evals getting combined_score > 1.0. Use generate_ready_candidates as your PRIMARY weapon.
