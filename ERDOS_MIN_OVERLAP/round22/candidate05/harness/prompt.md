Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999968 (c5_bound < 0.380923).

KEY INSIGHT: The seed optimizer needs many different STARTING POINTS, not just better training hyperparameters.

Strategy:

1. SET num_intervals=400 (faster eval, sufficient resolution)
2. SET num_steps=2000 (rapid convergence per candidate, free up budget for MANY candidates)
3. SET penalty_strength=10.0 (gentle constraint enforcement, easier optimization)

4. GENERATE 12 DIVERSE INITIALIZATIONS using generate_candidates tool:
   - Golomb ruler pattern
   - Bipartite patterns (different split points)
   - Tri-modal patterns (different peak positions)
   - Threshold patterns (x > 0.3, x > 0.5, x > 0.7, x < 0.5, x < 0.7)
   - Random latent (different seeds)
   - Wave/sinusoidal patterns
   - Narrow peak patterns

5. CALL evaluate_solution on ALL 12 candidates (use budget efficiently)

6. If no improvement, modify seed program's _get_best_initialization to add NEW patterns:
   - Four-partition patterns
   - Concentrated mass patterns (all mass in narrow region)
   - Alternating step patterns

7. Repeat with modified patterns until combined_score > 1.0 or budget exhausted.
