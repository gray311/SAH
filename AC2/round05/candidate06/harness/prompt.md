You are optimizing C2 = ||f ★ f||₂² / ((∫f)² ||f ★ f||_∞). Current score: 1.02665.

CRITICAL: The seed program uses piecewise-linear functions with ~400 intervals and achieves 1.02665. This is already very close to the theoretical maximum of 1.0. Do NOT immediately try step functions or other families.

STRATEGY: DEEPLY OPTIMIZE THE CURRENT APPROACH FIRST.

WORKFLOW:
1. Call analyze_convolution to diagnose why C2 cannot be improved
2. Systematically refine the piecewise-linear representation:
   - Try num_intervals in [500, 800, 1200, 1600] (finer discretization)
   - Tune learning_rate in [0.1, 0.15, 0.2, 0.25, 0.3]
   - Adjust num_steps in [30000, 50000, 80000, 100000]
   - Refine warmup_steps and cosine_decay_schedule
3. Use probe_solution to rank 3-5 variants before any full eval
4. Only after exhausting the current approach (3+ failed evals) try step functions

PROBE-BEFORE-EVAL: Always probe 3+ variants before evaluating. Never eval without probing.

TOOL PRIORITY:
1. analyze_convolution — get diagnostic info on current function
2. edit_solution — refine intervals, learning rate, or steps
3. probe_solution — rank variants
4. evaluate_solution — confirm top 1-2
5. finish — when budget exhausted

Remember: The seed is already excellent. Small refinements may push it higher, but massive architectural changes are premature.
