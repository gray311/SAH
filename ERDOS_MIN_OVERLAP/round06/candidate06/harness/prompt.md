You are solving the Erdős minimum overlap problem. Goal: Find a step function h:[0,2]→[0,1] with ∫h=1 that minimizes max_k ∫h(x)(1-h(x+k))dx.

Current best bound: 0.38092303510845016. Your score = 0.38092303510845016 / c5_bound. Beat 1.0!

**KEY INSIGHT**: The seed's gradient-based optimizer is stuck because the optimal solution likely has a specific discrete structure. You must CONSTRUCT step functions explicitly, not optimize vaguely.

**FOCUSED STRATEGY**:
1. Try explicit step function constructions with few breakpoints (2-5 intervals)
2. Use the probe_solution tool to rank ~10 candidates cheaply before full eval
3. Once you find c5_bound < 0.3809, refine by adjusting breakpoint positions
4. Common structures to try: single-block, double-block, symmetric triple-block

**CONSTRAINTS**: h∈[0,1], ∫h=1 over [0,2]. Discretize with num_intervals=800.

**USE probe_solution extensively** - it's FREE (30 probes, separate budget). Rank your constructions before spending evals.

**EDIT STYLE**: Replace the entire EVOLVE-BLOCK with a new explicit construction. Don't patch - rewrite the _get_best_initialization or main optimization loop.
