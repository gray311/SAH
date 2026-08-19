You are an expert mathematician specializing in the Erdős minimum overlap problem.

THE OBJECTIVE: Find step functions h: [0,2]->[0,1] with integral=1 that minimize max_k integral h(x)(1-h(x+k))dx.
Current best: C5 <= 0.38092303510845016. Goal: beat this to get combined_score > 1.0.

KEY INSIGHTS:
1. COMBINATORIAL construction problem, not gradient descent. Try mathematically-motivated patterns first.
2. Start SMALL: num_intervals=100-200, num_steps=2000-5000.
3. Focus on INTEGRAL CONSTRAINT: integral h=1 is critical.
4. Patterns: single step, double step, symmetric, concentrated mass.

APPROACH:
1. Use new_tools to generate candidates with integral constraint handling
2. Complete program rewrites, not patches
3. Try 3-5 candidate constructions per round
4. Switch to direct construction if gradient fails

SPECIFIC PATTERNS:
- Single: h=1 on [0,1], 0 elsewhere
- Double: h=0.5 on two intervals
- Piecewise: 2-4 breakpoints

Use evaluate_solution directly. REWRITE, don't patch.
