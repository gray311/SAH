Erdos minimum overlap (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY: TRY DIFFERENT SOLVER ARCHITECTURES. The seed uses a JAX gradient-based optimizer with 800 intervals. This often gets stuck.

NEW APPROACH: Generate COMPLETELY DIFFERENT solver designs:
1. Coarse-to-fine discretization: Start with 10-20 intervals, optimize, then refine to 800+
2. Explicit step function: Build h as a series of plateaus with controlled spacing
3. Spectral approach: Design h using symmetric patterns or combinatorial structures
4. Multi-objective: Optimize both integral constraint and overlap reduction simultaneously

For each architecture:
- Write a clean, simple implementation
- Call probe_solution to check c5_bound < 0.382
- Call evaluate_solution if promising
- FINISH if combined_score > 1.0

Remember: The seed's 14 initialization patterns are already tried. You need a NEW search approach, not better parameters.
