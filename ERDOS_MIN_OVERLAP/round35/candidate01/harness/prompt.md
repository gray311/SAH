Erdos minimum overlap problem (C5): Find a step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).
KEY INSIGHT: The optimal h is likely a simple step function (plateaus of 0 and 1).
STRATEGY:
1. Use step_function_builder to create simple step functions with plateau patterns: - Two plateau patterns: h=1 on [0,a], h=0 on [a,2] (satisfies integral=1 if a=0.5) - Three plateau patterns: h=1 on [0,a], h=0 on [a,b], h=1 on [b,2] - Alternating patterns: h=1 on multiple small intervals
2. For each candidate, use probe_solution to quickly estimate c5_bound
3. Evaluate the best probe candidates fully
4. If combined_score > 1.0, finish
5. Try different plateau configurations systematically: - First: simple bipartite (one transition at a=0.5) - Second: two transitions (plateau-hi, plateau-lo, plateau-hi) - Third: three transitions (alternating 1-0-1-0 pattern)
Remember: Focus on SIMPLE step functions with clear plateau boundaries. Avoid complex sigmoidal or random patterns. The constraint integral(h)=1 means the total "on" time must be exactly 1.0.
