Erdos minimum overlap problem: find a step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Current best: C5 <= 0.38092303510845016.
Goal: Beat seed score by finding c5_bound < 0.380923.

CRITICAL: The seed uses continuous gradient descent. Instead, try DISCRETE STEP FUNCTION CONSTRUCTIONS -
define h as piecewise constant with few intervals, heights optimized to satisfy integral(h)=1.

METHOD:
1. Start with few intervals (30-50) and DISCRETE step heights (0, 1, or simple fractions).
2. Use probe_solution to rank many discrete constructions (50-100 cheap evals).
3. Only call evaluate_solution on top 3-5 candidates.
4. If discrete fails, try seed's continuous approach with LOW penalty_strength (5-15) and FIXED num_intervals=100.

CONSTRAINT: integral(h)=1.0 exactly. For discrete: sum(heights * interval_width) = 1.0.

BUDGET: Use 20-25 probes for ranking, 5-7 full evaluations.
