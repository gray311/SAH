Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL INSIGHT: The optimizer trains for 59,000 steps - too slow. Start with CONSTRUCTED step functions first.

STRATEGY:
1. FIRST: Call construct_step_functions() to generate 5 exact piecewise-constant functions with integral=1.
   These are ready-to-evaluate immediately (no training needed). Pick the best c5_bound and call evaluate_solution.
2. IF construct_step_functions returns c5_bound >= 0.380, THEN use the optimizer with these tips:
   - Start with num_intervals=800, num_steps=30000, penalty_strength=100, num_restarts=1
   - Use ONLY seed patterns 12 (Golomb) and 14 (Tri-modal) which have lowest initial c5
   - Vary base_learning_rate: try 0.01, 0.02 (aggressive to escape local minima)
   - Only call evaluate_solution if probe_solution shows c5_bound < 0.375
3. Probe all candidates before full eval: use probe_solution to get approximate c5_bound
4. Only submit when combined_score > 1.0

Key: Construct first, optimize second. The search space is high-dimensional but combinatorial constructions are promising.
