Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score (combined_score > 1.0, i.e., c5_bound < 0.380923).

Strategy:

1. Generate 10 diverse candidates with generate_10_candidates

2. Use probe_solution to quickly rank them (cheap analytical c5)

3. Evaluate only top 2-3 with c5 < 0.37

4. If no improvement, try MUTATING hyperparameters:
   - Increase num_intervals to 1000 or 1200 for better FFT accuracy
   - Adjust learning_rate (try 0.004 or 0.01)
   - Adjust penalty_strength (try 80-100 for stronger constraint)
   - Reduce num_steps to 30000 (faster convergence)
   - Increase num_restarts to 5 or 7

5. After each eval, use analyze_results to determine which mutations to try

6. Never waste evals on integral-violating candidates (check precomputed integral)

7. Budget: 30 evals total. Use probes freely, save evals for best candidates.

Key: The seed optimizer is expensive (59k steps × 3 restarts). We need to find BETTER hyperparameters, not just new initializations.
